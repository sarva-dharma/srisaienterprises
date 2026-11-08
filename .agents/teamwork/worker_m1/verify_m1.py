import sys
import json
from bs4 import BeautifulSoup

def verify_m1():
    print("==================================================")
    print("VERIFICATION SUITE: WORKER M1 (STOREFRONT AUDIT)")
    print("==================================================")
    
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    passed = 0
    total = 0

    def check(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f"[PASS] {name}: {details}")
        else:
            print(f"[FAIL] {name}: {details}")
            sys.exit(1)

    # 1. Title & Meta Description
    title = soup.title.string.strip() if soup.title else ""
    check("Title presence", bool(title), f"Title: {title}")
    check("Title bilingual", "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್" in title and "Sri Sai Enterprises" in title)
    
    meta_desc = soup.find('meta', {'name': 'description'})
    desc_content = meta_desc['content'] if meta_desc else ""
    check("Meta description presence", bool(desc_content), f"Length: {len(desc_content)}")
    check("Meta description < 160 chars", len(desc_content) <= 160, f"Actual length: {len(desc_content)} chars")
    check("Meta description bilingual", "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್" in desc_content and "Sri Sai Enterprises" in desc_content)

    # 2. Robots Directives
    robots = soup.find('meta', {'name': 'robots'})
    check("Robots meta tag", robots and "index, follow" in robots.get('content', ''))
    googlebot = soup.find('meta', {'name': 'googlebot'})
    check("Googlebot meta tag", googlebot and "index, follow" in googlebot.get('content', ''))
    bingbot = soup.find('meta', {'name': 'bingbot'})
    check("Bingbot meta tag", bingbot and "index, follow" in bingbot.get('content', ''))

    # 3. Canonical Tag
    canonical = soup.find('link', {'rel': 'canonical'})
    check("Canonical link", canonical and canonical.get('href') == 'https://sarva-dharma.github.io/srisaienterprises/')

    # 4. Site Verification
    gsc = soup.find('meta', {'name': 'google-site-verification'})
    check("Google site verification tag", gsc and gsc.get('content') == 'GSC_VERIFICATION_TOKEN_PLACEHOLDER')

    # 5. Open Graph Suite
    og_props = {
        'og:title': 'Sri Sai Enterprises | ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್ - Since 1989',
        'og:description': 'Since 1989 (37+ years): Premier Building Plan Approvals, PreDCR CAD Drafting, Architecture, Estimations & Land Surveying across BBMP, GBA & BDA in Bengaluru.',
        'og:type': 'website',
        'og:url': 'https://sarva-dharma.github.io/srisaienterprises/',
        'og:site_name': 'Sri Sai Enterprises | ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್',
        'og:locale': 'en_IN',
        'og:locale:alternate': 'kn_IN',
        'og:image': 'https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg',
        'og:image:secure_url': 'https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg',
        'og:image:width': '1200',
        'og:image:height': '630',
        'og:image:alt': 'Sri Sai Enterprises Bengaluru Building Plan Approvals and Architecture Estd 1989',
    }
    for prop, expected in og_props.items():
        tag = soup.find('meta', {'property': prop})
        check(f"OG tag {prop}", tag and (expected in tag.get('content', '') or tag.get('content') == expected), f"Found: {tag.get('content') if tag else 'None'}")

    # 6. Twitter Cards Suite
    tw_names = {
        'twitter:card': 'summary_large_image',
        'twitter:title': 'Sri Sai Enterprises | Building Plan Approvals & Architecture Since 1989',
        'twitter:image': 'https://sarva-dharma.github.io/srisaienterprises/static/images/bbmp_tower_web.jpg',
        'twitter:image:alt': 'Sri Sai Enterprises Bengaluru Office & Architectural Practice',
    }
    for name, expected in tw_names.items():
        tag = soup.find('meta', {'name': name})
        check(f"Twitter tag {name}", tag and tag.get('content') == expected)

    # 7. Local Geographic & ICBM
    geo_tags = {
        'geo.region': 'IN-KA',
        'geo.placename': 'Bengaluru',
        'geo.position': '12.9965;77.5562',
        'ICBM': '12.9965, 77.5562',
    }
    for name, expected in geo_tags.items():
        tag = soup.find('meta', {'name': name})
        check(f"Geo tag {name}", tag and tag.get('content') == expected)

    # 8. GA4 Safe Script
    ga_script = False
    for s in soup.find_all('script'):
        if s.string and 'GA_MEASUREMENT_ID' in s.string and 'isFileProtocol' in s.string:
            ga_script = True
            break
    check("GA4 safe offline script hook", ga_script)

    # 9. Schema.org JSON-LD Structured Data
    ld_script = soup.find('script', {'type': 'application/ld+json'})
    check("Schema.org script tag presence", bool(ld_script))
    schema = json.loads(ld_script.string)
    check("Schema @context", schema.get('@context') == 'https://schema.org')
    graph = schema.get('@graph', [])
    check("Schema @graph entity count", len(graph) == 11, f"Entities: {len(graph)}")

    # 9a. LocalBusiness
    lb = next((e for e in graph if 'LocalBusiness' in e.get('@type', [])), None)
    check("LocalBusiness entity", lb is not None and lb.get('@id') == 'https://sarva-dharma.github.io/srisaienterprises/#store')
    check("LocalBusiness founder", lb.get('founder', {}).get('name') == 'S. M. Thyagaraja')
    check("LocalBusiness credentials", len(lb.get('founder', {}).get('hasCredential', [])) == 2)
    check("LocalBusiness phone", lb.get('telephone') == '+91-9448054185')
    check("LocalBusiness address", 'Gayathrinagar' in lb.get('address', {}).get('streetAddress', ''))
    check("LocalBusiness coordinates", lb.get('geo', {}).get('latitude') == 12.9965 and lb.get('geo', {}).get('longitude') == 77.5562)

    # 9b. WebSite
    ws = next((e for e in graph if e.get('@type') == 'WebSite'), None)
    check("WebSite entity", ws is not None and ws.get('potentialAction', {}).get('@type') == 'SearchAction')

    # 9c. BreadcrumbList
    bc = next((e for e in graph if e.get('@type') == 'BreadcrumbList'), None)
    check("BreadcrumbList entity", bc is not None and len(bc.get('itemListElement', [])) == 6)

    # 9d. Products / Services
    products = [e for e in graph if isinstance(e.get('@type'), list) and 'Product' in e.get('@type') and 'Service' in e.get('@type')]
    check("Product/Service count", len(products) == 6, f"Found: {len(products)}")
    for p in products:
        offer = p.get('offers', {})
        check(f"Offer for {p.get('@id')}", offer.get('priceCurrency') == 'INR' and float(offer.get('price', 0)) > 0 and offer.get('availability') == 'https://schema.org/InStock')

    # 9e. FAQPage
    faq = next((e for e in graph if e.get('@type') == 'FAQPage'), None)
    check("FAQPage entity", faq is not None and len(faq.get('mainEntity', [])) == 6)

    # 9f. WebPage & Speakable
    wp = next((e for e in graph if e.get('@type') == 'WebPage'), None)
    check("WebPage entity", wp is not None and 'speakable' in wp)
    css_selectors = wp.get('speakable', {}).get('cssSelector', [])
    for sel in css_selectors:
        matched = soup.select(sel)
        check(f"Speakable selector '{sel}' matches DOM", len(matched) > 0)

    # 10. Semantic Structure: <main id="main-content">
    main_tag = soup.find('main', {'id': 'main-content'})
    check("<main id='main-content'> tag exists", main_tag is not None)
    
    # Check that main is between header and footer
    header = soup.find('header')
    footer = soup.find('footer')
    check("Header precedes <main>", header is not None and header.find_next_sibling() == main_tag or main_tag in header.find_next_siblings())
    check("<main> precedes Footer", footer is not None and main_tag.find_next_sibling() == footer or footer in main_tag.find_next_siblings())

    # 11. Heading Hierarchy Normalization
    roadmap_h4 = soup.select('#construction-roadmap h4')
    check("Zero h4 tags in #construction-roadmap", len(roadmap_h4) == 0, f"h4 count: {len(roadmap_h4)}")
    roadmap_h3 = soup.select('#construction-roadmap h3')
    check("5 normalized h3 tags in #construction-roadmap", len(roadmap_h3) == 5, f"h3 count: {len(roadmap_h3)}")

    # 12. Strict Preservation of Interactive & Bilingual Features
    check("Booking modal exists", soup.find('div', {'id': 'booking-modal'}) is not None)
    for field_id in ['lead-name', 'lead-phone', 'lead-email', 'lead-location', 'lead-dimensions', 'lead-service', 'lead-message']:
        check(f"Form field #{field_id} exists", soup.find(id=field_id) is not None)
    
    for calc_id in ['calc-width', 'calc-length', 'calc-floors', 'calc-b-khata', 'calc-locality']:
        check(f"Calculator field #{calc_id} exists", soup.find(id=calc_id) is not None)

    check("Jurisdiction form exists", soup.find(id='jurisdiction-form') is not None)
    check("Jurisdiction select exists", soup.find(id='jurisdiction-select') is not None)
    check("Client portal container exists", soup.find(id='portal-live-container') is not None)

    # Bilingual strings check
    kannada_snippets = [
        "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್",
        "ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ",
        "ಖಾತಾ ಮತ್ತು ನಿವೇಶನ ಪರಿಶೀಲನೆ",
        "ವಾಸ್ತು ಮತ್ತು ಬೈಲಾ ವಿನ್ಯಾಸ",
        "ಆಟೋಡಿಸಿಆರ್ ಸಿಎಡಿ ನಕ್ಷೆ",
        "ಸಕಾಲ ಮಂಜೂರಾತಿ",
        "ಅಂದಾಜು ಪಟ್ಟಿ &amp; ಭೂಮಿಪೂಜೆ",
        "37+ ವರ್ಷಗಳ ನಿರಂತರ ಸೇವೆ"
    ]
    for s in kannada_snippets:
        check(f"Kannada text preserved: '{s}'", s in html)

    print("==================================================")
    print(f"ALL {passed}/{total} VERIFICATION CHECKS PASSED PERFECTLY!")
    print("==================================================")

if __name__ == '__main__':
    verify_m1()
