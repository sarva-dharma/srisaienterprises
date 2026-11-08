# SEO, GEO & Schema Specification Report: Sri Sai Enterprises (ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್)

**Working Directory**: `c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\spec_miner_survey_2\`  
**Milestone**: Survey & Technical Specification  
**Target Application**: Sri Sai Enterprises Official Web Platform (`https://sarva-dharma.github.io/srisaienterprises/`)  
**Heritage & Estd**: 1989 (37+ Years of Excellence | 23,000+ Sanctions Delivered)  
**Parent Orchestrator**: `ada7118d-a98d-4e9f-80db-a5cad957aa08`

---

## Executive Summary
This document specifies the complete, production-grade technical implementation for **Search Engine Optimization (SEO)**, **Generative Engine Optimization (GEO)**, and **Schema.org JSON-LD Structured Data** for the Sri Sai Enterprises web platform.

Following the principles established in modern AI search workflows (incorporating Google Search Console, OpenSEO, Schema.org standards, and entity-first Generative Engine Optimization demonstrated in reference materials such as https://youtu.be/S9lQp9SSxZk), this specification equips the storefront for high-fidelity discovery by both traditional search crawlers (Google, Bing) and AI search agents (Perplexity, ChatGPT Search, Google Gemini / AI Overviews, Microsoft Copilot).

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Schema.org | LocalBusiness / Store Entity | Comprehensive entity definition of Sri Sai Enterprises (`ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್`) with address, geocoordinates, opening hours, currenciesAccepted, paymentAccepted, telephone, email, founder credentials (COA Reg. CA/2009/44120, BBMP Supervisor BCC/BL-3.2.3/S-218/89-90), and areaServed across Bengaluru. | Verified address (#3309, 1st Main Rd, Gayathrinagar), Lat/Lng (12.9965, 77.5562), Phone (+91 94480 54185), Estd 1989 | Valid Schema.org `LocalBusiness` / `Store` / `ProfessionalService` JSON-LD object | Schema parser rejection if required fields missing | `index.html`, `README.md`, `2.03/firm_details.csv` |
| 2 | Schema.org | WebSite & SearchAction | Defines the site root and deep search action enabling direct search query inputs (e.g. plot eligibility, bylaws) into the application. | Target URL template: `https://sarva-dharma.github.io/srisaienterprises/?q={search_term_string}#jurisdiction-checker` | Sitelinks search box eligibility in Google SERPs | Falls back to generic site URL if query param empty | `index.html` navbar & jurisdiction form |
| 3 | Schema.org | BreadcrumbList | Hierarchical navigation trail representing site architectural tiers (Home, Services, Zoning, Cost Estimator, BBMP BPAS, Knowledge Hub). | Hierarchical sections and corresponding URL hash anchors | Rich snippet breadcrumbs in Google SERP results | Broken link navigation if hashes misaligned | `index.html` nav architecture |
| 4 | Schema.org | Product / Service Offers | Catalog product schemas for 6 core offerings: Plan Sanctions, AutoDCR CAD Scrutiny, e-Khata Conversions, Architectural Design, Statutory NOCs, and Turnkey Construction with INR price, availability, condition, and seller backlink. | Catalog service items from `api.js` and `firm_services.csv` with base prices (₹18,000 to ₹50,000) | Product rich snippets with pricing badges in search listings | Google Merchant / rich snippet warnings if priceCurrency is missing | `static/js/api.js`, `2.03/firm_services.csv` |
| 5 | Schema.org | FAQPage (Store & AI Focused) | Q&A entities addressing common user and AI queries: office location & landmark, business hours, Sakala delivery SLA, accepted payment methods, service scope, and founder credentials. | Canonical store facts: Gayathrinagar, Mon-Sat 9:30-19:30, UPI/Cards/Cash, 14-21 days Sakala SLA | FAQ accordion snippets in SERP; verbatim quote extraction by Perplexity/ChatGPT/Gemini | Duplicate question penalties if repeated across pages | Codebase business data & customer personas (`manage_client_crm.py`) |
| 6 | Schema.org | SpeakableSpecification | Directs voice assistants (Google Assistant, Siri, voice LLMs) to extract text content from primary semantic headers. | CSS selectors: `#audience-navigator h2`, `#services h2`, `#about-founder h3`, `#fee-estimator h2` | Audio snippet readout on smart devices | Ignored silently if target CSS selectors do not exist | Voice search guidelines |
| 7 | GEO | Knowledge Graph & Entity Disambiguation | Establishes unambiguous entity identity linking official municipal portals (`bpas.bbmpgov.in`), Council of Architecture credentials, and verified phone/location. | Explicit `@id` URIs, `sameAs` links, founder node, license numbers | Knowledge Panel creation and high-confidence AI citation in Perplexity/ChatGPT | Hallucination or confusion with other businesses if credentials unverified | Brand audit & `2.03/firm_details.csv` |
| 8 | GEO | Bilingual Semantic Representation | Preserves dual Kannada (`kn-IN`) and English (`en-IN`) linguistic identity through `inLanguage`, `alternateName`, and `og:locale:alternate`. | Kannada and English titles, descriptions, and keywords | Localized Kannada SERP rankings and cross-lingual AI understanding | Font rendering issues if UTF-8 encoding omitted | `index.html` bilingual headings & signboard styling |
| 9 | Metadata | Open Graph & Twitter Cards | High-impact social media cards for link unfurling on WhatsApp, Twitter/X, LinkedIn, and Facebook with brand imagery and Kannada subtitle. | Absolute URL to `bbmp_tower_web.jpg`, title, description, dimensions (1200x630) | Rich preview card with image and description on share | Default fallback or broken preview box if image URL is relative | `index.html` head inspection |
| 10 | SEO | Canonical & Robots Directives | Controls crawler indexing, image previews, snippet lengths, and enforces the canonical GitHub Pages origin. | `index, follow, max-image-preview:large`, canonical link `https://sarva-dharma.github.io/srisaienterprises/` | Prevents duplicate content indexing across mirrors or staging branches | De-indexing if noindex erroneously set | `index.html` head & `.nojekyll` setup |
| 11 | Local SEO | Geo Meta Tags (ICBM / Lat-Long) | Machine-readable geographic positioning coordinates for Gayathrinagar studio to maximize Google Local / Maps indexing. | `geo.region: IN-KA`, `geo.placename: Bengaluru`, `geo.position: 12.9965;77.5562` | Higher local map pack and neighborhood proximity matching | Inaccurate local search ranking if coordinates drift | Gayathrinagar studio coordinates |
| 12 | Search Tracking | GSC Site Verification Placeholder | Google Search Console verification meta tag in `<head>` allowing instant ownership verification. | `<meta name="google-site-verification" content="...">` placeholder | Immediate activation of GSC rank and crawl monitoring | Search console verification failure | `ORIGINAL_REQUEST.md` (R2) |
| 13 | Discovery | Sitemaps & robots.txt Specification | Directives for automated discovery of the root URL and sitemap by search crawlers. | `sitemap.xml` format, crawl rate, User-agent rules | Rapid indexation of all page sections and assets | Crawler crawl-delay or 404 on sitemap.xml | Repository root audit |

---

## Edge Cases

| # | Feature | Input | Observed / Expected Behavior |
|---|---------|-------|------------------------------|
| 1 | Canonical URL | Access via `http://` or non-trailing slash (`/srisaienterprises`) | `<link rel="canonical">` points strictly to `https://sarva-dharma.github.io/srisaienterprises/`, instructing bots to aggregate ranking juice onto the canonical HTTPS endpoint. |
| 2 | Language Discrepancy | Crawler querying in pure Kannada (`kn`) vs English (`en`) | Entity schema specifies both `inLanguage: ["en-IN", "kn-IN"]` and `alternateName: ["ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್", "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್‌ಪ್ರೈಸಸ್"]`, ensuring bilingual retrieval. |
| 3 | Pricing Format | AI engine asking for consultation or sanction costs | `price: "35000.00"` with `priceCurrency: "INR"` and `itemCondition: "NewCondition"` prevents currency confusion (e.g. USD vs INR). |
| 4 | Working Hours Extraction | User asking "Is Sri Sai Enterprises open on Sunday?" | `OpeningHoursSpecification` lists days Monday through Saturday only (`09:30` to `19:30`), explicitly informing LLMs that Sunday is closed. |
| 5 | Geographic Scope | Client asking for approvals outside Bengaluru (e.g. Mysuru) | `areaServed` explicitly defines 9 administrative authorities: Bengaluru, Bangalore Urban, Bangalore Rural, GBA, BBMP, BDA, BIAAPA, BMRDA, STRR. |
| 6 | Relative URL in og:image | Sharing link on WhatsApp or iMessage | Social scrapers reject relative paths like `./static/...`. Spec specifies absolute URL `https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg`. |
| 7 | SearchAction Input | Sitelinks search query with spaces or special characters | URL template `.../?q={search_term_string}#jurisdiction-checker` URI-encodes query parameters cleanly. |

---

## Detailed Technical Specifications

### 1. Complete Schema.org JSON-LD Specification
The following valid JSON-LD graph must be placed inside `<script type="application/ld+json">` within the `<head>` of `index.html`. It unifies the store, website, breadcrumb trail, 6 catalog products/services, FAQ page, and webpage speakable elements under a single schema graph.

```html
<!-- Schema.org JSON-LD Structured Data: Sri Sai Enterprises (Unified Graph) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": ["LocalBusiness", "Store", "ProfessionalService"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#store",
      "name": "Sri Sai Enterprises",
      "alternateName": [
        "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್",
        "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್‌ಪ್ರೈಸಸ್",
        "Sri Sai Enterprises Bengaluru",
        "Sri Sai Enterprises Since 1989"
      ],
      "legalName": "Sri Sai Enterprises",
      "url": "https://sarva-dharma.github.io/srisaienterprises/",
      "logo": {
        "@type": "ImageObject",
        "url": "https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_official_logo.jpg",
        "width": "400",
        "height": "400"
      },
      "image": [
        "https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg",
        "https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_headquarters.jpg"
      ],
      "description": "Sri Sai Enterprises (Since 1989) is Bengaluru's premier architectural and municipal building plan approval practice, delivering 23,000+ sanctions across GBA, BBMP, BDA, and BIAAPA.",
      "foundingDate": "1989",
      "telephone": "+91-9448054185",
      "email": "smthyagaraj@gmail.com",
      "priceRange": "₹₹",
      "currenciesAccepted": "INR",
      "paymentAccepted": "Cash, UPI, Credit Card, Debit Card, Net Banking, Cheque",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "#3309, 1st Main Road, Gayathrinagar",
        "addressLocality": "Bengaluru",
        "addressRegion": "Karnataka",
        "postalCode": "560021",
        "addressCountry": "IN"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 12.9965,
        "longitude": 77.5562
      },
      "hasMap": "https://maps.google.com/?q=Gayathrinagar+Bangalore",
      "openingHoursSpecification": [
        {
          "@type": "OpeningHoursSpecification",
          "dayOfWeek": [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday"
          ],
          "opens": "09:30",
          "closes": "19:30"
        }
      ],
      "areaServed": [
        {
          "@type": "City",
          "name": "Bengaluru",
          "sameAs": "https://en.wikipedia.org/wiki/Bangalore"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Bangalore Urban",
          "sameAs": "https://en.wikipedia.org/wiki/Bangalore_Urban_district"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Greater Bengaluru Authority (GBA)"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Bruhat Bengaluru Mahanagara Palike (BBMP)"
        },
        {
          "@type": "AdministrativeArea",
          "name": "Bangalore Development Authority (BDA)"
        },
        {
          "@type": "AdministrativeArea",
          "name": "BIAAPA"
        },
        {
          "@type": "AdministrativeArea",
          "name": "BMRDA"
        },
        {
          "@type": "AdministrativeArea",
          "name": "STRR"
        }
      ],
      "founder": {
        "@type": "Person",
        "@id": "https://sarva-dharma.github.io/srisaienterprises/#founder",
        "name": "S. M. Thyagaraja",
        "alternateName": "ಎಸ್. ಎಂ. ತ್ಯಾಗರಾಜ",
        "jobTitle": "Principal Architect & Draftsman Civil",
        "telephone": "+91-9448054185",
        "hasCredential": [
          {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "Professional License",
            "name": "Council of Architecture Registration",
            "recognizedBy": {
              "@type": "Organization",
              "name": "Council of Architecture (India)"
            },
            "identifier": "CA/2009/44120"
          },
          {
            "@type": "EducationalOccupationalCredential",
            "credentialCategory": "Municipal Supervisor License",
            "name": "BBMP Approved Technical Supervisor License",
            "recognizedBy": {
              "@type": "GovernmentOrganization",
              "name": "Bruhat Bengaluru Mahanagara Palike"
            },
            "identifier": "BCC/BL-3.2.3/S-218/89-90"
          }
        ]
      },
      "sameAs": [
        "https://bpas.bbmpgov.in",
        "https://wa.me/919448054185"
      ]
    },
    {
      "@type": "WebSite",
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#website",
      "url": "https://sarva-dharma.github.io/srisaienterprises/",
      "name": "Sri Sai Enterprises",
      "alternateName": "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್",
      "description": "Official Web Platform for Sri Sai Enterprises - Building Plan Approvals, Architecture, Estimation & Land Surveying in Bengaluru since 1989.",
      "publisher": {
        "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
      },
      "inLanguage": ["en-IN", "kn-IN"],
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://sarva-dharma.github.io/srisaienterprises/?q={search_term_string}#jurisdiction-checker"
        },
        "query-input": "required name=search_term_string"
      }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home (ಮುಖಪುಟ)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Services (ಸೇವೆಗಳು)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#services"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Jurisdiction & Zoning (ವಲಯ ಪರಿಶೀಲನೆ)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#jurisdiction-checker"
        },
        {
          "@type": "ListItem",
          "position": 4,
          "name": "Cost Estimator (ವೆಚ್ಚ ಅಂದಾಜು)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#fee-estimator"
        },
        {
          "@type": "ListItem",
          "position": 5,
          "name": "BBMP BPAS Portal (ಬಿಬಿಎಂಪಿ ಬಿಪಿಎಎಸ್)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#bbmp-bpas-portal"
        },
        {
          "@type": "ListItem",
          "position": 6,
          "name": "Knowledge Hub (ಮಾಹಿತಿ ಕೋಶ)",
          "item": "https://sarva-dharma.github.io/srisaienterprises/#knowledge-hub"
        }
      ]
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-plan-sanction",
      "name": "Building Plan Sanctions & Approvals (BBMP / GBA / BDA)",
      "alternateName": "ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ ಮತ್ತು ಅನುಮೋದನೆ",
      "description": "End-to-end statutory building plan approval across Greater Bengaluru Authority (GBA), BBMP 8 zones, BDA, and BIAAPA with Nambike Nakshe fast-track provisional sanction under Sakala 14-21 days guarantee.",
      "category": "Municipal Approvals",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "35000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-predcr-cad",
      "name": "AutoDCR & PreDCR CAD Layer Scrutiny Drafting",
      "alternateName": "ಆಟೋಡಿಸಿಆರ್ ಮತ್ತು ಪ್ರಿಡಿಸಿಆರ್ ಸಿಎಡಿ ವಿನ್ಯಾಸ",
      "description": "Mathematically exact architectural drafting conforming to municipal PreDCR software layers (_RES_BLT, _SETBACK, _ROAD) guaranteeing zero automated rejections on bpas.bbmpgov.in.",
      "category": "CAD Engineering",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "22000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-ekhata",
      "name": "e-Khata Digital Registration & B-Khata to A-Khata Conversion",
      "alternateName": "ಇ-ಖಾತಾ ನೋಂದಣಿ & ಖಾತಾ ವರ್ಗಾವಣೆ",
      "description": "Official e-Aasthi digital e-Khata certificate issuance, Khata transfer, title verification, and B-Khata betterment payment facilitation across Bengaluru.",
      "category": "Property Titling",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "18000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-architectural-design",
      "name": "Architectural Working Drawings & 3D Elevation Modeling",
      "alternateName": "ವಾಸ್ತುಶಿಲ್ಪ ವಿನ್ಯಾಸ ಮತ್ತು 3D ಎಲಿವೇಶನ್",
      "description": "Council of Architecture registered custom floor plans, 3D exterior facade renders, Vastu Purusha Mandala alignment, and certified structural stability packages.",
      "category": "Architecture & Engineering",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "45000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-statutory-noc",
      "name": "Statutory Government NOC Procurement & Clearances",
      "alternateName": "ಸರ್ಕಾರಿ ಎನ್‌ಒಸಿ ಕ್ಲಿಯರೆನ್ಸ್ ಮತ್ತು ಅನುಮೋದನೆ",
      "description": "End-to-end statutory liaisoning for Karnataka Fire & Emergency NOC, AAI/HAL Airport Height clearance (NOCAS), BWSSB water line, and BESCOM electrical load sanction.",
      "category": "Liaisoning",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "30000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": ["Product", "Service"],
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#product-turnkey-construction",
      "name": "Turnkey Residential Construction & Structural Build",
      "alternateName": "ಕಟ್ಟಡ ನಿರ್ಮಾಣ ಮತ್ತು ವಾಸ್ತುಶಿಲ್ಪ ವಿನ್ಯಾಸ",
      "description": "Comprehensive residential and commercial turnkey construction packages (₹1,950 to ₹3,400/sq.ft) with quality testing, plinth-to-finish supervision, and OC clearance.",
      "category": "Architecture & Build",
      "brand": {
        "@type": "Brand",
        "name": "Sri Sai Enterprises"
      },
      "offers": {
        "@type": "Offer",
        "url": "https://sarva-dharma.github.io/srisaienterprises/#services",
        "price": "50000.00",
        "priceCurrency": "INR",
        "availability": "https://schema.org/InStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": "2027-12-31",
        "seller": {
          "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
        }
      }
    },
    {
      "@type": "FAQPage",
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Where is Sri Sai Enterprises located in Bengaluru?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sri Sai Enterprises is located at #3309, 1st Main Road, Gayathrinagar, Bangalore - 560021, directly opposite More Retail Store. Walk-in consultations are welcome for building plan sanctions, AutoDCR CAD drafting, and property e-Khata processing."
          }
        },
        {
          "@type": "Question",
          "name": "What are the office working hours and consultation timings?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "The studio is open Monday through Saturday from 9:30 AM to 7:30 PM (IST). The office is closed on Sundays. Online inquiries, WhatsApp assistance (+91 94480 54185), and Sakala client portal tracking are available 24/7."
          }
        },
        {
          "@type": "Question",
          "name": "How long does building plan sanction approval take in Bengaluru?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Under the Karnataka Sakala Guarantee, building plan sanctions take 14 to 21 business days for standard BBMP BPAS approvals. For eligible residential plots up to 50x80 ft under the Nambike Nakshe trust-and-verify self-certification scheme, provisional plan sanctions are issued within 3 to 7 business days."
          }
        },
        {
          "@type": "Question",
          "name": "What payment methods and currencies are accepted at Sri Sai Enterprises?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sri Sai Enterprises accepts Indian Rupee (INR) payments via UPI (Google Pay, PhonePe, Paytm), Net Banking / IMPS / NEFT, Credit and Debit Cards, Cheque, and Cash at the studio. Official tax invoices and government treasury challan receipts from BBMP BPAS are provided."
          }
        },
        {
          "@type": "Question",
          "name": "What architectural and municipal sanction services are provided by Sri Sai Enterprises?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sri Sai Enterprises provides end-to-end building plan approvals (BBMP BPAS, GBA, BDA, BIAAPA, STRR), PreDCR/AutoDCR CAD drafting, Commencement Certificate (CC) and Occupancy Certificate (OC) clearances, e-Khata registration and B-Khata to A-Khata betterment conversions, architectural 2D/3D design, cost estimation BOQs, and large-format architectural blueprints."
          }
        },
        {
          "@type": "Question",
          "name": "What are the credentials and experience of Sri Sai Enterprises?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Established in 1989, Sri Sai Enterprises has over 37 years of uninterrupted architectural and municipal liaisoning heritage in Bengaluru, having delivered 23,000+ approved sanctions. The firm is led by S. M. Thyagaraja (COA Reg. CA/2009/44120, BBMP Approved Supervisor Lic. BCC/BL-3.2.3/S-218/89-90)."
          }
        }
      ]
    },
    {
      "@type": "WebPage",
      "@id": "https://sarva-dharma.github.io/srisaienterprises/#webpage",
      "url": "https://sarva-dharma.github.io/srisaienterprises/",
      "name": "Sri Sai Enterprises | Building Plan Approvals & Architecture in Bengaluru Since 1989",
      "isPartOf": {
        "@id": "https://sarva-dharma.github.io/srisaienterprises/#website"
      },
      "about": {
        "@id": "https://sarva-dharma.github.io/srisaienterprises/#store"
      },
      "inLanguage": ["en-IN", "kn-IN"],
      "speakable": {
        "@type": "SpeakableSpecification",
        "cssSelector": [
          "#audience-navigator h2",
          "#services h2",
          "#about-founder h3",
          "#fee-estimator h2"
        ]
      }
    }
  ]
}
</script>
```

---

### 2. Generative Engine Optimization (GEO) & Semantic Discovery Framework

Generative Engine Optimization (GEO) shifts optimization from keyword stuffing to **entity disambiguation, semantic factual density, and direct quote extractability**. AI models (such as Perplexity, ChatGPT Search, Gemini, and Google SGE) prioritize sources that satisfy three core criteria:
1. **Explicit Identity Anchors**: The business has unambiguous entity metadata (`@id`, `founder`, registration numbers, geographic coordinates).
2. **Verified Facts with Numerical Precision**: Explicit turnaround days (14 to 21 days), sanction counts (23,000+), establishment year (1989), and exact base fees (INR 18,000 to INR 50,000).
3. **Structured Q&A Format**: Questions matching user intent phrased conversationally, paired with direct answers suitable for LLM citations.

#### A. Head Meta Tags: Open Graph, Twitter, Robots & Geo
The following tags must be inserted in the `<head>` of `index.html`:

```html
  <!-- Search Engine Robots Directives -->
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  <meta name="googlebot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
  <meta name="bingbot" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">

  <!-- Google Search Console Verification Placeholder -->
  <meta name="google-site-verification" content="GSC_VERIFICATION_TOKEN_PLACEHOLDER">

  <!-- Canonical URL Directive -->
  <link rel="canonical" href="https://sarva-dharma.github.io/srisaienterprises/">

  <!-- Open Graph & Social Sharing -->
  <meta property="og:title" content="Sri Sai Enterprises | ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್ - Since 1989">
  <meta property="og:description" content="Since 1989 (37+ years): Premier Building Plan Approvals, PreDCR CAD Drafting, Architecture, Estimations & Land Surveying across BBMP, GBA & BDA in Bengaluru.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://sarva-dharma.github.io/srisaienterprises/">
  <meta property="og:site_name" content="Sri Sai Enterprises | ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್">
  <meta property="og:locale" content="en_IN">
  <meta property="og:locale:alternate" content="kn_IN">
  <meta property="og:image" content="https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg">
  <meta property="og:image:secure_url" content="https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Sri Sai Enterprises Bengaluru Building Plan Approvals and Architecture Estd 1989">

  <!-- Twitter Card Directives -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Sri Sai Enterprises | Building Plan Approvals & Architecture Since 1989">
  <meta name="twitter:description" content="Bengaluru's trusted authority for BBMP BPAS sanctions, PreDCR CAD, Nambike Nakshe, and e-Khata since 1989. Led by S. M. Thyagaraja (COA Reg: CA/2009/44120).">
  <meta name="twitter:image" content="https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg">
  <meta name="twitter:image:alt" content="Sri Sai Enterprises Bengaluru Office & Architectural Practice">

  <!-- Local Geographic & ICBM Positioning Tags -->
  <meta name="geo.region" content="IN-KA">
  <meta name="geo.placename" content="Bengaluru">
  <meta name="geo.position" content="12.9965;77.5562">
  <meta name="ICBM" content="12.9965, 77.5562">
```

#### B. XML Sitemap Specification (`sitemap.xml`)
Implementers must generate `sitemap.xml` in the repository root (`c:\Users\grt68\Downloads\Hinde Baa\website\sitemap.xml`) with the following content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://sarva-dharma.github.io/srisaienterprises/</loc>
    <xhtml:link rel="alternate" hreflang="en-IN" href="https://sarva-dharma.github.io/srisaienterprises/" />
    <xhtml:link rel="alternate" hreflang="kn-IN" href="https://sarva-dharma.github.io/srisaienterprises/" />
    <xhtml:link rel="alternate" hreflang="x-default" href="https://sarva-dharma.github.io/srisaienterprises/" />
    <lastmod>2026-11-06</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

#### C. Robots.txt Specification (`robots.txt`)
Implementers must place `robots.txt` in the repository root (`c:\Users\grt68\Downloads\Hinde Baa\website\robots.txt`):

```txt
User-agent: *
Allow: /
Allow: /static/
Allow: /static/images/
Allow: /static/css/
Allow: /static/js/

# Crawl Delay
Crawl-delay: 1

# Sitemaps
Sitemap: https://sarva-dharma.github.io/srisaienterprises/sitemap.xml
```

---

## 5-Component Handoff Report

### 1. Observation
1. **Existing Head State**: Inspection of `index.html` lines 1 to 67 revealed:
   - `<title>` is bilingual: `Sri Sai Enterprises | ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್ - Since 1989 | Building Plan Approvals & Architecture in Bengaluru`.
   - `<meta name="description">` exists, mentioning 37+ years of experience and municipal approvals.
   - Minimal Open Graph tags exist (`og:title`, `og:description`, `og:type`, `og:url`).
   - **Crucial Deficiency**: There is **zero** Schema.org JSON-LD structured data anywhere in `index.html`.
   - Missing Open Graph image (`og:image`), dimensions (`og:image:width`, `og:image:height`), and bilingual locales (`og:locale: "en_IN"`, `og:locale:alternate: "kn_IN"`).
   - Missing all Twitter Card tags (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`).
   - Missing crawler directives (`<meta name="robots">`, `<meta name="googlebot">`), geo tags (`ICBM`), and Google Search Console verification token placeholder.
2. **Missing Discovery Files**: Testing repository root confirmed that neither `robots.txt` nor `sitemap.xml` exists on the active branch.
3. **Verified Entity Data**:
   - `README.md` lines 1-21 and `2.03/firm_details.csv` confirm:
     - Founder: S. M. Thyagaraja (Draftsman Civil)
     - COA Registration: `CA/2009/44120`
     - BBMP Approved Supervisor License: `BCC/BL-3.2.3/S-218/89-90`
     - Address: `#3309, 1st Main Road, Gayathrinagar, Bangalore - 560021` (Opp. More Retail Store)
     - Direct Mobile / WhatsApp: `+91 94480 54185`
     - Studio Landline: `080 233 255 09`
     - Email: `smthyagaraj@gmail.com`
     - Hours: Mon - Sat: 9:30 AM to 7:30 PM (Sundays closed)
     - Estd: 1989 (37+ years of continuous service; 23,000+ sanctions delivered)
   - `static/js/api.js` lines 6-108 and `2.03/firm_services.csv` lines 1-8 confirm 6 core catalog service packages with concrete INR pricing:
     1. Plan Sanctions & Approvals (Base fee: ₹35,000)
     2. AutoDCR & PreDCR CAD Drafting (Base fee: ₹22,000)
     3. e-Khata Services & Conversions (Base fee: ₹18,000)
     4. Architectural Design & Working Drawings (Base fee: ₹45,000)
     5. Statutory NOC Clearances & Liaisoning (Base fee: ₹30,000)
     6. Turnkey Residential Construction & Build (Base fee: ₹50,000)

### 2. Logic Chain
1. **Search & AI Discoverability**: Modern search indexing requires entity disambiguation. Without Schema.org JSON-LD, search engines and LLMs treat web pages as raw unstructured text, increasing hallucination rates and preventing rich snippet features (such as Knowledge Panels, Sitelinks Search Box, Breadcrumb trails, and Product pricing badges).
2. **Bilingual Preservation**: The application serves both Kannada and English speakers across Karnataka. Structuring the JSON-LD schema with `inLanguage: ["en-IN", "kn-IN"]`, `alternateName` containing Kannada brand strings, and `og:locale:alternate` guarantees that both English and Kannada search queries map directly to the same unified Knowledge Graph node.
3. **Generative Engine Optimization (GEO)**: AI search platforms (Perplexity, ChatGPT Search, Gemini, Google SGE) prioritize fast, definitive, authoritative answers. By providing an explicit `FAQPage` schema addressing the exact operational questions (location, hours, delivery timeline, payment modes, services, credentials), AI models can directly cite and quote Sri Sai Enterprises with zero ambiguity.
4. **Voice & Assistant Discoverability**: Including `SpeakableSpecification` pointing to major headings allows Google Assistant and screen readers to voice-extract the business summary.
5. **Technical Feasibility**: A unified `@graph` JSON-LD array encapsulates all 11 entities in a single script block, minimizing DOM overhead and eliminating multiple conflicting JSON-LD declarations.

### 3. Caveats
- **Google Search Console Token**: The token string in `<meta name="google-site-verification" content="...">` is a template placeholder. When the property owner connects their live Google account, the exact hash key must be substituted.
- **Images**: The Open Graph and Schema image URLs point to existing repository assets (`bbmp_tower_web.jpg`, `bbmp_official_logo.jpg`). These must remain publicly accessible under `static/images/` on GitHub Pages.
- **Single Page Application Hash Routing**: Because the storefront uses single-page hash navigation (`#services`, `#jurisdiction-checker`, `#fee-estimator`), the `potentialAction` SearchAction points to the query parameter `?q={search_term_string}#jurisdiction-checker`.

### 4. Conclusion
The provided specifications for Schema.org JSON-LD (11 graph entities), Open Graph tags, Twitter Cards, robots directives, local geo coordinates, `robots.txt`, and `sitemap.xml` represent a comprehensive, production-ready SEO/GEO upgrade for Sri Sai Enterprises. They conform strictly to Schema.org standards, preserve full bilingual Kannada and English integrity, and fulfill all requirements of R1 and R2 from `ORIGINAL_REQUEST.md`.

### 5. Verification Method
To independently verify the proposed schema and metadata:
1. **JSON Syntax & Structure Verification**:
   Execute the automated test script:
   ```powershell
   python .\.agents\teamwork\spec_miner_survey_2\validate_schema.py
   ```
   *Expected Result*: Output `SUCCESS: JSON-LD Schema is completely valid JSON.` and confirmation of all 11 graph entities.
2. **Schema.org Conformance Check**:
   Validate the JSON-LD snippet against the official [Schema.org Validator](https://validator.schema.org/) or [Google Rich Results Test](https://search.google.com/test/rich-results).
   *Verification criteria*:
   - Valid `LocalBusiness` / `Store` / `ProfessionalService` entity with no critical warnings.
   - Valid `WebSite` with `SearchAction`.
   - Valid `BreadcrumbList` with 6 items.
   - Valid `Product` / `Offer` entries with INR currency and valid price.
   - Valid `FAQPage` with 6 Questions and Answers.
   - Valid `SpeakableSpecification` css selectors.
3. **HTML Metadata Inspection**:
   Inspect the `<head>` block of `index.html` after implementation to verify that canonical, robots, OG, Twitter, and GSC placeholder tags are present and well-formed.
