# Bengaluru Building Plan Sanctions & Architectural Liaisoning Platform (2026)

A full-stack, responsive, and dynamic web application for a premium **Building Plan Sanction, Architectural Design, and Liaisoning Service** based in Bengaluru, Karnataka.

Built to comply with the latest **Greater Bengaluru Authority (GBA 2026)** metropolitan planning norms and **Nambike Nakshe (Trust-Based Instant Self-Declaration)** building sanction rules.

---

## 🌟 Core Features

### Part 1: Front-End (Client-Facing Website)
- **High-Converting Hero Section**:
  - Headline: *"Expert Building Plan Approvals & Architecture in Bengaluru."*
  - Statutory highlights: **GBA 2026** compliance and **Nambike Nakshe** trust-based self-declaration rules.
  - CTAs: *"Book a Free Consultation"* and *"Track Your Approval"*.
  - Quick Sakala / EoDB reference tracking bar.
- **Interactive Bengaluru Jurisdiction & Bylaw Checker**:
  - Search/select from 25+ real Bengaluru areas & wards (Whitefield, Indiranagar, Yelahanka, HSR Layout, Electronic City, Devanahalli, Nelamangala, Sarjapur, etc.).
  - Instant calculation of:
    - Governing Authority (GBA, BBMP, BDA, BIAAPA, STRR, BMICPA).
    - Nambike Nakshe Eligibility (Fast-track self-declaration for residential plots up to 50x80 ft / 4,000 sq.ft).
    - Permissible Floor Area Ratio (FAR / FSI) by road width.
    - Setbacks Matrix (Front, Rear, Left, Right).
    - Mandatory NOC checklist (BWSSB, BESCOM, Fire CFO, AAI Airport Height NOC).
- **Dynamic Services Catalog (Pulled from Backend CMS)**:
  1. **Plan Sanctions & Approvals** (GBA, BBMP, BDA, BMRDA, BIAAPA, BMICPA, STRR)
  2. **e-Khata Services & Conversions** (Digital e-Khata, transfers, B-Khata to A-Khata with betterment charges)
  3. **AutoDCR & PreDCR CAD Drafting** (Municipal bypass CAD rules, algorithmic layer scrutiny)
  4. **Turnkey Construction & Architectural Design** (Vastu-compliant drawings, structural engineering)
  5. **NOC Procurement & Clearances** (BWSSB, BESCOM, Fire Department, Airport Authority)
- **Building Sanction Cost & Betterment Fee Estimator**:
  - Live interactive calculation of municipal scrutiny fees, statutory cess, betterment levies (for B-Khata), and AutoDCR drafting charges.
- **Client Portal (Live Sakala & EoDB Tracker)**:
  - Track by reference number (e.g., `SAKALA-GBA-2026-0894`).
  - 6-Milestone audit trail: *Drafting &rarr; PreDCR Scrutiny &rarr; AutoDCR Submission &rarr; Site Inspection &rarr; NOC Clearance &rarr; Approved*.
  - Secure document download vault with simulated CAD drawing downloads (.dxf/.dwg) and digitally signed sanction certificates with SHA-256 tokens.
- **Trust Signals & Footer**:
  - Council of Architecture (COA) registration badge: `CA/2009/44120`.
  - Physical studio address at MG Road / Lavelle Road Junction, Bengaluru - 560001.
  - Real Google Maps link integration.
  - WhatsApp Concierge floating widget.
  - Verified client reviews from Indiranagar, Whitefield, and Devanahalli.

### Part 2: Back-End (Admin Dashboard & CRM/CMS)
- **Lead Management CRM**:
  - View, sort, filter incoming consultation requests.
  - Update lead status (*New, Contacted, Quote Sent, Converted, Archived*).
  - Internal private notes field.
  - 1-Click direct WhatsApp response link.
- **Client Application Tracker**:
  - Create new client files and auto-generate unique Sakala reference numbers.
  - Advance project stage (*PreDCR &rarr; AutoDCR &rarr; Site Inspection &rarr; Approved*).
  - **Live Reflection**: Advancing a stage in the Admin CRM immediately updates the client's front-end portal!
- **Service & Content Editor (CMS)**:
  - GUI editor to update service descriptions, base fees, betterment fee rates per sq.ft, and scrutiny rates without editing code.
  - Add new services directly into the public catalog.
- **Zoning Law Knowledge Hub (CMS)**:
  - Publish articles and municipal policy updates directly to the website.

---

## 🚀 Quick Start Instructions

### Prerequisites
- Python 3.10+ (Python 3.11 pre-installed)
- No Node.js required! (Runs zero-dependency with Flask & SQLite)

### Launching the Application

1. **Double-click `run_app.bat`** (on Windows) or run in terminal:
   ```bash
   python run.py
   ```
2. Open your browser and navigate to:
   ```
   http://127.0.0.1:5005
   ```

### Pre-Configured Demo Credentials

| Portal | URL | Username | Password |
|---|---|---|---|
| **Admin CRM & CMS** | `http://127.0.0.1:5005/admin` | `admin@bengaluruapprovals.com` | `admin123` |
| **Client Portal** | `http://127.0.0.1:5005/portal` | `client@example.com` | `client123` |
| **Live Sakala Ref** | Tracking Input | `SAKALA-GBA-2026-0894` | N/A |

---

## 📁 Project Architecture

```
website 2.02/
├── backend/
│   ├── app.py                 # Flask factory & blueprint registration
│   ├── config.py              # Application settings & database URI
│   ├── database.py            # SQLAlchemy database instance
│   ├── models.py              # User, Service, Lead, Project, Timeline, Document, Blog
│   ├── seed_data.py           # Auto-seeds Bengaluru municipal accounts & demo applications
│   ├── routes/
│   │   ├── auth_routes.py     # Login, Register, Session check
│   │   ├── public_routes.py   # Services, Jurisdiction Checker, Cost Calculator, Leads
│   │   ├── client_routes.py   # Sakala project tracking, document downloads
│   │   └── admin_routes.py    # Leads CRM, Stage advancing, Service & Blog CMS
│   └── services/
│       └── jurisdiction_data.py # 25+ Bengaluru localities, GBA 2026 & Nambike Nakshe rules
├── static/
│   ├── css/custom.css         # Luxury architectural palette & glassmorphism
│   └── js/
│       ├── api.js             # Central REST API client
│       ├── jurisdiction.js    # Interactive jurisdiction & bylaw engine
│       ├── calculator.js      # Fee & betterment estimator
│       ├── portal.js          # Client portal live timeline & download vault
│       ├── admin.js           # Admin CRM & CMS console
│       └── main.js            # Main UI orchestrator
├── templates/
│   └── index.html             # High-converting master UI template
├── docs/
│   ├── DATABASE_SCHEMA.md     # Entity Relationship diagrams & table definitions
│   └── NODE_EXPRESS_REF.md    # Equivalent Node.js / Express + Prisma reference
├── tests/
│   └── test_api.py            # Complete automated test suite
├── run.py                     # Single-command application launcher
├── run_app.bat                # Windows double-click runner
├── requirements.txt           # Python dependencies
└── README.md                  # Complete documentation
```

---

## 🧪 Automated Testing

Run the test suite at any time:
```bash
python -m unittest tests/test_api.py
```
*All 9 integration tests cover public endpoints, Nambike Nakshe evaluation, CRM lead creation, client tracking, and CMS live updates.*
