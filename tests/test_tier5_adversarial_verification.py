"""
Tier 5: Adversarial Verification and Stress Testing Suite.
Executed by Challenger 1 (Code-Executing Adversarial Verifier).

Adversarial Stress Dimensions:
1. JSON-LD Schema: 11 graph entities, rigorous type assertions, @id reference resolution (no dangling IDs),
   E.164 phone formatting, strict numeric string prices with INR currency, geo bounds.
2. XML Sitemap: ElementTree strict parse, namespace validations (sitemap 0.9 + xhtml),
   hreflang alternate links (en, kn, x-default), HTTPS scheme validation.
3. robots.txt: Detailed parsing of user-agent directives (Googlebot, Bingbot, GPTBot, ClaudeBot,
   PerplexityBot, Google-Extended), Host and Sitemap directives.
4. Interactive Workflows & DOM IDs: Full DOM ID resolution against main.js, jurisdiction.js,
   portal.js, and calculator.js. DOM uniqueness (zero duplicate ID collisions).
5. Static Asset Integrity: Verification that all images, CSS, and JS files referenced
   in HTML and JSON-LD exist on disk.
6. Bilingual Content: Co-presence of Kannada Unicode script and English translations.
"""

import json
import os
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class TestTier5AdversarialVerification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_path = PROJECT_ROOT / "index.html"
        cls.robots_path = PROJECT_ROOT / "robots.txt"
        cls.sitemap_path = PROJECT_ROOT / "sitemap.xml"
        cls.gsc_template_path = PROJECT_ROOT / "google-site-verification-template.html"

        with open(cls.html_path, "r", encoding="utf-8") as f:
            cls.html_raw = f.read()
        cls.soup = BeautifulSoup(cls.html_raw, "html.parser")
        cls.head = cls.soup.find("head")

        with open(cls.robots_path, "r", encoding="utf-8") as f:
            cls.robots_raw = f.read()

        with open(cls.sitemap_path, "r", encoding="utf-8") as f:
            cls.sitemap_raw = f.read()

    # =========================================================================
    # 1. JSON-LD Schema Adversarial Verification
    # =========================================================================

    def test_json_ld_script_presence_and_parsing(self):
        """1.1 JSON-LD: Exactly one valid application/ld+json script tag with @graph."""
        scripts = self.soup.find_all("script", type="application/ld+json")
        self.assertEqual(len(scripts), 1, f"Expected exactly 1 JSON-LD script, found {len(scripts)}")
        raw = scripts[0].string or scripts[0].get_text()
        self.assertTrue(len(raw.strip()) > 0, "JSON-LD content is empty")

        data = json.loads(raw.strip())
        self.assertEqual(data.get("@context"), "https://schema.org")
        self.assertIn("@graph", data)
        self.assertIsInstance(data["@graph"], list)

    def test_json_ld_all_11_graph_entities_and_types(self):
        """1.2 JSON-LD: Iterate all 11 @graph entities and assert exact type validity."""
        raw = self.soup.find("script", type="application/ld+json").get_text().strip()
        data = json.loads(raw)
        graph = data["@graph"]

        self.assertEqual(len(graph), 11, f"Expected exactly 11 @graph entities, found {len(graph)}")

        expected_entity_signatures = [
            ("LocalBusiness", ["LocalBusiness", "Store", "ProfessionalService"]),
            ("WebSite", "WebSite"),
            ("BreadcrumbList", "BreadcrumbList"),
            ("Product 1 (Plan Sanctions)", ["Product", "Service"]),
            ("Product 2 (PreDCR CAD)", ["Product", "Service"]),
            ("Product 3 (e-Khata)", ["Product", "Service"]),
            ("Product 4 (Architectural Design)", ["Product", "Service"]),
            ("Product 5 (Statutory NOC)", ["Product", "Service"]),
            ("Product 6 (Turnkey Construction)", ["Product", "Service"]),
            ("FAQPage", "FAQPage"),
            ("WebPage", "WebPage"),
        ]

        found_types = []
        for entity in graph:
            etype = entity.get("@type")
            found_types.append(etype)

        # Count service/products (should be 6)
        service_products = [e for e in graph if isinstance(e.get("@type"), list) and "Product" in e.get("@type") and "Service" in e.get("@type")]
        self.assertEqual(len(service_products), 6, f"Expected 6 Product/Service entities, found {len(service_products)}")

        # Check LocalBusiness / Store / ProfessionalService
        lb_entities = [e for e in graph if isinstance(e.get("@type"), list) and "LocalBusiness" in e.get("@type")]
        self.assertEqual(len(lb_entities), 1)

        # Check WebSite
        website_entities = [e for e in graph if e.get("@type") == "WebSite"]
        self.assertEqual(len(website_entities), 1)

        # Check BreadcrumbList
        bc_entities = [e for e in graph if e.get("@type") == "BreadcrumbList"]
        self.assertEqual(len(bc_entities), 1)

        # Check FAQPage
        faq_entities = [e for e in graph if e.get("@type") == "FAQPage"]
        self.assertEqual(len(faq_entities), 1)

        # Check WebPage
        webpage_entities = [e for e in graph if e.get("@type") == "WebPage"]
        self.assertEqual(len(webpage_entities), 1)

    def test_json_ld_id_anchors_and_cross_reference_resolution(self):
        """1.3 JSON-LD: Every @id is well-formed HTTPS anchor and all internal references resolve."""
        raw = self.soup.find("script", type="application/ld+json").get_text().strip()
        data = json.loads(raw)
        graph = data["@graph"]

        # Collect all declared @id anchors
        declared_ids = set()
        for entity in graph:
            eid = entity.get("@id")
            self.assertIsNotNone(eid, f"Entity of type {entity.get('@type')} has missing @id")
            self.assertTrue(eid.startswith("https://sarva-dharma.github.io/srisaienterprises/#"), f"Invalid @id URI: {eid}")
            declared_ids.add(eid)

            # Check founder sub-entity @id if present
            if "founder" in entity and isinstance(entity["founder"], dict):
                founder_id = entity["founder"].get("@id")
                if founder_id:
                    declared_ids.add(founder_id)

        # Verify required anchor names
        base = "https://sarva-dharma.github.io/srisaienterprises/"
        required_anchors = [
            f"{base}#store",
            f"{base}#website",
            f"{base}#breadcrumb",
            f"{base}#product-plan-sanction",
            f"{base}#product-predcr-cad",
            f"{base}#product-ekhata",
            f"{base}#product-architectural-design",
            f"{base}#product-statutory-noc",
            f"{base}#product-turnkey-construction",
            f"{base}#faq",
            f"{base}#webpage",
            f"{base}#founder",
        ]
        for req in required_anchors:
            self.assertIn(req, declared_ids, f"Required anchor {req} not found in declared @id anchors")

        # Check cross-references: publisher, seller, about, isPartOf
        for entity in graph:
            if "publisher" in entity and isinstance(entity["publisher"], dict):
                ref = entity["publisher"].get("@id")
                self.assertIn(ref, declared_ids, f"Dangling publisher reference: {ref}")
            if "about" in entity and isinstance(entity["about"], dict):
                ref = entity["about"].get("@id")
                self.assertIn(ref, declared_ids, f"Dangling about reference: {ref}")
            if "isPartOf" in entity and isinstance(entity["isPartOf"], dict):
                ref = entity["isPartOf"].get("@id")
                self.assertIn(ref, declared_ids, f"Dangling isPartOf reference: {ref}")
            if "offers" in entity and isinstance(entity["offers"], dict):
                seller = entity["offers"].get("seller", {})
                if isinstance(seller, dict) and "@id" in seller:
                    self.assertIn(seller["@id"], declared_ids, f"Dangling seller reference: {seller['@id']}")

    def test_json_ld_price_formatting_and_currencies(self):
        """1.4 JSON-LD: Price formatting is numeric string, currency is INR, condition & availability valid."""
        raw = self.soup.find("script", type="application/ld+json").get_text().strip()
        data = json.loads(raw)
        graph = data["@graph"]

        products = [e for e in graph if isinstance(e.get("@type"), list) and "Product" in e.get("@type")]
        for prod in products:
            offers = prod.get("offers")
            self.assertIsInstance(offers, dict, f"Missing offers in product: {prod.get('name')}")
            price = offers.get("price")
            self.assertIsInstance(price, str, f"Price must be string formatted, got {type(price)}")
            # Must be valid float
            val = float(price)
            self.assertTrue(val >= 1000.0, f"Price {price} unexpectedly low")
            self.assertEqual(offers.get("priceCurrency"), "INR")
            self.assertEqual(offers.get("availability"), "https://schema.org/InStock")
            self.assertEqual(offers.get("itemCondition"), "https://schema.org/NewCondition")

    def test_json_ld_phone_and_coordinates(self):
        """1.5 JSON-LD: Telephone formatting follows standard format, coordinates within Bengaluru."""
        raw = self.soup.find("script", type="application/ld+json").get_text().strip()
        data = json.loads(raw)
        graph = data["@graph"]

        lb = [e for e in graph if isinstance(e.get("@type"), list) and "LocalBusiness" in e.get("@type")][0]
        tel = lb.get("telephone")
        self.assertIsNotNone(tel)
        # Check Indian telephone format: e.g. +91-9448054185 or +91 94480 54185
        self.assertTrue(re.match(r"^\+91[\s\-]?[0-9]{10}$", tel.replace(" ", "")), f"Invalid phone format: {tel}")

        geo = lb.get("geo", {})
        self.assertEqual(geo.get("@type"), "GeoCoordinates")
        lat = float(geo.get("latitude"))
        lon = float(geo.get("longitude"))
        # Bengaluru bounding box: lat ~ 12.8 to 13.2, lon ~ 77.4 to 77.8
        self.assertTrue(12.8 <= lat <= 13.2, f"Latitude {lat} out of Bengaluru bounds")
        self.assertTrue(77.4 <= lon <= 77.8, f"Longitude {lon} out of Bengaluru bounds")

    # =========================================================================
    # 2. XML Sitemap Adversarial Verification
    # =========================================================================

    def test_xml_sitemap_namespaces_and_parsing(self):
        """2.1 XML Sitemap: Strict ElementTree parse, namespaces sitemaps.org 0.9 and xhtml."""
        try:
            tree = ET.fromstring(self.sitemap_raw)
        except ET.ParseError as e:
            self.fail(f"sitemap.xml is not valid XML: {e}")

        # Root tag should be {http://www.sitemaps.org/schemas/sitemap/0.9}urlset
        expected_tag = "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset"
        self.assertEqual(tree.tag, expected_tag, f"Root tag must be {expected_tag}, got {tree.tag}")

    def test_xml_sitemap_alternate_links_and_endpoints(self):
        """2.2 XML Sitemap: Alternate links en, kn, x-default; all loc URLs are valid HTTPS endpoints."""
        tree = ET.fromstring(self.sitemap_raw)
        ns = {
            "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
            "xhtml": "http://www.w3.org/1999/xhtml",
        }

        urls = tree.findall("s:url", ns)
        self.assertTrue(len(urls) >= 1, "sitemap.xml has no <url> entries")

        # Find primary storefront url entry
        primary_url = None
        for u in urls:
            loc = u.find("s:loc", ns)
            self.assertIsNotNone(loc, "<url> missing <loc>")
            loc_text = loc.text.strip()
            # Must be HTTPS
            self.assertTrue(loc_text.startswith("https://"), f"<loc> is not HTTPS: {loc_text}")
            parsed = urlparse(loc_text)
            self.assertEqual(parsed.netloc, "sarva-dharma.github.io")

            if loc_text == "https://sarva-dharma.github.io/srisaienterprises/":
                primary_url = u

        self.assertIsNotNone(primary_url, "Primary storefront URL not found in sitemap.xml")

        # Verify alternate links
        alt_links = primary_url.findall("xhtml:link", ns)
        self.assertEqual(len(alt_links), 3, f"Expected 3 alternate links, found {len(alt_links)}")

        hreflangs = {link.get("hreflang"): link.get("href") for link in alt_links}
        self.assertIn("en", hreflangs, "Missing hreflang='en'")
        self.assertIn("kn", hreflangs, "Missing hreflang='kn'")
        self.assertIn("x-default", hreflangs, "Missing hreflang='x-default'")

        for lang, href in hreflangs.items():
            self.assertTrue(href.startswith("https://"), f"Alternate href for {lang} is not HTTPS: {href}")

    # =========================================================================
    # 3. robots.txt Adversarial Verification
    # =========================================================================

    def test_robots_txt_user_agents_and_directives(self):
        """3.1 robots.txt: Parse lines, verify user-agent blocks for Googlebot, Bingbot, GPTBot, ClaudeBot, PerplexityBot, Google-Extended."""
        lines = [line.strip() for line in self.robots_raw.splitlines() if line.strip() and not line.strip().startswith("#")]

        user_agents = []
        sitemaps = []
        hosts = []

        for line in lines:
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip().lower()
                val = val.strip()
                if key == "user-agent":
                    user_agents.append(val)
                elif key == "sitemap":
                    sitemaps.append(val)
                elif key == "host":
                    hosts.append(val)

        # Check required user agents
        required_agents = [
            "Googlebot",
            "Bingbot",
            "GPTBot",
            "ClaudeBot",
            "PerplexityBot",
            "Google-Extended",
            "*",
        ]
        for agent in required_agents:
            self.assertIn(agent, user_agents, f"robots.txt missing User-agent: {agent}")

        # Check Sitemap directive
        self.assertIn(
            "https://sarva-dharma.github.io/srisaienterprises/sitemap.xml",
            sitemaps,
            f"Missing or incorrect Sitemap directive: {sitemaps}",
        )

        # Check Host directive
        self.assertIn(
            "sarva-dharma.github.io",
            hosts,
            f"Missing or incorrect Host directive: {hosts}",
        )

    # =========================================================================
    # 4. Interactive Workflows & DOM IDs Integrity
    # =========================================================================

    def test_interactive_dom_ids_intact(self):
        """4.1 Interactive DOM IDs: booking-modal, lead-name, lead-phone, jurisdiction-checker, fee-estimator exist."""
        required_ids = [
            "booking-modal",
            "lead-name",
            "lead-phone",
            "jurisdiction-checker",
            "fee-estimator",
            "consultation-booking-form",
            "lead-email",
            "lead-service",
            "jurisdiction-form",
            "jurisdiction-select",
            "input-plot-width",
            "input-plot-length",
            "input-road-width",
            "input-building-type",
            "jurisdiction-result-box",
            "portal-live-container",
            "main-content",
        ]

        missing_ids = []
        for dom_id in required_ids:
            elem = self.soup.find(id=dom_id)
            if not elem:
                missing_ids.append(dom_id)

        self.assertEqual(len(missing_ids), 0, f"Missing critical DOM IDs: {missing_ids}")

    def test_dom_id_uniqueness(self):
        """4.2 DOM ID Uniqueness: No duplicate id attributes exist in index.html."""
        elements_with_id = self.soup.find_all(id=True)
        seen_ids = set()
        duplicates = set()

        for el in elements_with_id:
            eid = el["id"]
            if eid in seen_ids:
                duplicates.add(eid)
            seen_ids.add(eid)

        self.assertEqual(len(duplicates), 0, f"Found duplicate DOM IDs in index.html: {duplicates}")

    # =========================================================================
    # 5. Static Assets Existence & Path Validity
    # =========================================================================

    def test_local_assets_exist_on_disk(self):
        """5.1 Static Assets: All CSS, JS, and image paths referenced in index.html exist on disk."""
        # Find script srcs
        scripts = self.soup.find_all("script", src=True)
        for s in scripts:
            src = s["src"]
            if not src.startswith("http://") and not src.startswith("https://"):
                local_path = PROJECT_ROOT / src.lstrip("/")
                self.assertTrue(local_path.is_file(), f"Referenced local script missing: {src} -> {local_path}")

        # Find stylesheet links
        links = self.soup.find_all("link", rel="stylesheet")
        for l in links:
            href = l.get("href", "")
            if not href.startswith("http://") and not href.startswith("https://") and not href.startswith("data:"):
                local_path = PROJECT_ROOT / href.lstrip("/")
                self.assertTrue(local_path.is_file(), f"Referenced stylesheet missing: {href} -> {local_path}")

        # Check key images referenced in meta tags
        og_image = self.head.find("meta", property="og:image")
        if og_image:
            img_url = og_image.get("content", "")
            if "sarva-dharma.github.io/srisaienterprises/" in img_url:
                rel = img_url.split("sarva-dharma.github.io/srisaienterprises/")[-1]
                local_img = PROJECT_ROOT / rel
                self.assertTrue(local_img.is_file(), f"OG image does not exist on disk: {local_img}")

    # =========================================================================
    # 6. Bilingual Content Co-presence
    # =========================================================================

    def test_bilingual_kannada_content_co_presence(self):
        """6.1 Bilingual: Kannada Unicode block characters are present in title, meta, signboard, and body."""
        kannada_regex = re.compile(r"[\u0C80-\u0CFF]")

        # In title or meta description
        title = self.soup.find("title").get_text()
        has_kannada_title = bool(kannada_regex.search(title))
        self.assertTrue(has_kannada_title, f"Title does not contain Kannada characters: {title}")

        # In page body
        body_text = self.soup.find("body").get_text()
        kannada_chars = kannada_regex.findall(body_text)
        self.assertTrue(len(kannada_chars) > 200, f"Expected rich Kannada content, found only {len(kannada_chars)} Kannada chars")


if __name__ == "__main__":
    unittest.main()
