import os
from flask import Flask, render_template, send_from_directory, jsonify
from backend.config import Config, UPLOAD_FOLDER
from backend.database import db
from backend.routes.auth_routes import auth_bp
from backend.routes.public_routes import public_bp
from backend.routes.client_routes import client_bp
from backend.routes.admin_routes import admin_bp

def create_app(config_class=Config):
    # Setup paths
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    template_dir = os.path.join(base_dir, 'templates')
    static_dir = os.path.join(base_dir, 'static')

    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_object(config_class)

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register API blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(public_bp, url_prefix='/api')
    app.register_blueprint(client_bp, url_prefix='/api/client')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Load dynamic firm profile from CSV-generated JSON or default
    def get_firm_profile():
        profile_path = os.path.join(os.path.dirname(__file__), 'firm_profile.json')
        data = {}
        if os.path.exists(profile_path):
            try:
                import json
                with open(profile_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                pass

        defaults = {
            'firm_name': 'Sri Sai Enterprises',
            'tagline': 'Council of Architecture Reg. Practice',
            'principal_architect': 'S M Thyagaraja (Draftsman Civil)',
            'coa_registration_no': 'CA/2009/44120',
            'experience_years': '37',
            'sanctions_delivered': '23,000+',
            'sakala_sla_days': '5-7 Days',
            'approval_rate': '100%',
            'primary_phone': '94480 54185',
            'secondary_phone': '080 233 255 09',
            'whatsapp_number': '94480 54185',
            'official_email': 'smthyagaraj@gmail.com',
            'office_address': '#3309, 1st Main Road, Gayathrinagara, Bengaluru - 560021',
            'office_landmark': 'Opp. More Retail Store',
            'google_maps_url': 'https://maps.google.com/?q=Gayathrinagara+Bengaluru',
            'working_hours': 'Mon - Sat: 9:30 AM - 7:30 PM'
        }
        for k, v in defaults.items():
            if not data.get(k):
                data[k] = v

        raw_wa = str(data.get('whatsapp_number', '9448054185')).replace(' ', '').replace('-', '').replace('+', '')
        if len(raw_wa) == 10:
            raw_wa = '91' + raw_wa
        data['clean_whatsapp'] = raw_wa
        return data

    @app.context_processor
    def inject_firm():
        return {'firm': get_firm_profile()}

    # Frontend Single-Page Application routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/portal')
    def portal_view():
        return render_template('index.html', initial_view='portal')

    @app.route('/admin')
    def admin_view():
        return render_template('index.html', initial_view='admin')

    # Static file serving fallback
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # API health check
    @app.route('/api/health')
    def health():
        return jsonify({
            'status': 'healthy',
            'service': 'Bengaluru Building Plan Sanction & Architectural Liaisoning API',
            'version': '2.0.2',
            'regulation_compliance': 'GBA 2026 & Nambike Nakshe'
        })

    return app

if __name__ == '__main__':
    from backend.seed_data import seed_database
    app = create_app()
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(host='0.0.0.0', port=5000, debug=True)
