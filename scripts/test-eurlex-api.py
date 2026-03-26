#!/usr/bin/env python3
"""
EUR-Lex API Response Verification Script
Tests what the SOAP API actually returns for GDPR (CELEX: 32016R0679)
"""

import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Load .env
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            key, val = line.strip().split("=", 1)
            os.environ[key] = val

USERNAME = os.environ.get("EURLEX_USERNAME", "")
PASSWORD = os.environ.get("EURLEX_PASSWORD", "")

if not USERNAME or not PASSWORD:
    print("ERROR: EURLEX_USERNAME and EURLEX_PASSWORD must be set in .env")
    sys.exit(1)

SOAP_ENDPOINT = "https://eur-lex.europa.eu/EURLexWebService"

# Test 1: SOAP API search for GDPR
print("=" * 60)
print("TEST 1: EUR-Lex SOAP API - Search for GDPR")
print("=" * 60)

soap_request = f"""<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:sear="http://eur-lex.europa.eu/search">
  <soap:Body>
    <sear:searchRequest>
      <sear:expertQuery>SELECT DN, TI WHERE DN = 32016R0679</sear:expertQuery>
      <sear:page>1</sear:page>
      <sear:pageSize>1</sear:pageSize>
      <sear:searchLanguage>en</sear:searchLanguage>
    </sear:searchRequest>
  </soap:Body>
</soap:Envelope>"""

try:
    req = urllib.request.Request(
        SOAP_ENDPOINT,
        data=soap_request.encode("utf-8"),
        headers={
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "",
        },
    )
    # Add basic auth
    import base64
    credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    req.add_header("Authorization", f"Basic {credentials}")

    with urllib.request.urlopen(req, timeout=30) as resp:
        status = resp.status
        body = resp.read().decode("utf-8")
        print(f"Status: {status}")
        print(f"Response length: {len(body)} chars")
        # Save full response for inspection
        out_path = Path(__file__).parent / "logs" / "eurlex-soap-response.xml"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(body)
        print(f"Full response saved to: {out_path}")
        # Print first 2000 chars
        print("\n--- Response (first 2000 chars) ---")
        print(body[:2000])
        print("--- End ---\n")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}")
    body = e.read().decode("utf-8", errors="replace")
    print(f"Response: {body[:500]}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: CELLAR REST API - direct document access
print("\n" + "=" * 60)
print("TEST 2: CELLAR REST API - Direct GDPR access (no auth)")
print("=" * 60)

cellar_url = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679"

try:
    req = urllib.request.Request(cellar_url)
    req.add_header("User-Agent", "GDPR-Expert-Bot/1.0")
    with urllib.request.urlopen(req, timeout=30) as resp:
        status = resp.status
        body = resp.read().decode("utf-8")
        print(f"Status: {status}")
        print(f"Response length: {len(body)} chars")
        # Save for inspection
        out_path = Path(__file__).parent / "logs" / "eurlex-html-response.html"
        out_path.write_text(body)
        print(f"Full response saved to: {out_path}")
        # Check for article structure
        import re
        articles = re.findall(r'id="(art_\d+)"', body) or re.findall(r'Article\s+(\d+)', body[:5000])
        print(f"Article references found: {len(articles)} (first 10: {articles[:10]})")
except Exception as e:
    print(f"Error: {e}")

# Test 3: CELLAR REST API - Formex XML via content negotiation
print("\n" + "=" * 60)
print("TEST 3: CELLAR REST API - Formex XML attempt")
print("=" * 60)

# Try CELLAR SPARQL to get the Formex URI first
sparql_url = "https://publications.europa.eu/webapi/rdf/sparql"
sparql_query = """
SELECT ?work ?expression ?format WHERE {
  ?work cdm:resource_legal_id_celex "32016R0679" .
  ?expression cdm:expression_belongs_to_work ?work .
  ?expression cdm:expression_uses_language <http://publications.europa.eu/resource/authority/language/ENG> .
  ?manifestation cdm:manifestation_manifests_expression ?expression .
  ?manifestation cdm:manifestation_type ?format .
} LIMIT 10
"""

try:
    import urllib.parse
    params = urllib.parse.urlencode({
        "query": sparql_query,
        "format": "application/json"
    })
    req = urllib.request.Request(f"{sparql_url}?{params}")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
        import json
        data = json.loads(body)
        bindings = data.get("results", {}).get("bindings", [])
        print(f"SPARQL results: {len(bindings)} bindings")
        for b in bindings[:10]:
            fmt = b.get("format", {}).get("value", "unknown")
            print(f"  Format: {fmt}")
        # Save full response
        out_path = Path(__file__).parent / "logs" / "cellar-sparql-response.json"
        out_path.write_text(json.dumps(data, indent=2))
        print(f"Full response saved to: {out_path}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("Check scripts/logs/ for full responses.")
print("Key question: Does SOAP API return structured XML with article-level data?")
print("If not, we need CELLAR REST + HTML parsing as primary path.")
