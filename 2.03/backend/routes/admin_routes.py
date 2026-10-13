from datetime import datetime
import json
from flask import Blueprint, request, jsonify, session
from backend.database import db
from backend.models import User, Lead, Project, ProjectTimeline, ProjectDocument, Service, BlogPost

admin_bp = Blueprint('admin_bp', __name__)

def require_admin_or_architect():
    """Verify session has admin or architect authorization."""
    role = session.get('user_role')
    if role not in ['admin', 'architect']:
        return jsonify({'error': 'Unauthorized: Admin or Architect privileges required'}), 403
    return None


@admin_bp.route('/metrics', methods=['GET'])
def get_metrics():
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    total_leads = Lead.query.count()
    new_leads = Lead.query.filter_by(status='new').count()
    active_projects = Project.query.filter(Project.current_stage != 'Approved').count()
    approved_projects = Project.query.filter_by(current_stage='Approved').count()
    total_services = Service.query.count()

    return jsonify({
        'total_leads': total_leads,
        'new_leads': new_leads,
        'active_projects': active_projects,
        'approved_projects': approved_projects,
        'total_services': total_services
    })


# ---------------- LEAD MANAGEMENT (CRM) ---------------- #

@admin_bp.route('/leads', methods=['GET'])
def get_leads():
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    status_filter = request.args.get('status', '').strip()
    query = Lead.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    leads = query.order_by(Lead.created_at.desc()).all()
    return jsonify({
        'count': len(leads),
        'leads': [l.to_dict() for l in leads]
    })


@admin_bp.route('/leads/<int:lead_id>', methods=['PATCH'])
def update_lead(lead_id):
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    lead = Lead.query.get_or_404(lead_id)
    data = request.get_json() or {}

    if 'status' in data:
        lead.status = data['status']
    if 'internal_notes' in data:
        lead.internal_notes = data['internal_notes']

    lead.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'message': 'Lead updated successfully',
        'lead': lead.to_dict()
    })


# ---------------- CLIENT APPLICATION TRACKER ---------------- #

@admin_bp.route('/projects', methods=['GET'])
def get_all_projects():
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    projects = Project.query.order_by(Project.updated_at.desc()).all()
    return jsonify({
        'count': len(projects),
        'projects': [p.to_dict(include_details=True) for p in projects]
    })


@admin_bp.route('/projects', methods=['POST'])
def create_project():
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    data = request.get_json() or {}
    client_id = data.get('client_id')
    client_name = data.get('client_name', '').strip()
    title = data.get('title', '').strip()
    plot_location = data.get('plot_location', '').strip()
    authority = data.get('authority', 'GBA / BBMP')
    plot_area = float(data.get('plot_area_sqft', 1200))
    builtup_area = float(data.get('builtup_area_sqft', 2400))
    nambike_eligible = bool(data.get('nambike_nakshe_eligible', False))

    if not client_name or not title or not plot_location:
        return jsonify({'error': 'Client name, project title, and plot location are required'}), 400

    # If client_id is not given, find or create client user
    if not client_id:
        email = data.get('client_email', f"client_{int(datetime.utcnow().timestamp())}@bengaluru.in")
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name=client_name, email=email, role='client', phone=data.get('client_phone', ''))
            user.set_password('client123')
            db.session.add(user)
            db.session.flush()
        client_id = user.id

    # Generate unique Sakala Reference Number
    ref_year = datetime.utcnow().year
    random_suffix = int(datetime.utcnow().timestamp()) % 10000
    authority_code = authority.split()[0].replace('/', '')
    reference_no = f"SAKALA-{authority_code}-{ref_year}-{random_suffix:04d}"

    project = Project(
        reference_no=reference_no,
        client_id=client_id,
        client_name=client_name,
        title=title,
        plot_location=plot_location,
        ward_no=data.get('ward_no', 'Ward 85'),
        survey_no=data.get('survey_no', 'Sy. No. 44/2'),
        authority=authority,
        current_stage='Drafting',
        nambike_nakshe_eligible=nambike_eligible,
        plot_area_sqft=plot_area,
        builtup_area_sqft=builtup_area,
        assigned_architect=data.get('assigned_architect', 'Ar. Rajesh V., CA/2012/55481'),
        completion_percent=15,
        remarks=data.get('remarks', 'Initial architectural survey and site boundary CAD plotting initialized.')
    )
    db.session.add(project)
    db.session.flush()

    # Create initial stages
    stages = [
        ('Drafting', 'in_progress', 'Architectural base CAD drafting & layer preparation.'),
        ('PreDCR Scrutiny', 'pending', 'Mathematical pre-check for setbacks, light, ventilation, FAR.'),
        ('AutoDCR Submission', 'pending', 'Government EoDB-OBPS portal algorithm verification.'),
        ('Site Inspection', 'pending', 'Municipal engineer field survey or Nambike Nakshe self-verification.'),
        ('NOC Clearance', 'pending', 'BESCOM / BWSSB / Airport Authority clearances.'),
        ('Approved', 'pending', 'Digitally signed Building Plan Sanction order release.')
    ]
    for stage_name, status, remarks in stages:
        timeline = ProjectTimeline(
            project_id=project.id,
            stage_name=stage_name,
            status=status,
            date_updated=datetime.utcnow().strftime('%d-%b-%Y') if status != 'pending' else None,
            remarks=remarks
        )
        db.session.add(timeline)

    db.session.commit()

    return jsonify({
        'message': 'Client project created successfully',
        'project': project.to_dict(include_details=True)
    }), 201


