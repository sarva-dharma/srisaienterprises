# Project: Sri Sai Enterprises Storefront SEO, GEO & Discovery Architecture

## Architecture
The Sri Sai Enterprises web platform is a high-performance, static-first, bilingual (Kannada & English) web application deployed via GitHub Pages (`https://sarva-dharma.github.io/srisaienterprises/`).
It represents Sri Sai Enterprises (ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್), Estd. 1989 (37+ Years of Heritage, 23,000+ Sanctions Delivered), Bengaluru's premier architectural and municipal building plan approvals consultancy led by S. M. Thyagaraja (COA Reg. CA/2009/44120, BBMP Approved Supervisor BCC/BL-3.2.3/S-218/89-90).

### Core Components:
1. **Storefront Presentation Layer (`index.html`)**:
   - Modern, responsive Tailwind CSS interface with custom signboard plaques, gold/red gradients, and dual-language co-presentation.
   - Comprehensive semantic `<head>` metadata, Open Graph tags, Twitter Cards, GEO positioning, and search console verification tags.
   - Unified Schema.org JSON-LD `@graph` embedding LocalBusiness, WebSite, Breadcrumbs, Product/Offers, FAQPage, and Speakable entities.
   - Accessible landmark structures (`<main id="main-content">`) and standardized heading levels.
   - Resilient, production-safe GA4 / GTM hook with environment guards.
2. **Search Engine & AI Discovery Assets (Root Directory)**:
   - `robots.txt`: Comprehensive crawling rules for traditional search engines and 16 Generative AI answer engines (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.).
   - `sitemap.xml`: XML sitemap with bilingual hreflang (`en`, `kn`, `x-default`) annotations.
   - `google-site-verification-template.html`: Dedicated file verification template for Google Search Console.
3. **Automated Verification & E2E Test Suite (`tests/`)**:
   - 5-Tier test suite covering Feature Coverage, Boundary Cases, Cross-Feature Combinations, Real-World Workload Scenarios, and Adversarial Oracle Stress Tests (108/108 passing).

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Head SEO Metadata | Title & meta description optimization (<160 chars, bilingual, high CTR) | M1 | Survey |
| 2 | Crawler Directives | Standard robots, googlebot, and bingbot meta directives | M1 | Survey |
| 3 | Canonical URL | Explicit `<link rel="canonical">` to production GitHub Pages origin | M1 | Survey |
| 4 | Open Graph Suite | Complete OG tags (title, description, type, url, site_name, locale, image, dimensions, alt) | M1 | Survey |
| 5 | Twitter Cards | Summary large image card tags (card, title, description, image, alt) | M1 | Survey |
| 6 | Local GEO Tags | Geographic positioning tags (geo.region, geo.placename, geo.position, ICBM) | M1 | Survey |
| 7 | Semantic HTML Polish | Wrap main content in `<main id="main-content">` and normalize roadmap headings | M1 | Survey |
| 8 | LocalBusiness Schema | Schema.org LocalBusiness/Store/ProfessionalService entity with credentials & geo | M1 | Survey |
| 9 | WebSite Schema | Schema.org WebSite entity with SearchAction deep-link template | M1 | Survey |
| 10 | BreadcrumbList Schema | Schema.org BreadcrumbList representing 6 architectural tiers | M1 | Survey |
| 11 | Product/Service Offers | 6 catalog offerings with INR pricing, condition, availability, seller | M1 | Survey |
| 12 | FAQPage Schema | 6 high-intent Q&A entities optimized for generative AI answer engines | M1 | Survey |
| 13 | Speakable Specification | Schema.org SpeakableSpecification targeting key semantic headings | M1 | Survey |
| 14 | GSC Meta Tag | `<meta name="google-site-verification" content="...">` hook in head | M1 | Survey |
| 15 | Offline-Safe Analytics | GA4 / GTM hook with environment guards preventing offline errors | M1 | Survey |
| 16 | GSC File Verification | Dedicated `google-site-verification-template.html` in root | M2 | Survey |
| 17 | Discovery robots.txt | Root `robots.txt` permitting search & 10+ AI crawlers with sitemap link | M2 | Survey |
| 18 | Discovery sitemap.xml | Root `sitemap.xml` with bilingual hreflang alternate links and lastmod | M2 | Survey |
| 19 | Bilingual Preservation | Strict preservation of Kannada & English co-located text and dictionaries | M1, M2, M3 | Survey |
| 20 | Zero-Regression Workflows | Zero console errors, intact modals, calculators, and client portal | M1, M2, M3 | Survey |

