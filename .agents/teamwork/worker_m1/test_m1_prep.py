import json
from bs4 import BeautifulSoup

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("Title:", soup.title.string if soup.title else "None")
print("Meta desc:", soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else "None")
print("Canonical:", soup.find('link', {'rel': 'canonical'})['href'] if soup.find('link', {'rel': 'canonical'}) else "None")
print("Existing JSON-LD:", soup.find_all('script', {'type': 'application/ld+json'}))
print("Main tag present:", soup.find('main'))

roadmap_h4 = soup.select('#construction-roadmap h4')
print(f"Roadmap h4 count: {len(roadmap_h4)}")
for h in roadmap_h4:
    print(" -", h.get_text(strip=True))