@admin_bp.route('/projects/<int:project_id>/stage', methods=['PATCH'])
def update_project_stage(project_id):
    """
    Update project stage. This immediately reflects on the client's portal!
    Stages: Drafting -> PreDCR Scrutiny -> AutoDCR Submission -> Site Inspection -> NOC Clearance -> Approved
    """
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    project = Project.query.get_or_404(project_id)
    data = request.get_json() or {}
    new_stage = data.get('stage')
    remarks = data.get('remarks', '')

    valid_stages = ['Drafting', 'PreDCR Scrutiny', 'AutoDCR Submission', 'Site Inspection', 'NOC Clearance', 'Approved']
    if new_stage not in valid_stages:
        return jsonify({'error': f'Invalid stage. Must be one of: {", ".join(valid_stages)}'}), 400

    stage_percentages = {
        'Drafting': 20,
        'PreDCR Scrutiny': 40,
        'AutoDCR Submission': 60,
        'Site Inspection': 75,
        'NOC Clearance': 85,
        'Approved': 100
    }

    project.current_stage = new_stage
    project.completion_percent = stage_percentages.get(new_stage, 50)
    if remarks:
        project.remarks = remarks
    project.updated_at = datetime.utcnow()

    # Update timelines
    found_current = False
    now_str = datetime.utcnow().strftime('%d-%b-%Y %H:%M')
    for timeline in project.timelines:
        if timeline.stage_name == new_stage:
            timeline.status = 'completed' if new_stage == 'Approved' else 'in_progress'
            timeline.date_updated = now_str
            if remarks: timeline.remarks = remarks
            found_current = True
        elif not found_current:
            timeline.status = 'completed'
            if not timeline.date_updated:
                timeline.date_updated = now_str
        else:
            timeline.status = 'pending'

    # If approved and no sanction cert exists, attach one
    if new_stage == 'Approved':
        has_cert = any(d.doc_type == 'SANCTION_CERT' for d in project.documents)
        if not has_cert:
            sanction_doc = ProjectDocument(
                project_id=project.id,
                title='Digitally Signed Building Plan Sanction Order (LP-GBA)',
                doc_type='SANCTION_CERT',
                filename=f"{project.reference_no}_Sanction_Order.pdf",
                file_path=f"uploads/{project.reference_no}_Sanction_Order.pdf",
                file_size_display='2.4 MB',
                is_downloadable=True
            )
            db.session.add(sanction_doc)

    db.session.commit()

    return jsonify({
        'message': f'Project stage advanced to {new_stage}',
        'project': project.to_dict(include_details=True)
    })


