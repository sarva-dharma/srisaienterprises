## 2026-11-06T20:04:41Z
You are Worker M1 (Storefront Semantic, Metadata & Schema.org Worker).
Working directory: c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\worker_m1\
Parent orchestrator conversation ID: ada7118d-a98d-4e9f-80db-a5cad957aa08

EXCLUSIVE WRITE OWNERSHIP:
You exclusively own and modify: c:\Users\grt68\Downloads\Hinde Baa\website\index.html.
DO NOT modify any other application files (do not touch robots.txt, sitemap.xml, or files under static/).

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your task:
1. FIRST, read:
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\ORIGINAL_REQUEST.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\PROJECT.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\spec_miner_survey_2\handoff.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\explorer_survey_1\handoff.md
2. Implement Milestone 1 in c:\Users\grt68\Downloads\Hinde Baa\website\index.html:
   a. Head SEO, GEO & Social Metadata:
      - Title & Description optimization (keep bilingual, crisp, under 160 chars for description).
      - Robots directives (<meta name="robots">, <meta name="googlebot">, <meta name="bingbot">).
      - Canonical tag (<link rel="canonical" href="https://sarva-dharma.github.io/srisaienterprises/">).
      - Google Search Console verification meta tag: <meta name="google-site-verification" content="GSC_VERIFICATION_TOKEN_PLACEHOLDER">.
      - Full Open Graph suite (og:title, og:description, og:type, og:url, og:site_name, og:locale "en_IN", og:locale:alternate "kn_IN", og:image "https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg", og:image:width, og:image:height, og:image:alt).
      - Full Twitter Cards suite (twitter:card "summary_large_image", twitter:title, twitter:description, twitter:image, twitter:image:alt).
      - Local Geographic & ICBM Positioning tags (geo.region "IN-KA", geo.placename "Bengaluru", geo.position "12.9965;77.5562", ICBM "12.9965, 77.5562").
      - Production-safe Google Analytics 4 (GA4) / GTM hook with offline/file: protocol and placeholder guards (see spec in explorer_survey_3/handoff.md or spec_miner_survey_2/handoff.md).
   b. Schema.org JSON-LD Structured Data:
      - Inject the unified @graph JSON-LD script (exactly specified in spec_miner_survey_2/handoff.md):
        * LocalBusiness / Store / ProfessionalService entity (#3309 Gayathrinagar, geo coordinates, opening hours, currencies accepted INR, payment methods, phone +91 94480 54185, founder S.M. Thyagaraja credentials COA CA/2009/44120, BBMP Supervisor BCC/BL-3.2.3/S-218/89-90).
        * WebSite entity with SearchAction.
        * BreadcrumbList entity with 6 tiers.
        * 6 Product / Service offerings with INR prices, InStock, NewCondition, seller backlink.
        * FAQPage with 6 operational store Q&As for Generative AI engine discovery.
        * WebPage entity with SpeakableSpecification pointing to key headings.
   c. Semantic HTML & Accessible Structure Polish:
      - Wrap the primary sections in <main id="main-content"> (placing it after the header and closing before the footer).
      - Normalize any heading hierarchy skips (e.g. in #construction-roadmap).
   d. Strict Preservation:
      - Preserve ALL existing English and Kannada co-located text strings, typography classes (font-kannada, signboard-kannada), modal triggers (openBookingModal, booking-modal), form element IDs (lead-name, lead-phone, lead-service, etc.), fee calculator IDs, and client portal tracking.
3. Verification:
   - Parse index.html to ensure JSON-LD script is valid JSON and extractable.
   - Run python validation script to check schema syntax.
   - Document commands executed and test outputs in your handoff report.
4. Output: Write your completion report to:
   c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\worker_m1\handoff.md
5. When finished, send a message to the orchestrator (ada7118d-a98d-4e9f-80db-a5cad957aa08).
