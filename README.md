# ZenRows vs Zyte Benchmark

Reproducible benchmark script for the article **"Best Zyte Alternatives for Anti-Bot Scraping"** published on zenrows.com.

## What this tests

8 targets at 100 requests per target per platform. Tested June 11, 2026 at 2 req/s.

| # | Target | Protection |
|---|---|---|
| 1 | Amazon product page | Cloudflare + behavioral detection |
| 2 | Glassdoor company page | DataDome |
| 3 | Datanyze | Standard bot protection |
| 4 | Google SERP | Google bot detection |
| 5 | IKEA | Cloudflare |
| 6 | Reuters | None (unprotected) |
| 7 | Python Docs | None (unprotected static) |
| 8 | LinkedIn public profile | Aggressive bot detection |

## Configuration

**ZenRows:** mode=auto on Developer plan ($69/month)

**Zyte:** Default automatic extraction endpoint, no manual tier overrides

## Results summary

| Target | ZenRows | Zyte |
|---|---|---|
| Amazon | 99% | 98% |
| Glassdoor | 99% | 58% |
| Datanyze | 100% | 99% |
| Google SERP | 87% | 0% |
| IKEA | 95% | 99% |
| Reuters | 100% | 68% |
| Python Docs | 100% | 100% |
| LinkedIn | 88% | 0% |
| **Average** | **96%** | **65.3%** |

## Files

- `zenrows_vs_zyte_test.py` — test script
- `benchmark_results_final.csv` — full raw results (2,400 rows)

## How to run

```bash
pip install requests beautifulsoup4
export ZENROWS_API_KEY="your_key"
export ZYTE_API_KEY="your_key"
python3 zenrows_vs_zyte_test.py
```
