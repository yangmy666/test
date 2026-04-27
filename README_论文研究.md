# 量化交易 AI 论文研究 · 成果导览

_完成时间：2026-04-27_

## 📦 你醒来该看的 7 个文件（按推荐顺序）

### 🥇 [量化AI论文_精华摘要.md](./量化AI论文_精华摘要.md) ⭐ 先看这个
**24 KB / 5-10 分钟读完**

包含：
- 6 条核心结论（一目了然的研究地图）
- 主题分布（哪个方向最热）
- **Top 30 必读论文**（Top 10 带详细摘要，11-30 一句话点评）
- 散户实操 3 条建议（立刻能做 / 中等难度 / 别做）
- 文件位置指引

### 🥈 [量化AI论文_方法论对比.md](./量化AI论文_方法论对比.md) ⭐ 强烈推荐
**7 KB / 5 分钟读完**

包含：
- **数据集使用 Top 25** — 学界都在用什么数据
- **Baseline Top 25** — 学界都在和什么比
- **Sharpe 比率分布** — 论文报告的真实数值范围（中位数 1.50！）
- 散户能用 vs 拿不到的数据划分
- 这是市面上**没人做过**的横向综合分析

### 🏅 [量化AI论文_开源代码索引.md](./量化AI论文_开源代码索引.md) ⭐ 实用价值高
**15 KB**

包含：
- **72 个直接 GitHub 链接**（论文摘要直接给出的开源仓库）
- 2 个 HuggingFace 模型链接
- 75 篇声称代码可用但未直链的论文
- 找代码的 5 条实用建议

### 🆕 [量化AI论文_最新60天.md](./量化AI论文_最新60天.md) 最前沿
**213 KB / 选读**

包含：
- 260 篇近 60 天（2026-02-27 至今）发表的金融 AI 论文
- Top 10 by 摘要质量（含具体方法+数字的论文）
- ⚠️ 注意：未经过同行评审，质量参差，少量有过滤误报

### 🎖 [量化AI论文_趋势演进.md](./量化AI论文_趋势演进.md) 短小精悍
**3 KB / 3 分钟**

包含：
- 25 个主题在 2024 → 2025 → 2026 的热度演进表
- **暴涨主题**：对抗鲁棒性、因果推理
- **新涌现主题**：Tool-use/ReAct、预训练时序基础模型（Lag-Llama）、MCTS 规划
- 衰退主题
- 5 条关键趋势解读

### 🥉 [AAAI_量化交易论文总结.md](./AAAI_量化交易论文总结.md) 深度版
**295 KB / 1-2 小时深读**

包含：
- 1419 篇唯一论文（2024+ 共 1358 篇）
- 按 22 个主题分类
- 每个主题 Top 5 论文带摘要
- Top 20 必读完整摘要
- 5 个关键论文方法论拆解

### 🥉 原始数据 JSON（可程序化二次处理）

- `browser-cli/aaai_papers_full.json` — AAAI 97 篇
- `browser-cli/arxiv_papers.json` — arXiv 1207 篇（2024+）
- `browser-cli/openreview_papers.json` — ICLR/OpenReview 172 篇

## 🔍 数据范围

- **时间**：2024-01 至 2026-04
- **平台**：AAAI（同行评审）+ arXiv（预印本）+ OpenReview（ICLR 同行评审）
- **关键词覆盖**（共 60+ 个）：
  - 通用：trading, portfolio, financial, stock prediction, market
  - 方法：reinforcement learning, LLM, transformer, GNN, diffusion
  - 专业：deep hedging, market making, alpha factor, factor investing, pairs trading, statistical arbitrage, limit order book, microstructure
  - 中文市场：A-share, SSE, SZSE, Chinese stock
  - 加密：crypto trading, DeFi
  - 衍生品：option pricing, Black-Scholes, hedging

## 🎯 研究核心发现（最浓缩版）

```
2024-2026 量化 AI 关键词 = LLM Agent
                          + 强化学习反思 OOS 失效
                          + 图神经网络替代 LSTM
                          + 多模态成为标配
                          + 生成模型增强训练样本
```

## 🛠 本研究使用的工具栈（可复用）

- `browser-cli/connect.py` — Playwright 连本地 Chrome
- `browser-cli/aaai_search.py` — AAAI 多关键词搜索
- `browser-cli/aaai_abstracts.py` — 抓摘要
- `browser-cli/arxiv_search.py` — arXiv API 通用搜索
- `browser-cli/arxiv_specialized.py` — 专业领域补充
- `browser-cli/openreview_search.py` — OpenReview API
- `browser-cli/final_doc.py` — 合并三源 → 主文档
- `browser-cli/exec_summary.py` — 合并三源 → 精华版

要换个领域跑（例如"自动驾驶 AI"或"医学影像 AI"），改下关键词列表就行。

## 🔁 下一步建议

1. **挑 Top 3 论文精读 PDF**（链接在精华摘要里）
2. **找开源代码**：很多 2025-2026 论文有 GitHub
3. **复现一篇 baseline** 验证你的工程链路
4. **告诉我具体方向**，我可以再深挖（做市、期权 vol smile、加密 RL 等）
