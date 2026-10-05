import os
import json
import csv
import io
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, jsonify, Response, abort
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask Application
app = Flask(__name__, template_folder='templates', static_folder='static')

# Application Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'taskflow-studio-secret-key-2026')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///taskflow.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True, default='')
    category = db.Column(db.String(50), nullable=False, default='General')
    priority = db.Column(db.String(20), nullable=False, default='Medium') # Low, Medium, High, Urgent
    status = db.Column(db.String(20), nullable=False, default='pending') # pending, in_progress, review, completed
    due_date = db.Column(db.String(30), nullable=True)
    assignee = db.Column(db.String(80), nullable=False, default='Unassigned')
    checklist = db.Column(db.Text, nullable=True, default='[]') # JSON string of [{"id": 1, "text": "...", "done": false}]
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_checklist_list(self):
        try:
            return json.loads(self.checklist) if self.checklist else []
        except Exception:
            return []

    def set_checklist_list(self, items):
        if isinstance(items, list):
            self.checklist = json.dumps(items)
        else:
            self.checklist = '[]'

    def to_dict(self):
        items = self.get_checklist_list()
        total_subtasks = len(items)
        done_subtasks = sum(1 for item in items if item.get('done'))

        return {
            'id': self.id,
            'title': self.title,
            'description': self.description or '',
            'category': self.category,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date or '',
            'assignee': self.assignee or 'Unassigned',
            'checklist': items,
            'checklist_summary': {
                'total': total_subtasks,
                'done': done_subtasks,
                'percent': round((done_subtasks / total_subtasks * 100), 1) if total_subtasks > 0 else 0
            },
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else '',
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else ''
        }

# Initial Data Seeder
def seed_initial_data():
    if Task.query.count() == 0:
        today = date.today()
        sample_tasks = [
            Task(
                title='Architect Core REST API & Database Schema',
                description='Finalize SQLite and SQLAlchemy data models with clean REST endpoints for full-stack integration.',
                category='Backend',
                priority='High',
                status='completed',
                due_date=(today - timedelta(days=2)).strftime('%Y-%m-%d'),
                assignee='Alex Chen',
                checklist=json.dumps([
                    {'id': 1, 'text': 'Draft schema specifications', 'done': True},
                    {'id': 2, 'text': 'Configure SQLite database connection', 'done': True},
                    {'id': 3, 'text': 'Implement CRUD endpoints', 'done': True}
                ])
            ),
            Task(
                title='Build Responsive Front-End Design System',
                description='Create modern glassmorphic UI components with dark and light themes, responsive grid, and interactive modals.',
                category='Frontend',
                priority='High',
                status='completed',
                due_date=(today - timedelta(days=1)).strftime('%Y-%m-%d'),
                assignee='Sarah Lin',
                checklist=json.dumps([
                    {'id': 1, 'text': 'Define CSS variables and design tokens', 'done': True},
                    {'id': 2, 'text': 'Build responsive grid system', 'done': True},
                    {'id': 3, 'text': 'Integrate theme switcher', 'done': True}
                ])
            ),
            Task(
                title='Implement Drag-and-Drop Kanban Board',
                description='Integrate HTML5 Drag and Drop events allowing seamless card movement across workflow columns.',
                category='Frontend',
                priority='Urgent',
                status='in_progress',
                due_date=today.strftime('%Y-%m-%d'),
                assignee='Sarah Lin',
                checklist=json.dumps([
                    {'id': 1, 'text': 'Implement dragstart and dragover listeners', 'done': True},
                    {'id': 2, 'text': 'Add visual dropzone indicator styling', 'done': True},
                    {'id': 3, 'text': 'Synchronize position state with backend API', 'done': False}
                ])
            ),
            Task(
                title='Integrate Subtask Checklists & Progress Meters',
                description='Allow nested checklist items for each task with real-time percentage indicators on cards.',
                category='Backend',
                priority='High',
                status='in_progress',
                due_date=(today + timedelta(days=1)).strftime('%Y-%m-%d'),
                assignee='Alex Chen',
                checklist=json.dumps([
                    {'id': 1, 'text': 'Add checklist field to database model', 'done': True},
                    {'id': 2, 'text': 'Create checklist toggle API route', 'done': True},
                    {'id': 3, 'text': 'Build modal subtask item creator', 'done': False}
                ])
            ),
            Task(
                title='QA Review: Bulk Operations & CSV Export',
                description='Verify multi-select batch updates, status transitions, and CSV/JSON data export compliance.',
                category='DevOps',
                priority='Medium',
                status='review',
                due_date=(today + timedelta(days=2)).strftime('%Y-%m-%d'),
                assignee='Marcus Brody',
                checklist=json.dumps([
                    {'id': 1, 'text': 'Test bulk status update endpoint', 'done': True},
                    {'id': 2, 'text': 'Verify CSV header structure', 'done': True},
                    {'id': 3, 'text': 'Cross-browser download validation', 'done': False}
                ])
            ),
            Task(
                title='Refine UI/UX Micro-Interactions & Transitions',
                description='Add smooth animations, toast notifications, search highlights, and keyboard shortcuts.',
                category='Design',
                priority='Medium',
                status='pending',
                due_date=(today + timedelta(days=4)).strftime('%Y-%m-%d'),
                assignee='Elena Vance',
                checklist=json.dumps([
                    {'id': 1, 'text': 'Card elevation hover transitions', 'done': False},
                    {'id': 2, 'text': 'Modal backdrop blur styling', 'done': False},
                    {'id': 3, 'text': 'Quick keyboard shortcuts help modal', 'done': False}
                ])
            ),
            Task(
                title='Security Audit & Input Sanitization Review',
                description='Verify XSS protection on rich text inputs, database query parameterized safety, and payload validation.',
                category='DevOps',
                priority='Urgent',
                status='pending',
                due_date=(today - timedelta(days=1)).strftime('%Y-%m-%d'), # Overdue sample
                assignee='Marcus Brody',
                checklist=json.dumps([
                    {'id': 1, 'text': 'Audit API input validation schemas', 'done': True},
                    {'id': 2, 'text': 'Test boundary length conditions', 'done': False}
                ])
            ),
            Task(
                title='Draft Comprehensive API Documentation & README',
                description='Document project architecture, endpoint specifications, and local development instructions.',
                category='Documentation',
                priority='Low',
                status='pending',
                due_date=(today + timedelta(days=7)).strftime('%Y-%m-%d'),
                assignee='Elena Vance',
                checklist=json.dumps([
                    {'id': 1, 'text': 'Document REST API routes', 'done': False},
                    {'id': 2, 'text': 'Provide Windows batch setup guide', 'done': False}
                ])
            )
        ]
        db.session.bulk_save_objects(sample_tasks)
        db.session.commit()
        print("[TaskFlow] Seeded fresh advanced management tasks into database.")

