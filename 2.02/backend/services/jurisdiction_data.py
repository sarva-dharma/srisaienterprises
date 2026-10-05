"""
Bengaluru Municipal Planning Authorities & Zoning Jurisdiction Engine (2026)
Compliant with Greater Bengaluru Authority (GBA), BBMP, BDA, BIAAPA, BMICPA, BMRDA, and STRR regulations.
Includes Nambike Nakshe trust-based self-declaration rules.
"""

BENGALURU_JURISDICTION_REGISTRY = [
    {
        "id": "whitefield",
        "name": "Whitefield (EPIP / ITPL / Kadugodi)",
        "zone": "East Zone",
        "primary_authority": "GBA / BBMP (Mahadevapura Zone)",
        "zonal_office": "RHB Colony, Mahadevapura, Bengaluru - 560048",
        "applicable_acts": ["Greater Bengaluru Governance Act 2024-2026", "BBMP Building Bye-Laws 2020", "KUDP Act"],
        "layout_authorities": ["BDA Approved", "BMRDA Approved", "GBA Regularized"],
        "is_airport_funnel": False,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 250, # INR per sq.ft for B-Khata or Unassessed
        "guidelines": "High IT-corridor compliance. Fire NOC mandatory for height > 15m. BWSSB dual piping compulsory for 20+ units."
    },
    {
        "id": "yelahanka",
        "name": "Yelahanka (New Town / Old Town / Kogilu)",
        "zone": "North Zone",
        "primary_authority": "GBA / BBMP (Yelahanka Zone) / BIAAPA Overlap",
        "zonal_office": "Byatarayanapura, Bellary Road, Bengaluru - 560092",
        "applicable_acts": ["GBA Act 2026", "BIAAPA Zoning Regulations", "AAI Height Restriction Grid"],
        "layout_authorities": ["BDA Layout", "BIAAPA Approved", "GBA"],
        "is_airport_funnel": True,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 220,
        "guidelines": "Subject to AAI (Airport Authority of India) NOC height clearance due to proximity to Yelahanka AFS and Kempegowda Intl Airport."
    },
    {
        "id": "indiranagar",
        "name": "Indiranagar (100ft Road / CMH Road / Defence Colony)",
        "zone": "East Zone",
        "primary_authority": "GBA / BBMP (East Zone)",
        "zonal_office": "Mayo Hall / Public Utility Building, Bengaluru - 560001",
        "applicable_acts": ["GBA 2026", "Revised Master Plan (RMP 2031 / 2015)"],
        "layout_authorities": ["BDA Formed Layout", "BBMP Ward 88/89"],
        "is_airport_funnel": True,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 350,
        "guidelines": "Strict residential zoning enforcement. Commercial usage requires min 40ft road width. HAL Airport NOC applicable for heights > 12m."
    },
    {
        "id": "electronic_city",
        "name": "Electronic City (Phase 1 & Phase 2 / Hebbagodi)",
        "zone": "South-East Periphery",
        "primary_authority": "ELCITA / BMICPA / BMRDA / GBA Border",
        "zonal_office": "ELCITA Office, West Phase, Electronic City, Bengaluru - 560100",
        "applicable_acts": ["Industrial Township Authority Act", "BMICPA Corridor Regulations", "BMRDA Master Plan"],
        "layout_authorities": ["KIADB", "BMRDA APA", "BMICPA Approved"],
        "is_airport_funnel": False,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 200,
        "guidelines": "Industrial and IT Special Zone. Proximity to NICE road triggers BMICPA liaisoning. ELCITA town planning clearance required."
    },
    {
        "id": "devanahalli",
        "name": "Devanahalli (Aerotropolis / Hardware Park / KIADB)",
        "zone": "North Peripheral Corridor",
        "primary_authority": "BIAAPA (Bangalore International Airport Area Planning Authority)",
        "zonal_office": "BIAAPA Office, BMTC Complex, Shanthinagar, Bengaluru",
        "applicable_acts": ["BIAAPA Master Plan 2031", "KTCP Act 1961"],
        "layout_authorities": ["BIAAPA Approved", "KIADB Industrial Allotment"],
        "is_airport_funnel": True,
        "nambike_nakshe_active": False, # BIAAPA has dedicated single-window OBPS portal
        "typical_betterment_rate": 180,
        "guidelines": "Strict Aerodrome Obstacle Limitation Surfaces (OLS) scrutiny. Every application requires automated AAI NOC integration."
    },
    {
        "id": "sarjapur_road",
        "name": "Sarjapur Road (Carmelaram / Dommasandra / Sompura)",
        "zone": "South-East Corridor",
        "primary_authority": "GBA / BBMP (Mahadevapura) & BMRDA Overlap",
        "zonal_office": "Bellandur Ward Office / Anekal Planning Authority",
        "applicable_acts": ["GBA Act 2026", "BMRDA Structure Plan"],
        "layout_authorities": ["BDA Approved", "BMRDA APA", "GBA Wards 149/150"],
        "is_airport_funnel": False,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 230,
        "guidelines": "RWH (Rainwater Harvesting) and KSPCB consent required for plots exceeding 4,000 sq ft built-up near lake buffer zones (75m lake buffer / 30m rajakevalu buffer rules apply strictly)."
    },
    {
        "id": "hsr_layout",
        "name": "HSR Layout (Sectors 1 to 7)",
        "zone": "South Zone",
        "primary_authority": "GBA / BBMP (Bommanahalli Zone)",
        "zonal_office": "Begur Main Road, Bommanahalli, Bengaluru - 560068",
        "applicable_acts": ["GBA Act 2026", "BBMP Bye-laws 2020"],
        "layout_authorities": ["BDA Formed Scheme Layout"],
        "is_airport_funnel": False,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 300,
        "guidelines": "100% BDA surveyed plots. Fast-track Nambike Nakshe eligible for 30x40, 40x60, and 50x80 residential plots with zero desk inspection."
    },
    {
        "id": "koramangala",
        "name": "Koramangala (Blocks 1 to 8 / ST Bed)",
        "zone": "South-East Zone",
        "primary_authority": "GBA / BBMP (South Zone)",
        "zonal_office": "9th Main, Jayanagar 2nd Block, Bengaluru - 560011",
        "applicable_acts": ["GBA Act 2026", "RMP 2015/2031"],
        "layout_authorities": ["BDA Formed Layout"],
        "is_airport_funnel": True,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 350,
        "guidelines": "High-density residential. Stormwater drain (Rajakaluve) buffer compliance must be validated using revenue village maps."
    },
    {
        "id": "nelamangala",
        "name": "Nelamangala (Tumkur Road / STRR Junction)",
        "zone": "North-West Peripheral",
        "primary_authority": "STRR Planning Authority / Nelamangala Local Planning Authority (BMRDA)",
        "zonal_office": "NLPA Complex, Subhash Nagar, Nelamangala - 562123",
        "applicable_acts": ["STRR Master Plan 2031", "KTCP Act 1961"],
        "layout_authorities": ["BMRDA Approved", "STRR Zonal Regulations"],
        "is_airport_funnel": False,
        "nambike_nakshe_active": False,
        "typical_betterment_rate": 150,
        "guidelines": "Logistics and warehousing hub. Road widening reservations and NHAI corridor setbacks must be factored into CAD drafting."
    },
    {
        "id": "kengeri_rr_nagar",
        "name": "Kengeri & Rajarajeshwari Nagar (Mysore Road)",
        "zone": "West Zone",
        "primary_authority": "GBA / BBMP (RR Nagar Zone)",
        "zonal_office": "Ideal Homes Township, RR Nagar, Bengaluru - 560098",
        "applicable_acts": ["GBA Act 2026", "BBMP Bye-laws 2020"],
        "layout_authorities": ["BDA Layout", "BMRDA Magadi Authority"],
        "is_airport_funnel": False,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 200,
        "guidelines": "Rapid metro influence corridor. Plots abutting Metro line enjoy higher Transit-Oriented Development (TOD) Premium FAR."
    },
    {
        "id": "hoskote",
        "name": "Hoskote (Old Madras Road / STRR East)",
        "zone": "East Peripheral",
        "primary_authority": "Hoskote Planning Authority (HPA / BMRDA / STRR)",
        "zonal_office": "HPA Complex, College Road, Hoskote - 562114",
        "applicable_acts": ["STRR Master Plan", "KTCP Act 1961"],
        "layout_authorities": ["BMRDA / HPA Approved"],
        "is_airport_funnel": False,
        "nambike_nakshe_active": False,
        "typical_betterment_rate": 160,
        "guidelines": "Industrial and suburban expansion zone. Conversion from DC conversion to planning approval requires DC endorsement and conversion order."
    },
    {
        "id": "kanakapura_road",
        "name": "Kanakapura Road (Thalaghattapura / Anjanapura / Kaggalipura)",
        "zone": "South Peripheral",
        "primary_authority": "GBA / BDA & BMRDA Kanakapura Planning Authority",
        "zonal_office": "Anjanapura BDA Office / Uttarahalli Hobli Sub-division",
        "applicable_acts": ["GBA Act 2026", "BDA CDP 2031"],
        "layout_authorities": ["BDA Scheme Layout", "BMRDA Approved"],
        "is_airport_funnel": False,
        "nambike_nakshe_active": True,
        "typical_betterment_rate": 220,
        "guidelines": "Green belt transitions require strict land use verification against Master Plan 2031 color coding."
    }
]


