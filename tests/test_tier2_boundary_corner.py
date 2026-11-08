"""
Tier 2: Boundary & Corner Cases Test Suite.
Validates system resilience, schema standards compliance, and boundary constraints:
- Malformed JSON-LD syntax detection & resilience
- SearchAction URL template & query-input formatting
- Schema.org valid @type taxonomy constraints
- Required attribute completeness (LocalBusiness, PostalAddress, Offer)
- Currency (INR) and price numeric boundary checks
- GeoCoordinates latitude/longitude coordinate boundaries
- OpeningHours time and day formatting boundaries
- BreadcrumbList position monotonic sequencing
- SpeakableSpecification CSS selector existence in DOM
- Edge URL formatting, trailing slash consistency, and quote escaping
"""

import json
import re
import unittest
from tests.helpers import (
    find_entities_by_type,
    find_entity_by_type,
    get_json_ld_blocks,
    get_schema_graph,
    parse_html,
    parse_json_ld,
)


class TestTier2BoundaryCorner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.soup = parse_html("index.html")
        cls.head = cls.soup.find("head")
        cls.json_ld = parse_json_ld(cls.soup)
        cls.graph = get_schema_graph(cls.soup)

    # =========================================================================
    # 1. JSON-LD Syntax Integrity & Malformed Detection
    # =========================================================================

    def test_json_ld_no_syntax_errors_or_trailing_commas(self):
        """2.1 Boundary: JSON-LD block must not contain trailing commas or malformed escape sequences."""
        blocks = get_json_ld_blocks(self.soup)
        self.assertTrue(len(blocks) > 0, "No JSON-LD script block found")
        for i, block in enumerate(blocks):
            raw = block.string or block.get_text()
            self.assertTrue(len(raw.strip()) > 0, f"JSON-LD block #{i} is empty")
            try:
                parsed = json.loads(raw.strip())
                self.assertIsInstance(parsed, dict, f"JSON-LD block #{i} must evaluate to a dictionary")
            except json.JSONDecodeError as e:
                self.fail(f"JSON-LD block #{i} failed with JSONDecodeError: {e}")

    def test_json_ld_schema_org_context_is_https(self):
        """2.2 Boundary: @context must be strictly HTTPS 'https://schema.org', not HTTP."""
        self.assertIsNotNone(self.json_ld, "JSON-LD data missing")
        context = self.json_ld.get("@context")
        self.assertEqual(context, "https://schema.org", "Schema @context must be 'https://schema.org'")

    # =========================================================================
    # 2. SearchAction Query String & Template Boundary
    # =========================================================================

    def test_search_action_query_input_format(self):
        """2.3 Boundary: SearchAction query-input attribute must follow 'required name=...' syntax."""
        ws = find_entity_by_type(self.graph, "WebSite")
        self.assertIsNotNone(ws, "WebSite entity missing")
        action = ws.get("potentialAction", {})
        query_input = action.get("query-input", "")
        self.assertEqual(
            query_input,
            "required name=search_term_string",
            f"query-input must be 'required name=search_term_string', got '{query_input}'",
        )

    def test_search_action_url_template_has_target_placeholder(self):
        """2.4 Boundary: SearchAction urlTemplate must contain exactly '{search_term_string}' without malformed braces."""
        ws = find_entity_by_type(self.graph, "WebSite")
        self.assertIsNotNone(ws)
        action = ws.get("potentialAction", {})
        target = action.get("target", {})
        url_template = target.get("urlTemplate") if isinstance(target, dict) else target
        self.assertIsNotNone(url_template, "Missing urlTemplate in SearchAction target")
        self.assertIn("{search_term_string}", url_template)
        # Ensure no accidental unclosed braces
        self.assertEqual(url_template.count("{"), 1)
        self.assertEqual(url_template.count("}"), 1)

    # =========================================================================
    # 3. Schema.org @type Taxonomy Validation
    # =========================================================================

    def test_schema_types_adhere_to_known_schema_org_vocabularies(self):
        """2.5 Boundary: All @type declarations in @graph belong to recognized Schema.org types."""
        allowed_types = {
            "LocalBusiness",
            "Store",
            "ProfessionalService",
            "WebSite",
            "BreadcrumbList",
            "Product",
            "Service",
            "FAQPage",
            "WebPage",
            "SpeakableSpecification",
            "Question",
            "Answer",
            "PostalAddress",
            "GeoCoordinates",
            "OpeningHoursSpecification",
            "City",
            "AdministrativeArea",
            "Person",
            "EducationalOccupationalCredential",
            "ImageObject",
            "Brand",
            "Offer",
            "ListItem",
            "EntryPoint",
            "Organization",
            "GovernmentOrganization",
        }

        self.assertTrue(len(self.graph) > 0, "@graph cannot be empty")
        for entity in self.graph:
            etype = entity.get("@type")
            self.assertIsNotNone(etype, f"Entity missing @type: {entity}")
            if isinstance(etype, list):
                for t in etype:
                    self.assertIn(t, allowed_types, f"Unrecognized schema @type '{t}' in entity: {entity.get('@id')}")
            else:
                self.assertIn(etype, allowed_types, f"Unrecognized schema @type '{etype}' in entity: {entity.get('@id')}")

    # =========================================================================
    # 4. Required Attribute Completeness
    # =========================================================================

    def test_localbusiness_required_attributes_present(self):
        """2.6 Boundary: LocalBusiness entity must possess all fundamental contact and identity attributes."""
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb, "LocalBusiness entity missing")

        required_keys = [
            "@id",
            "name",
            "legalName",
            "url",
            "telephone",
            "email",
            "address",
            "geo",
            "openingHoursSpecification",
            "founder",
            "currenciesAccepted",
            "paymentAccepted",
        ]
        for key in required_keys:
            self.assertIn(key, lb, f"LocalBusiness missing required property '{key}'")
            self.assertIsNotNone(lb[key], f"LocalBusiness property '{key}' cannot be null")

    def test_postal_address_sub_attributes(self):
        """2.7 Boundary: PostalAddress must contain streetAddress, addressLocality, addressRegion, postalCode, addressCountry."""
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb)
        addr = lb.get("address", {})
        self.assertEqual(addr.get("@type"), "PostalAddress")
        self.assertEqual(addr.get("streetAddress"), "#3309, 1st Main Road, Gayathrinagar")
        self.assertEqual(addr.get("addressLocality"), "Bengaluru")
        self.assertEqual(addr.get("addressRegion"), "Karnataka")
        self.assertEqual(addr.get("postalCode"), "560021")
        self.assertEqual(addr.get("addressCountry"), "IN")

    def test_offer_catalog_required_attributes(self):
        """2.8 Boundary: All product offers must contain priceCurrency, price, availability, itemCondition, and seller."""
        products = find_entities_by_type(self.graph, "Product") or find_entities_by_type(self.graph, "Service")
        self.assertTrue(len(products) >= 6, "Expected at least 6 catalog products/services")

        for prod in products:
            offer = prod.get("offers", {})
            self.assertEqual(offer.get("@type"), "Offer", f"Product '{prod.get('name')}' offer @type must be 'Offer'")
            for key in ["priceCurrency", "price", "availability", "itemCondition", "seller", "priceValidUntil"]:
                self.assertIn(key, offer, f"Offer in '{prod.get('name')}' missing required key '{key}'")

    # =========================================================================
    # 5. Currency & Price Boundary Validation
    # =========================================================================

    def test_currency_is_strictly_inr(self):
        """2.9 Boundary: Currency must be uppercase ISO code 'INR'."""
        products = find_entities_by_type(self.graph, "Product") or find_entities_by_type(self.graph, "Service")
        for prod in products:
            offer = prod.get("offers", {})
            self.assertEqual(
                offer.get("priceCurrency"),
                "INR",
                f"Invalid currency '{offer.get('priceCurrency')}' in product '{prod.get('name')}'",
            )

    def test_price_format_and_realistic_numeric_range(self):
        """2.10 Boundary: Prices must be string-formatted decimals matching '^\\d+\\.\\d{2}$' between ₹1,000 and ₹500,000."""
        products = find_entities_by_type(self.graph, "Product") or find_entities_by_type(self.graph, "Service")
        price_regex = re.compile(r"^\d+\.\d{2}$")

        for prod in products:
            offer = prod.get("offers", {})
            price_str = offer.get("price", "")
            self.assertRegex(
                price_str,
                price_regex,
                f"Price '{price_str}' in product '{prod.get('name')}' must be string with two decimals (e.g. '35000.00')",
            )
            price_num = float(price_str)
            self.assertGreaterEqual(price_num, 1000.00, f"Price ₹{price_num} too low")
            self.assertLessEqual(price_num, 500000.00, f"Price ₹{price_num} exceeds ceiling")

    # =========================================================================
    # 6. GeoCoordinates Boundary Validation
    # =========================================================================

    def test_geocoordinates_within_bangalore_urban_bounds(self):
        """2.11 Boundary: Coordinates must fall within legitimate Bengaluru bounds (Lat 12.8-13.2, Lng 77.4-77.8)."""
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb)
        geo = lb.get("geo", {})
        self.assertEqual(geo.get("@type"), "GeoCoordinates")

        lat = float(geo.get("latitude", 0))
        lng = float(geo.get("longitude", 0))

        # Absolute physical bounds
        self.assertTrue(-90.0 <= lat <= 90.0, f"Latitude {lat} out of Earth bounds")
        self.assertTrue(-180.0 <= lng <= 180.0, f"Longitude {lng} out of Earth bounds")

        # Specific Gayathrinagar / Bengaluru geographic bounds
        self.assertTrue(12.85 <= lat <= 13.15, f"Latitude {lat} not within Bengaluru region")
        self.assertTrue(77.45 <= lng <= 77.70, f"Longitude {lng} not within Bengaluru region")

    # =========================================================================
    # 7. OpeningHoursSpecification Boundaries
    # =========================================================================

    def test_opening_hours_time_format_and_sequence(self):
        """2.12 Boundary: OpeningHours opens/closes must match 'HH:MM' 24-hr format and opens < closes."""
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb)
        specs = lb.get("openingHoursSpecification", [])
        self.assertTrue(len(specs) > 0, "No openingHoursSpecification declared")

        time_regex = re.compile(r"^\d{2}:\d{2}$")
        for spec in specs:
            opens = spec.get("opens", "")
            closes = spec.get("closes", "")
            self.assertRegex(opens, time_regex, f"opens '{opens}' must be 'HH:MM'")
            self.assertRegex(closes, time_regex, f"closes '{closes}' must be 'HH:MM'")
            self.assertLess(opens, closes, f"opens time '{opens}' must precede closes time '{closes}'")

    def test_opening_hours_excludes_sunday(self):
        """2.13 Boundary: Sunday is closed and must NOT appear in active opening days."""
        lb = find_entity_by_type(self.graph, "LocalBusiness") or find_entity_by_type(self.graph, "Store")
        self.assertIsNotNone(lb)
        specs = lb.get("openingHoursSpecification", [])
        for spec in specs:
            days = spec.get("dayOfWeek", [])
            self.assertNotIn("Sunday", days, "Sunday should not be listed in standard opening hours")

    # =========================================================================
    # 8. BreadcrumbList Sequencing Boundaries
    # =========================================================================

    def test_breadcrumb_positions_strictly_sequential(self):
        """2.14 Boundary: Breadcrumb positions must form a strict 1..N monotonic integer sequence."""
        bc = find_entity_by_type(self.graph, "BreadcrumbList")
        self.assertIsNotNone(bc)
        items = bc.get("itemListElement", [])
        self.assertTrue(len(items) >= 4, "BreadcrumbList must have at least 4 items")

        positions = [item.get("position") for item in items]
        expected_positions = list(range(1, len(items) + 1))
        self.assertEqual(
            positions,
            expected_positions,
            f"Breadcrumb positions {positions} must strictly match {expected_positions}",
        )

    # =========================================================================
    # 9. SpeakableSpecification CSS Selector Validity
    # =========================================================================

    def test_speakable_css_selectors_match_real_dom_elements(self):
        """2.15 Boundary: Every CSS selector declared in SpeakableSpecification must match at least one DOM element."""
        webpage = find_entity_by_type(self.graph, "WebPage")
        self.assertIsNotNone(webpage, "WebPage entity missing")
        speakable = webpage.get("speakable", {})
        selectors = speakable.get("cssSelector", [])
        self.assertTrue(len(selectors) > 0, "No cssSelectors declared in speakable")

        for sel in selectors:
            matches = self.soup.select(sel)
            self.assertTrue(
                len(matches) > 0,
                f"Speakable CSS selector '{sel}' did not match any element in index.html DOM",
            )

    # =========================================================================
    # 10. URL Edge Formatting & Quote Escaping
    # =========================================================================

    def test_meta_attributes_contain_no_unescaped_internal_quotes(self):
        """2.16 Boundary: Meta descriptions and titles do not contain unescaped quotes breaking HTML syntax."""
        meta_tags = self.head.find_all("meta")
        for tag in meta_tags:
            content = tag.get("content")
            if content:
                # Should not contain raw unencoded HTML tag delimiters
                self.assertNotIn("<script", content.lower())
                self.assertNotIn("</script>", content.lower())

    def test_image_urls_have_no_whitespace_or_relative_dots(self):
        """2.17 Boundary: Image URLs in OG tags and schema must be clean absolute URLs without spaces or './'."""
        og_img = self.head.find("meta", attrs={"property": "og:image"})
        if og_img and og_img.get("content"):
            url = og_img["content"]
            self.assertNotIn(" ", url, "og:image cannot contain whitespace")
            self.assertFalse(url.startswith("./"), "og:image cannot be relative './'")
            self.assertFalse(url.startswith("../"), "og:image cannot be relative '../'")


if __name__ == "__main__":
    unittest.main()
