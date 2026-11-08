#!/usr/bin/env python3
"""
Independent Comprehensive Victory Audit Verification Script
Executed by Independent Victory Auditor
"""

import ast
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup

def audit_ast(test_files):
    print("=== AST & CHEATING DETECTION AUDIT ===")
    violations = []
    tautological_patterns = [
        "assert True", "assertTrue(True)", "assertEqual(1, 1)", "assertEqual(True, True)"
    ]
    
    for fpath in test_files:
        code = fpath.read_text(encoding="utf-8")
        tree = ast.parse(code, filename=str(fpath))
        
        # Check for empty test methods or hardcoded assert True
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                # Check if body has only 'pass' or return or assert True
                if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                    violations.append(f"{fpath.name}: {node.name} is an empty stub (pass)")
                elif len(node.body) == 1 and isinstance(node.body[0], ast.Assert):
                    test_cond = node.body[0].test
                    if isinstance(test_cond, ast.Constant) and test_cond.value is True:
                        violations.append(f"{fpath.name}: {node.name} has hardcoded assert True")

        # Regex scan for tautologies
        for pat in tautological_patterns:
            if pat in code:
                violations.append(f"{fpath.name} contains literal tautology '{pat}'")

    if violations:
        print(f"FAILED: Found {len(violations)} AST violations:")
        for v in violations:
            print(f"  - {v}")
        return False
    else:
        print(f"PASSED: All {len(test_files)} test files are free of tautological assertions and empty stubs.")
        return True

