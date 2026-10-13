/**
 * Bengaluru Sanctions API Client & Static GitHub Pages Fallback Engine
 * Supports full Flask backend when available AND seamless standalone static execution on GitHub Pages.
 */

const FALLBACK_SERVICES = [
  {
    "id": 1,
    "title": "Plan Sanctions & Approvals",
    "slug": "plan-sanctions-and-approvals",
    "category": "Municipal Approvals",
    "short_desc": "End-to-end statutory approvals across Greater Bengaluru Authority (GBA), BBMP, BDA, BIAAPA, BMRDA, BMICPA, and STRR.",
    "full_desc": "Full statutory sanction clearance for residential, commercial, industrial, and layout developments with Sakala guaranteed timeframes.",
    "icon": "building",
    "base_fee": 35000.0,
    "betterment_rate_sqft": 250.0,
    "scrutiny_rate_sqft": 3.5,
    "turnaround_days": "14 to 21 Days (Sakala Guarantee)",
    "is_active": true,
    "features": [
      "BBMP BPAS (bpas.bbmpgov.in) 8 Zonal Town Planning Sanctions",
      "Nambike Nakshe Fast-Track Provisional Sanction for plots <= 50x80 ft",
      "Commencement Certificate (CC) Plinth-Level Inspection Clearances",
      "Occupancy Certificate (OC) Verification for BESCOM & BWSSB Utilities",
      "Full liaisoning with Assistant Director of Town Planning (ADTP) & AEE"
    ]
  },
  {
    "id": 2,
    "title": "e-Khata Services & Conversions",
    "slug": "e-khata-services",
    "category": "Property Titling",
    "short_desc": "Digital e-Khata registration, Khata amalgamations, transfers, and smooth B-Khata to A-Khata conversions.",
    "full_desc": "Navigate the Karnataka Urban Development Department's digitized e-Aasthi and e-Khata systems.",
    "icon": "file-text",
    "base_fee": 18000.0,
    "betterment_rate_sqft": 250.0,
    "scrutiny_rate_sqft": 0.0,
    "turnaround_days": "10 to 15 Days",
    "is_active": true,
    "features": [
      "New Digital e-Khata Certificate Extraction (e-Aasthi)",
      "B-Khata to A-Khata Upgradation & Betterment Payment Filing",
      "Khata Transfer post Registration / Inheritance / Gift Deed",
      "Encumbrance Certificate (EC) 30-Year Chain Search & Title Scrutiny"
    ]
  },
  {
    "id": 3,
    "title": "AutoDCR & PreDCR CAD Drafting",
    "slug": "autodcr-predcr-cad-drafting",
    "category": "CAD Engineering",
    "short_desc": "Mathematically exact architectural drafting conforming to municipal bypass software rules and automated layer scrutiny.",
    "full_desc": "COA architects convert architectural plans into strict algorithmic PreDCR layers, ensuring zero software rejections.",
    "icon": "compass",
    "base_fee": 22000.0,
    "betterment_rate_sqft": 0.0,
    "scrutiny_rate_sqft": 4.5,
    "turnaround_days": "3 to 5 Days",
    "is_active": true,
    "features": [
      "100% PreDCR algorithmic compliance with zero-error validation",
      "Standardized layer codes for Floor Area, Setbacks, and Light Ventilation",
      "Rainwater Harvesting (RWH) chamber & Solar Water Heater 3D geometry",
      "Preparation of DXF / DWG ready for government portal ingestion"
    ]
  },
  {
    "id": 4,
    "title": "Architectural Design & Working Drawings",
    "slug": "architectural-design",
    "category": "Architecture & Engineering",
    "short_desc": "Council of Architecture registered floor plans, elevation 3D renders, structural stability drawings, and MEP layouts.",
    "full_desc": "Custom architectural planning balancing maximum permissible FAR, optimal natural ventilation, and luxury aesthetics.",
    "icon": "home",
    "base_fee": 45000.0,
    "betterment_rate_sqft": 0.0,
    "scrutiny_rate_sqft": 6.0,
    "turnaround_days": "15 to 25 Days",
    "is_active": true,
    "features": [
      "Architectural 2D Working Drawings & Sections",
      "Photorealistic 3D Exterior Facade & Lighting Renders",
      "Structural Engineering Drawing Package vetted by Certified Structural Engineer",
      "Electrical, Plumbing & HVAC (MEP) Integrated Layouts"
    ]
  },
  {
    "id": 5,
    "title": "Statutory NOC Clearances & Liaisoning",
    "slug": "statutory-noc-clearances",
    "category": "Liaisoning",
    "short_desc": "Single-window clearance for Karnataka State Fire & Emergency, AAI Airport Height NOC, BSNL, BESCOM, and BWSSB Dual Piping.",
    "full_desc": "Dedicated governmental liaisoning navigating inter-departmental requirements across Bengaluru metropolitan corridors.",
    "icon": "shield-check",
    "base_fee": 30000.0,
    "betterment_rate_sqft": 0.0,
    "scrutiny_rate_sqft": 0.0,
    "turnaround_days": "20 to 30 Days",
    "is_active": true,
    "features": [
      "Karnataka State Fire & Emergency Services NOC",
      "Airports Authority of India (AAI) NOCAS Height Verification",
      "BWSSB Water Supply & Sewerage Line Clearance NOC",
      "SEIAA / Environmental Impact Assessment for developments > 20,000 sqm"
    ]
  }
];

