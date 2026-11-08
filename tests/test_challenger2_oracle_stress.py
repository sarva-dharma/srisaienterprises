"""
Challenger 2: Generative Engine Optimization (GEO), AI Knowledge Extraction Oracle,
Bilingual Unicode Stress Test, GSC Verification Audit & GA4 Offline Resilience Suite.
"""

import json
import os
import re
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup
from tests.helpers import (
    file_exists,
    find_entities_by_type,
    find_entity_by_type,
    get_json_ld_blocks,
    get_project_root,
    get_schema_graph,
    load_file,
    parse_html,
    parse_json_ld,
)


class AIKnowledgeExtractionOracle:
    """
    Simulates a Perplexity / ChatGPT Search retrieval agent querying the
    JSON-LD structured knowledge graph and FAQPage.
    """

    def __init__(self, soup: BeautifulSoup):
        self.soup = soup
        self.json_ld = parse_json_ld(soup)
        self.graph = get_schema_graph(soup)
        self.faq_entity = find_entity_by_type(self.graph, "FAQPage")
        self.business_entity = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.founder_entity = (self.business_entity or {}).get("founder", {})

        # Build intent query index
        self.faq_items = []
        if self.faq_entity:
            for item in self.faq_entity.get("mainEntity", []):
                q = item.get("name", "")
                a = item.get("acceptedAnswer", {}).get("text", "")
                self.faq_items.append({"question": q, "answer": a})

    def query(self, intent_keywords: list[str]) -> str | None:
        """Find the best FAQ answer matching all or most keywords in intent_keywords."""
        scored = []
        for item in self.faq_items:
            q_lower = item["question"].lower()
            a_lower = item["answer"].lower()
            score = sum(1 for kw in intent_keywords if kw.lower() in q_lower or kw.lower() in a_lower)
            if score > 0:
                scored.append((score, item["answer"]))
        if not scored:
            return None
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]


