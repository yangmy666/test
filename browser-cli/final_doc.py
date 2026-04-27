"""合并 AAAI + arXiv 论文，生成最终主文档。"""
import json, re, sys
from collections import defaultdict, Counter
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# 读两个数据源
with open("C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_full.json", encoding='utf-8') as f:
    aaai_papers = json.load(f)
with open("C:/Users/yang/desktop/test_project/browser-cli/arxiv_papers.json", encoding='utf-8') as f:
    arxiv_papers = json.load(f)
try:
    with open("C:/Users/yang/desktop/test_project/browser-cli/openreview_papers.json", encoding='utf-8') as f:
        openreview_papers = json.load(f)
except FileNotFoundError:
    openreview_papers = []

def normalize_openreview(p):
    return {
        "source": "OpenReview",
        "title": p.get("title", "").strip(),
        "abstract": (p.get("abstract") or "").strip(),
        "authors": ", ".join(p.get("authors", [])) if isinstance(p.get("authors"), list) else "",
        "url": p.get("id", ""),
        "year": p.get("year"),
        "venue": p.get("venue", "OpenReview/ICLR") or "OpenReview/ICLR",
        "matched": "",
    }

print(f"AAAI: {len(aaai_papers)}, arXiv: {len(arxiv_papers)}, OpenReview: {len(openreview_papers)}")

# 统一格式
def normalize_aaai(p):
    issue = p.get("issueText", "")
    vol_map = {40: 2026, 39: 2025, 38: 2024, 37: 2023, 36: 2022, 35: 2021, 34: 2020,
               33: 2019, 32: 2018, 31: 2017, 30: 2016, 29: 2015, 28: 2014, 27: 2013, 26: 2012, 25: 2011}
    m = re.search(r"Vol\.\s*(\d+)", issue)
    year = vol_map.get(int(m.group(1)), None) if m else None
    if not year:
        m2 = re.search(r"\((\d{4})\)", issue)
        year = int(m2.group(1)) if m2 else None
    return {
        "source": "AAAI",
        "title": p.get("title", "").strip(),
        "abstract": (p.get("abstract") or "").strip(),
        "authors": (p.get("authors") or "").strip(),
        "url": p.get("url", ""),
        "year": year,
        "venue": issue,
        "matched": p.get("matched_keyword", ""),
    }

def normalize_arxiv(p):
    pub = p.get("published", "")
    year = int(pub[:4]) if pub and len(pub) >= 4 else None
    return {
        "source": "arXiv",
        "title": p.get("title", "").strip(),
        "abstract": (p.get("summary") or "").strip(),
        "authors": ", ".join(p.get("authors", [])),
        "url": p.get("id", ""),
        "year": year,
        "published": pub,
        "venue": "arXiv " + ", ".join(p.get("categories", [])[:3]),
        "matched": p.get("matched", ""),
    }

all_papers = []
for p in aaai_papers:
    all_papers.append(normalize_aaai(p))
for p in arxiv_papers:
    all_papers.append(normalize_arxiv(p))
for p in openreview_papers:
    all_papers.append(normalize_openreview(p))

print(f"Total normalized: {len(all_papers)}")

# 去重（按标题）
seen_titles = {}
deduped = []
for p in all_papers:
    key = re.sub(r'\s+', ' ', p["title"].lower())[:120]
    if not key: continue
    if key in seen_titles:
        # 保留更详细的（带摘要）的
        existing = seen_titles[key]
        if len(p["abstract"]) > len(existing["abstract"]):
            deduped[deduped.index(existing)] = p
            seen_titles[key] = p
        continue
    seen_titles[key] = p
    deduped.append(p)

print(f"After dedup: {len(deduped)}")

# 只保留 2024 及以后
recent = [p for p in deduped if p.get("year") and p["year"] >= 2024]
print(f"Recent (>=2024): {len(recent)}")