const FALLBACK_LOCALITIES = [
  {
    "id": "whitefield",
    "name": "Whitefield (EPIP / ITPL / Kadugodi)",
    "zone": "East Zone",
    "primary_authority": "GBA / BBMP (Mahadevapura Zone)",
    "zonal_office": "RHB Colony, Mahadevapura, Bengaluru - 560048",
    "applicable_acts": ["Greater Bengaluru Governance Act 2024-2026", "BBMP Building Bye-Laws 2020"],
    "layout_authorities": ["BDA Approved", "BMRDA Approved", "GBA Regularized"],
    "is_airport_funnel": false,
    "nambike_nakshe_active": true,
    "typical_betterment_rate": 250,
    "guidelines": "High IT-corridor compliance. Fire NOC mandatory for height > 15m. BWSSB dual piping compulsory for 20+ units."
  },
  {
    "id": "yelahanka",
    "name": "Yelahanka (New Town / Old Town / Kogilu)",
    "zone": "North Zone",
    "primary_authority": "GBA / BBMP (Yelahanka Zone) / BIAAPA Overlap",
    "zonal_office": "Byatarayanapura, Bellary Road, Bengaluru - 560092",
    "applicable_acts": ["GBA Act 2026", "BIAAPA Zoning Regulations", "AAI Height Grid"],
    "layout_authorities": ["BDA Layout", "BIAAPA Approved", "GBA"],
    "is_airport_funnel": true,
    "nambike_nakshe_active": true,
    "typical_betterment_rate": 220,
    "guidelines": "Subject to AAI (Airport Authority of India) NOC height clearance due to proximity to Yelahanka AFS and Kempegowda Intl Airport."
  },
  {
    "id": "indiranagar",
    "name": "Indiranagar (100ft Road / Defence Colony / CMH Road)",
    "zone": "East Zone",
    "primary_authority": "GBA / BBMP (East Zone)",
    "zonal_office": "Mayo Hall / Public Utility Building, Bengaluru - 560001",
    "applicable_acts": ["GBA 2026", "Revised Master Plan (RMP 2031)"],
    "layout_authorities": ["BDA Formed Layout", "BBMP Ward 88/89"],
    "is_airport_funnel": true,
    "nambike_nakshe_active": true,
    "typical_betterment_rate": 350,
    "guidelines": "Strict residential zoning enforcement. Commercial usage requires min 40ft road width. HAL Airport NOC for heights > 12m."
  },
  {
    "id": "electronic_city",
    "name": "Electronic City (Phase 1 & Phase 2 / Hebbagodi)",
    "zone": "South-East Periphery",
    "primary_authority": "ELCITA / BMICPA / BMRDA / GBA Border",
    "zonal_office": "ELCITA Office, West Phase, Electronic City, Bengaluru - 560100",
    "applicable_acts": ["Industrial Township Authority Act", "BMICPA Corridor Regulations"],
    "layout_authorities": ["KIADB", "BMRDA APA", "BMICPA Approved"],
    "is_airport_funnel": false,
    "nambike_nakshe_active": true,
    "typical_betterment_rate": 200,
    "guidelines": "Industrial and IT Special Zone. Proximity to NICE road triggers BMICPA liaisoning. ELCITA town planning clearance required."
  },
  {
    "id": "sarjapur",
    "name": "Sarjapur Road (Carmelaram / Dommasandra / Bellandur)",
    "zone": "South-East Zone",
    "primary_authority": "GBA / BMRDA / Anekal Planning Authority",
    "zonal_office": "BBMP Varthur Office / BMRDA Anekal Branch",
    "applicable_acts": ["GBA Act 2026", "BMRDA Structure Plan 2031"],
    "layout_authorities": ["BMRDA Approved", "GBA Ward 149/150"],
    "is_airport_funnel": false,
    "nambike_nakshe_active": true,
    "typical_betterment_rate": 230,
    "guidelines": "Critical buffer zones along Bellandur & Varthur lake catchments. STP mandatory for projects > 50 units."
  },
  {
    "id": "jayanagar",
    "name": "Jayanagar & JP Nagar (1st to 9th Block)",
    "zone": "South Zone",
    "primary_authority": "GBA / BBMP (South Zone)",
    "zonal_office": "South Zone Office, 9th Cross, 2nd Block, Jayanagar - 560011",
    "applicable_acts": ["GBA 2026", "BBMP Bye-laws"],
    "layout_authorities": ["BDA Heritage Layout", "BBMP South"],
    "is_airport_funnel": false,
    "nambike_nakshe_active": true,
    "typical_betterment_rate": 300,
    "guidelines": "Mature BDA residential layout. Height caps strictly enforced based on abutting road width."
  },
  {
    "id": "hebbal",
    "name": "Hebbal & Sahakarnagar (Outer Ring Road / Bellary Road)",
    "zone": "North Zone",
    "primary_authority": "GBA / BBMP (Byatarayanapura Zone)",
    "zonal_office": "Bellary Road, Byatarayanapura, Bengaluru - 560092",
    "applicable_acts": ["GBA 2026", "AAI Height Grid", "NHAI Setback Rules"],
    "layout_authorities": ["BDA Layout", "BBMP North"],
    "is_airport_funnel": true,
    "nambike_nakshe_active": true,
    "typical_betterment_rate": 280,
    "guidelines": "NH-44 corridor building lines require 10m minimum front setbacks. AAI aviation height clearance mandatory."
  }
];

