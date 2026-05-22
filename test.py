import requests
import time
import csv
from base64 import b64decode

ZENROWS_API_KEY = "YOUR_ZENROWS_API_KEY"
ZYTE_API_KEY = "YOUR_ZYTE_API_KEY"

URLS = [
    {"name": "Amazon",     "url": "https://www.amazon.com/dp/B09B8YWXDF"},
    {"name": "Glassdoor",  "url": "https://www.glassdoor.com/Overview/Working-at-Google-EI_IE9079.11,17.htm"},
    {"name": "Idealista",  "url": "https://www.idealista.com/en/news/real-estate-in-spain/housing/"},
    {"name": "Google",     "url": "https://www.google.com/search?q=best+web+scraping+api"},
    {"name": "Footlocker", "url": "https://www.footlocker.com/category/sale.html"},
    {"name": "BBC",        "url": "https://www.bbc.com/news/technology"},
    {"name": "PythonDocs", "url": "https://docs.python.org/3/library/requests.html"},
    {"name": "LinkedIn",   "url": "https://www.linkedin.com/in/satyanadella/"},
]

REQUESTS_PER_URL = 10
results = []

print("\n--- Starting ZenRows Tests ---\n")
for target in URLS:
    for i in range(REQUESTS_PER_URL):
        start = time.time()
        try:
            r = requests.get(
                "https://api.zenrows.com/v1/",
                params={
                    "url": target["url"],
                    "apikey": ZENROWS_API_KEY,
                    "mode": "auto",
                },
                timeout=60,
            )
            elapsed = round((time.time() - start) * 1000)
            has_title = "<title>" in r.text.lower()
            status = r.status_code
        except Exception as e:
            elapsed, has_title, status = 0, False, "ERROR"
        results.append({
            "platform": "ZenRows",
            "target": target["name"],
            "request_num": i + 1,
            "status_code": status,
            "has_title": has_title,
            "response_time_ms": elapsed,
        })
        print(f"ZenRows | {target['name']} | #{i+1} | {status} | Title: {has_title} | {elapsed}ms")
        time.sleep(1)

print("\n--- Starting Zyte Tests ---\n")
for target in URLS:
    for i in range(REQUESTS_PER_URL):
        start = time.time()
        try:
            r = requests.post(
                "https://api.zyte.com/v1/extract",
                auth=(ZYTE_API_KEY, ""),
                json={
                    "url": target["url"],
                    "httpResponseBody": True,
                },
                timeout=60,
            )
            elapsed = round((time.time() - start) * 1000)
            html = b64decode(r.json().get("httpResponseBody", "")).decode("utf-8", errors="ignore")
            has_title = "<title>" in html.lower()
            status = r.status_code
        except Exception as e:
            elapsed, has_title, status = 0, False, "ERROR"
        results.append({
            "platform": "Zyte",
            "target": target["name"],
            "request_num": i + 1,
            "status_code": status,
            "has_title": has_title,
            "response_time_ms": elapsed,
        })
        print(f"Zyte | {target['name']} | #{i+1} | {status} | Title: {has_title} | {elapsed}ms")
        time.sleep(1)

with open("results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["platform", "target", "request_num", "status_code", "has_title", "response_time_ms"])
    writer.writeheader()
    writer.writerows(results)

print("\n--- Done! Results saved to results.csv ---")
