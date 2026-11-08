"""
Tier 1: Feature Coverage Test Suite.
Verifies baseline feature presence and standards compliance with >= 5 tests per feature:
- SEO Tags (6 tests)
- GSC Meta Tag & Verification (5 tests)
- Canonical URL (5 tests)
- Robots Directives (6 tests)
- Open Graph Suite (7 tests)
- Twitter Cards (5 tests)
- JSON-LD Schemas (8 tests)
- Bilingual Text Nodes (6 tests)
"""

import json
import unittest
from pathlib import Path
from tests.helpers import (
    file_exists,
    find_entities_by_type,
    find_entity_by_type,
    get_json_ld_blocks,
    get_schema_graph,
    load_file,
    parse_html,
    parse_json_ld,
)


class TestTier1FeatureCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.soup = parse_html("index.html")
        cls.head = cls.soup.find("head")
        cls.json_ld = parse_json_ld(cls.soup)
        cls.graph = get_schema_graph(cls.soup)

    # =========================================================================
    # 1. SEO Tags (>= 5 tests)
    # =========================================================================

    def test_seo_title_present_and_non_empty(self):
        """1.1 SEO: <title> tag exists and is non-empty."""
        title = self.head.find("title") if self.head else None
        self.assertIsNotNone(title, "Missing <title> tag in <head>")
        self.assertTrue(len(title.get_text().strip()) > 10, "Title tag is empty or too short")

    def test_seo_title_contains_bilingual_brand(self):
        """1.2 SEO: <title> includes both English and Kannada brand identity or heritage."""
        title_text = self.head.find("title").get_text()
        self.assertIn("Sri Sai Enterprises", title_text, "Title must contain English brand name")
        # Check for Kannada brand or 'Since 1989'
        has_kannada_or_heritage = "ಶ್ರೀ ಸಾಯಿ" in title_text or "1989" in title_text
        self.assertTrue(has_kannada_or_heritage, "Title must include Kannada brand or '1989'")

    def test_seo_meta_description_present_and_length(self):
        """1.3 SEO: <meta name='description'> exists and adheres to snippet recommendations."""
        desc = self.head.find("meta", attrs={"name": "description"})
        self.assertIsNotNone(desc, "Missing <meta name='description'> in <head>")
        content = desc.get("content", "").strip()
        self.assertTrue(len(content) > 30, "Meta description is too short")
        self.assertLessEqual(
            len(content),
            165,
            f"Meta description is {len(content)} chars; should be <= 165 for search snippets",
        )

    def test_seo_meta_keywords_present(self):
        """1.4 SEO: <meta name='keywords'> exists and contains relevant municipal keywords."""
        keywords = self.head.find("meta", attrs={"name": "keywords"})
        self.assertIsNotNone(keywords, "Missing <meta name='keywords'> tag")
        content = keywords.get("content", "").lower()
        self.assertTrue(
            any(k in content for k in ["bbmp", "plan", "sanction", "approval", "bangalore", "bengaluru"]),
            "Keywords meta tag missing core municipal approval terms",
        )

    def test_seo_viewport_and_charset(self):
        """1.5 SEO: Standard viewport and UTF-8 charset declarations are present."""
        charset = self.head.find("meta", attrs={"charset": True})
        self.assertIsNotNone(charset, "Missing <meta charset='UTF-8'>")
        self.assertEqual(charset["charset"].lower(), "utf-8", "Charset must be UTF-8")

        viewport = self.head.find("meta", attrs={"name": "viewport"})
        self.assertIsNotNone(viewport, "Missing <meta name='viewport'>")
        self.assertIn("width=device-width", viewport.get("content", ""))

    def test_seo_html_lang_attribute(self):
        """1.6 SEO: Root <html> element declares primary lang attribute."""
        html_tag = self.soup.find("html")
        self.assertIsNotNone(html_tag, "Missing <html> root element")
        self.assertTrue(html_tag.has_attr("lang"), "<html> missing lang attribute")
        self.assertIn(html_tag["lang"].lower(), ["en", "en-in"], "<html> lang must be 'en' or 'en-IN'")

    # =========================================================================
    # 2. Google Search Console & External Verification (>= 5 tests)
    # =========================================================================

    def test_gsc_meta_tag_present(self):
        """2.1 GSC: <meta name='google-site-verification'> exists in <head>."""
        gsc = self.head.find("meta", attrs={"name": "google-site-verification"})
        self.assertIsNotNone(gsc, "Missing <meta name='google-site-verification'> in <head>")

    def test_gsc_meta_tag_content(self):
        """2.2 GSC: google-site-verification meta tag contains non-empty token attribute."""
        gsc = self.head.find("meta", attrs={"name": "google-site-verification"})
        self.assertIsNotNone(gsc, "Missing google-site-verification meta tag")
        content = gsc.get("content", "").strip()
        self.assertTrue(len(content) > 5, "google-site-verification content is empty or invalid")

    def test_bing_webmaster_meta_tag_present(self):
        """2.3 GSC/Bing: <meta name='msvalidate.01'> exists in <head> for Bing Webmaster Tools."""
        ms = self.head.find("meta", attrs={"name": "msvalidate.01"})
        self.assertIsNotNone(ms, "Missing <meta name='msvalidate.01'> in <head>")
        self.assertTrue(len(ms.get("content", "").strip()) > 5, "msvalidate.01 token is empty")

    def test_gsc_file_verification_template_exists(self):
        """2.4 GSC: Dedicated google-site-verification-template.html exists in project root."""
        self.assertTrue(
            file_exists("google-site-verification-template.html"),
            "google-site-verification-template.html missing in project root",
        )

    def test_gsc_file_verification_content_format(self):
        """2.5 GSC: Verification template file contains valid Google verification string format."""
        content = load_file("google-site-verification-template.html")
        self.assertIn(
            "google-site-verification:",
            content,
            "Template file must contain 'google-site-verification:' header line",
        )

    # =========================================================================
    # 3. Canonical URL (>= 5 tests)
    # =========================================================================

    def test_canonical_tag_exists(self):
        """3.1 Canonical: <link rel='canonical'> exists in <head>."""
        canonical = self.head.find("link", attrs={"rel": "canonical"})
        self.assertIsNotNone(canonical, "Missing <link rel='canonical'> in <head>")

    def test_canonical_tag_href_not_empty(self):
        """3.2 Canonical: Canonical href attribute is non-empty."""
        canonical = self.head.find("link", attrs={"rel": "canonical"})
        self.assertIsNotNone(canonical)
        href = canonical.get("href", "").strip()
        self.assertTrue(len(href) > 0, "Canonical href cannot be empty")

    def test_canonical_tag_points_to_production_origin(self):
        """3.3 Canonical: Canonical URL points to official GitHub Pages origin."""
        canonical = self.head.find("link", attrs={"rel": "canonical"})
        self.assertIsNotNone(canonical)
        href = canonical.get("href", "").strip()
        expected = "https://sarva-dharma.github.io/srisaienterprises/"
        self.assertEqual(href, expected, f"Canonical must be '{expected}', got '{href}'")

    def test_canonical_tag_has_trailing_slash(self):
        """3.4 Canonical: Canonical URL terminates with a trailing slash to avoid redirect hops."""
        canonical = self.head.find("link", attrs={"rel": "canonical"})
        self.assertIsNotNone(canonical)
        href = canonical.get("href", "").strip()
        self.assertTrue(href.endswith("/"), "Canonical URL must terminate with trailing slash '/'")

    def test_canonical_tag_is_singular(self):
        """3.5 Canonical: Exactly one canonical tag is declared in <head>."""
        canonicals = self.head.find_all("link", attrs={"rel": "canonical"})
        self.assertEqual(len(canonicals), 1, f"Expected exactly 1 canonical tag, found {len(canonicals)}")

    # =========================================================================
    # 4. Robots Directives (>= 5 tests)
    # =========================================================================

    def test_robots_meta_tag_exists(self):
        """4.1 Robots: <meta name='robots'> exists in <head>."""
        robots = self.head.find("meta", attrs={"name": "robots"})
        self.assertIsNotNone(robots, "Missing <meta name='robots'> in <head>")

    def test_robots_meta_tag_indexing_directives(self):
        """4.2 Robots: Robots meta tag explicitly permits indexing and link following."""
        robots = self.head.find("meta", attrs={"name": "robots"})
        self.assertIsNotNone(robots)
        content = robots.get("content", "").lower()
        self.assertIn("index", content, "Robots tag must declare 'index'")
        self.assertIn("follow", content, "Robots tag must declare 'follow'")

    def test_robots_meta_tag_preview_directives(self):
        """4.3 Robots: Robots meta tag declares max-image-preview:large for rich previews."""
        robots = self.head.find("meta", attrs={"name": "robots"})
        self.assertIsNotNone(robots)
        content = robots.get("content", "").lower()
        self.assertIn("max-image-preview:large", content, "Robots tag must include max-image-preview:large")

    def test_googlebot_meta_tag_exists(self):
        """4.4 Robots: Dedicated <meta name='googlebot'> directive is present."""
        googlebot = self.head.find("meta", attrs={"name": "googlebot"})
        self.assertIsNotNone(googlebot, "Missing <meta name='googlebot'> tag in <head>")
        content = googlebot.get("content", "").lower()
        self.assertIn("index", content)
        self.assertIn("max-snippet:-1", content)

    def test_bingbot_meta_tag_exists(self):
        """4.5 Robots: Dedicated <meta name='bingbot'> directive is present."""
        bingbot = self.head.find("meta", attrs={"name": "bingbot"})
        self.assertIsNotNone(bingbot, "Missing <meta name='bingbot'> tag in <head>")
        content = bingbot.get("content", "").lower()
        self.assertIn("index", content)

    def test_root_robots_txt_exists(self):
        """4.6 Robots: Root robots.txt exists in the repository."""
        self.assertTrue(file_exists("robots.txt"), "robots.txt missing in project root")

    # =========================================================================
    # 5. Open Graph Suite (>= 5 tests)
    # =========================================================================

    def test_og_title_present(self):
        """5.1 OG: og:title tag exists and contains brand name."""
        og_title = self.head.find("meta", attrs={"property": "og:title"})
        self.assertIsNotNone(og_title, "Missing <meta property='og:title'>")
        self.assertIn("Sri Sai Enterprises", og_title.get("content", ""))

    def test_og_description_present(self):
        """5.2 OG: og:description tag exists and is non-empty."""
        og_desc = self.head.find("meta", attrs={"property": "og:description"})
        self.assertIsNotNone(og_desc, "Missing <meta property='og:description'>")
        self.assertTrue(len(og_desc.get("content", "").strip()) > 20)

    def test_og_type_is_website(self):
        """5.3 OG: og:type is set to 'website'."""
        og_type = self.head.find("meta", attrs={"property": "og:type"})
        self.assertIsNotNone(og_type, "Missing <meta property='og:type'>")
        self.assertEqual(og_type.get("content", "").lower(), "website")

    def test_og_url_matches_canonical(self):
        """5.4 OG: og:url matches the canonical production URL."""
        og_url = self.head.find("meta", attrs={"property": "og:url"})
        self.assertIsNotNone(og_url, "Missing <meta property='og:url'>")
        self.assertEqual(
            og_url.get("content", "").strip(),
            "https://sarva-dharma.github.io/srisaienterprises/",
        )

    def test_og_image_is_absolute_https(self):
        """5.5 OG: og:image is an absolute HTTPS URL to an existing image asset."""
        og_image = self.head.find("meta", attrs={"property": "og:image"})
        self.assertIsNotNone(og_image, "Missing <meta property='og:image'>")
        img_url = og_image.get("content", "").strip()
        self.assertTrue(img_url.startswith("https://"), f"og:image must be absolute HTTPS: {img_url}")
        self.assertTrue(
            img_url.endswith(".jpg") or img_url.endswith(".png") or img_url.endswith(".webp"),
            f"og:image must point to image file: {img_url}",
        )

    def test_og_image_dimensions_and_alt(self):
        """5.6 OG: og:image:width, og:image:height, and og:image:alt are declared."""
        og_w = self.head.find("meta", attrs={"property": "og:image:width"})
        og_h = self.head.find("meta", attrs={"property": "og:image:height"})
        og_alt = self.head.find("meta", attrs={"property": "og:image:alt"})
        self.assertIsNotNone(og_w, "Missing <meta property='og:image:width'>")
        self.assertIsNotNone(og_h, "Missing <meta property='og:image:height'>")
        self.assertIsNotNone(og_alt, "Missing <meta property='og:image:alt'>")
        self.assertEqual(og_w.get("content"), "1200")
        self.assertEqual(og_h.get("content"), "630")

    def test_og_locale_and_alternate(self):
        """5.7 OG: og:locale is en_IN and og:locale:alternate is kn_IN."""
        og_loc = self.head.find("meta", attrs={"property": "og:locale"})
        og_alt_loc = self.head.find("meta", attrs={"property": "og:locale:alternate"})
        self.assertIsNotNone(og_loc, "Missing <meta property='og:locale'>")
        self.assertIsNotNone(og_alt_loc, "Missing <meta property='og:locale:alternate'>")
        self.assertEqual(og_loc.get("content"), "en_IN")
        self.assertEqual(og_alt_loc.get("content"), "kn_IN")

    # =========================================================================
    # 6. Twitter Cards (>= 5 tests)
    # =========================================================================

    def test_twitter_card_type(self):
        """6.1 Twitter: twitter:card is set to 'summary_large_image'."""
        tw_card = self.head.find("meta", attrs={"name": "twitter:card"})
        self.assertIsNotNone(tw_card, "Missing <meta name='twitter:card'>")
        self.assertEqual(tw_card.get("content"), "summary_large_image")

    def test_twitter_title_present(self):
        """6.2 Twitter: twitter:title exists and contains brand name."""
        tw_title = self.head.find("meta", attrs={"name": "twitter:title"})
        self.assertIsNotNone(tw_title, "Missing <meta name='twitter:title'>")
        self.assertIn("Sri Sai Enterprises", tw_title.get("content", ""))

    def test_twitter_description_present(self):
        """6.3 Twitter: twitter:description exists and describes approvals/heritage."""
        tw_desc = self.head.find("meta", attrs={"name": "twitter:description"})
        self.assertIsNotNone(tw_desc, "Missing <meta name='twitter:description'>")
        self.assertTrue(len(tw_desc.get("content", "").strip()) > 20)

    def test_twitter_image_present(self):
        """6.4 Twitter: twitter:image is an absolute HTTPS URL."""
        tw_img = self.head.find("meta", attrs={"name": "twitter:image"})
        self.assertIsNotNone(tw_img, "Missing <meta name='twitter:image'>")
        img_url = tw_img.get("content", "").strip()
        self.assertTrue(img_url.startswith("https://"), f"twitter:image must be absolute HTTPS: {img_url}")

    def test_twitter_image_alt_present(self):
        """6.5 Twitter: twitter:image:alt exists and is descriptive."""
        tw_alt = self.head.find("meta", attrs={"name": "twitter:image:alt"})
        self.assertIsNotNone(tw_alt, "Missing <meta name='twitter:image:alt'>")
        self.assertTrue(len(tw_alt.get("content", "").strip()) > 5)

    # =========================================================================
    # 7. JSON-LD Schemas (>= 5 tests)
    # =========================================================================

    def test_json_ld_script_exists_and_valid_json(self):
        """7.1 Schema: <script type='application/ld+json'> exists and parses cleanly."""
        blocks = get_json_ld_blocks(self.soup)
        self.assertTrue(len(blocks) > 0, "No <script type='application/ld+json'> tag found in index.html")
        self.assertIsNotNone(self.json_ld, "JSON-LD script failed to parse as valid JSON")

    def test_json_ld_schema_context_and_graph(self):
        """7.2 Schema: Root declares @context='https://schema.org' and '@graph' array."""
        self.assertIsNotNone(self.json_ld, "JSON-LD missing")
        self.assertEqual(self.json_ld.get("@context"), "https://schema.org")
        self.assertIn("@graph", self.json_ld)
        self.assertIsInstance(self.json_ld["@graph"], list)
        self.assertGreaterEqual(len(self.json_ld["@graph"]), 10, "Expected at least 10 graph entities")

    def test_json_ld_localbusiness_entity(self):
        """7.3 Schema: LocalBusiness/Store/ProfessionalService entity has complete credentials."""
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb, "LocalBusiness or Store entity missing in @graph")
        self.assertEqual(lb.get("name"), "Sri Sai Enterprises")
        self.assertEqual(lb.get("telephone"), "+91-9448054185")
        self.assertEqual(lb.get("email"), "smthyagaraj@gmail.com")
        self.assertEqual(lb.get("currenciesAccepted"), "INR")

        # Founder
        founder = lb.get("founder")
        self.assertIsNotNone(founder, "LocalBusiness missing founder object")
        self.assertEqual(founder.get("name"), "S. M. Thyagaraja")

        # Credentials
        credentials = founder.get("hasCredential", [])
        self.assertTrue(len(credentials) >= 2, "Founder missing professional credentials")
        ids = [c.get("identifier") for c in credentials]
        self.assertIn("CA/2009/44120", ids, "Missing COA Registration identifier CA/2009/44120")
        self.assertIn("BCC/BL-3.2.3/S-218/89-90", ids, "Missing BBMP Supervisor identifier BCC/BL-3.2.3/S-218/89-90")

    def test_json_ld_website_entity(self):
        """7.4 Schema: WebSite entity includes valid SearchAction deep-link template."""
        ws = find_entity_by_type(self.graph, "WebSite")
        self.assertIsNotNone(ws, "WebSite entity missing in @graph")
        action = ws.get("potentialAction")
        self.assertIsNotNone(action, "WebSite entity missing potentialAction (SearchAction)")
        self.assertEqual(action.get("@type"), "SearchAction")
        target = action.get("target")
        self.assertIsNotNone(target)
        url_template = target.get("urlTemplate") if isinstance(target, dict) else target
        self.assertIn("?q={search_term_string}", url_template)

    def test_json_ld_breadcrumb_list(self):
        """7.5 Schema: BreadcrumbList contains 6 architectural tiers."""
        bc = find_entity_by_type(self.graph, "BreadcrumbList")
        self.assertIsNotNone(bc, "BreadcrumbList entity missing in @graph")
        items = bc.get("itemListElement", [])
        self.assertEqual(len(items), 6, f"Expected 6 breadcrumb items, found {len(items)}")

    def test_json_ld_catalog_offers(self):
        """7.6 Schema: 6 catalog offerings have INR pricing and valid availability."""
        products = find_entities_by_type(self.graph, "Product")
        if not products:
            products = find_entities_by_type(self.graph, "Service")
        self.assertGreaterEqual(len(products), 6, f"Expected at least 6 catalog products/services, found {len(products)}")

        for prod in products:
            offer = prod.get("offers")
            self.assertIsNotNone(offer, f"Product '{prod.get('name')}' missing offers object")
            self.assertEqual(offer.get("priceCurrency"), "INR")
            self.assertEqual(offer.get("availability"), "https://schema.org/InStock")
            price_val = float(offer.get("price", 0))
            self.assertGreater(price_val, 0, f"Product {prod.get('name')} price must be positive")

    def test_json_ld_faq_page(self):
        """7.7 Schema: FAQPage contains 6 high-intent Q&A entities."""
        faq = find_entity_by_type(self.graph, "FAQPage")
        self.assertIsNotNone(faq, "FAQPage entity missing in @graph")
        main_entity = faq.get("mainEntity", [])
        self.assertEqual(len(main_entity), 6, f"Expected 6 FAQ questions, found {len(main_entity)}")
        for item in main_entity:
            self.assertEqual(item.get("@type"), "Question")
            self.assertTrue(len(item.get("name", "").strip()) > 10)
            ans = item.get("acceptedAnswer")
            self.assertIsNotNone(ans)
            self.assertTrue(len(ans.get("text", "").strip()) > 20)

    def test_json_ld_speakable_specification(self):
        """7.8 Schema: SpeakableSpecification targets key semantic headers."""
        webpage = find_entity_by_type(self.graph, "WebPage")
        self.assertIsNotNone(webpage, "WebPage entity missing in @graph")
        speakable = webpage.get("speakable")
        self.assertIsNotNone(speakable, "WebPage entity missing speakable object")
        self.assertEqual(speakable.get("@type"), "SpeakableSpecification")
        selectors = speakable.get("cssSelector", [])
        self.assertTrue(len(selectors) >= 3, "Speakable must target at least 3 selectors")

    # =========================================================================
    # 8. Bilingual Text Nodes (>= 5 tests)
    # =========================================================================

    def test_bilingual_top_banner(self):
        """8.1 Bilingual: Top bar contains Kannada text for plot eligibility."""
        body_text = self.soup.get_text()
        self.assertIn("ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ", body_text, "Missing Kannada text 'ಅರ್ಹತೆ ಪರಿಶೀಲಿಸಿ' in top bar")

    def test_bilingual_brand_header(self):
        """8.2 Bilingual: Brand header displays both English and Kannada typography."""
        body_text = self.soup.get_text()
        self.assertIn("Sri Sai Enterprises", body_text)
        has_kannada_brand = "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್" in body_text or "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್‌ಪ್ರೈಸಸ್" in body_text
        self.assertTrue(has_kannada_brand, "Missing Kannada brand string 'ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್'")

    def test_bilingual_navigation_links(self):
        """8.3 Bilingual: Navigation links display bilingual descriptors."""
        body_text = self.soup.get_text()
        self.assertTrue(
            "ಮಾರ್ಗದರ್ಶಿ" in body_text or "ಸೇವೆಗಳು" in body_text,
            "Navigation links missing bilingual Kannada labels",
        )

    def test_bilingual_hero_heading(self):
        """8.4 Bilingual: Main hero heading includes Kannada title."""
        h1 = self.soup.find("h1")
        self.assertIsNotNone(h1, "Missing <h1> tag on page")
        h1_text = h1.get_text()
        self.assertIn("ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ", h1_text, "Hero <h1> missing 'ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ'")

    def test_bilingual_cta_buttons(self):
        """8.5 Bilingual: Primary CTA buttons contain dual language text."""
        body_text = self.soup.get_text()
        self.assertIn("ಉಚಿತ ಸಮಾಲೋಚನೆ", body_text, "Missing 'ಉಚಿತ ಸಮಾಲೋಚನೆ' on Consultation button")
        self.assertIn("ನಕ್ಷೆ ಸ್ಥಿತಿ ತಿಳಿಯಿರಿ", body_text, "Missing 'ನಕ್ಷೆ ಸ್ಥಿತಿ ತಿಳಿಯಿರಿ' on Tracking button")

    def test_bilingual_founder_message(self):
        """8.6 Bilingual: Founder section co-presents Kannada translation."""
        body_text = self.soup.get_text()
        self.assertIn(
            "ಕುಟುಂಬದ ಮನೆಯಂತೆಯೇ",
            body_text,
            "Missing Kannada founder statement text 'ಕುಟುಂಬದ ಮನೆಯಂತೆಯೇ'",
        )


if __name__ == "__main__":
    unittest.main()