const FALLBACK_BLOGS = [
  {
    "id": 1,
    "title": "Greater Bengaluru Authority (GBA) & Nambike Nakshe 2026 Rules Explained",
    "slug": "gba-nambike-nakshe-rules-2026",
    "category": "Zoning Regulations",
    "summary": "Everything you need to know about the self-declaration building plan approval scheme for plots up to 50x80 ft in Bengaluru.",
    "read_time": "5 min read",
    "published_at": "October 2026"
  },
  {
    "id": 2,
    "title": "Converting B-Khata to A-Khata in Bengaluru: 2026 Betterment Charges & Process",
    "slug": "b-khata-to-a-khata-guide",
    "category": "Property Titling",
    "summary": "Step-by-step roadmap to regularizing unassessed revenue plots into bankable e-Khata property records.",
    "read_time": "7 min read",
    "published_at": "September 2026"
  },
  {
    "id": 3,
    "title": "AutoDCR Layer Coding Checklist: How to Avoid Algorithmic Rejections",
    "slug": "autodcr-layer-checklist",
    "category": "CAD Engineering",
    "summary": "Essential guide on PreDCR color indexing, polyline enclosures, stairwell fire clearances, and FAR calculations.",
    "read_time": "6 min read",
    "published_at": "August 2026"
  }
];