# Frontend View Route
@app.route('/')
def index():
    return render_template('index.html')

# REST API Endpoints
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'app': 'TaskFlow Studio 2.0',
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    search = request.args.get('search', '').strip().lower()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    priority = request.args.get('priority', '').strip()
    assignee = request.args.get('assignee', '').strip()
    overdue_only = request.args.get('overdue', '').strip().lower() == 'true'
    sort_by = request.args.get('sort', 'created_at_desc').strip()

    query = Task.query

    if search:
        query = query.filter(
            db.or_(
                Task.title.ilike(f'%{search}%'),
                Task.description.ilike(f'%{search}%'),
                Task.category.ilike(f'%{search}%'),
                Task.assignee.ilike(f'%{search}%')
            )
        )

    if category and category != 'All':
        query = query.filter(Task.category == category)

    if status and status != 'All':
        query = query.filter(Task.status == status)

    if priority and priority != 'All':
        query = query.filter(Task.priority == priority)

    if assignee and assignee != 'All':
        query = query.filter(Task.assignee == assignee)

    if overdue_only:
        today_str = date.today().strftime('%Y-%m-%d')
        query = query.filter(
            Task.status != 'completed',
            Task.due_date.isnot(None),
            Task.due_date != '',
            Task.due_date < today_str
        )

    # Sorting
    if sort_by == 'due_date_asc':
        query = query.order_by(Task.due_date.asc())
    elif sort_by == 'priority_desc':
        priority_case = db.case(
            (Task.priority == 'Urgent', 1),
            (Task.priority == 'High', 2),
            (Task.priority == 'Medium', 3),
            (Task.priority == 'Low', 4),
            else_=5
        )
        query = query.order_by(priority_case)
    elif sort_by == 'title_asc':
        query = query.order_by(Task.title.asc())
    else: # default newest first
        query = query.order_by(Task.created_at.desc())

    tasks = query.all()
    return jsonify({
        'success': True,
        'count': len(tasks),
        'tasks': [task.to_dict() for task in tasks]
    })

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    return jsonify({
        'success': True,
        'task': task.to_dict()
    })

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': 'Invalid or missing JSON payload'}), 400

    title = data.get('title', '').strip()
    if not title:
        return jsonify({'success': False, 'error': 'Task title is required'}), 400

    checklist_items = data.get('checklist', [])
    if isinstance(checklist_items, str):
        try:
            checklist_items = json.loads(checklist_items)
        except Exception:
            checklist_items = []

    new_task = Task(
        title=title,
        description=data.get('description', '').strip(),
        category=data.get('category', 'General').strip() or 'General',
        priority=data.get('priority', 'Medium').strip() or 'Medium',
        status=data.get('status', 'pending').strip() or 'pending',
        due_date=data.get('due_date', '').strip() or None,
        assignee=data.get('assignee', 'Unassigned').strip() or 'Unassigned'
    )
    new_task.set_checklist_list(checklist_items)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Task created successfully',
        'task': new_task.to_dict()
    }), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({'success': False, 'error': 'Invalid or missing JSON payload'}), 400

    if 'title' in data:
        title = data['title'].strip()
        if not title:
            return jsonify({'success': False, 'error': 'Task title cannot be empty'}), 400
        task.title = title

    if 'description' in data:
        task.description = data['description'].strip()

    if 'category' in data:
        task.category = data['category'].strip() or 'General'

    if 'priority' in data:
        task.priority = data['priority'].strip() or 'Medium'

    if 'status' in data:
        task.status = data['status'].strip() or 'pending'

    if 'due_date' in data:
        task.due_date = data['due_date'].strip() or None

    if 'assignee' in data:
        task.assignee = data['assignee'].strip() or 'Unassigned'

    if 'checklist' in data:
        checklist_items = data['checklist']
        if isinstance(checklist_items, str):
            try:
                checklist_items = json.loads(checklist_items)
            except Exception:
                checklist_items = []
        task.set_checklist_list(checklist_items)

    task.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Task updated successfully',
        'task': task.to_dict()
    })

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': f'Task #{task_id} deleted successfully'
    })

