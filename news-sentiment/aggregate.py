"""聚合分析：按标的、按事件类型、按方向汇总情绪信号。"""
import json, sys
from collections import defaultdict
from statistics import mean, median

sys.stdout.reconfigure(encoding="utf-8")

with open("C:/Users/yang/desktop/test_project/news-sentiment/news_analyzed.json", encoding="utf-8") as f:
    data = json.load(f)

# 只保留有 analysis 的
analyzed = [d for d in data if "analysis" in d]
print(f"有效分析: {len(analyzed)} / {len(data)}")

# === 按标的聚合 ===
ticker_signals = defaultdict(list)
for d in analyzed:
    a = d["analysis"]
    for t in a.get("tickers", []):
        ticker_signals[t].append(a)

print("\n" + "=" * 70)
print(f"{'Ticker':<8} {'#News':>6} {'AvgSent':>9} {'MedSent':>9} {'BullPct':>8} {'BearPct':>8} {'AvgConf':>8}")
print("=" * 70)
for ticker in sorted(ticker_signals.keys(), key=lambda t: -len(ticker_signals[t])):
    sigs = ticker_signals[ticker]
    if len(sigs) < 2: continue
    sentiments = [s["sentiment"] for s in sigs]
    confidences = [s["confidence"] for s in sigs]
    bull_pct = sum(1 for s in sigs if s["direction"] == "up") / len(sigs)
    bear_pct = sum(1 for s in sigs if s["direction"] == "down") / len(sigs)
    print(
        f"{ticker:<8} {len(sigs):>6} "
        f"{mean(sentiments):>+9.2f} {median(sentiments):>+9.2f} "
        f"{bull_pct:>7.0%} {bear_pct:>7.0%} {mean(confidences):>7.2f}"
    )

# === 按事件类型 ===
event_count = defaultdict(int)
for d in analyzed:
    event_count[d["analysis"]["event_type"]] += 1

print("\n=== 事件类型分布 ===")
for et, n in sorted(event_count.items(), key=lambda x: -x[1]):
    print(f"  {et:12s} {n:>3}")

# === 净信号（高置信度）===
print("\n=== 高置信度净看多（conf>=0.7 & sentiment>0.3）===")
hi_bull = [d for d in analyzed if d["analysis"]["confidence"] >= 0.7 and d["analysis"]["sentiment"] > 0.3 and d["analysis"]["direction"] == "up"]
for d in hi_bull[:10]:
    a = d["analysis"]
    print(f"  [{','.join(a['tickers'][:3])}] {d['title'][:90]}")
    print(f"    sent={a['sentiment']:+.2f} conf={a['confidence']:.2f} → {a['reasoning'][:100]}")

print("\n=== 高置信度净看空（conf>=0.7 & sentiment<-0.3）===")
hi_bear = [d for d in analyzed if d["analysis"]["confidence"] >= 0.7 and d["analysis"]["sentiment"] < -0.3 and d["analysis"]["direction"] == "down"]
for d in hi_bear[:10]:
    a = d["analysis"]
    print(f"  [{','.join(a['tickers'][:3])}] {d['title'][:90]}")
    print(f"    sent={a['sentiment']:+.2f} conf={a['confidence']:.2f} → {a['reasoning'][:100]}")

# === 写汇总 markdown ===
md = []
md.append("# 美股新闻情绪分析报告\n\n")
md.append(f"_基于 Claude API 对 {len(analyzed)} 条新闻的结构化分析_\n\n")

md.append("## 📊 按标的聚合\n\n")
md.append("| 标的 | 新闻数 | 平均情绪 | 中位情绪 | 看多% | 看空% | 平均信心 |\n")
md.append("|---|---:|---:|---:|---:|---:|---:|\n")
for ticker in sorted(ticker_signals.keys(), key=lambda t: -len(ticker_signals[t])):
    sigs = ticker_signals[ticker]
    if len(sigs) < 2: continue
    sentiments = [s["sentiment"] for s in sigs]
    confidences = [s["confidence"] for s in sigs]
    bull_pct = sum(1 for s in sigs if s["direction"] == "up") / len(sigs)
    bear_pct = sum(1 for s in sigs if s["direction"] == "down") / len(sigs)
    md.append(f"| **{ticker}** | {len(sigs)} | {mean(sentiments):+.2f} | {median(sentiments):+.2f} | {bull_pct:.0%} | {bear_pct:.0%} | {mean(confidences):.2f} |\n")

md.append("\n## 🔥 高置信度看多信号\n\n")
for d in hi_bull[:15]:
    a = d["analysis"]
    md.append(f"### {d['title'][:120]}\n")
    md.append(f"- **{','.join(a['tickers'])}** | sent {a['sentiment']:+.2f} | conf {a['confidence']:.2f} | {a['event_type']} | {a['horizon']}\n")
    md.append(f"- {a['reasoning']}\n")
    if a.get("key_facts"):
        for f in a["key_facts"][:3]:
            md.append(f"  - {f}\n")
    md.append(f"- [link]({d['link']})\n\n")

md.append("\n## 📉 高置信度看空信号\n\n")
for d in hi_bear[:15]:
    a = d["analysis"]
    md.append(f"### {d['title'][:120]}\n")
    md.append(f"- **{','.join(a['tickers'])}** | sent {a['sentiment']:+.2f} | conf {a['confidence']:.2f} | {a['event_type']} | {a['horizon']}\n")
    md.append(f"- {a['reasoning']}\n")
    if a.get("key_facts"):
        for f in a["key_facts"][:3]:
            md.append(f"  - {f}\n")
    md.append(f"- [link]({d['link']})\n\n")

out_md = "C:/Users/yang/desktop/test_project/news-sentiment/sentiment_report.md"
with open(out_md, "w", encoding="utf-8") as f:
    f.write("".join(md))
print(f"\n📝 markdown 报告: {out_md}")
