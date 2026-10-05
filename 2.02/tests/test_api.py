import unittest
import json
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.database import db
from backend.config import Config
from backend.seed_data import seed_database
from backend.models import User, Service, Lead, Project

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class BengaluruApprovalsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            seed_database()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_check(self):
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('GBA 2026', data['regulation_compliance'])

    def test_public_services(self):
        res = self.client.get('/api/services')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertGreaterEqual(data['count'], 5)
        titles = [s['title'] for s in data['services']]
        self.assertIn('Plan Sanctions & Approvals', titles)
        self.assertIn('AutoDCR & PreDCR CAD Drafting', titles)
        self.assertIn('e-Khata Services & Conversions', titles)
        self.assertIn('Turnkey Construction & Architectural Design', titles)
        self.assertIn('NOC Procurement & Clearances', titles)

    def test_jurisdiction_check_nambike_eligible(self):
        # 30x40 residential plot in Whitefield
        res = self.client.post('/api/jurisdictions/check', json={
            'locality_id': 'whitefield',
            'plot_width': 30,
            'plot_length': 40,
            'road_width': 30,
            'building_type': 'Residential'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['authority'], 'GBA / BBMP (Mahadevapura Zone)')
        self.assertTrue(data['nambike_nakshe']['eligible'])
        self.assertEqual(data['nambike_nakshe']['status'], 'APPROVED FOR INSTANT SELF-DECLARATION')

    def test_jurisdiction_check_large_plot_not_nambike(self):
        # 60x100 plot (>4000 sq ft)
        res = self.client.post('/api/jurisdictions/check', json={
            'locality_id': 'whitefield',
            'plot_width': 60,
            'plot_length': 100,
            'road_width': 40,
            'building_type': 'Residential'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertFalse(data['nambike_nakshe']['eligible'])
        self.assertIn('exceeds 50x80 ft', data['nambike_nakshe']['details'])

    def test_fee_calculator_estimate(self):
        res = self.client.post('/api/calculator/estimate', json={
            'plot_width': 30,
            'plot_length': 40,
            'floors': 3,
            'has_b_khata': True,
            'locality_id': 'whitefield'
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data['plot_area_sqft'], 1200)
        self.assertGreater(data['total_estimated'], 0)
        self.assertGreater(data['breakdown']['betterment_levy'], 0)

    def test_lead_submission(self):
        res = self.client.post('/api/leads', json={
            'full_name': 'Santosh Hegde',
            'phone': '+91 98450 99999',
            'email': 'santosh.hegde@gmail.com',
            'plot_location': 'Indiranagar 100ft Road',
            'plot_dimensions': '40x60',
            'service_title': 'Plan Sanctions & Approvals',
            'message': 'Need GBA approval for commercial building.'
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn('lead_id', data)

    def test_client_portal_tracking(self):
        res = self.client.get('/api/client/projects?reference_no=SAKALA-GBA-2026-0894')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(len(data['projects']), 1)
        proj = data['projects'][0]
        self.assertEqual(proj['reference_no'], 'SAKALA-GBA-2026-0894')
        self.assertGreaterEqual(len(proj['timelines']), 5)
        self.assertGreaterEqual(len(proj['documents']), 3)

    def test_admin_stage_advance(self):
        # Login as Admin
        login_res = self.client.post('/api/auth/login', json={
            'email': 'admin@bengaluruapprovals.com',
            'password': 'admin123'
        })
        self.assertEqual(login_res.status_code, 200)

        # Get project id
        proj_res = self.client.get('/api/admin/projects')
        proj_id = proj_res.get_json()['projects'][0]['id']

        # Advance stage to Site Inspection
        advance_res = self.client.patch(f'/api/admin/projects/{proj_id}/stage', json={
            'stage': 'Site Inspection',
            'remarks': 'AE inspection completed with positive remarks.'
        })
        self.assertEqual(advance_res.status_code, 200)
        updated_proj = advance_res.get_json()['project']
        self.assertEqual(updated_proj['current_stage'], 'Site Inspection')

        # Verify client portal immediately reflects new stage
        portal_check = self.client.get('/api/client/projects?reference_no=SAKALA-GBA-2026-0894')
        self.assertEqual(portal_check.get_json()['projects'][0]['current_stage'], 'Site Inspection')

    def test_admin_service_cms_update(self):
        # Login as Admin
        self.client.post('/api/auth/login', json={
            'email': 'admin@bengaluruapprovals.com',
            'password': 'admin123'
        })

        # Get services
        srv_res = self.client.get('/api/admin/services')
        srv_id = srv_res.get_json()['services'][0]['id']

        # Update base fee
        update_res = self.client.put(f'/api/admin/services/{srv_id}', json={
            'base_fee': 42000.0,
            'betterment_rate_sqft': 280.0,
            'scrutiny_rate_sqft': 5.0
        })
        self.assertEqual(update_res.status_code, 200)

        # Verify public API reflects new price
        public_srv = self.client.get('/api/services')
        first_service = public_srv.get_json()['services'][0]
        self.assertEqual(first_service['base_fee'], 42000.0)

if __name__ == '__main__':
    unittest.main()