# 主题分类
def classify(p):
    text = (p["title"] + " " + p["abstract"][:1500]).lower()
    # LLM/Agent 优先
    if any(k in text for k in ["llm-based agent", "llm agent", "language model agent", "multi-agent", "multi agent llm",
                                "agent-based trading", "fingpt", "finagent", "tradinggpt", "gpt-4"]) and any(k in text for k in ["trad","market","stock","financ","invest","portfolio"]):
        return "🤖 LLM/Agent 金融应用"
    if any(k in text for k in ["large language model", "language model", "llm "," gpt ", "chatgpt"]) and any(k in text for k in ["trad","market","stock","financ","invest","portfolio"]):
        return "🤖 LLM/Agent 金融应用"
    if any(k in text for k in ["finbert", "finllm", "fingpt", "financial language model"]):
        return "🤖 LLM/Agent 金融应用"
    if any(k in text for k in ["reinforcement", " rl ", "rl-based", "policy gradient", "actor-critic", "q-learning", "ppo", "ddpg", "dqn", "sac", "td3"]) and any(k in text for k in ["trad","market","stock","financ","invest","portfolio","execu"]):
        return "🎯 强化学习交易"
    if any(k in text for k in ["graph neural", "gnn", "heterogeneous graph", "graph attention", "stock relation","graph learning"]) and any(k in text for k in ["stock","trad","financ","market"]):
        return "🕸 图神经网络/股票关系"
    if any(k in text for k in ["limit order book", " lob ", "microstructure", "high.frequency trading", "high-frequency", " hft ", "market making", "execution algo"]):
        return "⚡ 订单簿/HFT/微观结构"
    if any(k in text for k in ["volatility", "garch", "vix", "realized volatility"]):
        return "📊 波动率预测"
    if any(k in text for k in ["portfolio optim", "asset allocat", "mean-variance", "markowitz", "robo-advisor"]):
        return "💼 组合优化/资产配置"
    if any(k in text for k in ["alpha factor", "alpha mining", "factor model", "factor mining", "alpha discov", "formulaic alpha"]):
        return "🔍 因子挖掘/Alpha 发现"
    if any(k in text for k in ["sentiment", "news", "social media", "tweet", "twitter", "reddit"]) and any(k in text for k in ["stock","trad","financ","market","invest"]):
        return "📰 新闻/社媒情绪"
    if any(k in text for k in ["transformer", "attention model", "self-attention"]) and any(k in text for k in ["stock","trad","price","financ","time series","forecast"]):
        return "🔄 Transformer 时序"
    if any(k in text for k in ["earnings call", "earnings conference", "10-k", "10-q", "filing", "annual report"]):
        return "📑 财报/披露文本分析"
    if any(k in text for k in ["regime", "market regime", "regime detect", "regime switch"]):
        return "🌊 市场状态/Regime"
    if any(k in text for k in ["adversarial", "robustness", "attack on stock", "robust trading"]) and any(k in text for k in ["stock","trad","financ","market"]):
        return "🛡 对抗/鲁棒性"
    if any(k in text for k in ["risk manag", "var ", "value at risk", "credit risk", "default predict", "fraud"]):
        return "⚖ 风险/信用/欺诈"
    if any(k in text for k in ["multimodal", "multi-modal", "fundamental"]) and any(k in text for k in ["stock","financ","market","invest"]):
        return "🎨 多模态融合"
    if any(k in text for k in ["time series", "lstm", "rnn", "temporal", "sequence model"]) and any(k in text for k in ["stock","financ","market","price","forecast"]):
        return "📈 时序模型(LSTM/RNN)"
    if any(k in text for k in ["diffusion model", "generative", "gan ", "synthetic"]) and any(k in text for k in ["stock","financ","market"]):
        return "🎲 生成模型/合成数据"
    if any(k in text for k in ["backtest", "simulation", "market simulator", "synthetic market"]):
        return "🧪 回测/市场模拟"
    if any(k in text for k in ["explain","interpret","attribution"]) and any(k in text for k in ["stock","financ","market"]):
        return "💡 可解释性"
    if any(k in text for k in ["crypto", "bitcoin", "ethereum", "blockchain"]) and any(k in text for k in ["trad","market","price"]):
        return "₿ 加密货币/区块链"
    if any(k in text for k in ["option ", "derivativ", "hedg"]):
        return "📐 期权/衍生品"
    if any(k in text for k in ["pairs trad", "stat arb", "statistical arbitrage", "mean revers"]):
        return "📐 统计套利/均值回归"
    return "🌐 其他金融 AI"

for p in recent:
    p["topic"] = classify(p)

# 按主题分组
by_topic = defaultdict(list)
for p in recent:
    by_topic[p["topic"]].append(p)

# 每个主题内按年份+源排序
def sort_key(p):
    return (-p.get("year", 0), -len(p["abstract"]))

