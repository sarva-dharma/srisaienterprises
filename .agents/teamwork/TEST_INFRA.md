# Sri Sai Enterprises Automated Test Infrastructure Specification (`TEST_INFRA.md`)

## 1. Overview & Architecture
This document defines the automated verification and End-to-End (E2E) testing infrastructure for the Sri Sai Enterprises web platform (`https://sarva-dharma.github.io/srisaienterprises/`).
The test infrastructure establishes a production-grade, reproducible Python verification suite located in `tests/` that executes in standard Python 3 environments without brittle third-party network services.

### Test Runner Execution
The test suite supports dual execution formats:
1. **Dedicated Test Runner with Tiered Diagnostics**:
   ```bash
   python tests/run_tests.py
   ```
   Provides categorized terminal reporting across Tiers 1 through 4, individual test status, pass/fail counts, and comprehensive failure root-cause analysis.
2. **Standard Library Discovery Format**:
   ```bash
   python -m unittest discover tests -p "test_*.py"
   ```
   Enables automated CI/CD integration with standard test runners.

---

## 2. Feature Inventory Mapping to Test Tiers

The 20 platform features defined in `PROJECT.md` map to the 4 test tiers as follows:

| Feature # | Feature Name | Description | Test Tier | Primary Test Module |
|---|---|---|---|---|
| F1 | Head SEO Metadata | Title, description, keywords, viewport, charset, lang | Tier 1 | `test_tier1_feature_coverage.py` |
| F2 | Crawler Directives | robots, googlebot, bingbot indexing directives | Tier 1 | `test_tier1_feature_coverage.py` |
| F3 | Canonical URL | `<link rel="canonical">` to production origin | Tier 1 | `test_tier1_feature_coverage.py` |
| F4 | Open Graph Suite | Complete OG tags (title, desc, type, url, site_name, locale, image) | Tier 1 | `test_tier1_feature_coverage.py` |
| F5 | Twitter Cards | Summary large image card tags (card, title, desc, image, alt) | Tier 1 | `test_tier1_feature_coverage.py` |
| F6 | Local GEO Tags | Geographic positioning (geo.region, geo.placename, geo.position, ICBM) | Tier 1 | `test_tier1_feature_coverage.py` |
| F7 | Semantic HTML Polish | Landmark `<main id="main-content">` and roadmap headings | Tier 1, 4 | `test_tier1_feature_coverage.py` |
| F8 | LocalBusiness Schema | Schema.org LocalBusiness/Store/ProfessionalService entity | Tier 1, 2, 4 | `test_tier1_feature_coverage.py` |
| F9 | WebSite Schema | Schema.org WebSite entity with SearchAction deep-link | Tier 1, 2 | `test_tier1_feature_coverage.py` |
| F10 | BreadcrumbList Schema | Schema.org BreadcrumbList representing 6 architectural tiers | Tier 1, 2 | `test_tier1_feature_coverage.py` |
| F11 | Product/Service Offers | 6 catalog offerings with INR pricing, condition, availability | Tier 1, 2 | `test_tier1_feature_coverage.py` |
| F12 | FAQPage Schema | 6 high-intent Q&A entities for AI answer engines | Tier 1, 4 | `test_tier1_feature_coverage.py` |
| F13 | Speakable Specification | SpeakableSpecification targeting semantic headings | Tier 1, 2 | `test_tier1_feature_coverage.py` |
| F14 | GSC Meta Tag | `<meta name="google-site-verification">` hook in head | Tier 1 | `test_tier1_feature_coverage.py` |
| F15 | Offline-Safe Analytics | GA4 / GTM hook with environment guards preventing offline errors | Tier 4 | `test_tier4_real_world_scenarios.py` |
| F16 | GSC File Verification | Dedicated `google-site-verification-template.html` in root | Tier 1, 3 | `test_tier1_feature_coverage.py` |
| F17 | Discovery robots.txt | Root `robots.txt` permitting search & 10+ AI crawlers with sitemap | Tier 1, 3 | `test_tier1_feature_coverage.py` |
| F18 | Discovery sitemap.xml | Root `sitemap.xml` with bilingual hreflang alternates and lastmod | Tier 1, 3 | `test_tier1_feature_coverage.py` |
| F19 | Bilingual Preservation | Strict preservation of Kannada & English co-located text | Tier 1, 3, 4 | `test_tier1_feature_coverage.py` |
| F20 | Zero-Regression Workflows | Intact modals (`booking-modal`), calculators, and client portal | Tier 4 | `test_tier4_real_world_scenarios.py` |