---

## Milestones
| # | Name | Scope | Dependencies | Status | Key Outputs |
|---|------|-------|-------------|--------|-------------|
| M1 | Storefront Semantic, Metadata & Schema.org Layer | `index.html` updates (Head metadata, Open Graph, Twitter Cards, Geo/ICBM, GSC Meta, GA4 safe hook, Semantic Main, Roadmap headings, Unified JSON-LD Graph) | None | DONE | `index.html` fully updated, verified by workers & reviewers |
| M2 | Search Engine Discovery & External Services | `robots.txt`, `sitemap.xml`, `google-site-verification-template.html` | None | DONE | `robots.txt`, `sitemap.xml`, `google-site-verification-template.html` created and validated |
| M3 | Final Milestone: Dual-Track E2E Acceptance & Adversarial Hardening | Pass 100% E2E test suite (Tiers 1-4) & adversarial coverage hardening (Tier 5) | M1, M2, E2E Test Suite | DONE | 108/108 tests passing, gate PASSED, Forensic Audit CLEAN |

---

## Interface Contracts

### 1. `index.html` Head Metadata ↔ External Crawlers
- Meta tags must follow standard W3C and Open Graph protocol specifications.
- `google-site-verification` must use attribute `content="GSC_VERIFICATION_TOKEN_PLACEHOLDER"`.
- Canonical must point to `https://sarva-dharma.github.io/srisaienterprises/`.
- All social image URLs must be absolute HTTPS paths to existing assets in `static/images/`.

### 2. `index.html` Structured Data ↔ Schema.org Parsers & Search Engines
- Script tag: `<script type="application/ld+json">`.
- Root structure: Valid JSON containing `@context: "https://schema.org"` and `@graph: [...]`.
- Entities must cross-reference via `@id` (`#store`, `#founder`, `#website`, etc.).
- Prices must be string-formatted numbers (e.g. `"35000.00"`) with `priceCurrency: "INR"`.

### 3. Root Discovery Files ↔ Search Crawlers
- `robots.txt` must declare `Sitemap: https://sarva-dharma.github.io/srisaienterprises/sitemap.xml`.
- `sitemap.xml` must declare XML version 1.0, UTF-8 encoding, and schema namespaces for sitemaps.org 0.9 and XHTML.

### 4. Interactive Workflows & Bilingual State Preservation
- Existing DOM element IDs (`booking-modal`, `lead-name`, `lead-phone`, `lead-service`, `jurisdiction-checker`, `fee-estimator`) must remain unaltered.
- Simultaneous English and Kannada text strings must remain present in both DOM nodes and `static/js/main.js`.

---

## Code Layout & Write Boundaries
- **Milestone M1 Exclusive Owner**: `c:\Users\grt68\Downloads\Hinde Baa\website\index.html`
- **Milestone M2 Exclusive Owner**:
  - `c:\Users\grt68\Downloads\Hinde Baa\website\robots.txt`
  - `c:\Users\grt68\Downloads\Hinde Baa\website\sitemap.xml`
  - `c:\Users\grt68\Downloads\Hinde Baa\website\google-site-verification-template.html`
- **E2E Testing Track Exclusive Owner**: `c:\Users\grt68\Downloads\Hinde Baa\website\tests\`
- **Project Orchestrator & Agent Metadata**: `c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\`