@admin_bp.route('/projects/<int:project_id>/documents', methods=['POST'])
def add_project_document(project_id):
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    project = Project.query.get_or_404(project_id)
    data = request.get_json() or {}

    title = data.get('title', '').strip()
    doc_type = data.get('doc_type', 'OTHER')
    filename = data.get('filename', f"{doc_type}_{project.reference_no}.pdf")
    file_size = data.get('file_size_display', '1.8 MB')

    if not title:
        return jsonify({'error': 'Document title is required'}), 400

    doc = ProjectDocument(
        project_id=project.id,
        title=title,
        doc_type=doc_type,
        filename=filename,
        file_path=f"uploads/{filename}",
        file_size_display=file_size,
        is_downloadable=True
    )
    db.session.add(doc)
    db.session.commit()

    return jsonify({
        'message': 'Document attached to project successfully',
        'document': doc.to_dict()
    }), 201


# ---------------- SERVICE & CONTENT EDITOR (CMS) ---------------- #

@admin_bp.route('/services', methods=['GET'])
def get_all_services_admin():
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    services = Service.query.order_by(Service.display_order.asc()).all()
    return jsonify({
        'count': len(services),
        'services': [s.to_dict() for s in services]
    })


@admin_bp.route('/services', methods=['POST'])
def create_service():
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    data = request.get_json() or {}
    title = data.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400

    slug = title.lower().replace(' ', '-').replace('&', 'and').replace('/', '-')
    
    # Check if slug exists
    counter = 1
    original_slug = slug
    while Service.query.filter_by(slug=slug).first():
        slug = f"{original_slug}-{counter}"
        counter += 1

    service = Service(
        title=title,
        slug=slug,
        category=data.get('category', 'Approval'),
        short_desc=data.get('short_desc', ''),
        full_desc=data.get('full_desc', ''),
        icon=data.get('icon', 'building'),
        base_fee=float(data.get('base_fee', 15000.0)),
        betterment_rate_sqft=float(data.get('betterment_rate_sqft', 250.0)),
        scrutiny_rate_sqft=float(data.get('scrutiny_rate_sqft', 3.5)),
        turnaround_days=data.get('turnaround_days', '14-21 Days'),
        is_active=bool(data.get('is_active', True)),
        features_json=json.dumps(data.get('features', []))
    )
    db.session.add(service)
    db.session.commit()

    return jsonify({
        'message': 'New service added to catalog',
        'service': service.to_dict()
    }), 201


@admin_bp.route('/services/<int:service_id>', methods=['PUT', 'PATCH'])
def update_service(service_id):
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    service = Service.query.get_or_404(service_id)
    data = request.get_json() or {}

    if 'title' in data: service.title = data['title']
    if 'category' in data: service.category = data['category']
    if 'short_desc' in data: service.short_desc = data['short_desc']
    if 'full_desc' in data: service.full_desc = data['full_desc']
    if 'base_fee' in data: service.base_fee = float(data['base_fee'])
    if 'betterment_rate_sqft' in data: service.betterment_rate_sqft = float(data['betterment_rate_sqft'])
    if 'scrutiny_rate_sqft' in data: service.scrutiny_rate_sqft = float(data['scrutiny_rate_sqft'])
    if 'turnaround_days' in data: service.turnaround_days = data['turnaround_days']
    if 'is_active' in data: service.is_active = bool(data['is_active'])
    if 'features' in data: service.features_json = json.dumps(data['features'])

    db.session.commit()

    return jsonify({
        'message': 'Service details and pricing updated successfully',
        'service': service.to_dict()
    })


@admin_bp.route('/blogs', methods=['POST'])
def create_blog_post():
    auth_err = require_admin_or_architect()
    if auth_err: return auth_err

    data = request.get_json() or {}
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    slug = title.lower().replace(' ', '-').replace('/', '-')
    counter = 1
    orig_slug = slug
    while BlogPost.query.filter_by(slug=slug).first():
        slug = f"{orig_slug}-{counter}"
        counter += 1

    blog = BlogPost(
        title=title,
        slug=slug,
        category=data.get('category', 'Zoning Regulations'),
        excerpt=data.get('excerpt', title),
        content=content,
        author=data.get('author', 'Senior Liaisoning Architect'),
        read_time=data.get('read_time', '4 min read'),
        is_published=True
    )
    db.session.add(blog)
    db.session.commit()

    return jsonify({
        'message': 'Blog article published to Knowledge Hub',
        'blog': blog.to_dict()
    }), 201
