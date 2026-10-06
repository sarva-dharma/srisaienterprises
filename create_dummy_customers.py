import os
import sys

# Add 2.02 directory to path
sys.path.insert(0, os.path.abspath('2.02'))
from backend.app import create_app
from backend.database import db
from backend.models import User, Lead, Project, ProjectTimeline, ProjectDocument

def create_dummy_customers():
    app = create_app()
    with app.app_context():
        customers_data = [
            {
                'name': 'Nandini Ramanathan',
                'email': 'nandini.ramanathan@gmail.com',
                'phone': '+91 98450 12345',
                'password': 'Nandini@Bangalore2026',
                'location': 'RMV 2nd Stage, Ward 18, Bengaluru',
                'dimensions': '40x60 ft (2,400 sq.ft)',
                'service': 'Plan Sanctions & Approvals (GBA / BBMP)',
                'ref_no': 'SAKALA-GBA-2026-1041',
                'project_title': 'G+3 Luxury Residential Villa - RMV 2nd Stage',
                'authority': 'GBA / BBMP',
                'plot_area': 2400.0,
                'builtup_area': 4800.0,
                'stage': 'PreDCR Scrutiny',
                'progress': 45,
                'nambike': False
            },
            {
                'name': 'Kiran Kumar Gowda',
                'email': 'kiran.gowda@techblr.io',
                'phone': '+91 99002 67890',
                'password': 'Kiran@Gowda2026',
                'location': 'JP Nagar 7th Phase, Ward 187, Bengaluru',
                'dimensions': '30x40 ft (1,200 sq.ft)',
                'service': 'Nambike Nakshe Fast-Track Sanction',
                'ref_no': 'SAKALA-GBA-2026-1042',
                'project_title': 'Duplex House Trust-Based Approval - JP Nagar',
                'authority': 'GBA / BBMP',
                'plot_area': 1200.0,
                'builtup_area': 2700.0,
                'stage': 'AutoDCR Submission',
                'progress': 60,
                'nambike': True
            },
            {
                'name': 'Deepika Shastry',
                'email': 'deepika.shastry@outlook.com',
                'phone': '+91 97411 98765',
                'password': 'Deepika@Shastry2026',
                'location': 'HSR Layout Sector 2, Ward 174, Bengaluru',
                'dimensions': '50x80 ft (4,000 sq.ft)',
                'service': 'AutoDCR & PreDCR CAD Drafting',
                'ref_no': 'SAKALA-GBA-2026-1043',
                'project_title': 'Residential Apartment Complex (6 Units) - HSR Layout',
                'authority': 'GBA / BBMP',
                'plot_area': 4000.0,
                'builtup_area': 9600.0,
                'stage': 'Site Inspection',
                'progress': 75,
                'nambike': False
            },
            {
                'name': 'Mohammed Tariq Mansoor',
                'email': 'tariq.mansoor@gmail.com',
                'phone': '+91 98860 45678',
                'password': 'Tariq@Mansoor2026',
                'location': 'Whitefield Borewell Road, Ward 84, Bengaluru',
                'dimensions': '30x50 ft (1,500 sq.ft)',
                'service': 'e-Khata / B-Khata to A-Khata Conversion',
                'ref_no': 'SAKALA-GBA-2026-1044',
                'project_title': 'B-Khata Betterment & Sanction - Whitefield',
                'authority': 'GBA / BBMP',
                'plot_area': 1500.0,
                'builtup_area': 3375.0,
                'stage': 'Drafting',
                'progress': 25,
                'nambike': True
            },
            {
                'name': 'Dr. Ramesh Chandrasekhar',
                'email': 'dr.ramesh.chandra@manipal.edu',
                'phone': '+91 94481 87654',
                'password': 'Ramesh@Chandra2026',
                'location': 'Devanahalli Airport Corridor, Bengaluru',
                'dimensions': '60x100 ft (6,000 sq.ft)',
                'service': 'BIAAPA & STRR Multi-Authority Clearance',
                'ref_no': 'SAKALA-BIAAPA-2026-1045',
                'project_title': 'Commercial Healthcare & Diagnostic Center - Devanahalli',
                'authority': 'BIAAPA',
                'plot_area': 6000.0,
                'builtup_area': 15000.0,
                'stage': 'NOC Clearance',
                'progress': 85,
                'nambike': False
            }
        ]

        created_users = []
        for c in customers_data:
            user = User.query.filter_by(email=c['email']).first()
            if not user:
                user = User(
                    name=c['name'],
                    email=c['email'],
                    phone=c['phone'],
                    role='client'
                )
                user.set_password(c['password'])
                db.session.add(user)
                db.session.flush()
            else:
                user.name = c['name']
                user.phone = c['phone']
                user.set_password(c['password'])

            # Check / Create Lead
            lead = Lead.query.filter_by(email=c['email']).first()
            if not lead:
                lead = Lead(
                    full_name=c['name'],
                    email=c['email'],
                    phone=c['phone'],
                    plot_location=c['location'],
                    plot_dimensions=c['dimensions'],
                    service_title=c['service'],
                    message=f"Requested architectural plan sanction review for {c['dimensions']} plot at {c['location']}.",
                    status='converted'
                )
                db.session.add(lead)

            # Check / Create Project
            proj = Project.query.filter_by(reference_no=c['ref_no']).first()
            if not proj:
                proj = Project(
                    reference_no=c['ref_no'],
                    client_id=user.id,
                    client_name=user.name,
                    title=c['project_title'],
                    plot_location=c['location'],
                    authority=c['authority'],
                    current_stage=c['stage'],
                    nambike_nakshe_eligible=c['nambike'],
                    plot_area_sqft=c['plot_area'],
                    builtup_area_sqft=c['builtup_area'],
                    completion_percent=c['progress'],
                    assigned_architect='S M Thyagaraja (Draftsman Civil), CA/2009/44120'
                )
                db.session.add(proj)
                db.session.flush()

                # Add Timelines
                stages = ['Drafting', 'PreDCR Scrutiny', 'AutoDCR Submission', 'Site Inspection', 'NOC Clearance', 'Approved']
                current_idx = stages.index(c['stage']) if c['stage'] in stages else 1
                for i, stg in enumerate(stages[:4]):
                    is_done = i <= current_idx
                    t = ProjectTimeline(
                        project_id=proj.id,
                        stage_name=stg,
                        status='completed' if is_done else 'pending',
                        date_updated='2026-10-06' if is_done else None,
                        remarks='Processed and verified by town planning desk.' if is_done else 'Awaiting stage trigger.'
                    )
                    db.session.add(t)

                # Add sample documents
                doc1 = ProjectDocument(
                    project_id=proj.id,
                    title=f"{c['name'].split()[0]}_AutoDCR_Plan_Drawing.dwg",
                    doc_type='CAD_DWG',
                    filename=f"{c['ref_no']}_PreDCR.dwg",
                    file_path=f"uploads/{c['ref_no']}_PreDCR.dwg",
                    file_size_display='3.2 MB'
                )
                doc2 = ProjectDocument(
                    project_id=proj.id,
                    title='Sakala_Municipal_Sanction_Acknowledgement.pdf',
                    doc_type='SANCTION_CERT',
                    filename=f"{c['ref_no']}_Acknowledgement.pdf",
                    file_path=f"uploads/{c['ref_no']}_Acknowledgement.pdf",
                    file_size_display='580 KB'
                )
                db.session.add(doc1)
                db.session.add(doc2)

            created_users.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'phone': user.phone,
                'password': c['password'],
                'ref_no': c['ref_no'],
                'project_title': c['project_title'],
                'location': c['location']
            })

        db.session.commit()

        print("=" * 80)
        print("DATABASE LOCATION PATH:")
        print(os.path.abspath('2.02/backend/bengaluru_sanctions.db'))
        print("=" * 80)
        print(f"SUCCESSFULLY CREATED/VERIFIED {len(created_users)} DUMMY CUSTOMER ACCOUNTS:")
        for idx, u in enumerate(created_users, 1):
            print(f"\n[Customer {idx}]")
            print(f"  ID in Database (users table): {u['id']}")
            print(f"  Name:                         {u['name']}")
            print(f"  Email:                        {u['email']}")
            print(f"  Role:                         {u['role']} (Customer)")
            print(f"  Phone:                        {u['phone']}")
            print(f"  Password:                     {u['password']}")
            print(f"  Associated Sakala Reference:  {u['ref_no']}")
            print(f"  Project Title:                {u['project_title']}")
            print(f"  Plot Location:                {u['location']}")
        print("=" * 80)

if __name__ == '__main__':
    create_dummy_customers()
