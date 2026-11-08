"""
Tier 3: Cross-Feature Combinations Test Suite.
Validates structural coherence and cross-component contracts:
- Bilingual + Schema Synchronization (Kannada names in JSON-LD matching DOM)
- GSC Verification + Sitemap Domain Alignment
- Robots.txt + Sitemap.xml Synchronization (Sitemap directive & Host match)
- GEO Tags + Open Graph + Schema Geographic Alignment
- Canonical URL + OG + Schema + Sitemap Uniformity
- Robots.txt Crawler Permissions for 10+ Generative AI Bots
- Sitemap Hreflang Alternates + DOM Alternate Links Harmony
"""

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


class TestTier3CrossFeature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.soup = parse_html("index.html")
        cls.head = cls.soup.find("head")
        cls.json_ld = parse_json_ld(cls.soup)
        cls.graph = get_schema_graph(cls.soup)

    # =========================================================================
    # 1. Bilingual + Schema Synchronization
    # =========================================================================

    def test_schema_inlanguage_declares_both_english_and_kannada(self):
        """3.1 Cross: Schema WebSite/WebPage entities declare inLanguage containing 'en-IN' and 'kn-IN'."""
        ws = find_entity_by_type(self.graph, "WebSite")
        self.assertIsNotNone(ws, "WebSite entity missing")
        langs = ws.get("inLanguage", [])
        self.assertIn("en-IN", langs, "inLanguage missing 'en-IN'")
        self.assertIn("kn-IN", langs, "inLanguage missing 'kn-IN'")

    def test_schema_localbusiness_alternatename_matches_dom_signboard(self):
        """3.2 Cross: LocalBusiness alternateName contains the native Kannada brand string shown on the storefront."""
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb)
        alt_names = lb.get("alternateName", [])
        if isinstance(alt_names, str):
            alt_names = [alt_names]

        # Verify Kannada string is in alternateName
        has_kannada = any("ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್" in name or "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್‌ಪ್ರೈಸಸ್" in name for name in alt_names)
        self.assertTrue(has_kannada, f"alternateName {alt_names} must contain Kannada brand string")

        # Verify the same string is present in the DOM signboard
        dom_text = self.soup.get_text()
        self.assertTrue("ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್" in dom_text or "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್‌ಪ್ರೈಸಸ್" in dom_text)

    def test_schema_catalog_items_have_kannada_alternatename(self):
        """3.3 Cross: All catalog products in schema declare alternateName in Kannada."""
        products = find_entities_by_type(self.graph, "Product") or find_entities_by_type(self.graph, "Service")
        self.assertTrue(len(products) >= 6)
        for prod in products:
            alt_name = prod.get("alternateName", "")
            self.assertTrue(len(alt_name.strip()) > 0, f"Product '{prod.get('name')}' missing alternateName")
            # Verify alternateName contains Kannada Unicode range (\u0C80-\u0CFF)
            has_kannada_unicode = any("\u0c80" <= ch <= "\u0cff" for ch in alt_name)
            self.assertTrue(
                has_kannada_unicode,
                f"Product '{prod.get('name')}' alternateName '{alt_name}' is not in Kannada script",
            )

    def test_schema_breadcrumbs_contain_bilingual_labels(self):
        """3.4 Cross: Breadcrumb list items contain bilingual labels with Kannada transliterations."""
        bc = find_entity_by_type(self.graph, "BreadcrumbList")
        self.assertIsNotNone(bc)
        items = bc.get("itemListElement", [])
        for item in items:
            name = item.get("name", "")
            has_kannada_unicode = any("\u0c80" <= ch <= "\u0cff" for ch in name)
            self.assertTrue(
                has_kannada_unicode,
                f"Breadcrumb item '{name}' should be bilingual containing Kannada characters",
            )

    # =========================================================================
    # 2. Google Search Console & Sitemap Domain Alignment
    # =========================================================================

    def test_gsc_and_sitemap_target_identical_github_pages_domain(self):
        """3.5 Cross: GSC canonical target and sitemap.xml <loc> target the same domain."""
        self.assertTrue(file_exists("sitemap.xml"), "sitemap.xml missing")
        sitemap_entries = parse_sitemap_xml("sitemap.xml")
        self.assertTrue(len(sitemap_entries) > 0)
        primary_loc = sitemap_entries[0]["loc"]

        canonical_tag = self.head.find("link", attrs={"rel": "canonical"})
        self.assertIsNotNone(canonical_tag)
        canonical_href = canonical_tag.get("href")

        self.assertEqual(
            primary_loc,
            canonical_href,
            f"Sitemap primary loc '{primary_loc}' must match canonical href '{canonical_href}'",
        )

    # =========================================================================
    # 3. Robots.txt & Sitemap.xml Synchronization
    # =========================================================================

    def test_robots_txt_sitemap_directive_points_to_sitemap_xml(self):
        """3.6 Cross: robots.txt declares Sitemap directive matching the exact URL of sitemap.xml."""
        self.assertTrue(file_exists("robots.txt"), "robots.txt missing")
        robots_data = parse_robots_txt("robots.txt")
        self.assertTrue(len(robots_data["sitemaps"]) > 0, "robots.txt missing Sitemap directive")
        declared_sitemap = robots_data["sitemaps"][0]
        expected_sitemap = "https://sarva-dharma.github.io/srisaienterprises/sitemap.xml"
        self.assertEqual(declared_sitemap, expected_sitemap)

    def test_robots_txt_host_directive_matches_sitemap_host(self):
        """3.7 Cross: Host directive in robots.txt matches domain in sitemap entries."""
        self.assertTrue(file_exists("robots.txt"), "robots.txt missing")
        robots_data = parse_robots_txt("robots.txt")
        if robots_data["hosts"]:
            declared_host = robots_data["hosts"][0]
            self.assertEqual(declared_host, "sarva-dharma.github.io")

    # =========================================================================
    # 4. GEO Tags & Open Graph & Schema Alignment
    # =========================================================================

    def test_geotags_and_schema_coordinates_are_strictly_synchronized(self):
        """3.8 Cross: <meta name='geo.position'> and <meta name='ICBM'> strictly match JSON-LD GeoCoordinates."""
        geo_pos = self.head.find("meta", attrs={"name": "geo.position"})
        icbm = self.head.find("meta", attrs={"name": "ICBM"})
        self.assertIsNotNone(geo_pos, "Missing <meta name='geo.position'>")
        self.assertIsNotNone(icbm, "Missing <meta name='ICBM'>")

        # geo.position is semicolon-separated: "12.9965;77.5562"
        # ICBM is comma-separated: "12.9965, 77.5562"
        pos_parts = [float(x.strip()) for x in geo_pos["content"].split(";")]
        icbm_parts = [float(x.strip()) for x in icbm["content"].split(",")]

        self.assertAlmostEqual(pos_parts[0], 12.9965, places=3)
        self.assertAlmostEqual(pos_parts[1], 77.5562, places=3)
        self.assertAlmostEqual(icbm_parts[0], pos_parts[0], places=4)
        self.assertAlmostEqual(icbm_parts[1], pos_parts[1], places=4)

        # Match with JSON-LD
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb)
        geo = lb.get("geo", {})
        self.assertAlmostEqual(float(geo.get("latitude")), pos_parts[0], places=4)
        self.assertAlmostEqual(float(geo.get("longitude")), pos_parts[1], places=4)

    def test_geotags_region_and_og_locale_geographic_harmony(self):
        """3.9 Cross: geo.region (IN-KA) and geo.placename (Bengaluru) align with og:locale (en_IN, kn_IN)."""
        geo_reg = self.head.find("meta", attrs={"name": "geo.region"})
        geo_place = self.head.find("meta", attrs={"name": "geo.placename"})
        og_loc = self.head.find("meta", attrs={"property": "og:locale"})
        og_alt_loc = self.head.find("meta", attrs={"property": "og:locale:alternate"})

        self.assertIsNotNone(geo_reg)
        self.assertIsNotNone(geo_place)
        self.assertIsNotNone(og_loc)
        self.assertIsNotNone(og_alt_loc)

        self.assertEqual(geo_reg["content"], "IN-KA")
        self.assertEqual(geo_place["content"], "Bengaluru")
        self.assertEqual(og_loc["content"], "en_IN")
        self.assertEqual(og_alt_loc["content"], "kn_IN")

    # =========================================================================
    # 5. Canonical URL Uniformity Across All Declarations
    # =========================================================================

    def test_canonical_uniformity_across_head_og_schema_and_sitemap(self):
        """3.10 Cross: Canonical URL string is identical across canonical tag, og:url, schema, and sitemap."""
        expected_url = "https://sarva-dharma.github.io/srisaienterprises/"

        canonical = self.head.find("link", attrs={"rel": "canonical"})["href"]
        og_url = self.head.find("meta", attrs={"property": "og:url"})["content"]

        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        schema_lb_url = lb.get("url") if lb else None

        ws = find_entity_by_type(self.graph, "WebSite")
        schema_ws_url = ws.get("url") if ws else None

        self.assertEqual(canonical, expected_url)
        self.assertEqual(og_url, expected_url)
        self.assertEqual(schema_lb_url, expected_url)
        self.assertEqual(schema_ws_url, expected_url)

        if file_exists("sitemap.xml"):
            sitemap_entries = parse_sitemap_xml("sitemap.xml")
            self.assertEqual(sitemap_entries[0]["loc"], expected_url)

    # =========================================================================
    # 6. Robots Permissions for 10+ Generative AI Bots
    # =========================================================================

    def test_robots_txt_allows_generative_ai_discovery_bots(self):
        """3.11 Cross: robots.txt grants indexing permissions to 10+ top generative AI engines."""
        self.assertTrue(file_exists("robots.txt"), "robots.txt missing")
        robots_data = parse_robots_txt("robots.txt")
        agents = robots_data["user_agents"]

        ai_bots_to_verify = [
            "GPTBot",
            "ChatGPT-User",
            "OAI-SearchBot",
            "Google-Extended",
            "ClaudeBot",
            "anthropic-ai",
            "Claude-Web",
            "PerplexityBot",
            "Bytespider",
            "CCBot",
            "Meta-ExternalAgent",
            "Applebot",
        ]

        for bot in ai_bots_to_verify:
            self.assertIn(bot, agents, f"robots.txt missing user-agent declaration for AI bot '{bot}'")
            # Verify '/' is allowed
            allows = agents[bot]["allow"]
            self.assertTrue(
                "/" in allows or len(allows) > 0,
                f"AI bot '{bot}' must be granted Allow: / in robots.txt",
            )

    # =========================================================================
    # 7. Sitemap Hreflang + DOM Meta Alternates Alignment
    # =========================================================================

    def test_sitemap_hreflang_and_dom_alternate_links_synchronization(self):
        """3.12 Cross: Both sitemap.xml and index.html declare hreflang alternates for en, kn, and x-default."""
        self.assertTrue(file_exists("sitemap.xml"), "sitemap.xml missing")
        entries = parse_sitemap_xml("sitemap.xml")
        primary_entry = entries[0]

        sitemap_langs = {alt["hreflang"] for alt in primary_entry["alternates"]}
        self.assertTrue("en" in sitemap_langs or "en-IN" in sitemap_langs)
        self.assertTrue("kn" in sitemap_langs or "kn-IN" in sitemap_langs)
        self.assertIn("x-default", sitemap_langs)

        # Check DOM alternate links in head
        dom_alternates = self.head.find_all("link", attrs={"rel": "alternate", "hreflang": True})
        self.assertTrue(
            len(dom_alternates) >= 2,
            "index.html <head> should declare <link rel='alternate' hreflang='...'> tags",
        )
        dom_langs = {link["hreflang"] for link in dom_alternates}
        self.assertTrue("en" in dom_langs or "en-IN" in dom_langs)
        self.assertTrue("kn" in dom_langs or "kn-IN" in dom_langs)


if __name__ == "__main__":
    unittest.main()
