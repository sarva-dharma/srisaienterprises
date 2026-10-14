#!/usr/bin/env python3
"""
Sri Sai Enterprises (ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್) - Client Data & CRM Management System
Author: Antigravity IDE Pair Programmer for S.M. Thyagaraja
Heritage: Estd. 1989 • 37+ Years of Excellence
Contact: Mobile +91 94480 54185 | Studio Landline: 080-23325509

This utility manages background customer data, leads, Sakala project lifecycles,
and client portal communications for the 5 client personas who encountered the website.
"""

import os
import sys
import json
import sqlite3
import argparse
from datetime import datetime

# Configure UTF-8 encoding for Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Database paths
DB_PATHS = [
    os.path.abspath('2.03/backend/bengaluru_sanctions.db'),
    os.path.abspath('2.02/backend/bengaluru_sanctions.db')
]

CLIENT_PERSONAS = [
    {
        "id": 1,
        "ref_no": "SAKALA-GBA-2026-1041",
        "name": "Nandini Ramanathan",
        "persona_title": "Residential Plot Owner / Heritage Family",
        "email": "nandini.ramanathan@gmail.com",
        "phone": "+91 98450 12345",
        "password": "Nandini@Bangalore2026",
        "location": "RMV 2nd Stage, Ward 18, Bengaluru",
        "dimensions": "40x60 ft (2,400 sq.ft plot, 4,800 sq.ft built-up)",
        "service": "Plan Sanctions & Approvals (GBA / BBMP)",
        "project_title": "G+3 Luxury Residential Villa - RMV 2nd Stage",
        "authority": "GBA / BBMP (North Zone)",
        "discovery_journey": "Encountered website while searching for BDA layout sanction specialists in Rajajinagar/Gayathrinagar. Used Cost Estimator for 40x60 G+3.",
        "inbound_inquiry": "Namaskara! We own a 40x60 BDA plot in RMV 2nd Stage. We are planning a G+3 independent house. Need complete BBMP architectural sanction, PreDCR CAD layer clearance, and an SBI home loan estimation BOQ. Please confirm your Sakala SLA guarantee.",
        "stage": "Stage 2: PreDCR Scrutiny & Municipal Layer Coding",
        "progress": 45,
        "nambike_eligible": False,
        "estimated_cost": "Rs. 1,48,500 (Sanction, Betterment & Scrutiny)",
        "next_action": "Submit PreDCR DWG to BBMP BPAS portal and notify client for municipal challan payment."
    },
    {
        "id": 2,
        "ref_no": "SAKALA-GBA-2026-1042",
        "name": "Kiran Kumar Gowda",
        "persona_title": "Tech Professional / Young Home Builder",
        "email": "kiran.gowda@techblr.io",
        "phone": "+91 99002 67890",
        "password": "Kiran@Gowda2026",
        "location": "JP Nagar 7th Phase, Ward 187, Bengaluru",
        "dimensions": "30x40 ft (1,200 sq.ft plot, 2,700 sq.ft built-up)",
        "service": "Nambike Nakshe Fast-Track Sanction",
        "project_title": "Duplex House Trust-Based Approval - JP Nagar",
        "authority": "GBA / BBMP (South Zone)",
        "discovery_journey": "Found website via tech company internal Slack real estate channel. Impressed by Nambike Nakshe self-declaration guide and online client tracking.",
        "inbound_inquiry": "Hi Thyagaraja sir, I work at an Outer Ring Road tech firm. I have a 30x40 site in JP Nagar 7th Phase. Can I get immediate provisional approval under the new Nambike Nakshe scheme? Need end-to-end digital tracking as I cannot visit BBMP office on weekdays.",
        "stage": "Stage 3: AutoDCR Submission & Algorithmic Validation",
        "progress": 60,
        "nambike_eligible": True,
        "estimated_cost": "Rs. 62,000 (Fast-Track Municipal Scrutiny + Plan Drafting)",
        "next_action": "Issue digital provisional approval certificate for download via client portal."
    },
    {
        "id": 3,
        "ref_no": "SAKALA-GBA-2026-1043",
        "name": "Deepika Shastry",
        "persona_title": "Boutique Architect / CAD Consultant",
        "email": "deepika.shastry@outlook.com",
        "phone": "+91 97411 98765",
        "password": "Deepika@Shastry2026",
        "location": "HSR Layout Sector 2, Ward 174, Bengaluru",
        "dimensions": "50x80 ft (4,000 sq.ft plot, 9,600 sq.ft built-up)",
        "service": "AutoDCR & PreDCR CAD Drafting",
        "project_title": "Residential Apartment Complex (6 Units) - HSR Layout",
        "authority": "GBA / BBMP (Bommanahalli Zone)",
        "discovery_journey": "Looking for a seasoned municipal liaisoning partner to convert architectural concept drawings into zero-error PreDCR layers for BBMP BPAS.",
        "inbound_inquiry": "Hello S.M. Thyagaraja Sir, I run an architecture practice in Indiranagar. We have a 6-unit residential project in HSR Layout 50x80 plot. We need Sri Sai Enterprises to handle PreDCR CAD layer structuring, FAR optimization, and ADTP liaisoning for site inspection.",
        "stage": "Stage 3: Site Inspection Coordination by Ward AEE",
        "progress": 75,
        "nambike_eligible": False,
        "estimated_cost": "Rs. 2,85,000 (Full Multi-Unit Sanction, Rainwater Harvesting & Fire Verification)",
        "next_action": "Coordinate Ward 174 Assistant Executive Engineer (AEE) site inspection schedule."
    },
    {
        "id": 4,
        "ref_no": "SAKALA-GBA-2026-1044",
        "name": "Mohammed Tariq Mansoor",
        "persona_title": "Local Property Owner / Revenue Plot Upgrader",
        "email": "tariq.mansoor@gmail.com",
        "phone": "+91 98860 45678",
        "password": "Tariq@Mansoor2026",
        "location": "Whitefield Borewell Road, Ward 84, Bengaluru",
        "dimensions": "30x50 ft (1,500 sq.ft plot, 3,375 sq.ft built-up)",
        "service": "e-Khata / B-Khata to A-Khata Conversion",
        "project_title": "B-Khata Betterment & Sanction - Whitefield",
        "authority": "GBA / BBMP (Mahadevapura Zone)",
        "discovery_journey": "Encountered website's B-Khata to A-Khata conversion guide and e-Aasthi betterment rate calculation table.",
        "inbound_inquiry": "Respected Sir, My property on Borewell Road Whitefield is currently on B-Khata. I need to pay betterment charges, get e-Khata, and subsequently apply for a G+2 residential building plan sanction. Can your Gayathrinagar office manage the title scrutiny?",
        "stage": "Stage 1: e-Aasthi Document Ingestion & Title Check",
        "progress": 25,
        "nambike_eligible": True,
        "estimated_cost": "Rs. 1,12,000 (Betterment Payment + e-Khata Regularization + Sanction)",
        "next_action": "Complete 30-year Encumbrance Certificate (EC) chain verification and generate BBMP betterment challan."
    },
    {
        "id": 5,
        "ref_no": "SAKALA-BIAAPA-2026-1045",
        "name": "Dr. Ramesh Chandrasekhar",
        "persona_title": "Institutional Developer / Healthcare Entrepreneur",
        "email": "dr.ramesh.chandra@manipal.edu",
        "phone": "+91 94481 87654",
        "password": "Ramesh@Chandra2026",
        "location": "Devanahalli Airport Corridor, Bengaluru",
        "dimensions": "60x100 ft (6,000 sq.ft plot, 15,000 sq.ft built-up)",
        "service": "BIAAPA & STRR Multi-Authority Clearance",
        "project_title": "Commercial Healthcare & Diagnostic Center - Devanahalli",
        "authority": "BIAAPA / STRR (North Bengaluru)",
        "discovery_journey": "Searched for 30+ year veteran liaisoners with direct experience handling BIAAPA and AAI height clearance grids along NH-44.",
        "inbound_inquiry": "Dear Thyagaraja Garu, We are establishing an advanced diagnostic center in Devanahalli corridor. Need comprehensive single-window clearance from BIAAPA, Karnataka Fire & Emergency, and Airport Authority of India (AAI NOCAS). Strict timeline required.",
        "stage": "Stage 3: BIAAPA Technical Committee & AAI Height Clearance",
        "progress": 85,
        "nambike_eligible": False,
        "estimated_cost": "Rs. 4,50,000 (Multi-Agency Institutional Clearance + NOC Filing)",
        "next_action": "Attend BIAAPA Technical Committee hearing and obtain final NOC sanction dispatch."
    }
]