@app.route('/api/tasks/<int:task_id>/checklist/toggle', methods=['POST'])
def toggle_checklist_item(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'success': False, 'error': 'Task not found'}), 404

    data = request.get_json(silent=True) or {}
    item_id = data.get('itemId')
    if item_id is None:
        return jsonify({'success': False, 'error': 'itemId is required'}), 400

    items = task.get_checklist_list()
    found = False
    for item in items:
        if item.get('id') == item_id:
            item['done'] = not item.get('done', False)
            found = True
            break

    if not found:
        return jsonify({'success': False, 'error': f'Checklist item {item_id} not found'}), 404

    task.set_checklist_list(items)
    task.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Checklist item toggled',
        'task': task.to_dict()
    })

@app.route('/api/tasks/bulk', methods=['POST'])
def bulk_tasks_action():
    data = request.get_json(silent=True) or {}
    action = data.get('action') # 'update_status' or 'delete'
    task_ids = data.get('ids', [])

    if not task_ids or not isinstance(task_ids, list):
        return jsonify({'success': False, 'error': 'ids list is required'}), 400

    if action == 'delete':
        Task.query.filter(Task.id.in_(task_ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Deleted {len(task_ids)} tasks successfully'
        })
    elif action == 'update_status':
        new_status = data.get('status')
        if not new_status or new_status not in ['pending', 'in_progress', 'review', 'completed']:
            return jsonify({'success': False, 'error': 'Valid status is required'}), 400

        Task.query.filter(Task.id.in_(task_ids)).update({'status': new_status, 'updated_at': datetime.utcnow()}, synchronize_session=False)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Updated status of {len(task_ids)} tasks to {new_status}'
        })
    else:
        return jsonify({'success': False, 'error': 'Unsupported bulk action'}), 400

