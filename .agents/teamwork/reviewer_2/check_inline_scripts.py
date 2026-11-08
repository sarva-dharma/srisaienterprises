import subprocess
import tempfile
import os
from bs4 import BeautifulSoup
from pathlib import Path

index_html = Path("index.html").read_text(encoding="utf-8")
soup = BeautifulSoup(index_html, "html.parser")
scripts = soup.find_all("script")

print(f"Total script tags in index.html: {len(scripts)}")
for i, s in enumerate(scripts):
    stype = s.get("type", "")
    src = s.get("src", "")
    if src:
        print(f"Script #{i}: external -> {src}")
        continue
    if stype == "application/ld+json":
        print(f"Script #{i}: application/ld+json (Schema.org)")
        continue
    
    code = s.string or s.get_text()
    if not code.strip():
        continue
    
    # write to temp js and run node --check
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(code)
        temp_name = f.name
    
    try:
        res = subprocess.run(["node", "--check", temp_name], capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Script #{i}: JS syntax valid (length {len(code)} chars)")
        else:
            print(f"Script #{i}: JS syntax ERROR:\n{res.stderr}")
    finally:
        os.remove(temp_name)
