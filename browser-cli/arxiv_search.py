"""arXiv 搜索量化交易/金融 AI 论文。

arXiv API: http://export.arxiv.org/api/query
分类：
  q-fin.TR  Trading and Market Microstructure
  q-fin.PM  Portfolio Management
  q-fin.ST  Statistical Finance
  q-fin.RM  Risk Management
  q-fin.MF  Mathematical Finance
  cs.LG    + finance 关键词
  cs.CL    + financial NLP
"""
import sys, time, json, re, ssl
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ARXIV_API = "http://export.arxiv.org/api/query"
NS = {"atom": "http://www.w3.org/2005/Atom"}


def fetch(query, max_results=100, sort="submittedDate"):
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": sort,
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "research-tool/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30, context=SSL_CTX) as resp:
            data = resp.read().decode("utf-8")
    except Exception as e:
        return [], f"fetch failed: {e}"

    try:
        root = ET.fromstring(data)
    except Exception as e:
        return [], f"parse failed: {e}"

    papers = []
    for entry in root.findall("atom:entry", NS):
        arxiv_id = entry.find("atom:id", NS).text
        title = (entry.find("atom:title", NS).text or "").strip().replace("\n", " ").replace("  ", " ")
        summary = (entry.find("atom:summary", NS).text or "").strip().replace("\n", " ")
        published = entry.find("atom:published", NS).text
        updated = entry.find("atom:updated", NS).text
        authors = [a.find("atom:name", NS).text for a in entry.findall("atom:author", NS)]
        # 主分类
        cats = [c.get("term") for c in entry.findall("atom:category", NS)]
        papers.append({
            "id": arxiv_id,
            "title": title,
            "summary": summary[:2500],
            "published": published,
            "updated": updated,
            "authors": authors[:8],
            "categories": cats,
            "pdf": arxiv_id.replace("/abs/", "/pdf/") + ".pdf" if "/abs/" in arxiv_id else None,
        })
    return papers, None


# 多个查询：分类查询 + 主题词查询
QUERIES = [
    # 量化金融分类（取最新的）
    ("cat:q-fin.TR", 80),       # Trading & Microstructure
    ("cat:q-fin.PM", 80),       # Portfolio Management
    ("cat:q-fin.ST", 80),       # Statistical Finance
    ("cat:q-fin.RM", 50),       # Risk Management
    # 跨领域搜索
    ("all:\"quantitative trading\" AND cat:cs.LG", 80),
    ("all:\"algorithmic trading\" AND cat:cs.LG", 80),
    ("all:\"stock prediction\" AND cat:cs.LG", 80),
    ("all:\"portfolio optimization\" AND cat:cs.LG", 80),
    ("all:\"limit order book\" AND cat:cs.LG", 50),
    ("all:\"financial time series\" AND cat:cs.LG", 80),
    ("all:\"FinBERT\" OR all:\"FinGPT\" OR all:\"FinLLM\"", 80),
    ("all:\"reinforcement learning\" AND all:\"trading\"", 80),
    ("all:\"alpha factor\" AND cat:cs.LG", 50),
    ("all:\"market regime\" AND cat:cs.LG", 50),
    ("all:\"financial sentiment\"", 80),
    ("all:\"earnings call\" AND cat:cs.LG", 50),
    ("all:\"large language model\" AND all:\"trading\"", 80),
    ("all:\"LLM\" AND all:\"finance\"", 80),
    ("all:\"agent\" AND all:\"trading\" AND cat:cs.AI", 80),
]

all_papers = {}

for q, maxr in QUERIES:
    papers, err = fetch(q, max_results=maxr)
    if err:
        print(f"  [{q}] {err}", file=sys.stderr)
        time.sleep(2)
        continue
    added = 0
    for p in papers:
        pid = p["id"]
        if pid in all_papers:
            continue
        # 过滤年份：保留 2024 之后
        pub_year = int(p["published"][:4])
        if pub_year < 2024:
            continue
        p["matched"] = q
        all_papers[pid] = p
        added += 1
    print(f"  [{q[:50]}] +{added} (累计 {len(all_papers)})", file=sys.stderr)
    time.sleep(2.5)  # arXiv 友好

# 标题相关性过滤
FIN_RE = re.compile(
    r"(stock|trading|portfolio|finan|invest|market|asset|price|volatility|risk|alpha|"
    r"option|future|hedg|arbitr|bond|equit|forex|crypto|economic|"
    r"earnings|fundamental|FinBERT|FinGPT|FinLLM|backtest|sharpe|"
    r"return predict|order book|microstructure|quant|HFT|"
    r"sentiment.*(news|stock|finan)|news.*sentiment)",
    re.IGNORECASE,
)

filtered = []
for pid, p in all_papers.items():
    text = p["title"] + " " + p["summary"][:500]
    if FIN_RE.search(text):
        filtered.append(p)

# 按时间排序
filtered.sort(key=lambda x: x["published"], reverse=True)

print(f"\n总计 {len(all_papers)} 篇 / 金融相关 {len(filtered)} 篇", file=sys.stderr)

out_path = "C:/Users/yang/desktop/test_project/browser-cli/arxiv_papers.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)
print(f"保存到 {out_path}", file=sys.stderr)

# 打印 Top 30
print("\n=== Top 30 by date ===")
for i, p in enumerate(filtered[:30], 1):
    print(f"  {i}. [{p['published'][:10]}] {p['title'][:120]}")
    print(f"     {p['id']}")