@app.route('/api/tasks/export', methods=['GET'])
def export_tasks():
    fmt = request.args.get('format', 'json').lower()
    tasks = Task.query.order_by(Task.id.asc()).all()

    if fmt == 'csv':
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Title', 'Category', 'Priority', 'Status', 'Due Date', 'Assignee', 'Subtasks (Done/Total)', 'Description', 'Created At'])
        for t in tasks:
            summary = t.to_dict()['checklist_summary']
            subtasks_str = f"{summary['done']}/{summary['total']}"
            writer.writerow([t.id, t.title, t.category, t.priority, t.status, t.due_date or '', t.assignee, subtasks_str, t.description or '', t.created_at])

        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=tasks_export.csv'}
        )
    else:
        # JSON export
        tasks_data = [t.to_dict() for t in tasks]
        return Response(
            json.dumps(tasks_data, indent=2),
            mimetype='application/json',
            headers={'Content-Disposition': 'attachment; filename=tasks_export.json'}
        )

@app.route('/api/tasks/import', methods=['POST'])
def import_tasks():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, list):
        return jsonify({'success': False, 'error': 'Invalid JSON array payload for import'}), 400

    imported_count = 0
    for item in data:
        title = item.get('title', '').strip()
        if not title:
            continue
        task = Task(
            title=title,
            description=item.get('description', '').strip(),
            category=item.get('category', 'General').strip() or 'General',
            priority=item.get('priority', 'Medium').strip() or 'Medium',
            status=item.get('status', 'pending').strip() or 'pending',
            due_date=item.get('due_date', '').strip() or None,
            assignee=item.get('assignee', 'Unassigned').strip() or 'Unassigned'
        )
        checklist_items = item.get('checklist', [])
        task.set_checklist_list(checklist_items)
        db.session.add(task)
        imported_count += 1

    db.session.commit()
    return jsonify({
        'success': True,
        'message': f'Imported {imported_count} tasks successfully',
        'count': imported_count
    })

@app.route('/api/reset-data', methods=['POST'])
def reset_data():
    Task.query.delete()
    db.session.commit()
    seed_initial_data()
    return jsonify({
        'success': True,
        'message': 'Database reset with fresh demo management data'
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    total = Task.query.count()
    completed = Task.query.filter_by(status='completed').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    review = Task.query.filter_by(status='review').count()
    pending = Task.query.filter_by(status='pending').count()
    high_priority = Task.query.filter(Task.priority.in_(['High', 'Urgent'])).count()

    today_str = date.today().strftime('%Y-%m-%d')
    overdue = Task.query.filter(
        Task.status != 'completed',
        Task.due_date.isnot(None),
        Task.due_date != '',
        Task.due_date < today_str
    ).count()

    completion_rate = round((completed / total * 100), 1) if total > 0 else 0

    # Category breakdown
    categories_raw = db.session.query(Task.category, db.func.count(Task.id)).group_by(Task.category).all()
    categories = [{'name': cat, 'count': count} for cat, count in categories_raw]

    # Assignee breakdown
    assignees_raw = db.session.query(Task.assignee, db.func.count(Task.id)).group_by(Task.assignee).all()
    assignees = [{'name': a, 'count': count} for a, count in assignees_raw]

    # Priority breakdown
    priority_raw = db.session.query(Task.priority, db.func.count(Task.id)).group_by(Task.priority).all()
    priorities = [{'name': p, 'count': count} for p, count in priority_raw]

    return jsonify({
        'success': True,
        'stats': {
            'total': total,
            'completed': completed,
            'in_progress': in_progress,
            'review': review,
            'pending': pending,
            'high_priority': high_priority,
            'overdue': overdue,
            'completion_rate': completion_rate,
            'categories': categories,
            'assignees': assignees,
            'priorities': priorities
        }
    })

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Resource not found'}), 404
    return render_template('index.html'), 200

@app.errorhandler(500)
def server_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# Initialize DB and Seed Data
with app.app_context():
    try:
        db.create_all()
        # Check if table schema matches current model
        _ = db.session.query(Task.assignee).first()
        if Task.query.count() == 0:
            seed_initial_data()
    except Exception as e:
        print(f"[TaskFlow] Refreshing database schema ({e})...")
        db.session.rollback()
        db.drop_all()
        db.create_all()
        seed_initial_data()

if __name__ == '__main__':
    print("==================================================")
    print(" 🚀 TaskFlow Studio 2.0 Management Server Running!")
    print(" 🌐 Access Website: http://127.0.0.1:5000")
    print(" 📡 REST API:       http://127.0.0.1:5000/api/tasks")
    print("==================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
