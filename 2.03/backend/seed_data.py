import json
from datetime import datetime, timedelta
from backend.database import db
from backend.models import User, Service, Lead, Project, ProjectTimeline, ProjectDocument, BlogPost

def seed_database():
    """Populate database with initial administrative accounts, core services, and realistic Bengaluru projects."""
    
    # Check if already seeded
    if User.query.filter_by(email='admin@bengaluruapprovals.com').first():
        print("Database already contains seed data.")
        return

    print("Seeding database with Bengaluru municipal data...")

    # 1. Users
    admin_user = User(
        name="Ar. Karthik Somanna (COA Reg. CA/2009/44120)",
        email="admin@bengaluruapprovals.com",
        role="admin",
        phone="+91 98450 12345"
    )
    admin_user.set_password("admin123")
    db.session.add(admin_user)

    client_user = User(
        name="Vikramaditya Hegde",
        email="client@example.com",
        role="client",
        phone="+91 99001 88776"
    )
    client_user.set_password("client123")
    db.session.add(client_user)

    db.session.flush()

    # 2. Core Services (Mandated by Prompt)
    services_data = [
        {
            "title": "Plan Sanctions & Approvals",
            "slug": "plan-sanctions-and-approvals",
            "category": "Municipal Approvals",
            "short_desc": "End-to-end statutory approvals across Greater Bengaluru Authority (GBA), BBMP, BDA, BIAAPA, BMRDA, BMICPA, and STRR.",
            "full_desc": "Full statutory sanction clearance for residential, commercial, industrial, and layout developments. We ensure 100% adherence to the Greater Bengaluru Governance Act 2024-2026, Comprehensive Development Plans (CDP), and online EoDB-OBPS workflows with Sakala guaranteed timeframes.",
            "icon": "building",
            "base_fee": 35000.0,
            "betterment_rate_sqft": 250.0,
            "scrutiny_rate_sqft": 3.5,
            "turnaround_days": "14 to 21 Days (Sakala Guarantee)",
            "is_active": True,
            "display_order": 1,
            "features": [
                "Greater Bengaluru Authority (GBA) & BBMP 8 Zonal Sanctions",
                "BDA Layout Approval & CDP 2031 Land-use verification",
                "BIAAPA & STRR Peripheral Authority Single-Window Approvals",
                "Nambike Nakshe Fast-Track Provisional Sanction for plots <= 50x80 ft",
                "Full liaisoning with Assistant Director of Town Planning (ADTP)"
            ]
        },
        {
            "title": "e-Khata Services & Conversions",
            "slug": "e-khata-services",
            "category": "Property Titling",
            "short_desc": "Digital e-Khata registration, Khata amalgamations, transfers, and smooth B-Khata to A-Khata conversions.",
            "full_desc": "Navigate the Karnataka Urban Development Department's digitized e-Aasthi and e-Khata systems. We rectify Khata discrepancies, assist with Betterment Fee assessments, and transition non-regularized B-Khata assets into fully marketable, bank-mortgageable A-Khata certificates.",
            "icon": "file-text",
            "base_fee": 18000.0,
            "betterment_rate_sqft": 250.0,
            "scrutiny_rate_sqft": 0.0,
            "turnaround_days": "10 to 15 Days",
            "is_active": True,
            "display_order": 2,
            "features": [
                "New Digital e-Khata Certificate Extraction (e-Aasthi)",
                "B-Khata to A-Khata Upgradation & Betterment Payment Filing",
                "Khata Transfer post Registration / Inheritance / Gift Deed",
                "Encumbrance Certificate (EC) 30-Year Chain Search & Title Scrutiny"
            ]
        },
        {
            "title": "AutoDCR & PreDCR CAD Drafting",
            "slug": "autodcr-predcr-cad-drafting",
            "category": "CAD Engineering",
            "short_desc": "Mathematically exact architectural drafting conforming to municipal bypass software rules and automated layer scrutiny.",
            "full_desc": "Municipal building approvals now rely entirely on algorithmic scrutiny using AutoDCR / SoftTech software. Our COA architects convert architectural plans into strict algorithmic PreDCR layers, ensuring zero software rejections on setbacks, stairwell fire clearances, parking bays, and FAR.",
            "icon": "compass",
            "base_fee": 22000.0,
            "betterment_rate_sqft": 0.0,
            "scrutiny_rate_sqft": 4.5,
            "turnaround_days": "3 to 5 Days",
            "is_active": True,
            "display_order": 3,
            "features": [
                "100% PreDCR algorithmic compliance with zero-error validation",
                "Standardized layer codes for Floor Area, Setbacks, and Light Ventilation",
                "Rainwater Harvesting (RWH) chamber & Solar Water Heater 3D geometry",
                "Preparation of DXF / DWG ready for government portal ingestion"
            ]
        },
        {
            "title": "Turnkey Construction & Architectural Design",
            "slug": "turnkey-construction-and-design",
            "category": "Architecture & Build",
            "short_desc": "Vastu-compliant architectural planning, certified structural engineering, and end-to-end turnkey construction.",
            "full_desc": "From concept sketch to griha pravesha. We integrate sustainable contemporary architecture with 100% Vastu compliance, seismic structural stability certification, soil-testing reports, and luxury turnkey construction with milestone-based delivery.",
            "icon": "home",
            "base_fee": 50000.0,
            "betterment_rate_sqft": 0.0,
            "scrutiny_rate_sqft": 0.0,
            "turnaround_days": "Project-based Milestones",
            "is_active": True,
            "display_order": 4,
            "features": [
                "Contemporary 3D Elevation Modeling & VR Walkthroughs",
                "Vastu Purusha Mandala Alignment for Residential Plots",
                "Seismic Zone-II Structural Engineering & Soil Capacity Analysis",
                "Turnkey Construction packages (₹1,950 to ₹3,400 per sq ft)"
            ]
        },
        {
            "title": "NOC Procurement & Clearances",
            "slug": "noc-procurement-and-clearances",
            "category": "Regulatory Liaisoning",
            "short_desc": "Managing clearances from BWSSB, BESCOM, Fire Department, and Airport Authority of India (AAI).",
            "full_desc": "Multi-agency coordination to obtain statutory no-objection certificates. We handle water & sewerage design vetting with BWSSB, power load sanctioning with BESCOM, Chief Fire Officer (CFO) clearances for high-rises, and NOCAS height clearances from AAI for plots in flight funnels.",
            "icon": "shield-check",
            "base_fee": 28000.0,
            "betterment_rate_sqft": 0.0,
            "scrutiny_rate_sqft": 0.0,
            "turnaround_days": "15 to 30 Days",
            "is_active": True,
            "display_order": 5,
            "features": [
                "BWSSB Water Supply & Under-Ground Drainage (UGD) Clearance",
                "BESCOM Transformer Feasibility & Load Sanction",
                "Fire & Emergency Services Initial & Final NOC",
                "AAI / HAL Airport Height Clearance via NOCAS Portal"
            ]
        }
    ]

    for item in services_data:
        service = Service(
            title=item["title"],
            slug=item["slug"],
            category=item["category"],
            short_desc=item["short_desc"],
            full_desc=item["full_desc"],
            icon=item["icon"],
            base_fee=item["base_fee"],
            betterment_rate_sqft=item["betterment_rate_sqft"],
            scrutiny_rate_sqft=item["scrutiny_rate_sqft"],
            turnaround_days=item["turnaround_days"],
            is_active=item["is_active"],
            display_order=item["display_order"],
            features_json=json.dumps(item["features"])
        )
        db.session.add(service)

    db.session.flush()

    # 3. Active Client Project (Demo for Client Portal)
    demo_project = Project(
        reference_no="SAKALA-GBA-2026-0894",
        client_id=client_user.id,
        client_name=client_user.name,
        title="G+3 Residential Villa & Dual-Dwelling Unit",
        plot_location="Plot No. 42, Inner Circle, Whitefield, Bengaluru - 560066",
        ward_no="Ward 84 (Mahadevapura Zone)",
        survey_no="Sy. No. 89/3, Pattandur Agrahara Village",
        authority="GBA / BBMP (Mahadevapura)",
        current_stage="AutoDCR Scrutiny",
        nambike_nakshe_eligible=True,
        plot_area_sqft=2400.0,
        builtup_area_sqft=4650.0,
        assigned_architect="Ar. Karthik Somanna, CA/2009/44120",
        completion_percent=60,
        remarks="Architectural drawing validated through PreDCR software with zero setback errors. Uploaded to GBA EoDB-OBPS portal for automated algorithmic clearance."
    )
    db.session.add(demo_project)
    db.session.flush()

    # Project Timelines
    now = datetime.utcnow()
    stages = [
        ("Drafting", "completed", (now - timedelta(days=9)).strftime('%d-%b-%Y'), "Site measurements verified. Base CAD architectural floor plans, sections, and elevations drafted."),
        ("PreDCR Scrutiny", "completed", (now - timedelta(days=5)).strftime('%d-%b-%Y'), "Layer names, color indexing, setback lines, and FAR polyline parameters validated."),
        ("AutoDCR Scrutiny", "in_progress", (now - timedelta(days=1)).strftime('%d-%b-%Y'), "File submitted to Karnataka EoDB-OBPS. Automated algorithmic check running on GBA server."),
        ("Site Inspection", "pending", None, "Assistant Executive Engineer (AEE) site inspection or Nambike Nakshe verified self-declaration confirmation."),
        ("NOC Clearance", "pending", None, "BWSSB and BESCOM provisional connection endorsements."),
        ("Approved", "pending", None, "Final Building Plan Sanction order and LP number generation.")
    ]

    for s_name, s_status, s_date, s_remarks in stages:
        timeline = ProjectTimeline(
            project_id=demo_project.id,
            stage_name=s_name,
            status=s_status,
            date_updated=s_date,
            remarks=s_remarks
        )
        db.session.add(timeline)

    # Project Documents
    demo_docs = [
        {
            "title": "Architectural Working Plan & Sections (PreDCR Validated)",
            "doc_type": "CAD_DWG",
            "filename": "SAKALA-GBA-2026-0894_Architectural_PreDCR.dxf",
            "file_path": "uploads/SAKALA-GBA-2026-0894_Architectural_PreDCR.dxf",
            "file_size": "4.8 MB"
        },
        {
            "title": "Provisional Sanction Certificate (Nambike Nakshe Trust Order)",
            "doc_type": "SANCTION_CERT",
            "filename": "SAKALA-GBA-2026-0894_Provisional_Sanction.pdf",
            "file_path": "uploads/SAKALA-GBA-2026-0894_Provisional_Sanction.pdf",
            "file_size": "1.4 MB"
        },
        {
            "title": "Digitally Signed e-Khata Certificate (Form 3)",
            "doc_type": "E_KHATA",
            "filename": "SAKALA-GBA-2026-0894_eKhata_Certificate.pdf",
            "file_path": "uploads/SAKALA-GBA-2026-0894_eKhata_Certificate.pdf",
            "file_size": "850 KB"
        },
        {
            "title": "BWSSB Water & Sewage Line Feasibility Certificate",
            "doc_type": "NOC",
            "filename": "SAKALA-GBA-2026-0894_BWSSB_Feasibility.pdf",
            "file_path": "uploads/SAKALA-GBA-2026-0894_BWSSB_Feasibility.pdf",
            "file_size": "1.1 MB"
        }
    ]

    for d in demo_docs:
        doc = ProjectDocument(
            project_id=demo_project.id,
            title=d["title"],
            doc_type=d["doc_type"],
            filename=d["filename"],
            file_path=d["file_path"],
            file_size_display=d["file_size"],
            is_downloadable=True
        )
        db.session.add(doc)

    # 4. Realistic Demo Leads in CRM
    demo_leads = [
        {
            "full_name": "Dr. Anirudh Rao",
            "email": "anirudh.rao@apollo.in",
            "phone": "+91 98455 33221",
            "plot_location": "Indiranagar, HAL 2nd Stage",
            "plot_dimensions": "40x60",
            "service_title": "Plan Sanctions & Approvals",
            "message": "Planning to demolish 35-year-old house and construct G+3 residential duplex. Need GBA sanction and HAL airport height clearance.",
            "status": "new",
            "notes": "High priority client. Reached out via website consultation form."
        },
        {
            "full_name": "Meera Venkatesh",
            "email": "meera.v@techcorp.com",
            "phone": "+91 97400 55112",
            "plot_location": "Yelahanka New Town, Sector 4",
            "plot_dimensions": "50x80",
            "service_title": "AutoDCR & PreDCR CAD Drafting",
            "message": "Architect gave Revit model. Need it converted to official BBMP PreDCR CAD layers for fast approval.",
            "status": "contacted",
            "notes": "Spoke on phone; requested DWG files for initial scrutiny check."
        },
        {
            "full_name": "Suresh Babu",
            "email": "suresh.babu@bengaluruent.com",
            "phone": "+91 99808 77665",
            "plot_location": "Sarjapur Road, near Carmelaram",
            "plot_dimensions": "60x100",
            "service_title": "e-Khata Services & Conversions",
            "message": "Have B-Khata property under Gram Panchayat jurisdiction. Looking to convert to A-Khata with betterment charges.",
            "status": "quotation_sent",
            "notes": "Sent fee quote of ₹45,000 + Govt betterment fees. Awaiting bank clearance documents."
        }
    ]

    for l in demo_leads:
        lead = Lead(
            full_name=l["full_name"],
            email=l["email"],
            phone=l["phone"],
            plot_location=l["plot_location"],
            plot_dimensions=l["plot_dimensions"],
            service_title=l["service_title"],
            message=l["message"],
            status=l["status"],
            internal_notes=l["notes"]
        )
        db.session.add(lead)

    # 5. Regulatory & Zoning Articles (Knowledge Hub)
    articles = [
        {
            "title": "Greater Bengaluru Authority (GBA) 2026: Restructuring, Zones & Bylaws",
            "slug": "greater-bengaluru-authority-gba-2026-guide",
            "category": "Municipal Policy",
            "excerpt": "How the GBA Act replaces traditional municipal silos with unified metropolitan town planning across Bengaluru Urban & Rural sectors.",
            "content": "The Greater Bengaluru Governance framework brings BBMP, BDA, BMRDA, and peripheral local planning authorities under a coordinated metropolitan authority. For property owners, this streamlines building plan sanctions into a unified EoDB-OBPS single-window system with standardized setback and FAR calculations across zones.",
            "author": "Ar. Karthik Somanna",
            "read_time": "5 min read"
        },
        {
            "title": "Nambike Nakshe: How to Get Instant Self-Declaration Building Sanctions",
            "slug": "nambike-nakshe-self-declaration-sanction-bengaluru",
            "category": "Sanction Schemes",
            "excerpt": "A step-by-step guide to Karnataka Government's trust-based approval scheme for residential plots up to 50x80 ft.",
            "content": "Under the Nambike Nakshe (Trust Drawing) initiative, residential plots measuring up to 50 ft x 80 ft (4,000 sq.ft) no longer require tedious in-person desk scrutiny. A certified COA architect can verify the setbacks, FAR, and safety provisions, and submit a self-declaration on the municipal portal to obtain an immediate provisional sanction.",
            "author": "Liaisoning Desk",
            "read_time": "4 min read"
        },
        {
            "title": "Understanding AutoDCR & PreDCR: Why Traditional CAD Drawings Get Rejected",
            "slug": "autodcr-predcr-cad-rules-bengaluru",
            "category": "Technical CAD",
            "excerpt": "The mathematical requirements behind municipal CAD vetting: layer mapping, polyline closes, and ventilation shaft rules.",
            "content": "Government sanction portals do not review human-annotated architectural drawings. Instead, SoftTech AutoDCR algorithms parse exact CAD layer names (e.g. RESIDENTIAL_PLOT_BOUNDARY, BUILTUP_FLOOR_1). Even a minor gap in a polyline or an incorrect text height will fail the automated pre-check.",
            "author": "CAD Systems Lead",
            "read_time": "6 min read"
        }
    ]

    for a in articles:
        post = BlogPost(
            title=a["title"],
            slug=a["slug"],
            category=a["category"],
            excerpt=a["excerpt"],
            content=a["content"],
            author=a["author"],
            read_time=a["read_time"],
            is_published=True
        )
        db.session.add(post)

    db.session.commit()
    print("Database successfully seeded with Bengaluru accounts, services, and live Sakala project!")
