"""OpenReview API 搜索 ICLR 量化金融相关论文。"""
import sys, time, json, re, ssl
import urllib.request, urllib.parse

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# OpenReview API: https://api2.openreview.net/notes/search
def search(query, limit=50):
    url = "https://api2.openreview.net/notes/search?" + urllib.parse.urlencode({
        "query": query,
        "limit": limit,
        "sort": "tmdate:desc",  # 按时间倒序
    })
    req = urllib.request.Request(url, headers={"User-Agent": "research-tool/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}


KEYWORDS = [
    "quantitative trading",
    "stock prediction",
    "portfolio optimization",
    "limit order book",
    "financial sentiment",
    "trading agent",
    "alpha factor",
    "reinforcement learning trading",
    "financial time series",
    "FinBERT",
    "FinGPT",
    "earnings call",
    "stock movement",
]

results = {}
for kw in KEYWORDS:
    res = search(kw, limit=50)
    if "error" in res:
        print(f"  [{kw}] err: {res['error'][:60]}", file=sys.stderr)
        time.sleep(2)
        continue
    notes = res.get("notes", [])
    added = 0
    for n in notes:
        nid = n.get("id")
        if not nid or nid in results: continue
        content = n.get("content", {})
        title = content.get("title", {}).get("value") if isinstance(content.get("title"), dict) else content.get("title", "")
        abstract = content.get("abstract", {}).get("value") if isinstance(content.get("abstract"), dict) else content.get("abstract", "")
        venue = content.get("venue", {}).get("value") if isinstance(content.get("venue"), dict) else content.get("venue", "")
        authors = content.get("authors", {}).get("value") if isinstance(content.get("authors"), dict) else content.get("authors", [])
        # 时间戳
        cdate = n.get("cdate", 0) // 1000  # ms to s
        from datetime import datetime
        year = datetime.fromtimestamp(cdate).year if cdate else None
        if year is None or year < 2024:
            continue
        results[nid] = {
            "id": f"https://openreview.net/forum?id={nid}",
            "title": (title or "").strip(),
            "abstract": (abstract or "").strip()[:2500],
            "year": year,
            "venue": venue,
            "authors": authors[:8] if isinstance(authors, list) else [],
            "cdate": cdate,
        }
        added += 1
    print(f"  [{kw}] +{added} (累计 {len(results)})", file=sys.stderr)
    time.sleep(1.5)

# 标题财金过滤
FIN_RE = re.compile(
    r"(stock|trad|portfolio|finan|invest|market|asset|price|volatil|risk|alpha|"
    r"option|hedg|crypto|earnings|FinBERT|FinGPT|backtest|sharpe|"
    r"return predict|order book|microstructure|HFT)",
    re.IGNORECASE,
)
filtered = {k: v for k, v in results.items() if FIN_RE.search(v["title"] + " " + v["abstract"][:500])}

print(f"\n共 {len(results)} 篇 / 金融相关 {len(filtered)}", file=sys.stderr)

out_path = "C:/Users/yang/desktop/test_project/browser-cli/openreview_papers.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(list(filtered.values()), f, ensure_ascii=False, indent=2)
print(f"保存到 {out_path}", file=sys.stderr)