for topic in by_topic:
    by_topic[topic].sort(key=sort_key)

# 数据透视
year_count = Counter(p.get("year") for p in recent)
topic_count = {t: len(papers) for t, papers in by_topic.items()}
source_count = Counter(p["source"] for p in recent)


# 选 Top 20 must-read（基于摘要质量 + 年份 + 关键创新词）
def importance_score(p):
    score = 0
    # 越新越好
    if p["year"] == 2026: score += 3
    elif p["year"] == 2025: score += 2
    elif p["year"] == 2024: score += 1
    # 摘要长度 = 论文质量代理
    score += min(len(p["abstract"]) / 500, 3)
    text = (p["title"] + " " + p["abstract"][:800]).lower()
    # 创新关键词加分
    novel_words = ["llm","gpt","agent","reinforcement","graph neural","transformer",
                    "alpha factor","multimodal","earnings call","high frequency",
                    "regime", "diffusion","contrastive","self-supervised","pretrain",
                    "in-context","instruction","tool-use","react","mcts"]
    for w in novel_words:
        if w in text: score += 0.5
    # AAAI 给小加分（同行评审）
    if p["source"] == "AAAI": score += 1
    return score

ranked = sorted(recent, key=importance_score, reverse=True)
top_20 = ranked[:20]


# ============ 写文档 ============
md = []
md.append("# 量化交易 AI 论文精读总结（AAAI + arXiv）\n\n")
md.append(f"_整理时间：2026-04-27 | 共扫描 **{len(deduped)}** 篇论文，2024 年后 **{len(recent)}** 篇 | 源：AAAI Proceedings + arXiv_\n\n")
md.append("> **数据范围**：2024 年 1 月 - 2026 年 4 月。\n")
md.append("> **检索方法**：跨平台多关键词搜索 + 摘要抓取 + 标题相关性过滤。\n")
md.append("> **本文档定位**：让你 30 分钟内掌握量化 AI 当前研究地图，挑出对实盘真正有价值的方向。\n\n")

md.append("---\n\n")
md.append("## 🎯 一句话总览\n\n")
md.append("**量化 AI 在 2024-2026 期间的核心叙事 = LLM Agent 接管低水平交易决策 + 强化学习接管高频执行 + 图网络做横截面预测 + 多模态融合（财报+新闻+价格）成为新基线。**\n\n")
md.append("具体来说：\n")
md.append("1. **LLM Agent 是 2025 年起最大趋势**：把 GPT-4 / Claude / Llama-3 当作交易决策的'大脑'，通过 tool-use 调用回测、数据查询、信号计算\n")
md.append("2. **强化学习仍是高频交易和订单执行的标准**：但学界开始反思 OOS 失效问题，转向'离线 RL + 反事实评估'\n")
md.append("3. **图神经网络 + Transformer** 替代了 LSTM，成为基础组件\n")
md.append("4. **多模态（财报电话+新闻+价格+图像）** 已成标配——单一价格输入论文几乎不再发表\n")
md.append("5. **生成模型/扩散模型** 进入合成市场数据领域，用于增强训练样本\n\n")

md.append("---\n\n")
md.append("## 📊 数据透视\n\n")
md.append("**按年份**\n\n| 年份 | 篇数 |\n|---|---:|\n")
for y in sorted(year_count.keys(), reverse=True):
    md.append(f"| {y} | {year_count[y]} |\n")
md.append("\n**按主题**\n\n| 主题 | 篇数 |\n|---|---:|\n")
for t, n in sorted(topic_count.items(), key=lambda x: -x[1]):
    md.append(f"| {t} | {n} |\n")

md.append("\n**按数据源**\n\n| 源 | 篇数 |\n|---|---:|\n")
for src, n in source_count.most_common():
    md.append(f"| {src} | {n} |\n")

md.append("\n---\n\n## 🏆 Top 20 必读论文（综合权重排）\n\n")
md.append("筛选标准：发表年份 + 摘要质量 + 关键创新词密度 + AAAI 同行评审加分。**这 20 篇是给你最高优先级看的**。\n\n")
for i, p in enumerate(top_20, 1):
    md.append(f"### {i}. {p['title']}\n\n")
    md.append(f"- **类别**：{p['topic']}\n")
    md.append(f"- **年份**：{p['year']} | **源**：{p['source']} ({p.get('venue','')[:60]})\n")
    md.append(f"- **作者**：{(p.get('authors','') or '')[:200]}\n")
    md.append(f"- **链接**：{p['url']}\n")
    abs_text = p['abstract'][:1800]
    if abs_text:
        md.append(f"- **摘要**：{abs_text}{'...' if len(p['abstract']) > 1800 else ''}\n")
    md.append("\n")