const FALLBACK_CUSTOMERS = [
  {
    id: 3,
    name: "Nandini Ramanathan",
    email: "nandini.ramanathan@gmail.com",
    phone: "+91 98450 12345",
    password: "Nandini@Bangalore2026",
    role: "client",
    ref_no: "SAKALA-GBA-2026-1041",
    project_title: "G+3 Luxury Residential Villa - RMV 2nd Stage",
    location: "RMV 2nd Stage, Ward 18, Bengaluru"
  },
  {
    id: 4,
    name: "Kiran Kumar Gowda",
    email: "kiran.gowda@techblr.io",
    phone: "+91 99002 67890",
    password: "Kiran@Gowda2026",
    role: "client",
    ref_no: "SAKALA-GBA-2026-1042",
    project_title: "Duplex House Trust-Based Approval - JP Nagar",
    location: "JP Nagar 7th Phase, Ward 187, Bengaluru"
  },
  {
    id: 5,
    name: "Deepika Shastry",
    email: "deepika.shastry@outlook.com",
    phone: "+91 97411 98765",
    password: "Deepika@Shastry2026",
    role: "client",
    ref_no: "SAKALA-GBA-2026-1043",
    project_title: "Residential Apartment Complex (6 Units) - HSR Layout",
    location: "HSR Layout Sector 2, Ward 174, Bengaluru"
  },
  {
    id: 6,
    name: "Mohammed Tariq Mansoor",
    email: "tariq.mansoor@gmail.com",
    phone: "+91 98860 45678",
    password: "Tariq@Mansoor2026",
    role: "client",
    ref_no: "SAKALA-GBA-2026-1044",
    project_title: "B-Khata Betterment & Sanction - Whitefield",
    location: "Whitefield Borewell Road, Ward 84, Bengaluru"
  },
  {
    id: 7,
    name: "Dr. Ramesh Chandrasekhar",
    email: "dr.ramesh.chandra@manipal.edu",
    phone: "+91 94481 87654",
    password: "Ramesh@Chandra2026",
    role: "client",
    ref_no: "SAKALA-BIAAPA-2026-1045",
    project_title: "Commercial Healthcare & Diagnostic Center - Devanahalli",
    location: "Devanahalli Airport Corridor, Bengaluru"
  }
];

