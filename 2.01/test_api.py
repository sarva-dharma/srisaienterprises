"""
TaskFlow Studio 2.0 - Automated Test Suite
Verifies backend Flask server, SQLite persistence, 4-stage workflow,
checklists, bulk operations, export/import, and analytics endpoints.
"""

import unittest
import json
from app import app, db, Task

class TaskFlow2TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            # Seed sample test tasks
            t1 = Task(
                title='Test Task 1',
                category='Backend',
                priority='High',
                status='pending',
                assignee='Alex Chen',
                checklist=json.dumps([{'id': 1, 'text': 'Subtask 1', 'done': False}])
            )
            t2 = Task(
                title='Test Task 2',
                category='Frontend',
                priority='Urgent',
                status='in_progress',
                assignee='Sarah Lin',
                due_date='2020-01-01', # guaranteed overdue
                checklist=json.dumps([{'id': 1, 'text': 'Item A', 'done': True}])
            )
            t3 = Task(
                title='Test Task 3',
                category='DevOps',
                priority='Medium',
                status='review',
                assignee='Marcus Brody'
            )
            t4 = Task(
                title='Test Task 4',
                category='Design',
                priority='Low',
                status='completed',
                assignee='Elena Vance'
            )
            db.session.add_all([t1, t2, t3, t4])
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_01_health_and_index(self):
        """Verify index HTML and health endpoint."""
        r_index = self.client.get('/')
        self.assertEqual(r_index.status_code, 200)
        self.assertIn(b'TaskFlow', r_index.data)

        r_health = self.client.get('/api/health')
        self.assertEqual(r_health.status_code, 200)
        self.assertEqual(r_health.get_json()['status'], 'healthy')

    def test_02_get_tasks_and_stages(self):
        """Verify fetching tasks across all 4 stages."""
        r = self.client.get('/api/tasks')
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        self.assertEqual(data['count'], 4)

        # Check checklist summary serialization
        t1 = next(t for t in data['tasks'] if t['title'] == 'Test Task 1')
        self.assertEqual(t1['checklist_summary']['total'], 1)
        self.assertEqual(t1['checklist_summary']['done'], 0)

    def test_03_create_task_with_checklist(self):
        """Verify creating task with checklist items and assignee."""
        payload = {
            'title': 'New Feature Task',
            'description': 'Integration details',
            'category': 'Architecture',
            'priority': 'Urgent',
            'status': 'pending',
            'assignee': 'Alex Chen',
            'checklist': [
                {'id': 1, 'text': 'Step 1', 'done': True},
                {'id': 2, 'text': 'Step 2', 'done': False}
            ]
        }
        r = self.client.post('/api/tasks', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(r.status_code, 201)
        data = r.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(data['task']['assignee'], 'Alex Chen')
        self.assertEqual(data['task']['checklist_summary']['total'], 2)
        self.assertEqual(data['task']['checklist_summary']['done'], 1)

    def test_04_toggle_checklist_item(self):
        """Verify toggling checklist item status."""
        r = self.client.post('/api/tasks/1/checklist/toggle', data=json.dumps({'itemId': 1}), content_type='application/json')
        self.assertEqual(r.status_code, 200)
        data = r.get_json()
        item = next(i for i in data['task']['checklist'] if i['id'] == 1)
        self.assertTrue(item['done'])

    def test_05_stage_transitions(self):
        """Verify moving a task between pending, in_progress, review, completed."""
        for stage in ['in_progress', 'review', 'completed']:
            r = self.client.put('/api/tasks/1', data=json.dumps({'status': stage}), content_type='application/json')
            self.assertEqual(r.status_code, 200)
            self.assertEqual(r.get_json()['task']['status'], stage)

    def test_06_bulk_operations(self):
        """Verify bulk status change and bulk delete."""
        # Bulk status update
        bulk_update_payload = {
            'action': 'update_status',
            'ids': [1, 2],
            'status': 'completed'
        }
        r = self.client.post('/api/tasks/bulk', data=json.dumps(bulk_update_payload), content_type='application/json')
        self.assertEqual(r.status_code, 200)

        r_check = self.client.get('/api/tasks?status=completed')
        self.assertEqual(r_check.get_json()['count'], 3) # t1, t2, and original t4

        # Bulk delete
        bulk_delete_payload = {
            'action': 'delete',
            'ids': [3, 4]
        }
        r_del = self.client.post('/api/tasks/bulk', data=json.dumps(bulk_delete_payload), content_type='application/json')
        self.assertEqual(r_del.status_code, 200)

        r_all = self.client.get('/api/tasks')
        self.assertEqual(r_all.get_json()['count'], 2)

    def test_07_export_json_and_csv(self):
        """Verify export functionality in JSON and CSV formats."""
        # JSON
        r_json = self.client.get('/api/tasks/export?format=json')
        self.assertEqual(r_json.status_code, 200)
        self.assertEqual(r_json.mimetype, 'application/json')
        tasks = json.loads(r_json.data)
        self.assertEqual(len(tasks), 4)

        # CSV
        r_csv = self.client.get('/api/tasks/export?format=csv')
        self.assertEqual(r_csv.status_code, 200)
        self.assertEqual(r_csv.mimetype, 'text/csv')
        self.assertIn(b'Title,Category,Priority', r_csv.data)

    def test_08_import_tasks(self):
        """Verify importing tasks from JSON array."""
        import_payload = [
            {'title': 'Imported Task Alpha', 'category': 'QA', 'priority': 'High', 'assignee': 'Tester'},
            {'title': 'Imported Task Beta', 'category': 'Ops', 'priority': 'Low', 'assignee': 'Admin'}
        ]
        r = self.client.post('/api/tasks/import', data=json.dumps(import_payload), content_type='application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()['count'], 2)

        r_tasks = self.client.get('/api/tasks')
        self.assertEqual(r_tasks.get_json()['count'], 6)

    def test_09_reset_data(self):
        """Verify resetting database to demo seed data."""
        r = self.client.post('/api/reset-data')
        self.assertEqual(r.status_code, 200)
        r_tasks = self.client.get('/api/tasks')
        self.assertEqual(r_tasks.get_json()['count'], 8)

    def test_10_analytics_stats(self):
        """Verify stats including overdue count, review stage, and distributions."""
        r = self.client.get('/api/stats')
        self.assertEqual(r.status_code, 200)
        stats = r.get_json()['stats']
        self.assertEqual(stats['total'], 4)
        self.assertEqual(stats['review'], 1)
        self.assertEqual(stats['overdue'], 1) # task 2
        self.assertEqual(len(stats['assignees']), 4)

if __name__ == '__main__':
    unittest.main()
