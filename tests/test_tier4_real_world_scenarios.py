"""
Tier 4: Real-World Application Scenarios Test Suite.
Simulates real-world crawler, AI agent, and end-user interactive workflows:
- Scenario 1: Search engine bot crawl pipeline (robots.txt -> sitemap.xml -> index.html rich snippets)
- Scenario 2: AI Search Agent (Perplexity/ChatGPT/Gemini) entity & fact extraction
- Scenario 3: FAQ Q&A factual answer extraction for generative answer engines
- Scenario 4: User Consultation Booking Modal & Lead Capture DOM ID preservation
- Scenario 5: Interactive Jurisdiction Checker, Fee Calculator & Sakala Client Portal preservation
- Scenario 6: Semantic HTML Landmark & Heading hierarchy accessibility
- Scenario 7: Production-Safe Analytics Guard (offline file:// and placeholder protection)
"""

import re
import unittest
from tests.helpers import (
    file_exists,
    find_entities_by_type,
    find_entity_by_type,
    get_schema_graph,
    load_file,
    parse_html,
    parse_json_ld,
    parse_robots_txt,
    parse_sitemap_xml,
)


class TestTier4RealWorldScenarios(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.soup = parse_html("index.html")
        cls.head = cls.soup.find("head")
        cls.json_ld = parse_json_ld(cls.soup)
        cls.graph = get_schema_graph(cls.soup)

    # =========================================================================
    # Scenario 1: Search Engine Crawler End-to-End Discovery Pipeline
    # =========================================================================

    def test_scenario_search_engine_crawler_discovery_pipeline(self):
        """4.1 Scenario: Crawler reads robots.txt, discovers sitemap.xml, fetches index.html, verifies canonical and schema."""
        # Step 1: Crawler requests /robots.txt
        self.assertTrue(file_exists("robots.txt"), "Crawler 404: robots.txt not found in root")
        robots = parse_robots_txt("robots.txt")
        self.assertTrue(len(robots["sitemaps"]) > 0, "Crawler finding: No Sitemap directive in robots.txt")

        # Step 2: Crawler follows sitemap link
        sitemap_url = robots["sitemaps"][0]
        self.assertTrue(sitemap_url.endswith("/sitemap.xml"))
        self.assertTrue(file_exists("sitemap.xml"), "Crawler 404: sitemap.xml not found")

        # Step 3: Crawler parses sitemap URLs
        entries = parse_sitemap_xml("sitemap.xml")
        locs = [e["loc"] for e in entries]
        self.assertIn("https://sarva-dharma.github.io/srisaienterprises/", locs)

        # Step 4: Crawler downloads index.html and checks canonical
        canonical = self.head.find("link", attrs={"rel": "canonical"})
        self.assertIsNotNone(canonical, "Crawler finding: Missing canonical link")
        self.assertEqual(canonical.get("href"), "https://sarva-dharma.github.io/srisaienterprises/")

        # Step 5: Crawler extracts Schema.org rich snippets
        self.assertIsNotNone(self.json_ld, "Crawler finding: No structured data found for Rich Results")
        self.assertTrue(len(self.graph) >= 5, "Crawler finding: Insufficient schema entities in @graph")

    # =========================================================================
    # Scenario 2: AI Search Agent Factual Extraction
    # =========================================================================

    def test_scenario_ai_agent_factual_extraction(self):
        """4.2 Scenario: Generative AI Agent queries identity, address, contact, and founder licenses from schema."""
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb, "AI Agent: Cannot identify business entity")

        # Query: "What is the contact phone and email for Sri Sai Enterprises?"
        phone = lb.get("telephone", "")
        email = lb.get("email", "")
        self.assertIn("9448054185", phone.replace("-", "").replace(" ", ""))
        self.assertEqual(email, "smthyagaraj@gmail.com")

        # Query: "Where is Sri Sai Enterprises studio located?"
        address = lb.get("address", {})
        street = address.get("streetAddress", "")
        self.assertIn("Gayathrinagar", street)
        self.assertEqual(address.get("postalCode"), "560021")

        # Query: "Who leads the firm and what are their statutory registration licenses?"
        founder = lb.get("founder", {})
        self.assertEqual(founder.get("name"), "S. M. Thyagaraja")
        credentials = founder.get("hasCredential", [])
        cred_map = {c.get("identifier"): c.get("name") for c in credentials}
        self.assertIn("CA/2009/44120", cred_map)
        self.assertIn("BCC/BL-3.2.3/S-218/89-90", cred_map)

        # Query: "What is the heritage and sanction count?"
        desc = lb.get("description", "")
        self.assertIn("1989", desc)
        self.assertTrue("23,000" in desc or "23000" in desc)

    # =========================================================================
    # Scenario 3: Generative Answer Engine FAQ Q&A Retrieval
    # =========================================================================

    def test_scenario_generative_qa_faq_extraction(self):
        """4.3 Scenario: AI conversational model retrieves precise answers to common customer intents from FAQPage."""
        faq = find_entity_by_type(self.graph, "FAQPage")
        self.assertIsNotNone(faq, "FAQPage missing in schema")

        qa_dict = {}
        for q in faq.get("mainEntity", []):
            q_name = q.get("name", "").lower()
            ans_text = q.get("acceptedAnswer", {}).get("text", "")
            qa_dict[q_name] = ans_text

        # Intent 1: Location & landmarks
        loc_answers = [ans for q, ans in qa_dict.items() if "located" in q or "where" in q]
        self.assertTrue(len(loc_answers) > 0, "No FAQ question answering location")
        self.assertIn("More Retail Store", loc_answers[0])

        # Intent 2: Hours & Sunday availability
        hours_answers = [ans for q, ans in qa_dict.items() if "hours" in q or "timings" in q]
        self.assertTrue(len(hours_answers) > 0, "No FAQ question answering working hours")
        self.assertIn("closed on sundays", hours_answers[0].lower())

        # Intent 3: Approval timeline (Sakala SLA)
        timeline_answers = [ans for q, ans in qa_dict.items() if "long" in q or "timeline" in q or "take" in q]
        self.assertTrue(len(timeline_answers) > 0, "No FAQ question answering approval turnaround")
        self.assertTrue("14 to 21" in timeline_answers[0] or "14-21" in timeline_answers[0])

        # Intent 4: Payment methods
        payment_answers = [ans for q, ans in qa_dict.items() if "payment" in q or "currencies" in q]
        self.assertTrue(len(payment_answers) > 0, "No FAQ question answering payment methods")
        self.assertTrue("upi" in payment_answers[0].lower() or "challan" in payment_answers[0].lower())

    # =========================================================================
    # Scenario 4: User Consultation Booking Modal Preservation
    # =========================================================================

    def test_scenario_booking_modal_and_lead_form_preservation(self):
        """4.4 Scenario: End-user opens booking modal; verifies modal ID and all lead form input fields remain intact."""
        modal = self.soup.find(id="booking-modal")
        self.assertIsNotNone(modal, "CRITICAL REGRESSION: #booking-modal DOM element missing")

        form = self.soup.find(id="consultation-booking-form")
        self.assertIsNotNone(form, "CRITICAL REGRESSION: #consultation-booking-form missing")

        required_input_ids = [
            "lead-name",
            "lead-phone",
            "lead-email",
            "lead-location",
            "lead-dimensions",
            "lead-service",
            "lead-message",
        ]
        for inp_id in required_input_ids:
            field = self.soup.find(id=inp_id)
            self.assertIsNotNone(field, f"CRITICAL REGRESSION: Lead form input #{inp_id} missing in DOM")

    # =========================================================================
    # Scenario 5: Interactive Calculators & Sakala File Tracker Preservation
    # =========================================================================

    def test_scenario_interactive_calculators_and_portal_preservation(self):
        """4.5 Scenario: End-user accesses Jurisdiction Checker, Scrutiny Calculator, and Sakala Tracker."""
        # Jurisdiction Checker
        jur_form = self.soup.find(id="jurisdiction-form")
        self.assertIsNotNone(jur_form, "CRITICAL REGRESSION: #jurisdiction-form missing")
        jur_select = self.soup.find(id="jurisdiction-select")
        self.assertIsNotNone(jur_select, "CRITICAL REGRESSION: #jurisdiction-select missing")

        # Fee Estimator & Inputs
        fee_est = self.soup.find(id="fee-estimator")
        self.assertIsNotNone(fee_est, "CRITICAL REGRESSION: #fee-estimator missing")
        calc_inputs = ["calc-width", "calc-length", "calc-floors", "calc-b-khata", "calc-locality"]
        for inp_id in calc_inputs:
            field = self.soup.find(id=inp_id)
            self.assertIsNotNone(field, f"CRITICAL REGRESSION: Fee calculator input #{inp_id} missing")

        # Client Portal Container
        portal_container = self.soup.find(id="portal-live-container")
        self.assertIsNotNone(portal_container, "CRITICAL REGRESSION: #portal-live-container missing")

    # =========================================================================
    # Scenario 6: Semantic HTML Landmark & Heading Structure
    # =========================================================================

    def test_scenario_semantic_main_landmark_and_headings(self):
        """4.6 Scenario: Screen readers and SEO parsers navigate via semantic <main id='main-content'>."""
        main_tag = self.soup.find("main", id="main-content")
        self.assertIsNotNone(main_tag, "Semantic landmark <main id='main-content'> missing")

        # Verify main contains primary sections
        sections = main_tag.find_all("section")
        self.assertTrue(len(sections) >= 3, "Semantic <main> must encapsulate primary page sections")

    # =========================================================================
    # Scenario 7: Production-Safe Analytics Script Guard
    # =========================================================================

    def test_scenario_analytics_guard_against_offline_and_placeholders(self):
        """4.7 Scenario: Opening site via file:// or with default placeholder ID safely suppresses remote hits."""
        html_content = load_file("index.html")

        # Look for GA4 / GTM snippet
        if "gtag" in html_content or "googletagmanager" in html_content:
            # Must contain file protocol check
            has_file_guard = "location.protocol === 'file:'" in html_content or "isFileProtocol" in html_content
            self.assertTrue(has_file_guard, "Analytics script missing offline file: protocol safety guard")

            # Must contain placeholder guard
            has_placeholder_guard = "G-XXXXXXXXXX" in html_content and (
                "isPlaceholder" in html_content or "!GA_MEASUREMENT_ID" in html_content
            )
            self.assertTrue(
                has_placeholder_guard,
                "Analytics script missing placeholder G-XXXXXXXXXX check preventing unconfigured network hits",
            )


if __name__ == "__main__":
    unittest.main()
