"""arXiv 专业领域补充搜索：deep hedging, market making, execution etc."""
import sys, time, json, re, ssl
import urllib.request, urllib.parse
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE
NS = {"atom": "http://www.w3.org/2005/Atom"}

with open("C:/Users/yang/desktop/test_project/browser-cli/arxiv_papers.json", encoding="utf-8") as f:
    existing = json.load(f)
existing_ids = {p["id"] for p in existing}
print(f"已有 arXiv {len(existing_ids)} 篇", file=sys.stderr)

def fetch(query, max_results=80):
    params = {"search_query": query, "start": 0, "max_results": max_results,
              "sortBy": "submittedDate", "sortOrder": "descending"}
    url = f"http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "research-tool/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
            data = resp.read().decode("utf-8")
        root = ET.fromstring(data)
    except Exception as e:
        return [], str(e)
    papers = []
    for entry in root.findall("atom:entry", NS):
        arxiv_id = entry.find("atom:id", NS).text
        title = (entry.find("atom:title", NS).text or "").strip().replace("\n", " ")
        summary = (entry.find("atom:summary", NS).text or "").strip().replace("\n", " ")
        published = entry.find("atom:published", NS).text
        authors = [a.find("atom:name", NS).text for a in entry.findall("atom:author", NS)]
        cats = [c.get("term") for c in entry.findall("atom:category", NS)]
        papers.append({"id": arxiv_id, "title": title, "summary": summary[:2500],
                       "published": published, "authors": authors[:8], "categories": cats})
    return papers, None


SPECIALIZED = [
    "all:\"deep hedging\"",
    "all:\"market making\" AND cat:cs.LG",
    "all:\"execution algorithm\" AND cat:cs.LG",
    "all:\"transaction cost\" AND cat:cs.LG",
    "all:\"factor investing\"",
    "all:\"pairs trading\"",
    "all:\"statistical arbitrage\"",
    "all:\"momentum strategy\" AND cat:cs.LG",
    "all:\"contrarian strategy\"",
    "all:\"option pricing\" AND cat:cs.LG",
    "all:\"black-scholes\" AND cat:cs.LG",
    "all:\"VaR\" AND cat:cs.LG",
    "all:\"backtest\" AND cat:cs.LG",
    "all:\"alpha decay\"",
    "all:\"signal generation\" AND all:\"finance\"",
    "all:\"index tracking\" AND cat:cs.LG",
    "all:\"smart beta\"",
    "all:\"risk parity\"",
    "all:\"mean reversion\" AND cat:cs.LG",
    "all:\"price impact\" AND cat:cs.LG",
    "all:\"liquidity\" AND cat:q-fin",
    "all:\"market impact\"",
    "all:\"chinese stock\" OR all:\"chinese market\" AND cat:cs.LG",
    "all:\"a-share\" OR all:\"sse\" OR all:\"szse\"",
    "all:\"crypto trading\" AND cat:cs.LG",
    "all:\"defi\" AND cat:cs.LG",
    "all:\"order flow\" AND cat:cs.LG",
    "all:\"price discovery\" AND cat:cs.LG",
    "all:\"fund manager\" AND cat:cs.LG",
    "all:\"hedge fund\" AND cat:cs.LG",
    "all:\"esg\" AND cat:cs.LG",
    "all:\"options trading\"",
    "all:\"futures trading\" AND cat:cs.LG",
    "all:\"event study\" AND cat:cs.LG",
    "all:\"quant fund\"",
    "all:\"alternative data\"",
    "all:\"time series forecasting\" AND all:\"financial\"",
    "all:\"causal inference\" AND all:\"finance\"",
    "all:\"meta-learning\" AND all:\"trading\"",
    "all:\"continual learning\" AND all:\"finance\"",
    "all:\"contrastive learning\" AND all:\"financial\"",
]

new_papers = {}
for q in SPECIALIZED:
    papers, err = fetch(q, max_results=80)
    if err:
        print(f"  [{q[:50]}] err: {err[:60]}", file=sys.stderr)
        time.sleep(2)
        continue
    added = 0
    for p in papers:
        pid = p["id"]
        if pid in existing_ids or pid in new_papers: continue
        if int(p["published"][:4]) < 2024: continue
        p["matched"] = q
        new_papers[pid] = p
        added += 1
    print(f"  [{q[:60]}] +{added} (新 {len(new_papers)})", file=sys.stderr)
    time.sleep(2.5)

# 合并保存
all_arxiv = list(existing) + list(new_papers.values())

# 标题相关性过滤
FIN_RE = re.compile(
    r"(stock|trading|portfolio|finan|invest|market|asset|price|volatility|risk|alpha|"
    r"option|future|hedg|arbitr|bond|equit|forex|crypto|economic|"
    r"earnings|fundamental|FinBERT|FinGPT|FinLLM|backtest|sharpe|return predict|"
    r"order book|microstructure|quant|HFT|liquidity)",
    re.IGNORECASE,
)
all_arxiv = [p for p in all_arxiv if FIN_RE.search(p["title"] + " " + p["summary"][:500])]

with open("C:/Users/yang/desktop/test_project/browser-cli/arxiv_papers.json", "w", encoding="utf-8") as f:
    json.dump(all_arxiv, f, ensure_ascii=False, indent=2)

print(f"\n总计 {len(all_arxiv)} 篇 (新增 {len(new_papers)})", file=sys.stderr)
