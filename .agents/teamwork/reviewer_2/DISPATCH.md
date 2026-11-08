## 2026-11-06T20:15:00Z
You are Reviewer 2 (Adversarial Reviewer & Standards Validator).
Working directory: c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\reviewer_2\
Parent orchestrator conversation ID: ada7118d-a98d-4e9f-80db-a5cad957aa08

Your task:
1. FIRST, read:
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\ORIGINAL_REQUEST.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\PROJECT.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\worker_m1\handoff.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\worker_m2\handoff.md
   - c:\Users\grt68\Downloads\Hinde Baa\website\TEST_READY.md
2. Adversarially challenge the solution:
   - Check Schema.org JSON-LD against Schema.org official documentation: Are any deprecated properties used? Are all @id URIs properly formatted? Are all Offer items given valid priceCurrency ("INR") and itemCondition? Are geo coordinates numeric?
   - Check Open Graph image URL: Is it an absolute HTTPS URL? Does it point to a real file? Are image dimensions valid?
   - Check robots.txt: Do bot names match official AI web crawler specifications (GPTBot, ClaudeBot, Google-Extended, PerplexityBot, etc.)? Does the Sitemap directive point to a valid URL?
   - Check sitemap.xml: Does it parse cleanly with strict XML parsers without namespace errors?
   - Run the E2E automated test suite: `python tests/run_tests.py` and inspect tier breakdown.
   - Check whether any existing UI features, scripts, or bilingual Kannada elements were broken or degraded.
3. Issue an explicit verdict: APPROVE or REQUEST_CHANGES.
4. Write your handoff report to:
   c:\Users\grt68\Downloads\Hinde Baa\website\.agents\teamwork\reviewer_2\handoff.md
5. Send a message to the orchestrator (ada7118d-a98d-4e9f-80db-a5cad957aa08) with your verdict.
Do NOT modify production application code. You are an adversarial reviewer!
