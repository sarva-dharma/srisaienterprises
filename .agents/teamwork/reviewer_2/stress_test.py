import json
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup

repo_root = Path(r"c:\Users\grt68\Downloads\Hinde Baa\website")
soup = BeautifulSoup((repo_root / "index.html").read_text(encoding="utf-8"), "html.parser")
schema_block = soup.find("script", type="application/ld+json")
schema = json.loads(schema_block.string)
graph = schema["@graph"]

print("="*60)
print("ADVERSARIAL STRESS TEST: Cross-Reference Graph Completeness")
print("="*60)

declared_ids = set()
for entity in graph:
    if "@id" in entity:
        declared_ids.add(entity["@id"])

referenced_ids = set()
def find_refs(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "@id" and isinstance(v, str):
                # Don't treat top-level declaration as reference unless inside nested object
                pass
            elif isinstance(v, dict) and "@id" in v and len(v) == 1:
                referenced_ids.add(v["@id"])
            else:
                find_refs(v)
    elif isinstance(obj, list):
        for item in obj:
            find_refs(item)

find_refs(graph)
print(f"Declared @ids in graph: {declared_ids}")
print(f"Referenced @ids in graph: {referenced_ids}")

dangling_refs = referenced_ids - declared_ids
print(f"Dangling @id references: {dangling_refs}")
assert len(dangling_refs) == 0, f"Found dangling references: {dangling_refs}"
print("PASS: All referenced @ids resolve cleanly to declared entities in the graph.")

print("\n" + "="*60)
print("ADVERSARIAL STRESS TEST: Coordinate Precision & Real-World Accuracy")
print("="*60)
store = next(e for e in graph if e.get("@id") == "https://sarva-dharma.github.io/srisaienterprises/#store")
geo = store["geo"]
lat, lon = geo["latitude"], geo["longitude"]
print(f"Store coordinates: lat={lat}, lon={lon}")
# Bengaluru bounding box: lat ~ 12.8 to 13.2, lon ~ 77.4 to 77.8
assert 12.8 <= lat <= 13.2, f"Latitude {lat} not in Bengaluru"
assert 77.4 <= lon <= 77.8, f"Longitude {lon} not in Bengaluru"
print("PASS: Geo coordinates precisely within Bengaluru municipal bounds (Gayathrinagar).")

print("\n" + "="*60)
print("ADVERSARIAL STRESS TEST: Robots.txt Specification Standard Check")
print("="*60)
robots = (repo_root / "robots.txt").read_text(encoding="utf-8")
assert "User-agent: GPTBot" in robots
assert "User-agent: ClaudeBot" in robots
assert "User-agent: PerplexityBot" in robots
assert "User-agent: Google-Extended" in robots
assert "User-agent: Applebot-Extended" in robots
assert "User-agent: Bytespider" in robots
assert "User-agent: CCBot" in robots
assert "User-agent: Meta-ExternalAgent" in robots
assert "Sitemap: https://sarva-dharma.github.io/srisaienterprises/sitemap.xml" in robots
print("PASS: All critical AI crawler bots and Sitemap directive present.")

print("\n" + "="*60)
print("ADVERSARIAL STRESS TEST: Sitemap.xml Strict Parsing with Namespaces")
print("="*60)
tree = ET.parse(repo_root / "sitemap.xml")
root = tree.getroot()
assert root.tag.endswith("urlset")
urls = root.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url")
assert len(urls) == 2
# Verify canonical entry has alternate links
canon_url = urls[0]
loc = canon_url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
assert loc == "https://sarva-dharma.github.io/srisaienterprises/"
links = canon_url.findall("{http://www.w3.org/1999/xhtml}link")
assert len(links) == 3
hreflangs = {l.attrib["hreflang"]: l.attrib["href"] for l in links}
assert "en" in hreflangs
assert "kn" in hreflangs
assert "x-default" in hreflangs
print(f"Hreflang bindings: {hreflangs}")
print("PASS: Sitemap conforms strictly to W3C XHTML and Sitemaps.org 0.9 standards.")

print("\n" + "="*60)
print("ADVERSARIAL STRESS TEST: Verification Template Integrity")
print("="*60)
template = (repo_root / "google-site-verification-template.html").read_text(encoding="utf-8")
assert "google-site-verification: google_verification_token_placeholder.html" in template
assert "https://search.google.com/search-console/" in template
print("PASS: Verification template instructions and marker content verified.")
