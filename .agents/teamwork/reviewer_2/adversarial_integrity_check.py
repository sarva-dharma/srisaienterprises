import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

repo_root = Path(r"c:\Users\grt68\Downloads\Hinde Baa\website")
index_html = (repo_root / "index.html").read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")

print("="*60)
print("1. VERIFYING SCHEMA.ORG SPEAKABLE SELECTORS")
print("="*60)

ld_script = soup.find("script", type="application/ld+json")
schema = json.loads(ld_script.string)

speakable_selectors = []
for entity in schema.get("@graph", []):
    if "speakable" in entity:
        sp = entity["speakable"]
        if "cssSelector" in sp:
            speakable_selectors = sp["cssSelector"]

print(f"Speakable selectors declared: {speakable_selectors}")
for sel in speakable_selectors:
    found = soup.select(sel)
    print(f"Selector '{sel}': Found {len(found)} elements")
    if found:
        print(f"   Text sample: {found[0].get_text(strip=True)[:60]}...")
    else:
        print(f"   FAIL: Selector '{sel}' matches nothing in the DOM!")

print("\n" + "="*60)
print("2. VERIFYING BREADCRUMB ANCHORS IN DOM")
print("="*60)

breadcrumbs = []
for entity in schema.get("@graph", []):
    if entity.get("@type") == "BreadcrumbList":
        breadcrumbs = entity.get("itemListElement", [])

for b in breadcrumbs:
    item_url = b.get("item", "")
    if "#" in item_url:
        fragment = item_url.split("#")[1]
        elem = soup.find(id=fragment)
        print(f"Anchor #{fragment} -> Found in DOM: {elem is not None}")
        if not elem:
            print(f"   FAIL: Missing anchor element with id='{fragment}'")

print("\n" + "="*60)
print("3. VERIFYING SEARCHACTION QUERY INPUT & TARGET")
print("="*60)

for entity in schema.get("@graph", []):
    if entity.get("@type") == "WebSite":
        action = entity.get("potentialAction", {})
        target = action.get("target", {})
        url_template = target.get("urlTemplate", "")
        query_input = action.get("query-input", "")
        print(f"urlTemplate: {url_template}")
        print(f"query-input: {query_input}")
        if "search_term_string" in url_template and "search_term_string" in query_input:
            print("SearchAction template parameter matches query-input parameter: PASS")
        else:
            print("FAIL: Parameter mismatch in SearchAction")

print("\n" + "="*60)
print("4. ADVERSARIAL INTEGRITY AUDIT OF TEST SUITE CODE")
print("="*60)

test_files = list((repo_root / "tests").glob("*.py"))
print(f"Discovered {len(test_files)} test files:")

dummy_assertions = []
hardcoded_shortcuts = []

for tf in test_files:
    content = tf.read_text(encoding="utf-8")
    lines = content.splitlines()
    for i, line in enumerate(lines, 1):
        clean = line.strip()
        # Check for dummy assertions
        if clean in ["self.assertTrue(True)", "assert True", "self.assertEqual(1, 1)", "self.assertEqual(True, True)"]:
            dummy_assertions.append((tf.name, i, clean))
        # Check for cheating or bypassing logic
        if "pass  #" in clean or "return True" in clean and "def test_" in lines[max(0, i-2)]:
            hardcoded_shortcuts.append((tf.name, i, clean))

print(f"Dummy assertions found: {len(dummy_assertions)}")
for item in dummy_assertions:
    print(f"  {item}")

print(f"Hardcoded bypass shortcuts found: {len(hardcoded_shortcuts)}")
for item in hardcoded_shortcuts:
    print(f"  {item}")

print("\n" + "="*60)
print("5. VERIFYING BILINGUAL TEXT PERSISTENCE (Kannada & English)")
print("="*60)

# Check essential Kannada phrases in index.html
kannada_samples = [
    "ಶ್ರೀ ಸಾಯಿ ಎಂಟರ್ ಪ್ರೈಸಸ್",
    "ಕಟ್ಟಡ ನಕ್ಷೆ ಮಂಜೂರಾತಿ",
    "ಖಾತಾ ಮತ್ತು ನಿವೇಶನ ಪರಿಶೀಲನೆ",
    "ವಾಸ್ತು ಮತ್ತು ಬೈಲಾ ವಿನ್ಯಾಸ",
    "ಆಟೋಡಿಸಿಆರ್ ಸಿಎಡಿ ನಕ್ಷೆ",
    "ಸಕಾಲ ಮಂಜೂರಾತಿ",
    "ಮುಖಪುಟ"
]

for phrase in kannada_samples:
    present = phrase in index_html
    print(f"Phrase '{phrase}': Present = {present}")
    if not present:
        print(f"   FAIL: Missing critical Kannada string '{phrase}'")
