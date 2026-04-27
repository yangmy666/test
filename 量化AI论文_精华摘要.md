# 量化交易 AI 论文 · 精华摘要

_整理：2026-04-27 | 涵盖 **1419** 篇唯一论文 / **1267** 篇 2024+ / 源：**AAAI** + **arXiv**_

> 这是给你**醒来后 5 分钟读完**的版本。完整深度版在 `AAAI_量化交易论文总结.md`（288 KB）。

---

## 🎯 核心结论 6 条

**1. 2024-2026 量化 AI 最大趋势 = LLM Agent 化**
- 单纯做'神经网络预测股价'的论文已经不再被顶会接收
- 主流是把 LLM 当大脑，配合 tool-use 调用回测/数据/信号 → 形成完整交易决策 agent
- 代表论文：FinAgent, TradingGPT, Navigating the Alpha Jungle (LLM+MCTS)

**2. 强化学习仍是高频/订单执行的标准，但学界开始反思 OOS 失效**
- 2026 年最新 RL 论文几乎都在解决 distribution shift / regime change
- 离线 RL + 反事实评估 + 多 agent 集成成为新范式
- 代表：MetaTrader, ArchetypeTrader, MARS

**3. 图神经网络（GNN）建模股票关系是横截面预测主流**
- 异构图 + 财报电话会议关系 + 时变关系
- 代表：ECHO-GL, MDGNN, MASTER

**4. 多模态（财报+新闻+价格）已成标配**
- 单一价格输入的论文不再有竞争力
- 财报电话会议 (earnings call) + SEC 文件文本是热门信号源

**5. 生成模型/扩散模型用于合成数据增强训练样本**
- 解决金融数据稀缺问题（特别是极端事件）
- 代表：Market-GAN, Diffusion Generated MoE

**6. 学术 ≠ 实盘——5 大常见陷阱**
- Look-ahead bias（前瞻偏差）
- Survivorship bias（存活者偏差）
- 交易成本严重低估
- Regime sensitivity（OOS 极不稳定）
- 因子搜索空间过拟合

---

## 📊 主题分布（2024+ 论文）

| 主题 | 篇数 | 占比 |
|---|---:|---:|
| LLM Agent | 389 | 31% |
| 其他 | 338 | 27% |
| 组合优化 | 105 | 8% |
| RL Trading | 101 | 8% |
| Transformer 时序 | 94 | 7% |
| 波动率 | 90 | 7% |
| HFT/订单簿 | 76 | 6% |
| GNN | 47 | 4% |
| Alpha 因子 | 15 | 1% |
| 情绪/财报文本 | 12 | 1% |

---

## 🏆 Top 10 必读（综合评分）

筛选权重：年份 + 摘要质量 + 创新关键词 + 是否同行评审 + 是否有具体方法名。

### 1. Navigating the Alpha Jungle: An LLM-Powered MCTS Framework for Formulaic Alpha Factor Mining