def evaluate_sanction_bylaws(locality_id, plot_width, plot_length, road_width=30, building_type="Residential"):
    """
    Evaluates exact municipal jurisdiction, Nambike Nakshe eligibility,
    setback requirements, FAR and mandatory NOC checklist.
    """
    # Find jurisdiction record
    locality_data = next((item for item in BENGALURU_JURISDICTION_REGISTRY if item['id'] == locality_id), None)
    
    if not locality_data:
        # Fallback to general GBA/BBMP
        locality_data = {
            "id": "general_bengaluru",
            "name": "Bengaluru Urban General",
            "zone": "Greater Bengaluru Metropolitan Area",
            "primary_authority": "Greater Bengaluru Authority (GBA) / BBMP",
            "zonal_office": "Central Office, Hudson Circle, Bengaluru - 560002",
            "applicable_acts": ["Greater Bengaluru Governance Act 2026", "BBMP Building Bye-Laws"],
            "layout_authorities": ["BDA", "BBMP", "BMRDA"],
            "is_airport_funnel": False,
            "nambike_nakshe_active": True,
            "typical_betterment_rate": 250,
            "guidelines": "Standard municipal sanction process via EoDB-OBPS with pre-DCR compliance."
        }

    plot_area_sqft = float(plot_width) * float(plot_length)
    
    # Nambike Nakshe Rules (Karnataka Govt 2024-2026 notification):
    # - Applicable to Residential plots up to 50ft x 80ft (4,000 sq ft or 371.6 sq m)
    # - In BBMP / GBA jurisdiction
    # - Self-declaration provisional sanction granted automatically upon submission by COA Architect
    nambike_eligible = False
    nambike_reason = ""
    
    if building_type.lower() == "residential":
        if locality_data["nambike_nakshe_active"]:
            if plot_area_sqft <= 4000 and (plot_width <= 50 and plot_length <= 80):
                nambike_eligible = True
                nambike_reason = "Eligible for instant trust-based 'Nambike Nakshe' self-declaration sanction. Provisional plan generated immediately with digital signature."
            else:
                nambike_reason = "Plot size exceeds 50x80 ft (4,000 sq.ft threshold). Subject to standard EoDB-OBPS AutoDCR scrutiny and physical site inspection."
        else:
            nambike_reason = f"Located in {locality_data['primary_authority']} jurisdiction where local planning authority single-window system applies."
    else:
        nambike_reason = "Commercial / Institutional / Multi-family properties are subject to comprehensive municipal scrutiny, CFO Fire NOC, and High-Rise Committee clearance."

    # Calculate Setback Matrix (Standard BBMP / GBA Residential norms)
    # Front, Rear, Left, Right setbacks (in meters and feet)
    if plot_area_sqft <= 1200: # 30x40 or smaller
        setbacks = {
            "front": "1.0 m (3.3 ft)",
            "rear": "1.0 m (3.3 ft)",
            "left": "0.75 m (2.5 ft)",
            "right": "0.75 m (2.5 ft)",
            "note": "Minimum setbacks for plots up to 1,200 sq.ft under RMP 2015/2031 norms."
        }
        far_base = 1.75
    elif plot_area_sqft <= 2400: # 40x60
        setbacks = {
            "front": "1.5 m (5.0 ft)",
            "rear": "1.2 m (4.0 ft)",
            "left": "1.0 m (3.3 ft)",
            "right": "1.0 m (3.3 ft)",
            "note": "Standard setbacks for 40x60 residential plots."
        }
        far_base = 2.00
    elif plot_area_sqft <= 4000: # 50x80
        setbacks = {
            "front": "2.5 m (8.2 ft)",
            "rear": "1.75 m (5.7 ft)",
            "left": "1.5 m (5.0 ft)",
            "right": "1.5 m (5.0 ft)",
            "note": "Standard setbacks for 50x80 residential plots."
        }
        far_base = 2.25
    else:
        setbacks = {
            "front": "3.5 m (11.5 ft)",
            "rear": "3.0 m (9.8 ft)",
            "left": "2.0 m (6.6 ft)",
            "right": "2.0 m (6.6 ft)",
            "note": "Large plot guidelines. Front setback depends on abutting road width."
        }
        far_base = 2.50

    # Road Width multiplier on FAR
    if road_width < 30:
        far = min(far_base, 1.5)
    elif road_width <= 40:
        far = far_base
    elif road_width <= 60:
        far = far_base + 0.25
    else:
        far = far_base + 0.50 # High road width bonus / Premium FAR eligible

    max_permissible_builtup = round(plot_area_sqft * far, 2)

    # Mandatory NOCs
    mandatory_nocs = [
        {"name": "BESCOM Power Feasibility", "mandatory": True, "notes": "Required for temporary construction power and permanent connection."},
        {"name": "BWSSB Water & Sanitary NOC", "mandatory": True if plot_area_sqft > 1200 or building_type != "Residential" else False, "notes": "Mandatory for built-up > 1,200 sq.ft or apartments."}
    ]

    if locality_data["is_airport_funnel"]:
        mandatory_nocs.append({
            "name": "AAI Airport NOC (Height Clearance)",
            "mandatory": True,
            "notes": "Plot lies within Airport Obstacle Limitation Surface funnel. Color-coded zoning map verification required."
        })

    if building_type != "Residential" or plot_area_sqft > 4000:
        mandatory_nocs.append({
            "name": "Fire & Emergency Services NOC",
            "mandatory": True,
            "notes": "Required for commercial, industrial or residential structures exceeding 15 meters in height."
        })

    if plot_area_sqft > 20000:
        mandatory_nocs.append({
            "name": "KSPCB Environmental Clearance",
            "mandatory": True,
            "notes": "State Environmental Impact Assessment for built-up > 20,000 sq.m."
        })

    return {
        "locality": locality_data["name"],
        "authority": locality_data["primary_authority"],
        "zone": locality_data["zone"],
        "zonal_office": locality_data["zonal_office"],
        "applicable_acts": locality_data["applicable_acts"],
        "plot_dimensions": f"{plot_width} ft x {plot_length} ft",
        "plot_area_sqft": plot_area_sqft,
        "road_width_ft": road_width,
        "building_type": building_type,
        "nambike_nakshe": {
            "eligible": nambike_eligible,
            "status": "APPROVED FOR INSTANT SELF-DECLARATION" if nambike_eligible else "STANDARD MUNICIPAL SCRUTINY",
            "details": nambike_reason,
            "sla_days": "Same-Day Provisional Sanction" if nambike_eligible else "14 to 21 Days (Sakala Guarantee)"
        },
        "byelaws": {
            "permissible_far": far,
            "max_permissible_builtup_sqft": max_permissible_builtup,
            "setbacks": setbacks
        },
        "mandatory_nocs": mandatory_nocs,
        "betterment_rate_per_sqft": locality_data["typical_betterment_rate"],
        "special_guidelines": locality_data["guidelines"]
    }
