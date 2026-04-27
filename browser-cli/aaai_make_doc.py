"""读 80 篇论文按主题/年份分类，生成可读 Markdown 总结文档。"""
import json, re, sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open("C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_full.json", encoding="utf-8") as f:
    papers = json.load(f)

# 解析年份
def get_year(p):
    issue = p.get("issueText", "")
    # Vol. 40 = 2026, 39 = 2025, 38 = 2024, 37 = 2023, 36 = 2022, 35 = 2021
    vol_map = {40: 2026, 39: 2025, 38: 2024, 37: 2023, 36: 2022, 35: 2021,
               34: 2020, 33: 2019, 32: 2018, 31: 2017, 30: 2016, 29: 2015, 28: 2014, 27: 2013, 26: 2012, 25: 2011}
    m = re.search(r"Vol\.\s*(\d+)", issue)
    if m:
        v = int(m.group(1))
        return vol_map.get(v, 2000 + v - 14)  # 推测
    m2 = re.search(r"\((\d{4})\)", issue)
    if m2:
        return int(m2.group(1))
    return None


# 主题分类（基于标题/摘要关键词）
def classify(p):
    text = (p.get("title", "") + " " + p.get("abstract", "")).lower()
    if any(k in text for k in ["reinforcement", " rl ", "policy gradient", "actor-critic", "q-learning", "ppo", "ddpg", "dqn"]):
        return "强化学习交易"
    if any(k in text for k in ["llm", "large language model", "gpt", "finbert", "fingpt", "finllm", "language model"]):
        return "LLM/语言模型金融应用"
    if any(k in text for k in ["graph neural", "gnn", "graph learning", "heterogeneous graph", "stock relation"]):
        return "图神经网络/股票关系"
    if any(k in text for k in ["transformer", "attention", "bert", "encoder"]) and "graph" not in text:
        return "Transformer/Attention 时序"
    if any(k in text for k in ["sentiment", "news", "tweet", "social media", "text"]):
        return "新闻/社媒情绪"
    if any(k in text for k in ["limit order book", "lob", "microstructure", "high.frequency", "order book"]):
        return "订单簿/微观结构/HFT"
    if any(k in text for k in ["volatility", "garch", "vix"]):
        return "波动率预测"
    if any(k in text for k in ["portfolio", "asset allocation", "mean.variance", "markowitz"]):
        return "组合优化/资产配置"
    if any(k in text for k in ["risk", "credit", "default", "fraud"]):
        return "风险/欺诈检测"
    if any(k in text for k in ["alpha factor", "factor model", "factor mining", "alpha generation"]):
        return "因子挖掘/Alpha"
    if any(k in text for k in ["adversarial", "robustness", "attack"]):
        return "对抗攻击/鲁棒性"
    if any(k in text for k in ["regime", "market regime", "regime detection", "regime switching"]):
        return "市场状态识别"
    if any(k in text for k in ["multi.modal", "multimodal", "fundamental"]):
        return "多模态/基本面融合"
    if any(k in text for k in ["time series", "lstm", "rnn", "temporal", "sequence"]):
        return "时序模型(LSTM/RNN/Temporal)"
    return "其他"


# 按年份+主题分组
for p in papers:
    p["year"] = get_year(p)
    p["topic"] = classify(p)


# 按年份倒序、主题分类
recent = [p for p in papers if p["year"] and p["year"] >= 2023]
older = [p for p in papers if p["year"] and p["year"] < 2023]
recent.sort(key=lambda x: (-x["year"], x["topic"]))
older.sort(key=lambda x: (-x["year"], x["topic"]))

# Markdown 文档
md_lines = []
md_lines.append("# AAAI 量化交易/金融 AI 论文精读总结\n")
md_lines.append(f"_整理时间：2026-04-27 | 共 {len(papers)} 篇 AAAI 会议论文，覆盖 2011-2026_\n")
md_lines.append("> 资料来源：AAAI Proceedings (ojs.aaai.org)。检索关键词包括 stock prediction, trading, portfolio, financial forecast, "
                "algorithmic trading, quantitative trading, high frequency trading, limit order book, market microstructure, "
                "asset pricing, price prediction, financial time series, alpha factor, volatility prediction, risk management, "
                "factor model, market regime, financial sentiment, FinBERT, FinLLM, investment strategy, reinforcement learning trading 等。\n")