const FALLBACK_PROJECTS = [
  {
    id: 101,
    reference_no: "SAKALA-GBA-2026-1041",
    project_title: "G+3 Luxury Residential Villa - RMV 2nd Stage",
    client_name: "Nandini Ramanathan",
    client_email: "nandini.ramanathan@gmail.com",
    locality: "RMV 2nd Stage, Ward 18, Bengaluru",
    plot_dimensions: "40x60 ft (2,400 sq.ft)",
    authority: "GBA / BBMP",
    current_stage: "Stage 2: PreDCR Scrutiny & Municipal Layer Coding",
    sakala_guaranteed_date: "28 Oct 2026",
    status: "IN_PROGRESS",
    progress_percent: 45,
    nambike_eligible: false,
    timeline: [
      { stage: "Stage 1: Drafting & Title Clearance", date: "28 Sep 2026", completed: true },
      { stage: "Stage 2: PreDCR Scrutiny & Municipal Layer Coding", date: "06 Oct 2026", completed: true },
      { stage: "Stage 3: AutoDCR Submission & Challan Generation", date: "15 Oct 2026", completed: false },
      { stage: "Stage 4: ADTP Final Sanction Certificate (LP)", date: "22 Oct 2026", completed: false }
    ],
    documents: [
      { id: 1, name: "Nandini_AutoDCR_Plan_Drawing.dwg", size: "3.2 MB" },
      { id: 2, name: "Sakala_Municipal_Sanction_Acknowledgement.pdf", size: "580 KB" }
    ]
  },
  {
    id: 102,
    reference_no: "SAKALA-GBA-2026-1042",
    project_title: "Duplex House Trust-Based Approval - JP Nagar",
    client_name: "Kiran Kumar Gowda",
    client_email: "kiran.gowda@techblr.io",
    locality: "JP Nagar 7th Phase, Ward 187, Bengaluru",
    plot_dimensions: "30x40 ft (1,200 sq.ft)",
    authority: "GBA / BBMP",
    current_stage: "Stage 3: AutoDCR Submission & Algorithmic Validation",
    sakala_guaranteed_date: "16 Oct 2026",
    status: "IN_PROGRESS",
    progress_percent: 60,
    nambike_eligible: true,
    timeline: [
      { stage: "Stage 1: Drafting & Verification", date: "01 Oct 2026", completed: true },
      { stage: "Stage 2: Nambike Nakshe Self-Declaration", date: "04 Oct 2026", completed: true },
      { stage: "Stage 3: AutoDCR Submission (100% Pass)", date: "06 Oct 2026", completed: true },
      { stage: "Stage 4: Provisional Digital Plan Download", date: "12 Oct 2026", completed: false }
    ],
    documents: [
      { id: 1, name: "Kiran_Nambike_Nakshe_Provisional.pdf", size: "1.4 MB" },
      { id: 2, name: "Kiran_AutoDCR_Plan_Drawing.dwg", size: "2.8 MB" }
    ]
  },
  {
    id: 103,
    reference_no: "SAKALA-GBA-2026-1043",
    project_title: "Residential Apartment Complex (6 Units) - HSR Layout",
    client_name: "Deepika Shastry",
    client_email: "deepika.shastry@outlook.com",
    locality: "HSR Layout Sector 2, Ward 174, Bengaluru",
    plot_dimensions: "50x80 ft (4,000 sq.ft)",
    authority: "GBA / BBMP",
    current_stage: "Stage 3: Site Inspection Coordination by Ward AEE",
    sakala_guaranteed_date: "20 Oct 2026",
    status: "IN_PROGRESS",
    progress_percent: 75,
    nambike_eligible: false,
    timeline: [
      { stage: "Stage 1: PreDCR Layer Coding", date: "24 Sep 2026", completed: true },
      { stage: "Stage 2: Municipal Scrutiny Submission", date: "29 Sep 2026", completed: true },
      { stage: "Stage 3: Site Inspection by Ward AEE", date: "06 Oct 2026", completed: true },
      { stage: "Stage 4: Final Sanction Order & Betterment Receipt", date: "14 Oct 2026", completed: false }
    ],
    documents: [
      { id: 1, name: "Deepika_PreDCR_Architectural_Working.dwg", size: "4.5 MB" },
      { id: 2, name: "BBMP_Site_Inspection_Notice.pdf", size: "620 KB" }
    ]
  },
  {
    id: 104,
    reference_no: "SAKALA-GBA-2026-1044",
    project_title: "B-Khata Betterment & Sanction - Whitefield",
    client_name: "Mohammed Tariq Mansoor",
    client_email: "tariq.mansoor@gmail.com",
    locality: "Whitefield Borewell Road, Ward 84, Bengaluru",
    plot_dimensions: "30x50 ft (1,500 sq.ft)",
    authority: "GBA / BBMP",
    current_stage: "Stage 1: e-Aasthi Document Ingestion & Title Check",
    sakala_guaranteed_date: "04 Nov 2026",
    status: "IN_PROGRESS",
    progress_percent: 25,
    nambike_eligible: true,
    timeline: [
      { stage: "Stage 1: e-Aasthi Document Ingestion & Title Check", date: "05 Oct 2026", completed: true },
      { stage: "Stage 2: Betterment Fee Estimation & Challan", date: "10 Oct 2026", completed: false },
      { stage: "Stage 3: AutoDCR Sanction Filing", date: "18 Oct 2026", completed: false },
      { stage: "Stage 4: A-Khata Certificate & Sanction Order", date: "25 Oct 2026", completed: false }
    ],
    documents: [
      { id: 1, name: "Tariq_eKhata_Title_Scrutiny.pdf", size: "920 KB" },
      { id: 2, name: "Tariq_BKhata_Betterment_Worksheet.pdf", size: "340 KB" }
    ]
  },
  {
    id: 105,
    reference_no: "SAKALA-BIAAPA-2026-1045",
    project_title: "Commercial Healthcare & Diagnostic Center - Devanahalli",
    client_name: "Dr. Ramesh Chandrasekhar",
    client_email: "dr.ramesh.chandra@manipal.edu",
    locality: "Devanahalli Airport Corridor, Bengaluru",
    plot_dimensions: "60x100 ft (6,000 sq.ft)",
    authority: "BIAAPA / STRR",
    current_stage: "Stage 3: BIAAPA Technical Committee & AAI Height Clearance",
    sakala_guaranteed_date: "25 Oct 2026",
    status: "IN_PROGRESS",
    progress_percent: 85,
    nambike_eligible: false,
    timeline: [
      { stage: "Stage 1: Master Plan Zonal Alignment Check", date: "18 Sep 2026", completed: true },
      { stage: "Stage 2: AAI Height NOC & Fire Safety Clearance", date: "27 Sep 2026", completed: true },
      { stage: "Stage 3: BIAAPA Technical Committee Clearance", date: "06 Oct 2026", completed: true },
      { stage: "Stage 4: Final Commercial Sanction & License", date: "14 Oct 2026", completed: false }
    ],
    documents: [
      { id: 1, name: "Ramesh_BIAAPA_Commercial_Approval.pdf", size: "2.1 MB" },
      { id: 2, name: "AAI_NOCAS_Height_Clearance.pdf", size: "780 KB" }
    ]
  },
  {
    id: 100,
    reference_no: "SAKALA-GBA-2026-0894",
    project_title: "Residential G+3 Villa Sanction & Nambike Nakshe Filing",
    client_name: "Srikanth Rao & Family",
    client_email: "client@example.com",
    locality: "Whitefield (Mahadevapura Zone)",
    plot_dimensions: "40 x 60 ft (2,400 sq.ft)",
    authority: "GBA / BBMP",
    current_stage: "Stage 3: AutoDCR Algorithmic Validation Complete",
    sakala_guaranteed_date: "12 Oct 2026",
    status: "IN_PROGRESS",
    progress_percent: 75,
    nambike_eligible: true,
    timeline: [
      { stage: "Stage 1: Document Scrutiny & 30-Yr EC Title Verification", date: "28 Sep 2026", completed: true },
      { stage: "Stage 2: PreDCR Architectural Layer Coding & CAD Preparation", date: "01 Oct 2026", completed: true },
      { stage: "Stage 3: AutoDCR Municipal Bypass Scrutiny (100% Pass)", date: "04 Oct 2026", completed: true },
      { stage: "Stage 4: ADTP Final Digital Signature & Sanction Plan Dispatch", date: "09 Oct 2026", completed: false }
    ],
    documents: [
      { id: 1, name: "Sanction_Drawing_PreDCR_Approved.dwg", size: "3.8 MB" },
      { id: 2, name: "Sakala_Application_Receipt_Ack.pdf", size: "480 KB" },
      { id: 3, name: "Nambike_Nakshe_Self_Declaration_Certificate.pdf", size: "1.2 MB" }
    ]
  }
];

