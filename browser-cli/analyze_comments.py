"""聚合 + 排序 1054 条评论：每个视频取点赞最高的 N 条 + 全局关键词词频。"""
import json
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")


def parse_likes(s):
    if not s or not s.strip():
        return 0
    s = s.strip().replace(",", "")
    m = re.match(r"([\d.]+)\s*([KMB万千]?)", s, re.IGNORECASE)
    if not m:
        return 0
    n = float(m.group(1))
    unit = m.group(2).upper()
    mult = {"K": 1000, "M": 1000000, "B": 1e9, "万": 10000, "千": 1000}.get(unit, 1)
    return int(n * mult)


with open("C:/Users/yang/desktop/test_project/browser-cli/comments.json", encoding="utf-8") as f:
    data = json.load(f)

print("=" * 80)
print("【按点赞数排序，每个视频取 Top 15 评论】")
print("=" * 80)

for url, info in data.items():
    comments = info.get("comments", [])
    if not comments:
        continue
    for c in comments:
        c["likes_n"] = parse_likes(c.get("likes", ""))
    comments.sort(key=lambda x: x["likes_n"], reverse=True)

    print(f"\n\n### {info['channel']} — {info['title']}")
    print(f"### 共 {len(comments)} 条评论\n")
    for i, c in enumerate(comments[:15], 1):
        print(f"[{c['likes_n']:>5}❤] {c['author']}: {c['text']}")
        print()

# 全局关键词频次
print("\n" + "=" * 80)
print("【全局关键词词频】")
print("=" * 80)

keywords = {
    "看多/Bullish": ["bull", "long", "bullish", "buy", "moon", "rocket", "rally", "看多", "买入", "抄底", "上涨", "突破", "看好", "potential", "to the moon", "all in", "牛", "涨", "🚀", "📈"],
    "看空/Bearish": ["bear", "short", "bearish", "sell", "crash", "dump", "drop", "看空", "做空", "下跌", "崩盘", "套牢", "割肉", "熊", "跌", "📉", "bubble", "泡沫"],
    "焦虑/恐惧": ["scared", "worried", "anxious", "fear", "panic", "risky", "uncertain", "焦虑", "担心", "恐慌", "害怕", "风险", "不安"],
    "乐观/兴奋": ["amazing", "excited", "love", "great", "awesome", "incredible", "兴奋", "看好", "稳了", "牛逼"],
    "Tesla": ["tesla", "tsla", "musk", "马斯克", "特斯拉", "robotaxi", "fsd"],
    "Nvidia": ["nvidia", "nvda", "huang", "黄仁勋", "英伟达", "h100", "h200", "gpu"],
    "Fed/政策": ["fed", "powell", "rate", "inflation", "美联储", "鲍威尔", "降息", "通胀", "warsh"],
    "Trump/政治": ["trump", "tariff", "biden", "tariffs", "川普", "特朗普", "关税", "政策"],
    "AI": ["ai", "deepseek", "openai", "gpt", "chatgpt", "agi", "huawei", "华为"],
    "财报": ["earnings", "report", "quarter", "财报", "季报", "业绩"],
    "Magnificent 7": ["mag 7", "mag7", "magnificent", "七巨头", "amazon", "google", "meta", "apple", "microsoft"],
    "Cash/Hold": ["cash", "hold", "持现", "持仓", "套现", "观望"],
    "Crash/熊市": ["recession", "crash", "bear market", "经济衰退", "熊市", "崩盘"],
    "印度市场": ["india", "indian", "印度", "rupee", "印度股市"],
}

all_text = ""
for info in data.values():
    for c in info.get("comments", []):
        all_text += " " + (c.get("text", "") or "").lower()

for cat, words in keywords.items():
    counts = sum(all_text.count(w.lower()) for w in words)
    print(f"  {cat}: {counts}")