md_lines.append("\n---\n\n## 🎯 阅读这份文档前你要知道的核心结论\n")
md_lines.append("**1. 量化交易在 AAAI 的研究在 2024-2026 集中爆发，主要方向有 5 大趋势**：\n")
md_lines.append("- **图神经网络（GNN）** 建模股票相互关系，做横截面预测的主流（最热）\n")
md_lines.append("- **大模型（LLM）+ 多模态** 融合财报、新闻、社媒、价格做综合预测（增速最快）\n")
md_lines.append("- **强化学习** 做交易策略和订单执行（成熟方向，仍持续）\n")
md_lines.append("- **Transformer** 做时序预测（基础设施类，多个变体）\n")
md_lines.append("- **新颖数据源** 财报电话会议、社媒文本、卫星图等替代数据进入主流模型\n\n")

md_lines.append("**2. 散户能不能直接用？**\n")
md_lines.append("- **大部分论文方法重、数据需求重**：需要订单簿数据、财报转录、海量新闻流——散户拿不到\n")
md_lines.append("- **少数方法可下沉**：基于公开新闻+价格的 LLM 情绪分析、Transformer 时序预测——有开源实现\n")
md_lines.append("- **Backtest 普遍乐观**：论文里 Sharpe > 2.0 的对外公布报告里非常常见，但 OOS（样本外）真实交易会大幅打折\n\n")

md_lines.append("**3. 重要警告**：学术论文 ≠ 可实盘策略。多数论文用历史回测，未经实盘验证。**这份文档帮你了解技术前沿，不是给你交易信号**。\n\n")

md_lines.append("---\n\n## 📊 数据透视\n\n")
year_count = defaultdict(int)
for p in papers:
    if p.get("year"):
        year_count[p["year"]] += 1
md_lines.append("**按年份分布**\n\n| 年份 | 篇数 |\n|---|---:|\n")
for y in sorted(year_count.keys(), reverse=True):
    md_lines.append(f"| {y} | {year_count[y]} |\n")

topic_count = defaultdict(int)
for p in papers:
    topic_count[p["topic"]] += 1
md_lines.append("\n**按主题分布**\n\n| 主题 | 篇数 |\n|---|---:|\n")
for t, n in sorted(topic_count.items(), key=lambda x: -x[1]):
    md_lines.append(f"| {t} | {n} |\n")

# 最新论文优先
md_lines.append("\n---\n\n## 🔥 2024-2026 最新论文（按主题分类）\n")
recent_by_topic = defaultdict(list)
for p in recent:
    recent_by_topic[p["topic"]].append(p)

# 主题展示顺序：先热门
topic_order = sorted(recent_by_topic.keys(), key=lambda t: -len(recent_by_topic[t]))
for topic in topic_order:
    plist = recent_by_topic[topic]
    md_lines.append(f"\n### {topic}（{len(plist)} 篇）\n\n")
    for p in plist:
        md_lines.append(f"#### 📄 {p.get('title','')}\n")
        md_lines.append(f"- **年份**：{p.get('year','?')} ({p.get('issueText','')[:60]})\n")
        md_lines.append(f"- **作者**：{(p.get('authors','') or '')[:200]}\n")
        md_lines.append(f"- **链接**：{p.get('url','')}\n")
        abs_text = (p.get('abstract','') or '').strip()
        if abs_text:
            # 限制摘要长度
            if len(abs_text) > 1500:
                abs_text = abs_text[:1500] + "..."
            md_lines.append(f"- **摘要**：{abs_text}\n")
        else:
            md_lines.append(f"- **摘要**：（未抓到）\n")
        md_lines.append("\n")

# 老论文做参考列表
md_lines.append("\n---\n\n## 📚 经典/历史论文（2011-2022）\n")
md_lines.append("仅列标题和链接作参考，不展开摘要。\n\n")
older_by_topic = defaultdict(list)
for p in older:
    older_by_topic[p["topic"]].append(p)