def get_db_connection():
    for p in DB_PATHS:
        if os.path.exists(p):
            return sqlite3.connect(p)
    return None

def cmd_list():
    print("=" * 90)
    print("  SRI SAI ENTERPRISES (ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್) - CLIENT PIPELINE CRM")
    print("  Direct Desk: +91 94480 54185  |  Landline: 080-23325509  |  Gayathrinagar, Bangalore")
    print("=" * 90)
    print(f"{'#':<3} {'CLIENT NAME':<24} {'SAKALA REF':<22} {'STAGE':<25} {'PROGRESS':<8}")
    print("-" * 90)
    for c in CLIENT_PERSONAS:
        print(f"{c['id']:<3} {c['name']:<24} {c['ref_no']:<22} {c['stage'][:24]:<25} {c['progress']}%")
    print("=" * 90)
    print("Run: 'python manage_client_crm.py view <id_or_ref>' for detailed client dossier.")
    print("Run: 'python manage_client_crm.py notify <id_or_ref>' for instant bilingual WhatsApp dispatch.")

def cmd_view(identifier):
    client = None
    for c in CLIENT_PERSONAS:
        if str(c['id']) == str(identifier) or c['ref_no'].lower() == str(identifier).lower() or identifier.lower() in c['name'].lower():
            client = c
            break

    if not client:
        print(f"[ERROR] Client matching '{identifier}' not found.")
        return

    print("\n" + "=" * 80)
    print(f"  CLIENT DOSSIER: {client['name'].upper()} ({client['persona_title']})")
    print("=" * 80)
    print(f"  Sakala Tracking Ref : {client['ref_no']}")
    print(f"  Client Portal Login : {client['email']} / {client['password']}")
    print(f"  Contact Phone       : {client['phone']}")
    print(f"  Property Location   : {client['location']}")
    print(f"  Plot & Built-up     : {client['dimensions']}")
    print(f"  Sanction Authority  : {client['authority']}")
    print(f"  Nambike Nakshe      : {'ELIGIBLE (Fast-Track Self Declaration)' if client['nambike_eligible'] else 'Standard Comprehensive Scrutiny'}")
    print("-" * 80)
    print(f"  HOW THEY FOUND US   :\n  {client['discovery_journey']}")
    print("-" * 80)
    print(f"  RAW INBOUND INQUIRY :\n  \"{client['inbound_inquiry']}\"")
    print("-" * 80)
    print(f"  CURRENT STATUS      : {client['stage']} ({client['progress']}% Complete)")
    print(f"  ESTIMATED CHARGES   : {client['estimated_cost']}")
    print(f"  NEXT ACTION ITEM    : {client['next_action']}")
    print("=" * 80 + "\n")

