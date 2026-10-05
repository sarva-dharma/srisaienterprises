# Database Schema Documentation

## Bengaluru Building Plan Sanction & Architectural Liaisoning System

This system uses a normalized relational schema (SQLite default with PostgreSQL / MySQL compatibility via SQLAlchemy ORM).

```mermaid
erDiagram
    USERS ||--o{ PROJECTS : "owns (clients)"
    USERS ||--o{ PROJECTS : "assigned (architects)"
    SERVICES ||--o{ LEADS : "inquired_in"
    PROJECTS ||--o{ PROJECT_TIMELINES : "tracks"
    PROJECTS ||--o{ PROJECT_DOCUMENTS : "contains"

    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        string role "admin | architect | client"
        string phone
        datetime created_at
    }

    SERVICES {
        int id PK
        string title
        string slug UK
        string category
        string short_desc
        text full_desc
        string icon
        float base_fee
        float betterment_rate_sqft
        float scrutiny_rate_sqft
        string turnaround_days
        boolean is_active
        int display_order
        text features_json
        datetime created_at
    }

    LEADS {
        int id PK
        string full_name
        string email
        string phone
        string plot_location
        string plot_dimensions
        int service_id FK
        string service_title
        text message
        string status "new | contacted | quotation_sent | converted | archived"
        text internal_notes
        datetime created_at
        datetime updated_at
    }

    PROJECTS {
        int id PK
        string reference_no UK "e.g. SAKALA-GBA-2026-0894"
        int client_id FK
        string client_name
        string title
        string plot_location
        string ward_no
        string survey_no
        string authority "GBA | BBMP | BDA | BIAAPA | STRR"
        string current_stage "Drafting | PreDCR Scrutiny | AutoDCR Submission | Site Inspection | NOC Clearance | Approved"
        boolean nambike_nakshe_eligible
        float plot_area_sqft
        float builtup_area_sqft
        string assigned_architect
        int completion_percent
        text remarks
        datetime created_at
        datetime updated_at
    }

    PROJECT_TIMELINES {
        int id PK
        int project_id FK
        string stage_name
        string status "completed | in_progress | pending"
        string date_updated
        string remarks
    }

    PROJECT_DOCUMENTS {
        int id PK
        int project_id FK
        string title
        string doc_type "CAD_DWG | SANCTION_CERT | E_KHATA | EC | NOC | OTHER"
        string filename
        string file_path
        string file_size_display
        boolean is_downloadable
        datetime uploaded_at
    }

    BLOG_POSTS {
        int id PK
        string title
        string slug UK
        string category
        text excerpt
        text content
        string author
        string read_time
        boolean is_published
        datetime created_at
    }
```

### Table Definitions & Indices

1. **`users`**
   - Stores credential hashes using Werkzeug PBKDF2/SHA-256.
   - Roles: `admin` (access to CRM & CMS), `architect` (can update project stages), `client` (can view their Sakala applications).
   - Index on `email`.

2. **`services`**
   - Editable via Admin CMS. Controls public pricing, scrutiny rates, and betterment estimation multipliers.
   - Index on `slug`, `is_active`, `display_order`.

3. **`leads`**
   - CRM records captured via consultation booking forms and contact widgets.
   - Status transitions: `new` -> `contacted` -> `quotation_sent` -> `converted`.

4. **`projects`**
   - Core municipal application entity. Represents an active file undergoing Karnataka Sakala / EoDB-OBPS scrutiny.
   - `reference_no`: Unique statutory reference format `SAKALA-[AUTHORITY]-[YEAR]-[ID]`.

5. **`project_timelines`**
   - Step-by-step audit milestones: Drafting, PreDCR Scrutiny, AutoDCR Submission, Site Inspection, NOC Clearance, Approved.

6. **`project_documents`**
   - Secure downloadable storage for PreDCR CAD drawings (.dxf / .dwg), digital sanction orders, e-Khata extract copies, and municipal NOCs.