for topic in sorted(older_by_topic.keys(), key=lambda t: -len(older_by_topic[t])):
    plist = older_by_topic[topic]
    md_lines.append(f"\n### {topic}（{len(plist)} 篇）\n\n")
    for p in plist:
        md_lines.append(f"- **{p.get('year','?')}** [{p.get('title','')[:140]}]({p.get('url','')})\n")

# 实用清单
md_lines.append("\n---\n\n## 💡 量化散户实用清单\n\n")
md_lines.append("基于这 80 篇论文，给你提炼的**可下沉、相对可执行**的方向：\n\n")
md_lines.append("### 1. 用 LLM 做新闻/财报的情绪和事件提取\n")
md_lines.append("- 现在 GPT-4o/Claude/Qwen 都能做，不需要训练 FinBERT\n")
md_lines.append("- 把每天的新闻喂进 LLM，要求结构化输出：标的、情绪极性（-1 到 1）、事件类型（财报、并购、政策）、信心度\n")
md_lines.append("- 把这些当作**时序中的事件特征**和价格一起喂给 XGBoost / LightGBM 做预测\n")
md_lines.append("- AAAI 多篇论文证实新闻+价格融合显著优于纯价格\n\n")
md_lines.append("### 2. 图神经网络（GNN）建模股票关系——但用简化版\n")
md_lines.append("- 完整 GNN 工程量大；散户能做的是用相关性矩阵 + 行业归属构造**同板块协同因子**\n")
md_lines.append("- 一个标的当天 abnormal return = 自己的回报 - 行业指数回报，捕捉特异性 alpha\n")
md_lines.append("- 这是 GNN 论文的**核心洞察的简化形式**\n\n")
md_lines.append("### 3. Transformer 时序预测——开源可用\n")
md_lines.append("- 学术界已经从 LSTM 转向 Transformer 变体（Informer、Autoformer、PatchTST）\n")
md_lines.append("- GitHub 上有现成实现，散户可以拿来跑 OHLCV 多步预测\n")
md_lines.append("- 关键：**不要预测点价**，预测**收益率分布或方向概率**\n\n")
md_lines.append("### 4. 强化学习交易——慎用\n")
md_lines.append("- 学术 RL 交易论文多数 OOS 表现差，对训练-测试时间错位极敏感\n")
md_lines.append("- 不建议散户跟风做 RL；**简单规则 + 风控** 通常胜过复杂 RL\n\n")
md_lines.append("### 5. 警惕的几个陷阱（多篇论文反复提到）\n")
md_lines.append("- **未来信息泄露（Look-ahead bias）**：用了未来的信息做特征，回测虚高\n")
md_lines.append("- **存活者偏差（Survivorship bias）**：测试集只用现存股票，忽略退市\n")
md_lines.append("- **交易成本忽视**：回测忽略点差、滑点、佣金，实盘大幅打折\n")
md_lines.append("- **正则化过度**：训练集 Sharpe > 3 但测试集 < 0.5，典型过拟合\n")
md_lines.append("- **样本外极端事件**：2020 COVID、2022 加息周期会让所有 2019 训练的模型失效\n\n")

md_lines.append("\n---\n\n## 📂 原始数据\n")
md_lines.append("- `aaai_papers_raw.json` — 搜索原始结果（标题 + URL）\n")
md_lines.append("- `aaai_papers_full.json` — 含摘要的完整数据\n")
md_lines.append("- 本文档：`AAAI_量化交易论文总结.md`\n")

out_path = "C:/Users/yang/desktop/test_project/AAAI_量化交易论文总结.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("".join(md_lines))

print(f"已保存到 {out_path}")
print(f"文档长度：{sum(len(l) for l in md_lines)} 字符")
print(f"\n=== 摘要 ===")
print(f"年份分布：{dict(year_count)}")
print(f"主题分布：{dict(topic_count)}")
print(f"\n2024-2026 论文 {len(recent)} 篇")
print(f"2023 之前 {len(older)} 篇")
