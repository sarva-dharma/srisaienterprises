"""
Firm Details Importer
Reads firm_details.csv and firm_services.csv and updates:
1. backend/firm_profile.json (Injected dynamically into all web pages)
2. Database admin user credentials
3. Database services and pricing catalog
"""
import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import csv
import json

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, BASE_DIR)

from backend.app import create_app
from backend.database import db
from backend.models import User, Service

def load_firm_details_csv(csv_path):
    details = {}
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found.")
        return details

    with open(csv_path, mode='r', encoding='utf-8') as f:
        first_line = f.readline()
        if first_line.startswith('sep='):
            delimiter = first_line.strip().split('=')[1]
        else:
            delimiter = ';' if ';' in first_line else ','
            f.seek(0)
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            key = row.get('Field_Key', '').strip()
            val = row.get('Value', '').strip()
            if key:
                details[key] = val
    return details


def load_firm_services_csv(csv_path):
    services = []
    if not os.path.exists(csv_path):
        return services

    with open(csv_path, mode='r', encoding='utf-8') as f:
        first_line = f.readline()
        if first_line.startswith('sep='):
            delimiter = first_line.strip().split('=')[1]
        else:
            delimiter = ';' if ';' in first_line else ','
            f.seek(0)
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            title = row.get('Title', '').strip()
            if not title:
                continue
            
            features_raw = (
                row.get('Key_Features') or
                row.get('Key_Features_Pipe_Separated') or
                row.get('Key_Features_Semicolon_Separated') or
                ''
            )
            import re
            features = [ft.strip() for ft in re.split(r'[|;]', features_raw) if ft.strip()]
            
            services.append({
                'title': title,
                'category': row.get('Category', 'Municipal Approvals').strip(),
                'base_fee': float(row.get('Base_Fee_INR') or 15000),
                'betterment_rate_sqft': float(row.get('Betterment_Rate_SqFt') or 0),
                'scrutiny_rate_sqft': float(row.get('Scrutiny_Rate_SqFt') or 3.5),
                'turnaround_days': row.get('Turnaround_Days', '14 to 21 Days').strip(),
                'short_desc': row.get('Short_Description', '').strip(),
                'full_desc': row.get('Short_Description', '').strip(),
                'features': features
            })
    return services


def main():
    print("\n=======================================================")
    print("      IMPORTING FIRM DETAILS FROM CSV FILES")
    print("=======================================================\n")

    csv_details_path = os.path.join(BASE_DIR, 'firm_details.csv')
    csv_services_path = os.path.join(BASE_DIR, 'firm_services.csv')

    firm_data = load_firm_details_csv(csv_details_path)
    if not firm_data:
        print("Error: Could not read firm_details.csv. Aborting.")
        return

    # 1. Save firm profile JSON for website dynamic rendering
    profile_path = os.path.join(BASE_DIR, 'backend', 'firm_profile.json')
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(firm_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved firm profile config to: {profile_path}")

    # 2. Update Database (Admin credentials & Services)
    app = create_app()
    with app.app_context():
        db.create_all()

        # Update or Create Admin Account
        admin_email = firm_data.get('admin_email', 'admin@bengaluruapprovals.com').strip().lower()
        admin_pass = firm_data.get('admin_password', 'admin123').strip()
        admin_name = firm_data.get('principal_architect') or firm_data.get('admin_name', 'Principal Architect')
        admin_phone = firm_data.get('primary_phone', '')

        admin_user = User.query.filter_by(role='admin').first()
        if admin_user:
            admin_user.email = admin_email
            admin_user.name = admin_name
            admin_user.phone = admin_phone
            admin_user.set_password(admin_pass)
            print(f"[OK] Updated Admin login: {admin_email} / (password updated)")
        else:
            admin_user = User(
                name=admin_name,
                email=admin_email,
                role='admin',
                phone=admin_phone
            )
            admin_user.set_password(admin_pass)
            db.session.add(admin_user)
            print(f"[OK] Created Admin user: {admin_email}")

        # Update Services if firm_services.csv is present
        services = load_firm_services_csv(csv_services_path)
        if services:
            print(f"\nProcessing {len(services)} services from firm_services.csv...")
            for idx, s in enumerate(services, start=1):
                slug = s['title'].lower().replace(' ', '-').replace('&', 'and').replace('/', '-')
                existing_service = Service.query.filter_by(slug=slug).first()
                if not existing_service:
                    existing_service = Service.query.filter_by(title=s['title']).first()

                if existing_service:
                    existing_service.title = s['title']
                    existing_service.category = s['category']
                    existing_service.base_fee = s['base_fee']
                    existing_service.betterment_rate_sqft = s['betterment_rate_sqft']
                    existing_service.scrutiny_rate_sqft = s['scrutiny_rate_sqft']
                    existing_service.turnaround_days = s['turnaround_days']
                    existing_service.short_desc = s['short_desc']
                    existing_service.full_desc = s['full_desc']
                    existing_service.features_json = json.dumps(s['features'])
                    existing_service.display_order = idx
                    print(f"  * Updated service: {s['title']} (Fee: INR {s['base_fee']:,.0f})")
                else:
                    new_srv = Service(
                        title=s['title'],
                        slug=slug,
                        category=s['category'],
                        base_fee=s['base_fee'],
                        betterment_rate_sqft=s['betterment_rate_sqft'],
                        scrutiny_rate_sqft=s['scrutiny_rate_sqft'],
                        turnaround_days=s['turnaround_days'],
                        short_desc=s['short_desc'],
                        full_desc=s['full_desc'],
                        icon='building',
                        display_order=idx,
                        features_json=json.dumps(s['features'])
                    )
                    db.session.add(new_srv)
                    print(f"  * Added new service: {s['title']} (Fee: INR {s['base_fee']:,.0f})")

        db.session.commit()

    print("\n" + "="*55)
    print("SUCCESS! All firm details and services have been imported.")
    print("Your website and database now reflect your firm's real data.")
    print("="*55 + "\n")

if __name__ == '__main__':
    main()
