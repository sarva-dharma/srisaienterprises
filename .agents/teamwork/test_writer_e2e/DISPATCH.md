## 2026-11-06T20:03:51Z
You are the E2E Test Writer (E2E Testing Track).
Working directory: c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\test_writer_e2e\
Parent orchestrator conversation ID: ada7118d-a98d-4e9f-80db-a5cad957aa08

Your task:
1. FIRST, read:
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\ORIGINAL_REQUEST.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\PROJECT.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\explorer_survey_1\handoff.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\spec_miner_survey_2\handoff.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\explorer_survey_3\handoff.md
2. Create c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\TEST_INFRA.md defining:
   - Test architecture and runner format
   - Feature inventory mapping to test tiers
   - The 4-tier methodology:
     * Tier 1: Feature Coverage (>=5 tests per feature: SEO tags, GSC meta tag, canonical, robots, OG tags, Twitter cards, JSON-LD schemas, bilingual text nodes)
     * Tier 2: Boundary & Corner Cases (malformed JSON-LD, empty queries, invalid schema types, missing attributes, edge URLs)
     * Tier 3: Cross-Feature Combinations (bilingual + schema, GSC verification + sitemap, robots + sitemap, GEO tags + Open Graph)
     * Tier 4: Real-World Application Scenarios (crawlers validating schema, AI agents extracting Q&A facts, user booking modal & portal preservation with zero regressions)
3. Implement the comprehensive, production-grade automated test suite in `c:\Users\grt68\Downloads\Hinde Baa\website\tests\`:
   - Create Python test runner and test modules (e.g. using `unittest` or `pytest`) that can be executed via a standard command (e.g. `python tests/run_tests.py` or `python -m unittest discover tests`).
   - The tests must rigorously inspect `index.html`, `robots.txt`, `sitemap.xml`, and `google-site-verification-template.html`.
   - The tests must validate JSON-LD syntax, schema.org types (`LocalBusiness`, `Store`, `ProfessionalService`, `WebSite`, `BreadcrumbList`, `Product`/`Offer`, `FAQPage`, `SpeakableSpecification`), INR prices, phone, email, address, geo coordinates, and bilingual text pairs.
   - The tests must verify that interactive DOM IDs (`booking-modal`, `jurisdiction-checker`, `fee-estimator`) and bilingual text remain intact.
4. Execute the test runner once to record initial baseline results (some tests will fail initially until implementation milestones complete, which is expected for TDD/Dual Track).
5. Publish c:\Users\grt68\Downloads\Hinde Baa\website\TEST_READY.md (and .agents\teamwork\TEST_READY.md) with runner command, tier breakdown, and test counts.
6. Write your handoff report to:
   c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\test_writer_e2e\handoff.md
7. Send a message to the orchestrator (ada7118d-a98d-4e9f-80db-a5cad957aa08) when TEST_READY.md is published.
Do NOT modify application code (index.html, static/js, etc.). You write test files and test metadata!
