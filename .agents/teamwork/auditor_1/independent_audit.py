#!/usr/bin/env python3
"""
Independent Forensic Integrity Verification Script
Executed by Forensic Auditor in .agents/teamwork/auditor_1/
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup

def main():
    root = Path(__file__).resolve().parent.parent.parent.parent

    print("=== 1. VERIFYING INDEX.HTML INTEGRITY ===")
    html_path = root / "index.html"
    assert html_path.exists(), "index.html does not exist!"
    html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    # 1. JSON-LD Verification
    scripts = soup.find_all("script", type="application/ld+json")
    assert len(scripts) == 1, f"Expected 1 ld+json script, found {len(scripts)}"
    ld = json.loads(scripts[0].string)
    assert ld["@context"] == "https://schema.org", "Invalid @context"
    graph = ld.get("@graph", [])
    print(f"JSON-LD @graph contains {len(graph)} entities.")
    assert len(graph) >= 10, f"Expected >= 10 entities, found {len(graph)}"

    # Check LocalBusiness
    lbs = [e for e in graph if "LocalBusiness" in e.get("@type") or e.get("@type") == "LocalBusiness" or "Store" in e.get("@type")]
    assert len(lbs) > 0, "Missing LocalBusiness entity"
    lb = lbs[0]
    print(f"LocalBusiness: name='{lb.get('name')}', phone='{lb.get('telephone')}', email='{lb.get('email')}'")
    assert lb["name"] == "Sri Sai Enterprises"
    assert lb["telephone"] == "+91-9448054185"
    assert lb["email"] == "smthyagaraj@gmail.com"
    founder = lb.get("founder", {})
    assert founder.get("name") == "S. M. Thyagaraja"
    creds = [c.get("identifier") for c in founder.get("hasCredential", [])]
    print(f"Founder Credentials: {creds}")
    assert "CA/2009/44120" in creds, "Missing COA license CA/2009/44120"
    assert "BCC/BL-3.2.3/S-218/89-90" in creds, "Missing BBMP supervisor license BCC/BL-3.2.3/S-218/89-90"

    # Check Products / Services
    prods = [e for e in graph if "Product" in e.get("@type") or e.get("@type") == "Product" or "Service" in e.get("@type")]
    print(f"Found {len(prods)} products/services in graph:")
    for p in prods:
        print(f"  - {p.get('name')}: INR {p.get('offers', {}).get('price')} (alternateName: {p.get('alternateName')})")
    assert len(prods) == 6, f"Expected 6 products/services, found {len(prods)}"

    # Check FAQPage
    faqs = [e for e in graph if e.get("@type") == "FAQPage"]
    assert len(faqs) > 0, "Missing FAQPage entity"
    qas = faqs[0].get("mainEntity", [])
    print(f"Found {len(qas)} FAQ questions:")
    for q in qas:
        print(f"  - Q: {q.get('name')}")
    assert len(qas) == 6, f"Expected 6 FAQ questions, found {len(qas)}"

    # Check Semantic Main
    main_tag = soup.find("main", id="main-content")
    assert main_tag is not None, "Missing semantic landmark <main id='main-content'>"
    print("Semantic <main id='main-content'> confirmed present.")

    # Check Head Meta Directives
    head = soup.find("head")
    assert head.find("meta", attrs={"name": "robots"}) is not None, "Missing meta robots"
    assert head.find("meta", attrs={"name": "googlebot"}) is not None, "Missing meta googlebot"
    assert head.find("meta", attrs={"name": "bingbot"}) is not None, "Missing meta bingbot"
    assert head.find("meta", attrs={"name": "google-site-verification"}) is not None, "Missing meta google-site-verification"
    assert head.find("meta", attrs={"name": "msvalidate.01"}) is not None, "Missing meta msvalidate.01"
    assert head.find("link", attrs={"rel": "canonical"}) is not None, "Missing canonical link"
    print("Meta directives & verification tags confirmed present.")

    # Check Bilingual Strings
    assert "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್" in html or "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್‌ಪ್ರೈಸಸ್" in html, "Missing Kannada brand"
    assert "ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ" in html, "Missing Kannada hero heading text"
    assert "ಉಚಿತ ಸಮಾಲೋಚನೆ" in html, "Missing Kannada CTA text"
    print("Bilingual Kannada strings verified present.")

    # Check Interactive DOM IDs
    core_ids = [
        "booking-modal",
        "consultation-booking-form",
        "lead-name",
        "lead-phone",
        "lead-email",
        "jurisdiction-form",
        "jurisdiction-select",
        "fee-estimator",
        "calc-width",
        "calc-length",
        "calc-floors",
        "portal-live-container",
    ]
    for cid in core_ids:
        assert soup.find(id=cid) is not None, f"Missing critical DOM ID: {cid}"
    print(f"All {len(core_ids)} interactive DOM elements verified intact.")

    print("\n=== 2. VERIFYING ROBOTS.TXT INTEGRITY ===")
    robots_path = root / "robots.txt"
    assert robots_path.exists(), "robots.txt missing in root!"
    robots_text = robots_path.read_text(encoding="utf-8")
    assert len(robots_text.strip().splitlines()) >= 50, "robots.txt is unexpectedly short"
    ai_bots = [
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
        "FacebookBot",
        "Applebot",
        "Applebot-Extended",
        "cohere-ai",
        "Diffbot",
    ]
    for bot in ai_bots:
        assert f"User-agent: {bot}" in robots_text, f"Missing User-agent: {bot} in robots.txt"
    print(f"All {len(ai_bots)} AI & GEO crawlers confirmed configured in robots.txt.")
    assert "Sitemap: https://sarva-dharma.github.io/srisaienterprises/sitemap.xml" in robots_text
    assert "Host: sarva-dharma.github.io" in robots_text
    print("Sitemap and Host directives verified.")

    print("\n=== 3. VERIFYING SITEMAP.XML INTEGRITY ===")
    sitemap_path = root / "sitemap.xml"
    assert sitemap_path.exists(), "sitemap.xml missing in root!"
    sitemap_tree = ET.parse(sitemap_path)
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9", "xhtml": "http://www.w3.org/1999/xhtml"}
    root_tag = sitemap_tree.getroot().tag
    assert root_tag == "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset", f"Unexpected root tag: {root_tag}"
    urls = sitemap_tree.findall("s:url", ns)
    assert len(urls) == 2, f"Expected 2 URLs in sitemap, found {len(urls)}"
    loc0 = urls[0].find("s:loc", ns).text
    assert loc0 == "https://sarva-dharma.github.io/srisaienterprises/", f"Unexpected loc: {loc0}"
    links = urls[0].findall("xhtml:link", ns)
    hreflangs = {l.attrib["hreflang"]: l.attrib["href"] for l in links}
    print(f"Primary sitemap URL: {loc0}")
    print(f"hreflang links: {hreflangs}")
    assert set(hreflangs.keys()) == {"en", "kn", "x-default"}
    print("sitemap.xml schema, locations, and hreflang annotations verified.")

    print("\n=== 4. VERIFYING GOOGLE SITE VERIFICATION TEMPLATE ===")
    gsc_path = root / "google-site-verification-template.html"
    assert gsc_path.exists(), "google-site-verification-template.html missing in root!"
    gsc_text = gsc_path.read_text(encoding="utf-8")
    assert "google-site-verification: google_verification_token_placeholder.html" in gsc_text
    print("google-site-verification-template.html confirmed valid.")

    print("\n=======================================================")
    print(">>> INDEPENDENT FORENSIC AUDIT: 100% CLEAN AND VALID <<<")
    print("=======================================================")

if __name__ == "__main__":
    main()