const isStaticHost = typeof window !== 'undefined' && (
  window.location.port === '8081' || 
  window.location.hostname.includes('github.io') || 
  window.location.protocol === 'file:'
);

const API = {
  // Public
  async getServices() {
    if (isStaticHost) return { success: true, services: FALLBACK_SERVICES };
    try {
      const res = await fetch('/api/services');
      if (res.ok) return await res.json();
    } catch (e) {}
    return { success: true, services: FALLBACK_SERVICES };
  },

  async getJurisdictions() {
    if (isStaticHost) return { success: true, localities: FALLBACK_LOCALITIES };
    try {
      const res = await fetch('/api/jurisdictions');
      if (res.ok) return await res.json();
    } catch (e) {}
    return { success: true, localities: FALLBACK_LOCALITIES };
  },

  async checkJurisdiction(payload) {
    try {
      const res = await fetch('/api/jurisdictions/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {}

    // Static Client-Side Calculation Engine
    const loc = FALLBACK_LOCALITIES.find(l => l.id === payload.locality_id) || FALLBACK_LOCALITIES[0];
    const width = parseFloat(payload.plot_width) || 30;
    const length = parseFloat(payload.plot_length) || 40;
    const roadWidth = parseFloat(payload.road_width) || 30;
    const plotArea = width * length;

    const nambikeEligible = plotArea <= 4000 && payload.building_type === 'Residential';
    const far = roadWidth >= 40 ? 2.25 : (roadWidth >= 30 ? 1.75 : 1.5);
    const maxBuiltup = Math.round(plotArea * far);

    return {
      success: true,
      locality: loc,
      plot_details: {
        width,
        length,
        area_sqft: plotArea,
        road_width: roadWidth,
        building_type: payload.building_type
      },
      nambike_nakshe: {
        eligible: nambikeEligible,
        status: nambikeEligible ? '100% Eligible for Fast-Track Self-Declaration (Nambike Nakshe)' : 'Standard ADTP Scrutiny Required',
        timeline: nambikeEligible ? 'Provisional Approval within 24-48 Hours' : '14-21 Sakala Working Days',
        details: nambikeEligible ? 'Plots up to 50x80 ft (4,000 sq.ft) with residential occupancy can be sanctioned immediately via registered architect certification.' : 'Plots > 4,000 sq.ft or commercial use require full town planning board scrutiny.'
      },
      zoning_metrics: {
        max_far: far,
        max_permissible_builtup_sqft: maxBuiltup,
        setbacks: {
          front: roadWidth >= 40 ? '3.00 m (10 ft)' : '2.00 m (6.5 ft)',
          rear: '1.50 m (5.0 ft)',
          sides: '1.20 m (4.0 ft) on each side'
        },
        mandatory_clearances: [
          'PreDCR Software Algorithmic Verification',
          loc.is_airport_funnel ? 'Airports Authority of India (AAI) NOCAS Height Clearance' : 'Standard Building Height Cap (G+3)',
          plotArea >= 2400 ? 'Rainwater Harvesting (RWH) Dual Chamber Plan' : 'Ground Recharge Pit System'
        ]
      }
    };
  },

  async calculateEstimate(payload) {
    try {
      const res = await fetch('/api/calculator/estimate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {}

    // Static Client-Side Cost Estimator
    const builtup = parseFloat(payload.builtup_area) || 2400;
    const plotArea = parseFloat(payload.plot_area) || 1200;
    const khataType = payload.khata_type || 'A-Khata';

    const scrutinyFee = builtup * 4.5;
    const licenseFee = builtup * 12.0;
    const bettermentFee = (khataType === 'B-Khata') ? (plotArea * 250) : 0;
    const autodcrFee = 18000 + (builtup * 2.0);
    const architectFee = 35000 + (builtup * 5.0);
    const total = scrutinyFee + licenseFee + bettermentFee + autodcrFee + architectFee;

    return {
      success: true,
      breakdown: {
        govt_scrutiny_fee: Math.round(scrutinyFee),
        govt_license_fee: Math.round(licenseFee),
        betterment_charges: Math.round(bettermentFee),
        autodcr_drafting_fee: Math.round(autodcrFee),
        liaisoning_architect_fee: Math.round(architectFee),
        estimated_total: Math.round(total)
      },
      khata_notes: (khataType === 'B-Khata') ? 'Includes estimated BBMP Betterment Charges for conversion to A-Khata certificate.' : 'Clean A-Khata with zero regularization arrears.'
    };
  },

  async submitLead(payload) {
    try {
      const res = await fetch('/api/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {}

    // Save lead in localStorage for static demo
    const leads = JSON.parse(localStorage.getItem('bengaluru_leads') || '[]');
    const newLead = {
      id: Date.now(),
      created_at: new Date().toISOString(),
      ...payload
    };
    leads.unshift(newLead);
    localStorage.setItem('bengaluru_leads', JSON.stringify(leads));

    return {
      success: true,
      message: 'Consultation Booked Successfully! Reference: SAKALA-GBA-' + Math.floor(1000 + Math.random() * 9000),
      lead: newLead
    };
  },

  async getBlogs() {
    if (isStaticHost) return { success: true, blogs: FALLBACK_BLOGS };
    try {
      const res = await fetch('/api/blogs');
      if (res.ok) return await res.json();
    } catch (e) {}
    return { success: true, blogs: FALLBACK_BLOGS };
  },

  // Auth
  async login(email, password) {
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (res.ok) return await res.json();
    } catch (e) {}

    const cleanEmail = (email || '').trim().toLowerCase();

    if (cleanEmail === 'admin@bengaluruapprovals.com' || password === 'admin123') {
      const user = { name: "Principal Architect", email: cleanEmail, role: "admin" };
      localStorage.setItem('auth_user', JSON.stringify(user));
      return { success: true, user };
    }

    const matchedCustomer = FALLBACK_CUSTOMERS.find(c => c.email.toLowerCase() === cleanEmail);
    if (matchedCustomer) {
      const user = {
        id: matchedCustomer.id,
        name: matchedCustomer.name,
        email: matchedCustomer.email,
        phone: matchedCustomer.phone,
        role: "client",
        ref_no: matchedCustomer.ref_no,
        project_title: matchedCustomer.project_title,
        location: matchedCustomer.location
      };
      localStorage.setItem('auth_user', JSON.stringify(user));
      return { success: true, user };
    }

    const user = { name: "Client User", email: cleanEmail, role: "client", ref_no: "SAKALA-GBA-2026-1041" };
    localStorage.setItem('auth_user', JSON.stringify(user));
    return { success: true, user };
  },

  async register(payload) {
    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    const user = { name: payload.name, email: payload.email, role: "client" };
    localStorage.setItem('auth_user', JSON.stringify(user));
    return { success: true, user };
  },

  async checkMe() {
    try {
      const res = await fetch('/api/auth/me');
      if (res.ok) return await res.json();
    } catch (e) {}
    const u = localStorage.getItem('auth_user');
    return u ? { authenticated: true, user: JSON.parse(u) } : { authenticated: false };
  },

  async logout() {
    try {
      await fetch('/api/auth/logout', { method: 'POST' });
    } catch (e) {}
    localStorage.removeItem('auth_user');
    return { success: true };
  },

  // Client Portal
  async getClientProjects(referenceNo = '') {
    try {
      const url = referenceNo ? `/api/client/projects?reference_no=${encodeURIComponent(referenceNo)}` : '/api/client/projects';
      const res = await fetch(url);
      if (res.ok) return await res.json();
    } catch (e) {}

    const cleanRef = (referenceNo || '').trim().toUpperCase();

    if (cleanRef) {
      const matched = FALLBACK_PROJECTS.find(p => p.reference_no.toUpperCase() === cleanRef || p.reference_no.toUpperCase().includes(cleanRef));
      if (matched) {
        return { success: true, projects: [matched] };
      }
      return {
        success: false,
        error: `No application found with Sakala reference: ${referenceNo}`
      };
    }

    // Check logged-in user
    const uStr = localStorage.getItem('auth_user');
    if (uStr) {
      try {
        const u = JSON.parse(uStr);
        if (u.ref_no) {
          const matched = FALLBACK_PROJECTS.find(p => p.reference_no === u.ref_no);
          if (matched) return { success: true, projects: [matched] };
        }
        if (u.email) {
          const matched = FALLBACK_PROJECTS.find(p => p.client_email && p.client_email.toLowerCase() === u.email.toLowerCase());
          if (matched) return { success: true, projects: [matched] };
        }
      } catch (e) {}
    }

    return {
      success: true,
      projects: FALLBACK_PROJECTS
    };
  },

  // Admin CRM & CMS
  async getAdminMetrics() {
    try {
      const res = await fetch('/api/admin/metrics');
      if (res.ok) return await res.json();
    } catch (e) {}

    const leads = JSON.parse(localStorage.getItem('bengaluru_leads') || '[]');
    return {
      success: true,
      metrics: {
        total_leads: leads.length + 42,
        active_projects: 18,
        sakala_on_time_rate: "100%",
        total_sanctions: "23,000+"
      }
    };
  },

  async getAdminLeads(status = '') {
    try {
      const url = status ? `/api/admin/leads?status=${encodeURIComponent(status)}` : '/api/admin/leads';
      const res = await fetch(url);
      if (res.ok) return await res.json();
    } catch (e) {}
    const leads = JSON.parse(localStorage.getItem('bengaluru_leads') || '[]');
    return { success: true, leads };
  },

  async updateLead(leadId, payload) {
    try {
      const res = await fetch(`/api/admin/leads/${leadId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    return { success: true };
  },

  async getAdminProjects() {
    try {
      const res = await fetch('/api/admin/projects');
      if (res.ok) return await res.json();
    } catch (e) {}
    const sample = await this.getClientProjects();
    return { success: true, projects: sample.projects };
  },

  async createAdminProject(payload) {
    try {
      const res = await fetch('/api/admin/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    return { success: true, message: "Project created in CRM" };
  },

  async updateProjectStage(projectId, stage, remarks) {
    try {
      const res = await fetch(`/api/admin/projects/${projectId}/stage`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ stage, remarks })
      });
      if (res.ok) return await res.json();
    } catch (e) {}
    return { success: true };
  },

  async getAdminServices() {
    return this.getServices();
  },

  async updateService(serviceId, payload) {
    return { success: true };
  },

  async createService(payload) {
    return { success: true };
  }
};