def cmd_notify(identifier):
    client = None
    for c in CLIENT_PERSONAS:
        if str(c['id']) == str(identifier) or c['ref_no'].lower() == str(identifier).lower() or identifier.lower() in c['name'].lower():
            client = c
            break

    if not client:
        print(f"[ERROR] Client matching '{identifier}' not found.")
        return

    first_name = client['name'].split()[0]
    wa_msg = (
        f"Namaskara {first_name} avare, Greetings from Sri Sai Enterprises (Estd. 1989).\n\n"
        f"Your building sanction project '{client['project_title']}' has progressed to: *{client['stage']}* ({client['progress']}% complete).\n\n"
        f"Sakala Reference: *{client['ref_no']}*\n"
        f"Next Step: {client['next_action']}\n\n"
        f"You can view your verified drawings & municipal receipts in your client portal at:\n"
        f"https://sarva-dharma.github.io/srisaienterprises/#client-portal-section\n"
        f"Login ID: {client['email']}\n\n"
        f"For any queries, call S.M. Thyagaraja (+91 94480 54185) or our Gayathrinagar studio landline at 080-23325509."
    )

    encoded_msg = json.dumps(wa_msg)[1:-1] # clean escape
    print("\n" + "=" * 80)
    print(f"  WHATSAPP / SMS ALERT FOR {client['name'].upper()} ({client['phone']})")
    print("=" * 80)
    print(wa_msg)
    print("-" * 80)
    print(f"Direct WhatsApp Click Link:")
    import urllib.parse
    phone_clean = client['phone'].replace('+', '').replace(' ', '')
    wa_url = f"https://wa.me/{phone_clean}?text={urllib.parse.quote(wa_msg)}"
    print(wa_url)
    print("=" * 80 + "\n")

def cmd_advance(ref_no, new_stage, new_progress):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("UPDATE projects SET current_stage = ?, completion_percent = ? WHERE reference_no = ?", (new_stage, new_progress, ref_no))
        conn.commit()
        conn.close()
        print(f"[SUCCESS] Updated database for {ref_no}: Stage -> '{new_stage}', Progress -> {new_progress}%")
    else:
        print("[NOTICE] Running in static mode; database not directly attached.")

def cmd_export():
    export_path = os.path.abspath('client_pipeline_export.json')
    with open(export_path, 'w', encoding='utf-8') as f:
        json.dump(CLIENT_PERSONAS, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Exported 5 client dossiers to: {export_path}")

def main():
    parser = argparse.ArgumentParser(description="Sri Sai Enterprises Client CRM Manager")
    parser.add_argument('action', choices=['list', 'view', 'notify', 'advance', 'export'], help="Action to execute")
    parser.add_argument('param', nargs='?', default=None, help="Client ID or Sakala Ref No")
    parser.add_argument('--stage', help="New stage name for advance")
    parser.add_argument('--progress', type=int, default=50, help="New progress percentage")

    args = parser.parse_args()

    if args.action == 'list':
        cmd_list()
    elif args.action == 'view':
        if not args.param:
            print("Please specify client id or ref_no, e.g., 'python manage_client_crm.py view 1'")
            sys.exit(1)
        cmd_view(args.param)
    elif args.action == 'notify':
        if not args.param:
            print("Please specify client id or ref_no, e.g., 'python manage_client_crm.py notify 2'")
            sys.exit(1)
        cmd_notify(args.param)
    elif args.action == 'advance':
        if not args.param or not args.stage:
            print("Usage: python manage_client_crm.py advance <ref_no> --stage '<stage_name>' --progress <percent>")
            sys.exit(1)
        cmd_advance(args.param, args.stage, args.progress)
    elif args.action == 'export':
        cmd_export()

if __name__ == '__main__':
    main()
