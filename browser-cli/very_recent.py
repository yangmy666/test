"""挖掘 2026-03 之后的最新论文（近 60 天内）。"""
import json, re, sys
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

with open("C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_full.json", encoding='utf-8') as f:
    aaai = json.load(f)
with open("C:/Users/yang/desktop/test_project/browser-cli/arxiv_papers.json", encoding='utf-8') as f:
    arxiv = json.load(f)
try:
    with open("C:/Users/yang/desktop/test_project/browser-cli/openreview_papers.json", encoding='utf-8') as f:
        openreview = json.load(f)
except FileNotFoundError:
    openreview = []

cutoff = datetime(2026, 2, 27)  # 60 天前

very_recent = []

# arXiv 有精确日期
for p in arxiv:
    pub = p.get("published","")
    try:
        dt = datetime.fromisoformat(pub.replace("Z","+00:00")).replace(tzinfo=None)
        if dt >= cutoff:
            very_recent.append({
                "src": "arXiv",
                "title": p.get("title",""),
                "abstract": (p.get("summary") or "")[:2000],
                "url": p.get("id",""),
                "date": dt.strftime("%Y-%m-%d"),
            })
    except: pass

# OpenReview 有 cdate
for p in openreview:
    cdate = p.get("cdate", 0)
    if cdate:
        dt = datetime.fromtimestamp(cdate)
        if dt >= cutoff:
            very_recent.append({
                "src": "OpenReview",
                "title": p.get("title",""),
                "abstract": (p.get("abstract") or "")[:2000],
                "url": p.get("id",""),
                "date": dt.strftime("%Y-%m-%d"),
            })

# AAAI 没有精确日期，跳过

# 按日期倒序
very_recent.sort(key=lambda x: x["date"], reverse=True)

# 严格金融过滤
FIN_RE = re.compile(
    r"(stock|trading|portfolio|finan|invest|market|asset.*pric|equity|"
    r"option|hedg|arbitr|crypto|earnings|FinBERT|FinGPT|backtest|sharpe|"
    r"return predict|order book|microstructure|alpha factor|alpha min|HFT|"
    r"volatility|risk manag|hedge fund|asset alloc|trading agent|"
    r"financial llm|financial agent|stock predict|trad.*strateg)",
    re.IGNORECASE,
)
filtered = [p for p in very_recent if FIN_RE.search(p["title"][:200] + " " + p["abstract"][:500])]

print(f"最近 60 天论文: {len(very_recent)}")
print(f"金融相关: {len(filtered)}")

# 写报告
md = []
md.append("# 量化 AI 论文 · 最近 60 天最新（2026-02-27 至今）\n\n")
md.append(f"_共 {len(filtered)} 篇 2026 年最近发表的金融 AI 论文_\n\n")
md.append("> 这些是写本研究时（2026-04-27）正在发酵的最前沿工作。\n")
md.append("> **重要**：这些论文还没经过同行评审或学界共识形成，**质量参差不齐**。\n\n")

md.append("---\n\n## 📅 时间线（按发表日期倒序）\n\n")

# 按月分组
by_month = {}
for p in filtered:
    month = p["date"][:7]
    by_month.setdefault(month, []).append(p)

for month in sorted(by_month.keys(), reverse=True):
    plist = by_month[month]
    md.append(f"\n### {month} ({len(plist)} 篇)\n\n")
    for p in plist:
        md.append(f"**📄 {p['title']}**\n")
        md.append(f"- {p['date']} | {p['src']} | [link]({p['url']})\n")
        md.append(f"- 摘要：{p['abstract'][:600]}{'...' if len(p['abstract']) > 600 else ''}\n\n")

# Top 10 by 摘要长度
top10 = sorted(filtered, key=lambda x: len(x["abstract"]), reverse=True)[:10]

md.append("\n---\n\n## 🏆 Top 10 by 摘要质量（含具体方法和数字）\n\n")
for i, p in enumerate(top10, 1):
    md.append(f"### {i}. {p['title']}\n\n")
    md.append(f"- **{p['date']} | {p['src']}** | [link]({p['url']})\n")
    md.append(f"- 摘要：{p['abstract']}\n\n")

out_path = "C:/Users/yang/desktop/test_project/量化AI论文_最新60天.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("".join(md))

print(f"\n✅ 最新 60 天专题写入 {out_path}")
print(f"   长度: {sum(len(s) for s in md):,} 字符")
print(f"\n=== 最新 5 篇 ===")
for p in filtered[:5]:
    print(f"  [{p['date']}] {p['title'][:90]}")
