from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='client', nullable=False)  # 'admin', 'architect', 'client'
    phone = db.Column(db.String(25), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    projects = db.relationship('Project', backref='client', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None
        }


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    category = db.Column(db.String(80), default='Approval')  # 'Approval', 'Titling', 'CAD Drafting', 'Construction', 'NOC'
    short_desc = db.Column(db.String(255), nullable=False)
    full_desc = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='building')
    base_fee = db.Column(db.Float, default=15000.0)
    betterment_rate_sqft = db.Column(db.Float, default=250.0)  # Rate for betterment fees if applicable
    scrutiny_rate_sqft = db.Column(db.Float, default=3.5)      # Municipal scrutiny per sq ft
    turnaround_days = db.Column(db.String(50), default='14-21 Days')
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    features_json = db.Column(db.Text, default='[]')  # JSON array stored as string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        import json
        try:
            features = json.loads(self.features_json) if self.features_json else []
        except Exception:
            features = []
            
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'category': self.category,
            'short_desc': self.short_desc,
            'full_desc': self.full_desc,
            'icon': self.icon,
            'base_fee': self.base_fee,
            'betterment_rate_sqft': self.betterment_rate_sqft,
            'scrutiny_rate_sqft': self.scrutiny_rate_sqft,
            'turnaround_days': self.turnaround_days,
            'is_active': self.is_active,
            'display_order': self.display_order,
            'features': features
        }


class Lead(db.Model):
    __tablename__ = 'leads'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    plot_location = db.Column(db.String(150), nullable=True)
    plot_dimensions = db.Column(db.String(80), nullable=True)  # e.g., '30x40', '40x60', '50x80'
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=True)
    service_title = db.Column(db.String(150), nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='new')  # 'new', 'contacted', 'quotation_sent', 'converted', 'archived'
    internal_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    service = db.relationship('Service', backref='leads', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'plot_location': self.plot_location,
            'plot_dimensions': self.plot_dimensions,
            'service_id': self.service_id,
            'service_title': self.service_title or (self.service.title if self.service else 'General Consultation'),
            'message': self.message,
            'status': self.status,
            'internal_notes': self.internal_notes or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    reference_no = db.Column(db.String(60), unique=True, nullable=False)  # e.g. 'SAKALA-GBA-2026-0894'
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_name = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    plot_location = db.Column(db.String(150), nullable=False)
    ward_no = db.Column(db.String(50), nullable=True)
    survey_no = db.Column(db.String(80), nullable=True)
    authority = db.Column(db.String(50), default='GBA / BBMP')  # 'GBA', 'BBMP', 'BDA', 'BIAAPA', 'BMRDA', 'STRR', 'BMICPA'
    current_stage = db.Column(db.String(50), default='Drafting')  # 'Drafting', 'PreDCR Scrutiny', 'AutoDCR Submission', 'Site Inspection', 'NOC Clearance', 'Approved'
    nambike_nakshe_eligible = db.Column(db.Boolean, default=False)
    plot_area_sqft = db.Column(db.Float, default=1200.0)
    builtup_area_sqft = db.Column(db.Float, default=2400.0)
    assigned_architect = db.Column(db.String(120), default='Ar. Rajesh V., CA/2012/55481')
    completion_percent = db.Column(db.Integer, default=20)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    timelines = db.relationship('ProjectTimeline', backref='project', cascade='all, delete-orphan', lazy=True, order_by='ProjectTimeline.id')
    documents = db.relationship('ProjectDocument', backref='project', cascade='all, delete-orphan', lazy=True, order_by='ProjectDocument.id')

    def to_dict(self, include_details=True):
        data = {
            'id': self.id,
            'reference_no': self.reference_no,
            'client_id': self.client_id,
            'client_name': self.client_name,
            'title': self.title,
            'plot_location': self.plot_location,
            'ward_no': self.ward_no,
            'survey_no': self.survey_no,
            'authority': self.authority,
            'current_stage': self.current_stage,
            'nambike_nakshe_eligible': self.nambike_nakshe_eligible,
            'plot_area_sqft': self.plot_area_sqft,
            'builtup_area_sqft': self.builtup_area_sqft,
            'assigned_architect': self.assigned_architect,
            'completion_percent': self.completion_percent,
            'remarks': self.remarks or '',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M') if self.updated_at else None
        }
        if include_details:
            data['timelines'] = [t.to_dict() for t in self.timelines]
            data['documents'] = [d.to_dict() for d in self.documents]
        return data


class ProjectTimeline(db.Model):
    __tablename__ = 'project_timelines'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    stage_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'completed', 'in_progress', 'pending'
    date_updated = db.Column(db.String(50), nullable=True)
    remarks = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'stage_name': self.stage_name,
            'status': self.status,
            'date_updated': self.date_updated,
            'remarks': self.remarks or ''
        }


class ProjectDocument(db.Model):
    __tablename__ = 'project_documents'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    doc_type = db.Column(db.String(50), default='OTHER')  # 'CAD_DWG', 'SANCTION_CERT', 'E_KHATA', 'EC', 'NOC', 'OTHER'
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_size_display = db.Column(db.String(30), default='1.2 MB')
    is_downloadable = db.Column(db.Boolean, default=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'doc_type': self.doc_type,
            'filename': self.filename,
            'file_size_display': self.file_size_display,
            'is_downloadable': self.is_downloadable,
            'uploaded_at': self.uploaded_at.strftime('%Y-%m-%d %H:%M') if self.uploaded_at else None
        }


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    category = db.Column(db.String(80), default='Zoning Regulations')
    excerpt = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='Principal Architect')
    read_time = db.Column(db.String(30), default='4 min read')
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'category': self.category,
            'excerpt': self.excerpt,
            'content': self.content,
            'author': self.author,
            'read_time': self.read_time,
            'is_published': self.is_published,
            'created_at': self.created_at.strftime('%b %d, %Y') if self.created_at else None
        }