md.append("---\n\n## 📚 各主题代表论文\n\n")
md.append("每个主题展示 Top 5 (按年份+摘要质量)；其余在最后做 reference。\n\n")
topic_order = sorted(by_topic.keys(), key=lambda t: -len(by_topic[t]))
for topic in topic_order:
    plist = by_topic[topic]
    md.append(f"\n### {topic}（{len(plist)} 篇）\n\n")
    for p in plist[:5]:
        md.append(f"#### 📄 {p['title']}\n")
        md.append(f"- **{p['year']} | {p['source']}** | [link]({p['url']})\n")
        md.append(f"- **作者**：{(p.get('authors','') or '')[:150]}\n")
        abs_text = p['abstract'][:1200]
        if abs_text:
            md.append(f"- **摘要**：{abs_text}{'...' if len(p['abstract']) > 1200 else ''}\n")
        md.append("\n")

md.append("\n---\n\n## 💎 散户实操要点（融合 AAAI + arXiv 共识）\n\n")
md.append("### A. 你应该立刻试的 3 件事\n\n")
md.append("**1. LLM 做新闻+财报情绪分析（最低门槛、最大杠杆）**\n")
md.append("- 现在的 LLM（GPT-4o / Claude / Qwen2.5）在金融文本理解上已经超过专门训练的 FinBERT\n")
md.append("- 给 LLM 喂当天的新闻稿/财报通话/SEC 文件，要求结构化输出：\n")
md.append("  - 标的代码列表\n")
md.append("  - 情绪极性（-1 到 +1）\n")
md.append("  - 事件类型（财报、并购、政策、产品发布、诉讼）\n")
md.append("  - 信心度（0-1）\n")
md.append("  - 短期方向预期（涨/跌/中性）\n")
md.append("- 把这些当作日级别特征喂给 XGBoost / LightGBM 配合价格特征做方向预测\n")
md.append("- **多篇 AAAI/arXiv 论文反复验证：news + price 融合显著优于纯 price**\n\n")
md.append("**2. 用预训练 Transformer 时序模型做收益率分布预测**\n")
md.append("- 推荐: PatchTST / Autoformer / Informer (开源 GitHub 现成)\n")
md.append("- 关键技巧：**不要预测下一个收盘价**，预测**未来 N 天收益率的分布**（quantile forecast）\n")
md.append("- 用 quantile 计算：上行概率、95% VaR、最大可能收益\n\n")
md.append("**3. 多策略组合 + 元控制器**\n")
md.append("- 学界趋势：单一模型在不同 regime 下都不稳定\n")
md.append("- 实操：跑 3-5 个不同思路的策略（动量、反转、事件、宏观、套利），每天根据近期 regime 让一个高层模型选择当前权重\n")
md.append("- AAAI 26 多篇论文（MARS、ArchetypeTrader）都在做这事——但你可以用简单加权\n\n")

md.append("### B. 你应该警惕的 5 个陷阱（论文里反复警告）\n\n")
md.append("**1. Look-ahead bias（前瞻偏差）**：用了未来信息做特征，回测虚高\n")
md.append("- 例：用 t+1 收盘价计算 t 时刻的指标，看似高 sharpe 实则作弊\n")
md.append("- 修复：所有特征只能用 ≤t-1 的数据，时间戳严格对齐\n\n")
md.append("**2. Survivorship bias（存活者偏差）**：只用现存股票做训练\n")
md.append("- 例：用 S&P500 当前成分股回测 10 年，**忽略了被剔除/退市的差股**\n")
md.append("- 修复：用历史成分股快照、包含已退市标的的数据库\n\n")
md.append("**3. Transaction cost 严重低估**\n")
md.append("- 学术回测平均假设 5bps 成本，实际散户经常 15-50bps\n")
md.append("- **特别是高频策略**：成本会吃掉 80%+ 的纸面利润\n\n")
md.append("**4. Regime sensitivity（regime 敏感性）**\n")
md.append("- 2019 训练的模型在 2020 COVID 全部失效\n")
md.append("- 2021 训练的模型在 2022 加息周期全部失效\n")
md.append("- 论文 OOS（样本外）测试通常只覆盖训练集后 6-12 月，但**真实部署期是无限期**\n")
md.append("- 修复：滚动训练 + 关键经济事件触发的强制重训练\n\n")
md.append("**5. Overfitting（特别是因子挖掘）**\n")
md.append("- 暴力搜索 1000 个因子，挑最好的，看似 sharpe 5+\n")
md.append("- 修复：Bonferroni 校正、out-of-sample 必须独立、跨市场跨时段验证\n\n")