def audit_requirements(project_root):
    print("\n=== REQUIREMENTS & ACCEPTANCE CRITERIA AUDIT ===")
    issues = []

    # 1. Inspect index.html
    html_file = project_root / "index.html"
    if not html_file.exists():
        issues.append("index.html missing")
        return False
    
    html_text = html_file.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_text, "html.parser")

    # R1: Title & Description
    title = soup.title.string.strip() if soup.title else ""
    if not title:
        issues.append("Title is empty")
    elif not ("Sri Sai Enterprises" in title and "1989" in title):
        issues.append("Title missing brand or year")
    print(f"Title: {title} (Length: {len(title)})")

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if not meta_desc or not meta_desc.get("content"):
        issues.append("Meta description missing")
    else:
        desc_len = len(meta_desc["content"])
        print(f"Meta description: {meta_desc['content']} (Length: {desc_len})")
        if desc_len > 160:
            issues.append(f"Meta description too long: {desc_len} chars > 160")

    # R1: Robots directives in head
    for bot in ["robots", "googlebot", "bingbot"]:
        tag = soup.find("meta", attrs={"name": bot})
        if not tag:
            issues.append(f"Meta tag for {bot} missing")
        else:
            print(f"Found meta {bot}: {tag.get('content')}")

    # R1: Canonical
    canonical = soup.find("link", rel="canonical")
    if not canonical or canonical.get("href") != "https://sarva-dharma.github.io/srisaienterprises/":
        issues.append(f"Invalid canonical URL: {canonical}")
    else:
        print(f"Canonical verified: {canonical['href']}")

    # R1: Hreflang
    hreflangs = {link.get("hreflang"): link.get("href") for link in soup.find_all("link", rel="alternate")}
    for lang in ["en", "kn", "x-default"]:
        if lang not in hreflangs:
            issues.append(f"Missing alternate hreflang for {lang}")
    print(f"Hreflang alternates: {hreflangs}")

    # R1: Open Graph tags
    og_expected = ["og:title", "og:description", "og:type", "og:url", "og:image", "og:site_name", "og:locale", "og:locale:alternate", "og:image:width", "og:image:height"]
    for og in og_expected:
        tag = soup.find("meta", property=og)
        if not tag or not tag.get("content"):
            issues.append(f"Missing OG property: {og}")
    print("Open Graph properties verified.")

    # R1: Twitter cards
    tw_expected = ["twitter:card", "twitter:title", "twitter:description", "twitter:image", "twitter:image:alt"]
    for tw in tw_expected:
        tag = soup.find("meta", attrs={"name": tw})
        if not tag or not tag.get("content"):
            issues.append(f"Missing Twitter property: {tw}")
    print("Twitter Card properties verified.")

    # R1: Local Geo tags
    for geo in ["geo.region", "geo.placename", "geo.position", "ICBM"]:
        tag = soup.find("meta", attrs={"name": geo})
        if not tag or not tag.get("content"):
            issues.append(f"Missing GEO tag: {geo}")
    print("Local GEO tags verified.")

    # R1: Schema.org JSON-LD
    json_scripts = soup.find_all("script", type="application/ld+json")
    if len(json_scripts) != 1:
        issues.append(f"Expected 1 JSON-LD script, found {len(json_scripts)}")
    else:
        try:
            ld = json.loads(json_scripts[0].string)
            graph = ld.get("@graph", [])
            print(f"JSON-LD @graph contains {len(graph)} entities.")
            types = set()
            id_map = {}
            for item in graph:
                t = item.get("@type")
                if isinstance(t, list):
                    for sub in t:
                        types.add(sub)
                else:
                    types.add(t)
                if "@id" in item:
                    id_map[item["@id"]] = item

            # Verify core entity types
            for req_type in ["LocalBusiness", "WebSite", "BreadcrumbList", "Product", "Service", "FAQPage", "WebPage"]:
                if req_type not in types:
                    issues.append(f"Missing schema entity type: {req_type}")
            print(f"Schema types present: {sorted(list(types))}")

            # Verify founder credentials
            store = id_map.get("https://sarva-dharma.github.io/srisaienterprises/#store")
            if not store:
                issues.append("Missing #store entity in graph")
            else:
                founder = store.get("founder")
                creds = [c.get("identifier") for c in founder.get("hasCredential", [])]
                print(f"Founder credentials: {creds}")
                if "CA/2009/44120" not in creds:
                    issues.append("Missing COA registration CA/2009/44120")
                if "BCC/BL-3.2.3/S-218/89-90" not in creds:
                    issues.append("Missing BBMP license BCC/BL-3.2.3/S-218/89-90")

            # Verify Products & Prices
            products = [item for item in graph if "Product" in item.get("@type", []) or item.get("@type") == "Product"]
            print(f"Catalog Products in Schema: {len(products)}")
            if len(products) < 6:
                issues.append(f"Expected 6 products in schema, found {len(products)}")
            for p in products:
                offer = p.get("offers", {})
                price = offer.get("price")
                curr = offer.get("priceCurrency")
                if not price or curr != "INR":
                    issues.append(f"Invalid offer in product {p.get('name')}: {offer}")

            # Verify FAQPage
            faq = id_map.get("https://sarva-dharma.github.io/srisaienterprises/#faq")
            if not faq:
                issues.append("Missing FAQPage in graph")
            else:
                qas = faq.get("mainEntity", [])
                print(f"FAQ Q&A count: {len(qas)}")
                if len(qas) < 6:
                    issues.append(f"Expected 6 FAQ questions, found {len(qas)}")

            # Verify Speakable
            webpage = id_map.get("https://sarva-dharma.github.io/srisaienterprises/#webpage")
            if not webpage or not webpage.get("speakable"):
                issues.append("Missing speakable specification in WebPage")
            else:
                selectors = webpage["speakable"].get("cssSelector", [])
                print(f"Speakable selectors: {selectors}")
                for sel in selectors:
                    matching = soup.select(sel)
                    if not matching:
                        issues.append(f"Speakable selector '{sel}' matches no elements in DOM")

        except Exception as e:
            issues.append(f"JSON-LD parsing exception: {e}")

    # R1: Semantic HTML landmark
    main_tag = soup.find("main", id="main-content")
    if not main_tag:
        issues.append("Missing <main id='main-content'> landmark")
    else:
        print("Semantic <main id='main-content'> landmark confirmed.")

    # R2: External Services Integration
    gsc = soup.find("meta", attrs={"name": "google-site-verification"})
    if not gsc or not gsc.get("content"):
        issues.append("Missing google-site-verification meta tag")
    else:
        print(f"Google Site Verification meta tag: {gsc.get('content')}")

    bing = soup.find("meta", attrs={"name": "msvalidate.01"})
    if not bing or not bing.get("content"):
        issues.append("Missing msvalidate.01 meta tag")
    else:
        print(f"Bing Webmaster meta tag: {bing.get('content')}")

    gsc_file = project_root / "google-site-verification-template.html"
    if not gsc_file.exists():
        issues.append("Missing google-site-verification-template.html")
    else:
        gsc_content = gsc_file.read_text(encoding="utf-8")
        if "google-site-verification:" not in gsc_content:
            issues.append("google-site-verification-template.html missing verification token format")
        print("google-site-verification-template.html verified.")

    # R2: GA4 Script Offline Safety
    ga_scripts = [s for s in soup.find_all("script") if "GA_MEASUREMENT_ID" in (s.string or "")]
    if not ga_scripts:
        issues.append("GA4 integration script missing")
    else:
        ga_text = ga_scripts[0].string
        if "location.protocol === 'file:'" not in ga_text or "G-XXXXXXXXXX" not in ga_text:
            issues.append("GA4 script lacks offline guard or placeholder protection")
        print("GA4 script offline guard verified.")

    # R3: Bilingual Storefront Preservation
    kannada_chars = re.findall(r"[\u0C80-\u0CFF]", html_text)
    print(f"Kannada characters in index.html: {len(kannada_chars)}")
    if len(kannada_chars) < 500:
        issues.append(f"Low Kannada character count: {len(kannada_chars)}")

    # Check key bilingual anchors
    bilingual_phrases = [
        "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್",
        "ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ",
        "ಇ-ಖಾತಾ",
        "ವಾಸ್ತುಶಿಲ್ಪ ವಿನ್ಯಾಸ",
        "ಸಕಾಲ",
    ]
    for phrase in bilingual_phrases:
        if phrase not in html_text:
            issues.append(f"Missing core bilingual phrase: {phrase}")
    print("Bilingual core vocabulary verified.")

    # R3: Interactive DOM element IDs
    dom_ids = [
        "booking-modal",
        "consultation-booking-form",
        "lead-name",
        "lead-phone",
        "lead-email",
        "lead-service",
        "jurisdiction-checker",
        "jurisdiction-form",
        "fee-estimator",
        "portal-live-container",
    ]
    for did in dom_ids:
        if not soup.find(id=did):
            issues.append(f"Missing interactive DOM element #{did}")
    print(f"Interactive DOM IDs verified: {dom_ids}")

    # 2. Inspect robots.txt
    robots_file = project_root / "robots.txt"
    if not robots_file.exists():
        issues.append("robots.txt missing")
    else:
        r_text = robots_file.read_text(encoding="utf-8")
        required_bots = [
            "Googlebot", "Bingbot", "GPTBot", "ChatGPT-User", "OAI-SearchBot",
            "Google-Extended", "ClaudeBot", "anthropic-ai", "Claude-Web",
            "PerplexityBot", "Bytespider", "CCBot", "Meta-ExternalAgent",
            "Applebot", "cohere-ai", "Diffbot"
        ]
        for bot in required_bots:
            if f"User-agent: {bot}" not in r_text:
                issues.append(f"robots.txt missing user-agent {bot}")
        if "Sitemap: https://sarva-dharma.github.io/srisaienterprises/sitemap.xml" not in r_text:
            issues.append("robots.txt missing valid Sitemap directive")
        if "Host: sarva-dharma.github.io" not in r_text:
            issues.append("robots.txt missing Host directive")
        print(f"robots.txt verified with all {len(required_bots)} search & AI bots.")

    # 3. Inspect sitemap.xml
    sitemap_file = project_root / "sitemap.xml"
    if not sitemap_file.exists():
        issues.append("sitemap.xml missing")
    else:
        try:
            tree = ET.parse(sitemap_file)
            root_elem = tree.getroot()
            ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "xhtml": "http://www.1999/xhtml"}
            # Check xmlns
            if "http://www.sitemaps.org/schemas/sitemap/0.9" not in root_elem.tag:
                issues.append("sitemap.xml missing sitemaps 0.9 namespace")
            urls = root_elem.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
            print(f"sitemap.xml contains {len(urls)} URLs")
            if len(urls) < 1:
                issues.append("sitemap.xml has no URLs")
            locs = [u.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text for u in urls]
            if "https://sarva-dharma.github.io/srisaienterprises/" not in locs:
                issues.append("sitemap.xml missing main landing page loc")
        except Exception as e:
            issues.append(f"sitemap.xml parse error: {e}")
        print("sitemap.xml structure verified.")

    # Final tally
    if issues:
        print(f"\nFAILED: Found {len(issues)} requirement issues:")
        for iss in issues:
            print(f"  - {iss}")
        return False
    else:
        print("\nPASSED: 100% of Requirements R1, R2, R3 and Acceptance Criteria satisfied!")
        return True

if __name__ == "__main__":
    proj_root = Path(__file__).resolve().parent.parent.parent.parent
    test_dir = proj_root / "tests"
    test_files = list(test_dir.glob("test_*.py"))
    
    ast_ok = audit_ast(test_files)
    reqs_ok = audit_requirements(proj_root)
    
    if ast_ok and reqs_ok:
        print("\n>>> INDEPENDENT VICTORY AUDITOR VERDICT: ALL AUDITS CLEAN & PASSED <<<")
        sys.exit(0)
    else:
        print("\n>>> INDEPENDENT VICTORY AUDITOR VERDICT: AUDIT FAILED <<<")
        sys.exit(1)