- **2026 | AAAI** | LLM Agent | [link](https://ojs.aaai.org/index.php/AAAI/article/view/37069)
- **摘要**：Alpha factor mining is pivotal in quantitative investment for identifying predictive signals from complex financial data. While traditional formulaic alpha mining relies on human expertise, contemporary automated methods, such as those based on genetic programming or reinforcement learning, often struggle with search inefficiency or yield alpha factors that are difficult to interpret. This paper introduces a novel framework that integrates Large Language Models (LLMs) with Monte Carlo Tree Search (MCTS) to overcome these limitations. Our framework leverages the LLM's instruction-following and reasoning capability to iteratively generate and refine symbolic alpha formulas within an MCTS-driven exploration. A key innovation is the guidance of MCTS exploration by rich, quantitative feedback from financial backtesting of each candidate factor, enabling efficient navigation of the vast search space. Furthermore, a frequent subtree avoidance mechanism is introduced to enhance search diversity and prevent formulaic homogenization, further improving performance. Experimental results on real-world stock market data demonstrate that our LLM-based framework outperforms existing methods by min

### 2. TrustTrade: Human-Inspired Selective Consensus Reduces Decision Uncertainty in LLM Trading Agents

- **2026 | arXiv** | LLM Agent | [link](http://arxiv.org/abs/2603.22567v1)
- **摘要**：Large language models (LLMs) are increasingly deployed as autonomous agents in financial trading. However, they often exhibit a hazardous behavioral bias that we term uniform trust, whereby retrieved information is implicitly assumed to be factual and heterogeneous sources are treated as equally informative. This assumption stands in sharp contrast to human decision-making, which relies on selective filtering, cross-validation, and experience-driven weighting of information sources. As a result, LLM-based trading systems are particularly vulnerable to multi-source noise and misinformation, amplifying factual hallucinations and leading to unstable risk-return performance. To bridge this behavioral gap, we introduce TrustTrade (Trust-Rectified Unified Selective Trader), a multi-agent selective consensus framework inspired by human epistemic heuristics. TrustTrade replaces uniform trust with cross-agent consistency by aggregating information from multiple independent LLM agents and dynamically weighting signals based on their semantic and numerical agreement. Consistent signals are prioritized, while divergent, weakly grounded, or temporally inconsistent inputs are selectively discoun

### 3. AlphaAgent: LLM-Driven Alpha Mining with Regularized Exploration to Counteract Alpha Decay

- **2025 | arXiv** | LLM Agent | [link](http://arxiv.org/abs/2502.16789v2)
- **摘要**：Alpha mining, a critical component in quantitative investment, focuses on discovering predictive signals for future asset returns in increasingly complex financial markets. However, the pervasive issue of alpha decay, where factors lose their predictive power over time, poses a significant challenge for alpha mining. Traditional methods like genetic programming face rapid alpha decay from overfitting and complexity, while approaches driven by Large Language Models (LLMs), despite their promise, often rely too heavily on existing knowledge, creating homogeneous factors that worsen crowding and accelerate decay. To address this challenge, we propose AlphaAgent, an autonomous framework that effectively integrates LLM agents with ad hoc regularizations for mining decay-resistant alpha factors. AlphaAgent employs three key mechanisms: (i) originality enforcement through a similarity measure based on abstract syntax trees (ASTs) against existing alphas, (ii) hypothesis-factor alignment via LLM-evaluated semantic consistency between market hypotheses and generated factors, and (iii) complexity control via AST-based structural constraints, preventing over-engineered constructions that are 

### 4. Evaluation and Benchmarking Suite for Financial Large Language Models and Agents

- **2026 | arXiv** | LLM Agent | [link](http://arxiv.org/abs/2602.19073v1)
- **摘要**：Over the past three years, the financial services industry has witnessed Large Language Models (LLMs) and agents transitioning from the exploration stage to readiness and governance stages. Financial large language models (FinLLMs), such as open FinGPT and proprietary BloombergGPT , have great potential in financial applications, including retrieving real-time data, tutoring, analyzing sentiment of social media, analyzing SEC filings, and agentic trading. However, general-purpose LLMs and agents lack financial expertise and often struggle to handle complex financial reasoning. This paper presents an evaluation and benchmarking suite that covers the lifecycle of FinLLMs and FinAgents. This suite led by SecureFinAI Lab includes an evaluation pipeline and a governance framework collaborating with Linux Foundation and PyTorch Foundation, a FinLLM Leaderboard with HuggingFace, an AgentOps framework with Red Hat, and a documentation website with Rensselear Center of Open Source. Our collaborative development evolves through three stages: FinLLM Exploration (2023), FinLLM Readiness (2024), and FinAI Governance (2025). The proposed suite serves as an open platform that enables researchers 

### 5. Market-Bench: Benchmarking Large Language Models on Economic and Trade Competition

- **2026 | arXiv** | LLM Agent | [link](http://arxiv.org/abs/2604.05523v2)
- **摘要**：The ability of large language models (LLMs) to manage and acquire economic resources remains unclear. In this paper, we introduce \textbf{Market-Bench}, a comprehensive benchmark that evaluates the capabilities of LLMs in economically-relevant tasks through economic and trade competition. Specifically, we construct a configurable multi-agent supply chain economic model where LLMs act as retailer agents responsible for procuring and retailing merchandise. In the \textbf{procurement} stage, LLMs bid for limited inventory in budget-constrained auctions. In the \textbf{retail} stage, LLMs set retail prices, generate marketing slogans, and provide them to buyers through a role-based attention mechanism for purchase. Market-Bench logs complete trajectories of bids, prices, slogans, sales, and balance-sheet states, enabling automatic evaluation with economic, operational, and semantic metrics. Benchmarking on 20 open- and closed-source LLM agents reveals significant performance disparities and winner-take-most phenomenon, \textit{i.e.}, only a small subset of LLM retailers can consistently achieve capital appreciation, while many hover around the break-even point despite similar semantic 

### 6. Semantics-Preserving Adversarial Attacks on Event-Driven Stock Prediction Models

- **2026 | AAAI** | LLM Agent | [link](https://ojs.aaai.org/index.php/AAAI/article/view/41099)
- **摘要**：Adversarial Security of Financial Language Models (ASFLM) is critical as Large Language Models (LLMs) pervade high-stakes financial applications. However, LLMs face two key challenges: their vulnerability to damaging adversarial attacks and the prevalent research gap concerning robust defenses against sophisticated, semantically coherent threats. To address these, we first theoretically analyze the relationship between discrete and continuous adversarial optimization, proving the continuous optimum provides a lower bound for the discrete. This foundation supports our novel two-stage framework, ChameleonAttack. It employs Adaptive Latent-space Optimization (ALO) for potent adversarial token discovery, followed by a Semantic-Translation Module (STM) module to generate fluent, coherent, and natural-sounding adversarial text. This dual approach aims to maximize attack impact while ensuring high linguistic quality and semantic integrity for evasion. Evaluated on state-of-the-art financial LLMs (e.g., FinBERT) and standard benchmarks (e.g., Financial PhraseBank), ChameleonAttack achieves a high Attack Success Rate (ASR) of 93.4%. These results highlight significant practical vulnerabilit

### 7. ArchetypeTrader: Reinforcement Learning for Selecting and Refining Learnable Strategic Archetypes in Quantitative Trading

- **2026 | AAAI** | RL Trading | [link](https://ojs.aaai.org/index.php/AAAI/article/view/40166)
- **摘要**：Quantitative trading using mathematical models and automated execution to generate trading decisions has been widely applied acorss financial markets. Recently, reinforcement learning (RL) has emerged as a promising approach for developing profitable trading strategies, especially in highly volatile markets like cryptocurrency. However, existing RL methods for cryptocurrency trading face two critical drawbacks: 1) Prior RL algorithms segment markets using handcrafted indicators (e.g., trend or volatility) to train specialized sub-policies. However, these coarse labels oversimplify market dynamics into rigid categories, biasing policies toward obvious patterns like trend-following and neglecting nuanced but lucrative opportunities. 2) Current RL methods fail to systematically use demonstration data. While some approaches ignore demonstrations altogether, others rely on “optimal” yet overly granular trajectories or human-crafted strategies, both of which can overwhelm learning and introduce significant bias, resulting in high variance and significant profit losses. To address these problems, we propose ArchetypeTrader, a novel reinforcement learning framework that automatically selec

### 8. SkyNet: Belief-Aware Planning for Partially-Observable Stochastic Games

- **2026 | arXiv** | LLM Agent | [link](http://arxiv.org/abs/2603.27751v1)
- **摘要**：In 2019, Google DeepMind released MuZero, a model-based reinforcement learning method that achieves strong results in perfect-information games by combining learned dynamics models with Monte Carlo Tree Search (MCTS). However, comparatively little work has extended MuZero to partially observable, stochastic, multi-player environments, where agents must act under uncertainty about hidden state. Such settings arise not only in card games but in domains such as autonomous negotiation, financial trading, and multi-agent robotics. In the absence of explicit belief modeling, MuZero's latent encoding has no dedicated mechanism for representing uncertainty over unobserved variables.   To address this, we introduce SkyNet (Belief-Aware MuZero), which adds ego-conditioned auxiliary heads for winner prediction and rank estimation to the standard MuZero architecture. These objectives encourage the latent state to retain information predictive of outcomes under partial observability, without requiring explicit belief-state tracking or changes to the search algorithm.   We evaluate SkyNet on Skyjo, a partially observable, non-zero-sum, stochastic card game, using a decision-granularity environme

### 9. TimeSeriesExamAgent: Creating Time Series Reasoning Benchmarks at Scale

- **2026 | arXiv** | 其他 | [link](http://arxiv.org/abs/2604.10291v1)
- **摘要**：Large Language Models (LLMs) have shown promising performance in time series modeling tasks, but do they truly understand time series data? While multiple benchmarks have been proposed to answer this fundamental question, most are manually curated and focus on narrow domains or specific skill sets. To address this limitation, we propose scalable methods for creating comprehensive time series reasoning benchmarks that combine the flexibility of templates with the creativity of LLM agents. We first develop TimeSeriesExam, a multiple-choice benchmark using synthetic time series to evaluate LLMs across five core reasoning categories: pattern recognitionnoise understandingsimilarity analysisanomaly detection, and causality. Then, with TimeSeriesExamAgent, we scale our approach by automatically generating benchmarks from real-world datasets spanning healthcare, finance and weather domains. Through multi-dimensional quality evaluation, we demonstrate that our automatically generated benchmarks achieve diversity comparable to manually curated alternatives. However, our experiments reveal that LLM performance remains limited in both abstract time series reasoning and domain-specific applica

### 10. ATLAS: Adaptive Trading with LLM AgentS Through Dynamic Prompt Optimization and Multi-Agent Coordination

- **2025 | OpenReview** | LLM Agent | [link](https://openreview.net/forum?id=SznTS60X8O)
- **摘要**：Large language models show promise for financial decision-making, yet deploying them as autonomous trading agents raises fundamental challenges: how to adapt instructions when rewards arrive late and obscured by market noise, how to synthesize heterogeneous information streams into coherent decisions, and how to bridge the gap between model outputs and executable market actions. We present ATLAS (Adaptive Trading with LLM AgentS), a unified multi-agent framework that integrates structured information from markets, news, and corporate fundamentals to support robust trading decisions. Within ATLAS, the central trading agent operates in an order-aware action space, ensuring that outputs correspond to executable market orders rather than abstract signals. The agent can incorporate feedback while trading using Adaptive-OPRO, a novel prompt-optimization technique that dynamically adapts the prompt by incorporating real-time, stochastic feedback, leading to increasing performance over time. Across regime-specific equity studies and multiple LLM families, Adaptive-OPRO consistently outperforms fixed prompts, while reflection-based feedback fails to provide systematic gains.


---

## 🥈 Top 11-30 一句话点评

**11. [2026|LLM Agent] Can Blindfolded LLMs Still Trade? An Anonymization-First Framework for Portfolio Optimization**
   - For LLM trading agents to be genuinely trustworthy, they must demonstrate understanding of market dynamics rather than exploitation of memorized ticker associations. Building respo...
   - http://arxiv.org/abs/2603.17692v1

**12. [2026|LLM Agent] MARS: A Meta-Adaptive Reinforcement Learning Framework for Risk-Aware Multi-Agent Portfolio Management**
   - Reinforcement Learning (RL) has shown significant promise in automated portfolio management; however, effectively balancing risk and return remains a central challenge, as many mod...
   - https://ojs.aaai.org/index.php/AAAI/article/view/39095

**13. [2026|LLM Agent] CHICO-Agent: An LLM Agent for the Cross-layer Optimization of 2.5D and 3D Chiplet-based Systems**
   - The rapid growth of large language models (LLMs) and AI workloads has pushed monolithic silicon to its reticle and economic limits, accelerating the adoption of 2.5D/3D chiplet sys...
   - http://arxiv.org/abs/2604.18764v1

**14. [2026|LLM Agent] Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems: Taxonomy, Coordination Primacy, and Cost Awareness**
   - Multi-agent systems based on large language models (LLMs) for financial trading have grown rapidly since 2023, yet the field lacks a shared framework for understanding what drives...
   - http://arxiv.org/abs/2603.27539v1

**15. [2026|LLM Agent] Design and Empirical Study of a Large Language Model-Based Multi-Agent Investment System for Chinese Public REITs**
   - This study addresses the low-volatility Chinese Public Real Estate Investment Trusts (REITs) market, proposing a large language model (LLM)-driven trading framework based on multi-...
   - http://arxiv.org/abs/2602.00082v1

**16. [2025|LLM Agent] QuantAgent: Price-Driven Multi-Agent LLMs for High-Frequency Trading**
   - Recent advances in Large Language Models (LLMs) have shown remarkable capabilities in financial reasoning and market understanding. Multi-agent LLM frameworks such as TradingAgent...
   - https://openreview.net/forum?id=fdKmhFYcQv

**17. [2026|LLM Agent] Time Series Augmented Generation for Financial Applications**
   - Evaluating the reasoning capabilities of Large Language Models (LLMs) for complex, quantitative financial tasks is a critical and unsolved challenge. Standard benchmarks often fail...
   - http://arxiv.org/abs/2604.19633v1

**18. [2025|LLM Agent] MountainLion: A Multi-Modal LLM-Based Agent System for Interpretable and Adaptive Financial Trading**
   - Cryptocurrency trading is a challenging task requiring the integration of heterogeneous data from multiple modalities. Traditional deep learning and reinforcement learning approach...
   - http://arxiv.org/abs/2507.20474v3

**19. [2026|LLM Agent] FinRpt: Dataset, Evaluation System and LLM-based Multi-agent Framework for Equity Research Report Generation**
   - While LLMs have shown great success in financial tasks like stock prediction and question answering, their application in fully automating Equity Research Report generation remains...
   - https://ojs.aaai.org/index.php/AAAI/article/view/37014

**20. [2026|LLM Agent] Machine Spirits: Speculation and Adaptation of LLM Agents in Asset Markets**
   - As Large Language Models (LLMs) become increasingly integrated into financial systems, understanding their behavioural properties is crucial. Do LLMs conform to the rational expect...
   - http://arxiv.org/abs/2604.18602v1

**21. [2026|LLM Agent] Let's Have a Conversation: Designing and Evaluating LLM Agents for Interactive Optimization**
   - Optimization is as much about modeling the right problem as solving it. Identifying the right objectives, constraints, and trade-offs demands extensive interaction between research...
   - http://arxiv.org/abs/2604.02666v1

**22. [2026|LLM Agent] Differential Harm Propensity in Personalized LLM Agents: The Curious Case of Mental Health Disclosure**
   - Large language models (LLMs) are increasingly deployed as tool-using agents, shifting safety concerns from harmful text generation to harmful task completion. Deployed systems ofte...
   - http://arxiv.org/abs/2603.16734v1

**23. [2026|LLM Agent] An Empirical Study of Multi-Agent Collaboration for Automated Research**
   - As AI agents evolve, the community is rapidly shifting from single Large Language Models (LLMs) to Multi-Agent Systems (MAS) to overcome cognitive bottlenecks in automated research...
   - http://arxiv.org/abs/2603.29632v1

**24. [2026|LLM Agent] Multi-Agent Reinforcement Learning for Modeling, Simulating, and Optimizing Energy Markets**
   - The objective of this study is to advance the optimization of hybrid electricity markets using multi-agent reinforcement learning (MARL). The transition from centralized systems to...
   - https://ojs.aaai.org/index.php/AAAI/article/view/41229

**25. [2026|LLM Agent] PolySwarm: A Multi-Agent Large Language Model Framework for Prediction Market Trading and Latency Arbitrage**
   - This paper presents PolySwarm, a novel multi-agent large language model (LLM) framework designed for real-time prediction market trading and latency arbitrage on decentralized plat...
   - http://arxiv.org/abs/2604.03888v1

**26. [2025|LLM Agent] Multimodal Financial Foundation Models (MFFMs): Progress, Prospects, and Challenges**
   - Financial Large Language Models (FinLLMs), such as open FinGPT and proprietary BloombergGPT, have demonstrated great potential in select areas of financial services. Beyond this ea...
   - http://arxiv.org/abs/2506.01973v2

**27. [2026|LLM Agent] A Hierarchical MARL-Based Approach for Coordinated Retail P2P Trading and Wholesale Market Participation of DERs**
   - The ongoing shift towards decentralization of the electric energy sector, driven by the growing electrification across end-use sectors, and widespread adoption of distributed energ...
   - http://arxiv.org/abs/2604.20586v1

**28. [2026|LLM Agent] Toward Expert Investment Teams:A Multi-Agent LLM System with Fine-Grained Trading Tasks**
   - The advancement of large language models (LLMs) has accelerated the development of autonomous financial trading systems. While mainstream approaches deploy multi-agent systems mimi...
   - http://arxiv.org/abs/2602.23330v1

**29. [2026|LLM Agent] Behavioral Consistency Validation for LLM Agents: An Analysis of Trading-Style Switching through Stock-Market Simulation**
   - Recent works have increasingly applied Large Language Models (LLMs) as agents in financial stock market simulations to test if micro-level behaviors aggregate into macro-level phen...
   - http://arxiv.org/abs/2602.07023v2

**30. [2026|LLM Agent] OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems**
   - The alignment of Multi-Agent Systems (MAS) for autonomous software engineering is constrained by evaluator epistemic uncertainty. Current paradigms, such as Reinforcement Learning...
   - http://arxiv.org/abs/2604.11477v1


---

## 💎 散户实操 3 条建议

### A. 立刻能做的（最低门槛 + 最大杠杆）

**用 LLM 做新闻 + 财报情绪/事件结构化提取**

```
Prompt 模板（每天跑一次）：
---
分析以下新闻，输出 JSON:
{
  "tickers": [...],          // 涉及标的
  "sentiment": -1 ~ 1,        // 极性
  "event_type": "earnings/M&A/policy/product/lawsuit",
  "confidence": 0~1,          // 信心度
  "direction": "up/down/neutral",  // 方向预期
  "horizon": "intraday/short/long"
}
```

把输出当作日级特征喂给 XGBoost 配合价格特征做方向预测。**多篇论文证实 news+price 显著优于纯 price**。

### B. 中等难度可做

**预训练 Transformer 做收益率分布预测（不要预测点价）**
- 推荐开源：PatchTST / Autoformer / Informer
- 关键：预测 quantile（p10/p50/p90），不是点估计
- 用 quantile 推算：上行概率、95% VaR、最大可能收益

### C. 暂时别做

**RL 直接预测明天涨跌——OOS 失败率极高**
- 学术 RL 训练集 Sharpe 3+，测试集 Sharpe 经常 <0.5
- 简单规则（动量+均线+成交量）+ 严格风控通常胜过 RL
- 论文里的 RL 都需要离线 RL + 反事实评估这种重型工程

---

## 📁 数据文件位置

- **本文件（精华版）**：`量化AI论文_精华摘要.md`
- **完整版（288KB）**：`AAAI_量化交易论文总结.md`
- **AAAI 原始 JSON**：`browser-cli/aaai_papers_full.json` (97 篇)
- **arXiv 原始 JSON**：`browser-cli/arxiv_papers.json` (1207 篇)
- 全部脚本可重跑：`browser-cli/aaai_search.py`, `arxiv_search.py`, `arxiv_specialized.py`, `final_doc.py`

---

## 🔁 后续动作建议

如果你想继续深入：
1. **挑 Top 10 里 1-2 篇** 真正去精读论文 PDF（链接里）
2. **找开源代码**：很多 2025-2026 论文有 GitHub 实现
3. **复现一篇**：随便挑一个能下载数据的论文，跑通 baseline → 验证你的工程链路
4. **再调用本工具**：让我用这套脚本搜其他主题（比如做市、期权 vol smile、加密货币 RL）

要继续深挖，告诉我具体方向。
