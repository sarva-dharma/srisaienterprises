from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models import Service, Lead, BlogPost
from backend.services.jurisdiction_data import (
    BENGALURU_JURISDICTION_REGISTRY,
    evaluate_sanction_bylaws
)

public_bp = Blueprint('public_bp', __name__)

@public_bp.route('/services', methods=['GET'])
def get_services():
    """Retrieve all active services ordered by display_order."""
    services = Service.query.filter_by(is_active=True).order_by(Service.display_order.asc()).all()
    return jsonify({
        'count': len(services),
        'services': [s.to_dict() for s in services]
    })


@public_bp.route('/services/<slug>', methods=['GET'])
def get_service_detail(slug):
    service = Service.query.filter_by(slug=slug, is_active=True).first()
    if not service:
        return jsonify({'error': 'Service not found'}), 404
    return jsonify({'service': service.to_dict()})


@public_bp.route('/jurisdictions', methods=['GET'])
def get_jurisdictions():
    """Retrieve list of registered Bengaluru localities and zones."""
    return jsonify({
        'localities': [
            {
                'id': item['id'],
                'name': item['name'],
                'zone': item['zone'],
                'primary_authority': item['primary_authority'],
                'nambike_nakshe_active': item['nambike_nakshe_active']
            }
            for item in BENGALURU_JURISDICTION_REGISTRY
        ]
    })


@public_bp.route('/jurisdictions/check', methods=['POST'])
def check_jurisdiction():
    """
    Evaluates plot parameters against GBA 2026, Nambike Nakshe,
    BBMP/BDA/BIAAPA/STRR bylaws, setbacks, FAR, and NOCs.
    """
    data = request.get_json() or {}
    locality_id = data.get('locality_id', 'whitefield')
    plot_width = float(data.get('plot_width', 30))
    plot_length = float(data.get('plot_length', 40))
    road_width = float(data.get('road_width', 30))
    building_type = data.get('building_type', 'Residential')

    result = evaluate_sanction_bylaws(
        locality_id=locality_id,
        plot_width=plot_width,
        plot_length=plot_length,
        road_width=road_width,
        building_type=building_type
    )

    return jsonify(result)


@public_bp.route('/calculator/estimate', methods=['POST'])
def calculate_estimate():
    """
    Computes estimated municipal scrutiny fees, betterment levy,
    AutoDCR drafting, and architect liaisoning charges.
    """
    data = request.get_json() or {}
    plot_width = float(data.get('plot_width', 30))
    plot_length = float(data.get('plot_length', 40))
    floors = int(data.get('floors', 3))  # e.g. G+2 = 3 floors
    has_b_khata = bool(data.get('has_b_khata', False))
    locality_id = data.get('locality_id', 'whitefield')

    plot_area_sqft = plot_width * plot_length
    builtup_area_sqft = plot_area_sqft * 0.75 * floors  # Approx coverage per floor

    # Lookup locality betterment rate
    loc = next((l for l in BENGALURU_JURISDICTION_REGISTRY if l['id'] == locality_id), None)
    betterment_rate = loc['typical_betterment_rate'] if loc else 250

    # Municipal Scrutiny fee (approx 3.5 INR per sq ft builtup + cess)
    scrutiny_fee = round(builtup_area_sqft * 3.5 + 2500, 2)
    
    # Ground water / RWH / Tree cess (statutory municipal levy)
    statutory_cess = round(builtup_area_sqft * 1.8, 2)

    # Betterment charges if B-Khata conversion is needed
    betterment_fee = round(plot_area_sqft * betterment_rate, 2) if has_b_khata else 0.0

    # AutoDCR / PreDCR drafting and Liaisoning fee
    cad_drafting_fee = round(max(18000.0, builtup_area_sqft * 8.5), 2)
    liaisoning_fee = round(max(25000.0, builtup_area_sqft * 10.0), 2)

    total_estimated = scrutiny_fee + statutory_cess + betterment_fee + cad_drafting_fee + liaisoning_fee

    return jsonify({
        'plot_area_sqft': plot_area_sqft,
        'builtup_area_sqft': builtup_area_sqft,
        'floors': floors,
        'has_b_khata': has_b_khata,
        'breakdown': {
            'municipal_scrutiny_fee': scrutiny_fee,
            'statutory_cess_rwh': statutory_cess,
            'betterment_levy': betterment_fee,
            'autodcr_drafting_fee': cad_drafting_fee,
            'architect_liaisoning_fee': liaisoning_fee
        },
        'total_estimated': total_estimated,
        'turnaround_estimate': '14-21 Business Days (Sakala SLA Guarantee)'
    })


@public_bp.route('/leads', methods=['POST'])
def submit_lead():
    """Capture booking consultation / lead inquiry."""
    data = request.get_json() or {}
    full_name = data.get('full_name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()

    if not full_name or not phone:
        return jsonify({'error': 'Name and phone number are required'}), 400

    lead = Lead(
        full_name=full_name,
        email=email or 'not-provided@client.com',
        phone=phone,
        plot_location=data.get('plot_location', ''),
        plot_dimensions=data.get('plot_dimensions', ''),
        service_id=data.get('service_id'),
        service_title=data.get('service_title', 'General Building Plan Consultation'),
        message=data.get('message', ''),
        status='new'
    )
    db.session.add(lead)
    db.session.commit()

    return jsonify({
        'message': 'Consultation request received successfully! Our senior architect will contact you within 2 hours.',
        'lead_id': lead.id
    }), 201


@public_bp.route('/blogs', methods=['GET'])
def get_blogs():
    """Retrieve published zoning knowledge hub articles."""
    blogs = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).all()
    return jsonify({
        'blogs': [b.to_dict() for b in blogs]
    })
