import os
import csv
import time
import json
import base64
import requests
from datetime import datetime
from bs4 import BeautifulSoup

ZENROWS_API_KEY = os.environ.get("ZENROWS_API_KEY", "")
ZYTE_API_KEY = os.environ.get("ZYTE_API_KEY", "")

REQUESTS_PER_TARGET = 100
REQUESTS_PER_SECOND = 2
OUTPUT_CSV = "benchmark_results_part2.csv"

TARGETS = [
    {"name": "ikea_cloudflare", "url": "https://www.ikea.com/"},
    {"name": "reuters_news", "url": "https://www.reuters.com/"},
    {"name": "python_docs", "url": "https://docs.python.org/3/"},
    {"name": "linkedin_profile", "url": "https://www.linkedin.com/in/hamna-ghufran/"},
]

def call_zenrows(url):
    api_url = "https://api.zenrows.com/v1/"
    params = {"apikey": ZENROWS_API_KEY, "url": url, "mode": "auto"}
    start = time.perf_counter()
    try:
        resp = requests.get(api_url, params=params, timeout=60)
        elapsed_ms = (time.perf_counter() - start) * 1000
        status = resp.status_code
        html = resp.text if status == 200 else ""
    except requests.RequestException:
        elapsed_ms = (time.perf_counter() - start) * 1000
        status = 0
        html = ""
    return status, elapsed_ms, html

def call_zyte(url):
    api_url = "https://api.zyte.com/v1/extract"
    auth = base64.b64encode(f"{ZYTE_API_KEY}:".encode()).decode()
    headers = {"Authorization": f"Basic {auth}", "Content-Type": "application/json"}
    payload = {"url": url, "httpResponseBody": True}
    start = time.perf_counter()
    try:
        resp = requests.post(api_url, headers=headers, data=json.dumps(payload), timeout=60)
        elapsed_ms = (time.perf_counter() - start) * 1000
        status = resp.status_code
        html = ""
        if status == 200:
            body = resp.json().get("httpResponseBody", "")
            if body:
                html = base64.b64decode(body).decode(errors="ignore")
    except requests.RequestException:
        elapsed_ms = (time.perf_counter() - start) * 1000
        status = 0
        html = ""
    return status, elapsed_ms, html

def has_valid_title(html):
    if not html:
        return False
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")
    return bool(title_tag and title_tag.get_text(strip=True))

def run_one(target, platform, call_fn):
    rows = []
    s200 = s400 = other = errors = success = 0
    total_time = 0
    delay = 1.0 / REQUESTS_PER_SECOND
    print(f"\n[{platform.upper()}] {target['name']} — starting 100 requests...")
    for i in range(REQUESTS_PER_TARGET):
        req_start = time.perf_counter()
        status, elapsed_ms, html = call_fn(target["url"])
        valid_title = has_valid_title(html)
        total_time += elapsed_ms
        if status == 200 and valid_title:
            success += 1
        if status == 200:
            s200 += 1
        elif status == 400:
            s400 += 1
        elif status == 0:
            errors += 1
        else:
            other += 1
        rows.append({
            "timestamp": datetime.utcnow().isoformat(),
            "platform": platform,
            "target": target["name"],
            "url": target["url"],
            "request_num": i + 1,
            "status_code": status,
            "response_time_ms": round(elapsed_ms, 1),
            "valid_title_found": valid_title,
        })
        print(f"  [{i+1:>3}/100] status={status} title={'yes' if valid_title else 'no'} {elapsed_ms:.0f}ms")
        time_spent = time.perf_counter() - req_start
        sleep_for = delay - time_spent
        if sleep_for > 0:
            time.sleep(sleep_for)
    avg_ms = total_time / REQUESTS_PER_TARGET
    rate = success / REQUESTS_PER_TARGET * 100
    print(f"  DONE — success={rate:.1f}% | 200={s200} 400={s400} other={other} err={errors} | avg={avg_ms:.0f}ms")
    return rows

def run_benchmark():
    all_rows = []
    for target in TARGETS:
        for platform, call_fn in [("zenrows", call_zenrows), ("zyte", call_zyte)]:
            rows = run_one(target, platform, call_fn)
            all_rows.extend(rows)

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
        writer.writeheader()
        writer.writerows(all_rows)
    print(f"\nAll done. Results saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    if not ZENROWS_API_KEY or not ZYTE_API_KEY:
        print("Set ZENROWS_API_KEY and ZYTE_API_KEY environment variables before running.")
    else:
        run_benchmark()