class TestChallenger2OracleStress(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = get_project_root()
        cls.index_path = cls.root / "index.html"
        cls.sitemap_path = cls.root / "sitemap.xml"
        cls.soup = parse_html("index.html")
        cls.oracle = AIKnowledgeExtractionOracle(cls.soup)

    # =========================================================================
    # 1. AI Knowledge Extraction Oracle Simulation
    # =========================================================================

    def test_oracle_extract_office_location(self):
        """Oracle Query 1: 'Where is the office located?'"""
        # Test FAQ retrieval
        answer = self.oracle.query(["office", "located", "where"])
        self.assertIsNotNone(answer, "Oracle failed to retrieve office location from FAQPage")
        self.assertIn("#3309, 1st Main Road, Gayathrinagar", answer)
        self.assertIn("560021", answer)
        self.assertIn("More Retail Store", answer)

        # Cross-reference with LocalBusiness PostalAddress entity
        address = (self.oracle.business_entity or {}).get("address", {})
        self.assertEqual(address.get("streetAddress"), "#3309, 1st Main Road, Gayathrinagar")
        self.assertEqual(address.get("addressLocality"), "Bengaluru")
        self.assertEqual(address.get("postalCode"), "560021")
        self.assertEqual(address.get("addressCountry"), "IN")

    def test_oracle_extract_working_hours(self):
        """Oracle Query 2: 'What are the working hours?'"""
        answer = self.oracle.query(["working", "hours", "timings"])
        self.assertIsNotNone(answer, "Oracle failed to retrieve working hours from FAQPage")
        self.assertIn("Monday through Saturday", answer)
        self.assertIn("9:30 AM to 7:30 PM", answer)
        self.assertIn("closed on Sundays", answer)
        self.assertIn("24/7", answer)

        # Cross-reference with OpeningHoursSpecification
        hours_specs = (self.oracle.business_entity or {}).get("openingHoursSpecification", [])
        self.assertTrue(len(hours_specs) > 0, "Missing openingHoursSpecification in LocalBusiness")
        spec = hours_specs[0]
        self.assertEqual(spec.get("opens"), "09:30")
        self.assertEqual(spec.get("closes"), "19:30")
        days = spec.get("dayOfWeek", [])
        self.assertIn("Monday", days)
        self.assertIn("Saturday", days)
        self.assertNotIn("Sunday", days)

    def test_oracle_extract_sakala_turnaround_time(self):
        """Oracle Query 3: 'What is the turnaround time for plan sanction under Sakala?'"""
        answer = self.oracle.query(["turnaround", "time", "sakala", "plan sanction"])
        self.assertIsNotNone(answer, "Oracle failed to retrieve Sakala turnaround time from FAQPage")
        self.assertIn("Sakala Guarantee", answer)
        self.assertIn("14 to 21 business days", answer)
        self.assertIn("Nambike Nakshe", answer)
        self.assertIn("3 to 7 business days", answer)

    def test_oracle_extract_payment_methods(self):
        """Oracle Query 4: 'What are the payment methods?'"""
        answer = self.oracle.query(["payment", "methods", "currencies"])
        self.assertIsNotNone(answer, "Oracle failed to retrieve payment methods from FAQPage")
        self.assertIn("Indian Rupee (INR)", answer)
        self.assertIn("UPI", answer)
        self.assertIn("Net Banking", answer)
        self.assertIn("Credit and Debit Cards", answer)
        self.assertIn("Cheque", answer)
        self.assertIn("Cash", answer)
        self.assertIn("treasury challan", answer)

        # Cross-reference with LocalBusiness attributes
        payment_accepted = (self.oracle.business_entity or {}).get("paymentAccepted", "")
        self.assertIn("UPI", payment_accepted)
        self.assertIn("Cash", payment_accepted)
        self.assertIn("Cheque", payment_accepted)
        self.assertEqual((self.oracle.business_entity or {}).get("currenciesAccepted"), "INR")

    def test_oracle_extract_founder_credentials(self):
        """Oracle Query 5: 'What are the credentials of S. M. Thyagaraja?'"""
        answer = self.oracle.query(["credentials", "experience", "Thyagaraja"])
        self.assertIsNotNone(answer, "Oracle failed to retrieve credentials from FAQPage")
        self.assertIn("S. M. Thyagaraja", answer)
        self.assertIn("1989", answer)
        self.assertIn("23,000+", answer)
        self.assertIn("CA/2009/44120", answer)
        self.assertIn("BCC/BL-3.2.3/S-218/89-90", answer)

        # Cross-reference with founder entity hasCredential array
        founder = self.oracle.founder_entity
        self.assertEqual(founder.get("name"), "S. M. Thyagaraja")
        self.assertEqual(founder.get("alternateName"), "ಎಸ್. ಎಂ. ತ್ಯಾಗರಾಜ")
        creds = founder.get("hasCredential", [])
        self.assertEqual(len(creds), 2, "Founder must have exactly 2 formal credentials")
        ids = {c.get("identifier"): c.get("name") for c in creds}
        self.assertIn("CA/2009/44120", ids)
        self.assertIn("Council of Architecture Registration", ids["CA/2009/44120"])
        self.assertIn("BCC/BL-3.2.3/S-218/89-90", ids)
        self.assertIn("BBMP Approved Technical Supervisor License", ids["BCC/BL-3.2.3/S-218/89-90"])

    # =========================================================================
    # 2. Bilingual Unicode & UTF-8 Crawler Robustness
    # =========================================================================

    def test_unicode_utf8_binary_cleanliness_index_html(self):
        """Crawler Stress: index.html raw bytes decode strictly as UTF-8 without BOM or replacement chars."""
        with open(self.index_path, "rb") as f:
            raw_bytes = f.read()

        # Check UTF-8 BOM
        self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"), "index.html has UTF-8 BOM, which may break some legacy crawlers")

        # Check strict decode
        try:
            decoded_text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            self.fail(f"index.html failed strict UTF-8 decode: {e}")

        # Check for Unicode Replacement Character \ufffd (indicates prior corrupted character conversion)
        self.assertNotIn("\ufffd", decoded_text, "Found Unicode Replacement Character (\ufffd) in index.html")

        # Check for typical UTF-8 mojibake patterns
        mojibake_patterns = [r"Ã[\x80-\xbf]", r"â[\x80-\xbf]{2}", r"ï¿½"]
        for pattern in mojibake_patterns:
            matches = re.findall(pattern, decoded_text)
            self.assertEqual(len(matches), 0, f"Found potential mojibake pattern '{pattern}' in index.html: {matches[:5]}")

    def test_unicode_kannada_range_presence_and_density(self):
        """Crawler Stress: Validate Kannada characters (U+0C80 - U+0CFF) throughout index.html."""
        html_text = load_file("index.html")
        kannada_chars = re.findall(r"[\u0c80-\u0cff]", html_text)
        self.assertTrue(len(kannada_chars) > 200, f"Expected >200 Kannada Unicode characters, found {len(kannada_chars)}")

        # Check brand name variations
        self.assertIn("ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್", html_text)

    def test_unicode_kannada_json_ld_alternate_names(self):
        """Crawler Stress: JSON-LD alternateName contains valid Kannada strings and parse cleanly."""
        lb = find_entity_by_type(self.oracle.graph, "LocalBusiness") or find_entity_by_type(self.oracle.graph, "Store")
        self.assertIsNotNone(lb)
        alt_names = lb.get("alternateName", [])
        self.assertIsInstance(alt_names, list)

        # Verify Kannada string in alternateName list
        kannada_alts = [n for n in alt_names if any("\u0c80" <= c <= "\u0cff" for c in n)]
        self.assertTrue(len(kannada_alts) >= 1, "LocalBusiness alternateName must contain Kannada brand representation")
        self.assertIn("ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್", kannada_alts)

        # Verify Products have Kannada alternateName
        products = find_entities_by_type(self.oracle.graph, "Product")
        self.assertEqual(len(products), 6, "Expected 6 Product entities")
        for prod in products:
            p_alt = prod.get("alternateName", "")
            has_kannada = any("\u0c80" <= c <= "\u0cff" for c in p_alt)
            self.assertTrue(has_kannada, f"Product '{prod.get('name')}' missing Kannada alternateName")

    def test_unicode_utf8_binary_cleanliness_sitemap_xml(self):
        """Crawler Stress: sitemap.xml decodes strictly as UTF-8 and parses with XML parser."""
        with open(self.sitemap_path, "rb") as f:
            raw_bytes = f.read()

        self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"), "sitemap.xml has UTF-8 BOM")

        try:
            tree = ET.fromstring(raw_bytes)
        except ET.ParseError as e:
            self.fail(f"sitemap.xml failed strict XML parsing: {e}")

        # Verify hreflang annotations for 'en' and 'kn'
        namespaces = {
            "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }
        urls = tree.findall("sm:url", namespaces)
        self.assertTrue(len(urls) > 0, "No <url> elements found in sitemap.xml")

        main_url = urls[0]
        hreflangs = [link.get("hreflang") for link in main_url.findall("xhtml:link", namespaces)]
        self.assertIn("en", hreflangs)
        self.assertIn("kn", hreflangs)
        self.assertIn("x-default", hreflangs)

    # =========================================================================
    # 3. Google Search Console Verification Tag Audit
    # =========================================================================

    def test_gsc_meta_tag_exact_format_and_clean_attributes(self):
        """GSC Audit: Validate meta name='google-site-verification' tag format and attribute hygiene."""
        head = self.soup.find("head")
        self.assertIsNotNone(head, "Missing <head>")

        gsc_tags = head.find_all("meta", attrs={"name": "google-site-verification"})
        self.assertEqual(len(gsc_tags), 1, "There must be exactly ONE google-site-verification meta tag")

        tag = gsc_tags[0]
        # Check attribute keys: should ONLY have 'name' and 'content'
        attr_keys = list(tag.attrs.keys())
        self.assertIn("name", attr_keys)
        self.assertIn("content", attr_keys)
        for key in attr_keys:
            self.assertIn(key, ["name", "content"], f"Unexpected attribute '{key}' found on google-site-verification meta tag")

        # Content must be non-empty and valid string without newlines or illegal quotes
        content_val = tag["content"]
        self.assertIsInstance(content_val, str)
        self.assertTrue(len(content_val.strip()) > 0, "google-site-verification content attribute is empty")
        self.assertNotIn("\n", content_val, "google-site-verification content contains unexpected newline")
        self.assertNotIn('"', content_val, "google-site-verification content contains unescaped quote")

    def test_gsc_template_file_format(self):
        """GSC Audit: Verify google-site-verification-template.html exists with compliant format."""
        self.assertTrue(file_exists("google-site-verification-template.html"))
        content = load_file("google-site-verification-template.html")
        self.assertIn("google-site-verification:", content)
        self.assertIn(".html", content)

    # =========================================================================
    # 4. GA4 Analytics Hook Stub Offline / File Protocol Resilience
    # =========================================================================

    def test_ga4_analytics_script_offline_execution_via_node(self):
        """GA4 Resilience: Execute inline GA4 script in Node.js under simulated file:// and placeholder environments."""
        html_text = load_file("index.html")

        # Extract the GA4 script block
        ga4_match = re.search(r"<!--\s*GOOGLE ANALYTICS 4.*?<script>(.*?)</script>", html_text, re.DOTALL)
        self.assertIsNotNone(ga4_match, "Could not locate GA4 script block in index.html")
        ga4_js_code = ga4_match.group(1).strip()

        # Create a test harness script for Node.js
        test_harness_js = f"""
        const assert = require('assert');

        // Test Scenario A: file:// protocol simulation
        (function testFileProtocol() {{
            const window = {{
                location: {{ protocol: 'file:' }}
            }};
            const document = {{
                head: {{
                    appendChild: function(node) {{
                        throw new Error('Remote script injected during offline file: protocol!');
                    }}
                }},
                createElement: function(tag) {{
                    return {{ tagName: tag }};
                }}
            }};

            // Wrap and evaluate script
            const runScript = new Function('window', 'document', `{ga4_js_code}`);
            runScript(window, document);

            // Assertions
            assert.strictEqual(typeof window.gtag, 'function', 'window.gtag must be defined as a function under file:');
            assert.ok(Array.isArray(window.dataLayer), 'window.dataLayer must be initialized as an Array');

            // Invoke gtag - MUST NOT THROW ReferenceError
            window.gtag('event', 'page_view', {{ page_title: 'Home' }});
            window.gtag('event', 'lead_form_submit', {{ lead_id: '123' }});

            assert.strictEqual(window.dataLayer.length, 2, 'dataLayer should contain 2 queued arguments');
        }})();

        // Test Scenario B: http:// protocol with default placeholder 'G-XXXXXXXXXX'
        (function testPlaceholderProtocol() {{
            const window = {{
                location: {{ protocol: 'http:' }}
            }};
            const document = {{
                head: {{
                    appendChild: function(node) {{
                        throw new Error('Remote script injected while GA_MEASUREMENT_ID is placeholder!');
                    }}
                }},
                createElement: function(tag) {{
                    return {{ tagName: tag }};
                }}
            }};

            const runScript = new Function('window', 'document', `{ga4_js_code}`);
            runScript(window, document);

            assert.strictEqual(typeof window.gtag, 'function', 'window.gtag must be defined as a function for placeholder');
            assert.ok(Array.isArray(window.dataLayer), 'window.dataLayer must be an Array');

            // Invoke gtag with various types
            window.gtag('config', 'G-XXXXXXXXXX');
            assert.strictEqual(window.dataLayer.length, 1);
        }})();

        // Test Scenario C: Stress test - 1000 calls without memory or prototype corruption
        (function testStressCalls() {{
            const window = {{
                location: {{ protocol: 'file:' }}
            }};
            const document = {{ head: {{}}, createElement: () => ({{}}) }};
            const runScript = new Function('window', 'document', `{ga4_js_code}`);
            runScript(window, document);

            for (let i = 0; i < 1000; i++) {{
                window.gtag('event', 'stress_' + i, {{ count: i }});
            }}
            assert.strictEqual(window.dataLayer.length, 1000, 'All 1000 events must be pushed cleanly');
        }})();

        console.log('NODE_GA4_STRESS_TEST_PASSED');
        """

        # Write to temporary file and execute via node
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(test_harness_js)
            temp_path = temp_file.name

        try:
            res = subprocess.run(
                ["node", temp_path],
                capture_output=True,
                text=True,
                timeout=10,
            )
            self.assertEqual(res.returncode, 0, f"Node.js GA4 test failed:\nSTDOUT: {res.stdout}\nSTDERR: {res.stderr}")
            self.assertIn("NODE_GA4_STRESS_TEST_PASSED", res.stdout)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()
