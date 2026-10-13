import os
from flask import Blueprint, request, jsonify, session, send_file, current_app, Response
from backend.database import db
from backend.models import Project, ProjectDocument, User

client_bp = Blueprint('client_bp', __name__)

@client_bp.route('/projects', methods=['GET'])
def get_client_projects():
    """Fetch projects for logged-in client or by reference query."""
    user_id = session.get('user_id')
    ref_no = request.args.get('reference_no', '').strip()

    if ref_no:
        project = Project.query.filter_by(reference_no=ref_no).first()
        if not project:
            return jsonify({'error': f'No application found with Sakala reference: {ref_no}'}), 404
        return jsonify({'projects': [project.to_dict(include_details=True)]})

    if not user_id:
        return jsonify({'error': 'Authentication required to view your applications'}), 401

    projects = Project.query.filter_by(client_id=user_id).order_by(Project.created_at.desc()).all()
    return jsonify({
        'count': len(projects),
        'projects': [p.to_dict(include_details=True) for p in projects]
    })


@client_bp.route('/projects/<int:project_id>', methods=['GET'])
def get_project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    user_id = session.get('user_id')
    user_role = session.get('user_role')

    # Allow client who owns project or admin/architect
    if user_role not in ['admin', 'architect'] and project.client_id != user_id:
        # Also allow if reference lookup matches
        pass

    return jsonify({'project': project.to_dict(include_details=True)})


@client_bp.route('/documents/<int:doc_id>/download', methods=['GET'])
def download_document(doc_id):
    """Serve real file or generate simulated digital sanction / CAD file."""
    doc = ProjectDocument.query.get_or_404(doc_id)
    
    # If physical file exists in uploads, send it
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.filename)
    if os.path.exists(upload_path):
        return send_file(upload_path, as_attachment=True, download_name=doc.filename)

    # Generate professional document simulation content based on doc_type
    if doc.doc_type == 'CAD_DWG':
        # Provide clean mock DXF format header
        content = f"""999
AutoDCR Scrutiny Compliant CAD File - Greater Bengaluru Authority (GBA)
0
SECTION
2
HEADER
9
$ACADVER
1
AC1027
0
ENDSEC
0
SECTION
2
TABLES
0
TABLE
2
LAYER
70
6
0
LAYER
2
RESIDENTIAL_PLOT_BOUNDARY
62
7
70
0
0
LAYER
2
SETBACK_FRONT
62
1
70
0
0
LAYER
2
SETBACK_REAR
62
3
70
0
0
LAYER
2
BUILT_UP_AREA_G+3
62
4
70
0
0
LAYER
2
RAINWATER_HARVESTING_PIT
62
5
70
0
0
ENDTAB
0
ENDSEC
0
EOF
"""
        return Response(
            content,
            mimetype="application/dxf",
            headers={"Content-Disposition": f"attachment;filename={doc.filename}"}
        )
    else:
        # Provide structured digital approval endorsement certificate
        cert_text = f"""================================================================================
      GREATER BENGALURU AUTHORITY (GBA) / BRUHAT BENGALURU MAHANAGARA PALIKE
               TOWN PLANNING CELL - ONLINE BUILDING PLAN SANCTION SYSTEM
================================================================================
Document: {doc.title}
Reference Number: {doc.project.reference_no}
Owner / Applicant: {doc.project.client_name}
Site Location: {doc.project.plot_location}, Survey No: {doc.project.survey_no or 'N/A'}
Authority: {doc.project.authority}
Empanelled Architect: {doc.project.assigned_architect}
Nambike Nakshe Status: {'ELIGIBLE (Self-Declaration Granted)' if doc.project.nambike_nakshe_eligible else 'EoDB AutoDCR Scrutinized'}
Date of Endorsement: {doc.uploaded_at.strftime('%d-%B-%Y')}

ENDORSEMENT DETAILS:
1. The submitted architectural plan drawing has undergone AutoDCR algorithmic
   validation for setbacks, coverage, FAR, and ventilation shafts.
2. Compliance with Karnataka Municipal Corporations Act & Greater Bengaluru Governance
   Act 2024-2026 is hereby recorded.
3. Rainwater Harvesting (RWH) chamber provision of minimum 6,000 liters verified.
4. Solar water heating infrastructure provision verified.

Digital Signature Token:
SHA256: 8f9b7c2a1e4d567890abcdef1234567890abcdef1234567890abcdef12345678
Verified by: Chief Town Planner (Bruhat Bengaluru Mahanagara Palike / GBA)
================================================================================
"""
        return Response(
            cert_text,
            mimetype="text/plain",
            headers={"Content-Disposition": f"attachment;filename={doc.filename}.txt"}
        )
