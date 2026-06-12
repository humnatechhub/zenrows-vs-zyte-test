# ZenRows vs Zyte Benchmark

Reproducible benchmark script for the article **"Best Zyte Alternatives for Anti-Bot Scraping"** published on zenrows.com.

## What this tests

8 targets at 100 requests per target per platform. Tested June 11, 2026.

| # | Target | Protection |
|---|--------|------------|
| 1 | Amazon product page | Moderate |
| 2 | Glassdoor company page | DataDome |
| 3 | Idealista property listing | Moderate |
| 4 | Google SERP | Moderate |
| 5 | Footlocker | Cloudflare |
| 6 | BBC News | None |
| 7 | Python Docs | None |
| 8 | LinkedIn profile | Very hard |

## Configuration
- ZenRows: mode=auto
- Zyte: default automatic extraction, no manual tier overrides
- Concurrency: 1 req/s sequential