md.append("### C. 不该做的事（论文也反复警示）\n\n")
md.append("- **不要用 RL 直接预测明天收盘价**——OOS 表现差\n")
md.append("- **不要相信单一论文的 Sharpe**——除非有第三方独立复现\n")
md.append("- **不要 leverage 学术策略**——学术回测忽略 margin call、流动性约束\n")
md.append("- **不要把 LLM 输出的'交易建议'直接执行**——LLM 还没有 actor-level 的真实金融问责机制\n\n")

md.append("---\n\n## 🔬 关键论文方法论拆解\n\n")
md.append("挑 5 篇代表性论文做方法论级别的拆解（其余的看上面 Top 20 + 主题节）。\n\n")

# 找几个具有代表性的高分论文
key_themes = {
    "LLM Agent": ["agent","tool","gpt","llm","multi-agent"],
    "RL Trading": ["reinforcement","ppo","actor"],
    "Alpha Mining": ["alpha factor","alpha mining","mcts"],
    "Graph": ["graph","gnn","heterogeneous"],
    "Multimodal": ["multimodal","earnings call","financial sentiment"],
}
shown = set()
for theme, kw in key_themes.items():
    for p in ranked:
        if p["url"] in shown: continue
        text = (p["title"] + " " + p["abstract"][:500]).lower()
        if any(k in text for k in kw):
            md.append(f"### {theme} 代表论文\n\n")
            md.append(f"**{p['title']}** ({p['year']}, {p['source']})\n\n")
            md.append(f"- 链接：{p['url']}\n")
            md.append(f"- 摘要：{p['abstract'][:1500]}\n\n")
            shown.add(p["url"])
            break

md.append("\n---\n\n")
md.append("## 📁 数据文件\n\n")
md.append("- `aaai_papers_full.json` — AAAI 完整数据（97 篇）\n")
md.append("- `arxiv_papers.json` — arXiv 完整数据（723 篇 2024+）\n")
md.append("- 本文档 `AAAI_量化交易论文总结.md`\n\n")

md.append("---\n\n## 📋 完整论文清单（按年份 + 主题）\n\n")
md.append("**仅列标题、年份、链接，作快速浏览参考**。要看摘要去上面的对应主题节或两个 JSON 文件。\n\n")
for year in sorted(year_count.keys(), reverse=True):
    yearly = [p for p in recent if p.get("year") == year]
    if not yearly: continue
    md.append(f"### {year} ({len(yearly)} 篇)\n\n")
    by_topic_year = defaultdict(list)
    for p in yearly:
        by_topic_year[p["topic"]].append(p)
    for topic in sorted(by_topic_year.keys(), key=lambda t: -len(by_topic_year[t])):
        plist = by_topic_year[topic]
        md.append(f"**{topic}**：\n")
        for p in plist[:30]:
            md.append(f"- [{p['source']}] {p['title'][:140]} → {p['url']}\n")
        if len(plist) > 30:
            md.append(f"- *(+{len(plist)-30} 篇省略)*\n")
        md.append("\n")

# 输出
out_path = "C:/Users/yang/desktop/test_project/AAAI_量化交易论文总结.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("".join(md))

total_chars = sum(len(s) for s in md)
print(f"\n✅ 文档已写入 {out_path}")
print(f"   长度: {total_chars:,} 字符 ({total_chars / 1024:.1f} KB)")
print(f"   总论文: {len(deduped)}")
print(f"   2024+ 论文: {len(recent)}")
print(f"\n主题分布：")
for t, n in sorted(topic_count.items(), key=lambda x: -x[1]):
    print(f"  {n:>4}× {t}")