---

## 3. Four-Tier Testing Methodology

### Tier 1: Feature Coverage (>=5 Tests per Feature)
Ensures every core feature is implemented according to specifications with at least 5 independent, behavior-oriented unit tests per feature:
1. **SEO Tags (>=5 tests)**:
   - `<title>` presence and non-empty content
   - `<title>` bilingual branding (Kannada and English)
   - `<meta name="description">` presence and length constraint (<=160 chars)
   - `<meta name="keywords">` presence with relevant municipal & architectural terms
   - Standard HTML `<html lang="en">`, `<meta charset="UTF-8">`, and viewport tags
2. **GSC Verification Tag (>=5 tests)**:
   - `<meta name="google-site-verification">` exists in `<head>`
   - `content` attribute contains the specified verification token placeholder
   - Bing Webmaster verification `<meta name="msvalidate.01">` exists
   - Dedicated verification file `google-site-verification-template.html` exists in root
   - Verification file content follows Google verification format (`google-site-verification: ...`)
3. **Canonical URL (>=5 tests)**:
   - `<link rel="canonical">` element exists in `<head>`
   - Canonical `href` points strictly to HTTPS origin
   - Canonical URL points to `https://sarva-dharma.github.io/srisaienterprises/`
   - Canonical URL has trailing slash consistency
   - Exactly one singular canonical tag is declared
4. **Robots Directives (>=5 tests)**:
   - `<meta name="robots">` exists in `<head>`
   - `robots` directive includes `index` and `follow`
   - `robots` directive includes `max-image-preview:large`
   - `googlebot` directive exists with `max-snippet:-1`
   - `bingbot` directive exists with `max-image-preview:large`
5. **Open Graph Tags (>=5 tests)**:
   - `og:title` present and contains brand name
   - `og:description` present and non-empty
   - `og:type` set to `website`
   - `og:url` matches canonical HTTPS URL
   - `og:image` is an absolute HTTPS URL pointing to an existing image asset
   - `og:locale` (`en_IN`) and `og:locale:alternate` (`kn_IN`) present
   - `og:site_name`, `og:image:width`, `og:image:height`, and `og:image:alt` present
6. **Twitter Cards (>=5 tests)**:
   - `twitter:card` set to `summary_large_image`
   - `twitter:title` present and concise
   - `twitter:description` present and highlights key services
   - `twitter:image` is an absolute HTTPS URL
   - `twitter:image:alt` provides descriptive alternative text
7. **JSON-LD Schema Graph Entities (>=5 tests)**:
   - Script tag `<script type="application/ld+json">` present and parses as valid JSON
   - Root structure declares `@context: "https://schema.org"` and `@graph` array
   - `LocalBusiness`/`Store`/`ProfessionalService` entity present with contact, address, founder, credentials
   - `WebSite` entity present with valid `SearchAction`
   - `BreadcrumbList` present with 6 structured hierarchy items
   - `Product`/`Service` offers present (6 catalog items with valid INR pricing)
   - `FAQPage` present with 6 high-intent Q&A entities
   - `SpeakableSpecification` present with target CSS selectors
8. **Bilingual Text Nodes (>=5 tests)**:
   - Top banner contains bilingual text (`ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ`)
   - Brand header contains both English and Kannada typography
   - Navigation links display English with Kannada parentheticals
   - Hero headline includes Kannada title (`ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ`)
   - CTA buttons contain bilingual text (`ಉಚಿತ ಸಮಾಲೋಚನೆ`, `ನಕ್ಷೆ ಸ್ಥಿತಿ ತಿಳಿಯಿರಿ`)
   - Founder statement co-presents Kannada translation

### Tier 2: Boundary & Corner Cases
Tests system resilience against malformed, edge-case, and boundary conditions:
- **Malformed JSON-LD Syntax**: Verifies tests reject unclosed strings, trailing commas, or invalid JSON syntax.
- **Missing Required Schema Properties**: Verifies that missing required fields (e.g. missing `priceCurrency`, `telephone`, `addressCountry`) trigger test failures.
- **Invalid Schema Types**: Verifies `@type` values strictly adhere to official Schema.org vocabularies.
- **SearchAction Query String Edge Cases**: Validates query template encoding with special characters and spaces (`?q={search_term_string}#jurisdiction-checker`).
- **Currency & Pricing Formatting**: Validates that all prices are positive numbers formatted as strings with two decimals (`35000.00`) and currency is strictly `"INR"`.
- **Geographic Coordinate Bounds**: Validates latitude (12.9965 ∈ [-90, 90]) and longitude (77.5562 ∈ [-180, 180]) matching Gayathrinagar, Bengaluru.
- **OpeningHours Time Boundaries**: Validates time string format (`09:30` to `19:30`) and day enum strings (`Monday` through `Saturday`).
- **Breadcrumb Hierarchy Integrity**: Validates `position` values are strictly sequential (1, 2, 3, 4, 5, 6) with no gaps or duplicates.
- **Speakable CSS Selectors**: Validates all CSS selectors declared in `SpeakableSpecification` correspond to real, identifiable DOM elements in `index.html`.

