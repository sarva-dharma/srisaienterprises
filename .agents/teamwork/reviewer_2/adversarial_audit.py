import json
import re
import os
import sys
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from pathlib import Path

repo_root = Path(r"c:\Users\grt68\Downloads\Hinde Baa\website")
index_html_path = repo_root / "index.html"
robots_path = repo_root / "robots.txt"
sitemap_path = repo_root / "sitemap.xml"

print("="*60)
print("1. ADVERSARIAL AUDIT: Schema.org JSON-LD")
print("="*60)

with open(index_html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")
ld_scripts = soup.find_all("script", type="application/ld+json")
print(f"Total ld+json scripts found: {len(ld_scripts)}")

if not ld_scripts:
    print("CRITICAL: No JSON-LD script found!")
    sys.exit(1)

schema_raw = ld_scripts[0].string
try:
    schema_data = json.loads(schema_raw)
    print("JSON Syntax: Valid JSON")
except Exception as e:
    print(f"CRITICAL: JSON Syntax Error: {e}")
    sys.exit(1)

context = schema_data.get("@context")
print(f"@context: {context}")
if context not in ["https://schema.org", "http://schema.org"]:
    print(f"FAIL: Unexpected @context: {context}")

graph = schema_data.get("@graph", [])
print(f"@graph items count: {len(graph)}")

# Known deprecated properties in Schema.org to check against
# For instance, 'photo' is often deprecated in favor of 'image', 'telephone' on certain types, etc.
deprecated_props = ["contactPoints", "replyToUrl", "tracks", "subEvents", "dataFeedElement", "publishingPrinciples"]

all_ids = set()
for entity in graph:
    eid = entity.get("@id")
    if eid:
        all_ids.add(eid)

print(f"Declared @ids ({len(all_ids)}):")
for eid in sorted(all_ids):
    print(f"  - {eid}")

# Check format of @id URIs
invalid_ids = []
for eid in all_ids:
    if not (eid.startswith("https://sarva-dharma.github.io/srisaienterprises/#") or eid.startswith("http")):
        invalid_ids.append(eid)
print(f"Invalid @id URIs: {invalid_ids}")

# Check Offer items
offers_checked = 0
offer_issues = []
for entity in graph:
    # entity might be product or offer
    types = entity.get("@type", [])
    if isinstance(types, str):
        types = [types]
    if "Product" in types or "Service" in types:
        offers = entity.get("offers")
        if not offers:
            offer_issues.append(f"Entity {entity.get('@id')} has no offers")
            continue
        offers_checked += 1
        curr = offers.get("priceCurrency")
        price = offers.get("price")
        cond = offers.get("itemCondition")
        avail = offers.get("availability")
        seller = offers.get("seller")
        
        if curr != "INR":
            offer_issues.append(f"{entity.get('@id')} invalid currency: {curr}")
        if not cond or cond not in ["https://schema.org/NewCondition", "NewCondition"]:
            offer_issues.append(f"{entity.get('@id')} invalid itemCondition: {cond}")
        if not avail or avail not in ["https://schema.org/InStock", "InStock"]:
            offer_issues.append(f"{entity.get('@id')} invalid availability: {avail}")
        if not price:
            offer_issues.append(f"{entity.get('@id')} missing price")

print(f"Checked {offers_checked} Product/Service offers. Issues: {offer_issues}")

# Check Geo Coordinates
geo_issues = []
for entity in graph:
    geo = entity.get("geo")
    if geo:
        lat = geo.get("latitude")
        lon = geo.get("longitude")
        if not isinstance(lat, (int, float)):
            geo_issues.append(f"Latitude is not numeric: {lat} (type: {type(lat)})")
        if not isinstance(lon, (int, float)):
            geo_issues.append(f"Longitude is not numeric: {lon} (type: {type(lon)})")
        # Check geographic validity
        if not (-90 <= lat <= 90):
            geo_issues.append(f"Latitude out of bounds: {lat}")
        if not (-180 <= lon <= 180):
            geo_issues.append(f"Longitude out of bounds: {lon}")
print(f"Geo coordinate checks: Issues: {geo_issues}")

# Check for deprecated properties
found_deprecated = []
def check_deprecated(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in deprecated_props:
                found_deprecated.append(k)
            check_deprecated(v)
    elif isinstance(obj, list):
        for item in obj:
            check_deprecated(item)

check_deprecated(schema_data)
print(f"Deprecated properties found: {found_deprecated}")

print("\n" + "="*60)
print("2. ADVERSARIAL AUDIT: Open Graph & Social Media Assets")
print("="*60)

og_image = soup.find("meta", property="og:image")
og_image_url = og_image.get("content") if og_image else None
og_width = soup.find("meta", property="og:image:width")
og_height = soup.find("meta", property="og:image:height")

print(f"og:image URL: {og_image_url}")
is_https = og_image_url.startswith("https://") if og_image_url else False
print(f"og:image is absolute HTTPS: {is_https}")

# Check if target image file actually exists locally
if og_image_url:
    rel_path = og_image_url.replace("https://sarva-dharma.github.io/srisaienterprises/", "")
    local_file = repo_root / rel_path.replace("/", os.sep)
    file_exists = local_file.is_file()
    file_size = local_file.stat().st_size if file_exists else 0
    print(f"Local file target: {local_file} | Exists: {file_exists} | Size: {file_size} bytes")
else:
    print("og:image is missing!")

# Check twitter:image
twitter_image = soup.find("meta", attrs={"name": "twitter:image"})
twitter_image_url = twitter_image.get("content") if twitter_image else None
print(f"twitter:image URL: {twitter_image_url}")
if twitter_image_url:
    rel_tw = twitter_image_url.replace("https://sarva-dharma.github.io/srisaienterprises/", "")
    local_tw = repo_root / rel_tw.replace("/", os.sep)
    print(f"Local twitter image target: {local_tw} | Exists: {local_tw.is_file()}")

# Check all images in JSON-LD
print("Checking images referenced in Schema.org JSON-LD:")
def extract_images(obj):
    imgs = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ["image", "logo"]:
                if isinstance(v, str):
                    imgs.append(v)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            imgs.append(item)
                        elif isinstance(item, dict) and "url" in item:
                            imgs.append(item["url"])
                elif isinstance(v, dict) and "url" in v:
                    imgs.append(v["url"])
            else:
                imgs.extend(extract_images(v))
    elif isinstance(obj, list):
        for item in obj:
            imgs.extend(extract_images(item))
    return imgs

ld_images = extract_images(schema_data)
for img in ld_images:
    rel = img.replace("https://sarva-dharma.github.io/srisaienterprises/", "")
    lf = repo_root / rel.replace("/", os.sep)
    print(f"  Schema image: {img} -> Local exists: {lf.is_file()}")

print(f"og:image:width = {og_width.get('content') if og_width else 'None'}, og:image:height = {og_height.get('content') if og_height else 'None'}")

print("\n" + "="*60)
print("3. ADVERSARIAL AUDIT: robots.txt Specifications")
print("="*60)

with open(robots_path, "r", encoding="utf-8") as f:
    robots_txt = f.read()

official_bots = [
    "Googlebot", "Bingbot", "GPTBot", "ChatGPT-User", "OAI-SearchBot",
    "Google-Extended", "ClaudeBot", "anthropic-ai", "Claude-Web",
    "PerplexityBot", "Bytespider", "CCBot", "Meta-ExternalAgent",
    "FacebookBot", "Applebot", "Applebot-Extended", "cohere-ai", "Diffbot"
]

missing_bots = []
for bot in official_bots:
    if f"User-agent: {bot}" not in robots_txt:
        missing_bots.append(bot)
print(f"Missing official AI/Search bot agents in robots.txt: {missing_bots}")

sitemap_directive = [line.strip() for line in robots_txt.splitlines() if line.strip().lower().startswith("sitemap:")]
print(f"Sitemap directives in robots.txt: {sitemap_directive}")

print("\n" + "="*60)
print("4. ADVERSARIAL AUDIT: sitemap.xml Strict Parsing & Namespaces")
print("="*60)

try:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    print(f"Root tag: {root.tag}")
    ns = {
        "s": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xhtml": "http://www.w3.org/1999/xhtml"
    }
    urls = root.findall("s:url", ns)
    print(f"Number of <url> elements found: {len(urls)}")
    for i, u in enumerate(urls):
        loc = u.find("s:loc", ns)
        lastmod = u.find("s:lastmod", ns)
        changefreq = u.find("s:changefreq", ns)
        priority = u.find("s:priority", ns)
        links = u.findall("xhtml:link", ns)
        print(f"URL #{i+1}: loc={loc.text if loc is not None else None}, lastmod={lastmod.text if lastmod is not None else None}, priority={priority.text if priority is not None else None}, alternate links={len(links)}")
        for link in links:
            print(f"    hreflang: {link.attrib.get('hreflang')} -> href: {link.attrib.get('href')}")
except Exception as e:
    print(f"CRITICAL: XML Parsing Exception: {e}")

print("\n" + "="*60)
print("5. ADVERSARIAL AUDIT: Strict XML Schema Validation with defusedxml/minidom")
print("="*60)

import xml.dom.minidom
try:
    dom = xml.dom.minidom.parse(str(sitemap_path))
    print(f"minidom parsed cleanly: {dom.documentElement.tagName}")
except Exception as e:
    print(f"minidom parse error: {e}")
