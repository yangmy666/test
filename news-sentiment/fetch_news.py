"""从 Yahoo Finance RSS 抓取多个标的的新闻。"""
import sys, ssl, json, re
from urllib.request import Request, urlopen
from urllib.parse import quote
import xml.etree.ElementTree as ET
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# Yahoo Finance RSS：https://finance.yahoo.com/rss/headline?s=<TICKER>
TICKERS = [
    "TSLA", "NVDA", "AAPL", "MSFT", "AMZN", "META", "GOOG",  # Mag 7
    "INTC", "AMD", "TSM",                                       # Semis
    "SPY", "QQQ",                                               # Indexes
    "JPM", "BAC",                                               # Banks (for diversity)
]


def fetch_yahoo(ticker):
    url = f"https://finance.yahoo.com/rss/headline?s={ticker}"
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=15, context=SSL_CTX) as resp:
            data = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return [], f"fetch fail: {e}"
    try:
        root = ET.fromstring(data)
    except Exception as e:
        return [], f"parse fail: {e}"

    items = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        desc = (it.findtext("description") or "").strip()
        # 清掉 HTML
        desc = re.sub(r"<[^>]+>", " ", desc).strip()
        link = (it.findtext("link") or "").strip()
        pub = (it.findtext("pubDate") or "").strip()
        items.append({
            "ticker": ticker,
            "title": title,
            "description": desc[:1500],
            "link": link,
            "published": pub,
        })
    return items, None


all_news = []
for t in TICKERS:
    items, err = fetch_yahoo(t)
    if err:
        print(f"  [{t}] {err}", file=sys.stderr)
    else:
        print(f"  [{t}] {len(items)} 条新闻", file=sys.stderr)
        all_news.extend(items)

# 去重（按标题）
seen = set()
deduped = []
for n in all_news:
    key = n["title"][:120]
    if key in seen: continue
    seen.add(key)
    deduped.append(n)

out_path = "C:/Users/yang/desktop/test_project/news-sentiment/news_raw.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(deduped, f, ensure_ascii=False, indent=2)
print(f"\n总计 {len(deduped)} 条唯一新闻", file=sys.stderr)
print(f"保存到 {out_path}", file=sys.stderr)