### Tier 3: Cross-Feature Combinations
Tests the interaction and contract alignment across multiple distinct components:
- **Bilingual & Schema Synchronization**: Validates that `alternateName` strings in JSON-LD exactly match Kannada text in the DOM.
- **Google Search Console Verification & Sitemap Alignment**: Validates that the domain verified in GSC matches the `<loc>` domain in `sitemap.xml`.
- **Robots.txt & Sitemap Synchronization**: Validates that `robots.txt` declares the exact URL of `sitemap.xml`, and that the referenced sitemap exists and is valid.
- **GEO Tags & Open Graph Alignment**: Validates that `geo.region` (`IN-KA`) and `geo.placename` (`Bengaluru`) correlate with `og:locale` (`en_IN`, `kn_IN`).
- **Canonical URL & Social Sharing Alignment**: Validates that `canonical href`, `og:url`, `WebSite.url`, and `LocalBusiness.url` point to the identical canonical origin.
- **Robots Permissions & AI Discovery Bots**: Validates that `robots.txt` explicitly allows 10+ AI search engines (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) without conflicting disallow rules on assets.
- **Sitemap Hreflang & DOM Meta Alternates**: Validates that `<xhtml:link>` tags in `sitemap.xml` match `<link rel="alternate">` in `index.html`.

### Tier 4: Real-World Application Scenarios
Simulates realistic production workloads, bot crawlers, and user interactions:
- **Search Engine Crawler Simulation**: Simulates Googlebot fetching `robots.txt`, finding `sitemap.xml`, extracting `index.html`, verifying canonical status, and indexing rich snippets.
- **Generative AI Fact Extraction**: Simulates an AI search agent (Perplexity/ChatGPT/Gemini) querying Sri Sai Enterprises for contact phone (`+91-9448054185`), address, license numbers (`CA/2009/44120`, `BCC/BL-3.2.3/S-218/89-90`), and service turnaround (14-21 days Sakala SLA).
- **FAQ Knowledge Extraction**: Simulates LLM factual retrieval from `FAQPage` schema (location, hours, sanction timeline, payment methods, services, experience).
- **Interactive Consultation Booking Modal**: Validates that `#booking-modal` and its form inputs (`lead-name`, `lead-phone`, `lead-email`, `lead-location`, `lead-dimensions`, `lead-service`, `lead-message`) remain present with identical IDs.
- **Interactive Jurisdiction & Fee Calculators**: Validates that `#jurisdiction-form`, `#jurisdiction-select`, `#calc-width`, `#calc-length`, `#calc-floors`, `#calc-b-khata`, `#calc-locality` remain intact.
- **Client Portal Application Tracking**: Validates that `#portal-live-container` and tracking reference input remain present.
- **Production-Safe Analytics Integration**: Validates that the GA4 integration script includes an environment guard that safely suppresses tracking on local `file:///` protocols or unconfigured placeholder IDs.

---

## 4. Test File Layout

```
tests/
├── __init__.py
├── helpers.py                          # Parser helpers, schema loaders, XML/Robots tools
├── test_tier1_feature_coverage.py      # Tier 1 tests (Feature coverage, >=5 per feature)
├── test_tier2_boundary_corner.py       # Tier 2 tests (Boundary conditions, error resistance)
├── test_tier3_cross_feature.py         # Tier 3 tests (Cross-component integration & sync)
├── test_tier4_real_world_scenarios.py  # Tier 4 tests (Real-world bots, AI agents & UI preservation)
└── run_tests.py                        # Master CLI test runner & diagnostics reporter
```

---

## 5. Verification Commands

Run the full automated test suite:
```bash
python tests/run_tests.py
```

Run via standard unittest runner:
```bash
python -m unittest discover tests -p "test_*.py" -v
```
