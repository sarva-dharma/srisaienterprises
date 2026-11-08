"""
Test Helpers and Utility Functions for Sri Sai Enterprises Automated Test Suite.
Provides resilient file loading, HTML parsing, JSON-LD extraction,
robots.txt parsing, and XML sitemap validation.
"""

import json
import os
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from bs4 import BeautifulSoup


def get_project_root() -> Path:
    """Return the absolute path to the project root directory."""
    return Path(__file__).resolve().parent.parent


def file_exists(filename: str) -> bool:
    """Check if a file exists relative to the project root."""
    path = get_project_root() / filename
    return path.is_file()


def load_file(filename: str) -> str:
    """Load text content of a file relative to project root with UTF-8 encoding."""
    path = get_project_root() / filename
    if not path.is_file():
        raise FileNotFoundError(f"Required project file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_html(filename: str = "index.html") -> BeautifulSoup:
    """Parse an HTML file into a BeautifulSoup tree."""
    content = load_file(filename)
    return BeautifulSoup(content, "html.parser")


def get_json_ld_blocks(soup: BeautifulSoup) -> list:
    """Find all script tags of type application/ld+json."""
    return soup.find_all("script", type="application/ld+json")


def parse_json_ld(soup: BeautifulSoup) -> dict | None:
    """Extract and parse the primary application/ld+json block into a Python dict."""
    scripts = get_json_ld_blocks(soup)
    if not scripts:
        return None
    raw_text = scripts[0].string or scripts[0].get_text()
    if not raw_text or not raw_text.strip():
        return None
    return json.loads(raw_text.strip())


def get_schema_graph(soup: BeautifulSoup) -> list:
    """Extract the @graph array from the primary JSON-LD block, or empty list."""
    data = parse_json_ld(soup)
    if not data or not isinstance(data, dict):
        return []
    return data.get("@graph", [])


def find_entity_by_type(graph: list, target_type: str) -> dict | None:
    """Find the first entity in the @graph matching the target @type (single or array)."""
    for entity in graph:
        etype = entity.get("@type")
        if etype == target_type:
            return entity
        if isinstance(etype, list) and target_type in etype:
            return entity
    return None


def find_entities_by_type(graph: list, target_type: str) -> list:
    """Find all entities in the @graph matching the target @type (single or array)."""
    matches = []
    for entity in graph:
        etype = entity.get("@type")
        if etype == target_type:
            matches.append(entity)
        elif isinstance(etype, list) and target_type in etype:
            matches.append(entity)
    return matches


def parse_robots_txt(filename: str = "robots.txt") -> dict:
    """
    Parse robots.txt into structured dictionary:
    {
      'user_agents': { 'agent_name': {'allow': [...], 'disallow': [...]} },
      'sitemaps': [...],
      'hosts': [...],
      'crawl_delays': [...]
    }
    """
    content = load_file(filename)
    result = {
        "user_agents": {},
        "sitemaps": [],
        "hosts": [],
        "crawl_delays": [],
    }

    current_agents = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" in line:
            key, val = [p.strip() for p in line.split(":", 1)]
            lower_key = key.lower()

            if lower_key == "user-agent":
                agent = val
                if agent not in result["user_agents"]:
                    result["user_agents"][agent] = {"allow": [], "disallow": []}
                current_agents.append(agent)
            elif lower_key == "allow":
                for agent in current_agents:
                    result["user_agents"][agent]["allow"].append(val)
            elif lower_key == "disallow":
                for agent in current_agents:
                    result["user_agents"][agent]["disallow"].append(val)
            elif lower_key == "sitemap":
                result["sitemaps"].append(val)
                current_agents = []
            elif lower_key == "host":
                result["hosts"].append(val)
                current_agents = []
            elif lower_key == "crawl-delay":
                result["crawl_delays"].append(val)

    return result


def parse_sitemap_xml(filename: str = "sitemap.xml") -> list:
    """
    Parse sitemap.xml and return list of url dictionaries:
    [
      {
        'loc': '...',
        'lastmod': '...',
        'changefreq': '...',
        'priority': '...',
        'alternates': [{'hreflang': '...', 'href': '...'}]
      }
    ]
    """
    content = load_file(filename)
    root = ET.fromstring(content)

    # Namespaces
    ns = {
        "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
        "xhtml": "http://www.w3.org/1999/xhtml",
    }

    entries = []
    for url_el in root.findall("sm:url", ns):
        loc_el = url_el.find("sm:loc", ns)
        lastmod_el = url_el.find("sm:lastmod", ns)
        changefreq_el = url_el.find("sm:changefreq", ns)
        priority_el = url_el.find("sm:priority", ns)

        entry = {
            "loc": loc_el.text.strip() if loc_el is not None and loc_el.text else None,
            "lastmod": lastmod_el.text.strip() if lastmod_el is not None and lastmod_el.text else None,
            "changefreq": changefreq_el.text.strip() if changefreq_el is not None and changefreq_el.text else None,
            "priority": priority_el.text.strip() if priority_el is not None and priority_el.text else None,
            "alternates": [],
        }

        for link_el in url_el.findall("xhtml:link", ns):
            entry["alternates"].append({
                "hreflang": link_el.get("hreflang"),
                "href": link_el.get("href"),
                "rel": link_el.get("rel"),
            })

        entries.append(entry)

    return entries
