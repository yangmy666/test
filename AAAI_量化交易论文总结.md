# 量化交易 AI 论文精读总结（AAAI + arXiv）

_整理时间：2026-04-27 | 共扫描 **1419** 篇论文，2024 年后 **1358** 篇 | 源：AAAI Proceedings + arXiv_

> **数据范围**：2024 年 1 月 - 2026 年 4 月。
> **检索方法**：跨平台多关键词搜索 + 摘要抓取 + 标题相关性过滤。
> **本文档定位**：让你 30 分钟内掌握量化 AI 当前研究地图，挑出对实盘真正有价值的方向。

---

## 🎯 一句话总览

**量化 AI 在 2024-2026 期间的核心叙事 = LLM Agent 接管低水平交易决策 + 强化学习接管高频执行 + 图网络做横截面预测 + 多模态融合（财报+新闻+价格）成为新基线。**

具体来说：
1. **LLM Agent 是 2025 年起最大趋势**：把 GPT-4 / Claude / Llama-3 当作交易决策的'大脑'，通过 tool-use 调用回测、数据查询、信号计算
2. **强化学习仍是高频交易和订单执行的标准**：但学界开始反思 OOS 失效问题，转向'离线 RL + 反事实评估'
3. **图神经网络 + Transformer** 替代了 LSTM，成为基础组件
4. **多模态（财报电话+新闻+价格+图像）** 已成标配——单一价格输入论文几乎不再发表
5. **生成模型/扩散模型** 进入合成市场数据领域，用于增强训练样本

---

## 📊 数据透视

**按年份**

| 年份 | 篇数 |
|---|---:|
| 2026 | 499 |
| 2025 | 515 |
| 2024 | 344 |

**按主题**

| 主题 | 篇数 |
|---|---:|
| 🤖 LLM/Agent 金融应用 | 360 |
| 🎯 强化学习交易 | 297 |
| 🌐 其他金融 AI | 141 |
| 📊 波动率预测 | 112 |
| 💼 组合优化/资产配置 | 66 |
| ⚡ 订单簿/HFT/微观结构 | 56 |
| 📈 时序模型(LSTM/RNN) | 41 |
| 🔄 Transformer 时序 | 40 |
| 🕸 图神经网络/股票关系 | 34 |
| 📰 新闻/社媒情绪 | 34 |
| ⚖ 风险/信用/欺诈 | 27 |
| 🛡 对抗/鲁棒性 | 25 |
| 📐 期权/衍生品 | 22 |
| 🌊 市场状态/Regime | 22 |
| 🧪 回测/市场模拟 | 20 |
| 🎨 多模态融合 | 16 |
| 🔍 因子挖掘/Alpha 发现 | 14 |
| 📑 财报/披露文本分析 | 9 |
| 🎲 生成模型/合成数据 | 7 |
| ₿ 加密货币/区块链 | 7 |
| 📐 统计套利/均值回归 | 5 |
| 💡 可解释性 | 3 |

**按数据源**

| 源 | 篇数 |
|---|---:|
| arXiv | 1201 |
| OpenReview | 122 |
| AAAI | 35 |

---

## 🏆 Top 20 必读论文（综合权重排）

筛选标准：发表年份 + 摘要质量 + 关键创新词密度 + AAAI 同行评审加分。**这 20 篇是给你最高优先级看的**。

### 1. Navigating the Alpha Jungle: An LLM-Powered MCTS Framework for Formulaic Alpha Factor Mining

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 2: AAAI-26 Technical Tracks 2)
- **作者**：Authors Yu Shi Institute for Interdisciplinary Information Sciences, Tsinghua University Yitong Duan Institute for Interdisciplinary Information Sciences, Tsinghua University Zhongguancun Institute of
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/37069
- **摘要**：Alpha factor mining is pivotal in quantitative investment for identifying predictive signals from complex financial data. While traditional formulaic alpha mining relies on human expertise, contemporary automated methods, such as those based on genetic programming or reinforcement learning, often struggle with search inefficiency or yield alpha factors that are difficult to interpret. This paper introduces a novel framework that integrates Large Language Models (LLMs) with Monte Carlo Tree Search (MCTS) to overcome these limitations. Our framework leverages the LLM's instruction-following and reasoning capability to iteratively generate and refine symbolic alpha formulas within an MCTS-driven exploration. A key innovation is the guidance of MCTS exploration by rich, quantitative feedback from financial backtesting of each candidate factor, enabling efficient navigation of the vast search space. Furthermore, a frequent subtree avoidance mechanism is introduced to enhance search diversity and prevent formulaic homogenization, further improving performance. Experimental results on real-world stock market data demonstrate that our LLM-based framework outperforms existing methods by mining alphas with superior predictive accuracy and trading performance. The resulting formulas are also more amenable to human interpretation, establishing a more effective and efficient paradigm for formulaic alpha mining.

### 2. An Interactive Simulation Framework by Ensemble Imitation Learning Agents for Training Robust Trading Policies

- **类别**：🎯 强化学习交易
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 47: AAAI-26 New Faculty Highlights, Journal Trac)
- **作者**：Authors Julian Zhong-Nan Zhang National Key Laboratory for Novel Software Technology, Nanjing University Yang Yu National Key Laboratory for Novel Software Technology, Nanjing University
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/41493
- **摘要**：The reliable deployment of reinforcement learning (RL) for real-world algorithmic trading is critically hindered by the ``simulation-to-reality gap.'' Standard industry backtesting on static historical data ignores market impact—the feedback loop where an agent's trades influence price dynamics—leading to strategies that are fragile and untrustworthy in live markets. To solve this significant problem, we present a novel and emerging application of AI: a framework for building an interactive, responsive market simulator. Our system first uses imitation learning (IL) to automatically train an ensemble of agents, each learning a distinct trading strategy from a different historical market regime (e.g., bull, bear). This creates a data-driven proxy for a diverse population of real-world traders. We then deploy an innovative Action Synthesis Network to synthesize the actions of this ensemble, generating a realistic, synthetic price trajectory that endogenously models the market's reaction to trades. This interactive environment is then used to train a final RL policy. We evaluate our system on NASDAQ-100 (QQQ) data, and the results demonstrate strong potential for deployment. The RL policy trained in our responsive simulator achieves significantly more robust performance, exhibiting superior downside protection during market downturns compared to various traditional baselines. This application provides a scalable and technically sound methodology for building more realistic training environments, presenting a clear path toward the development and eventual deployment of more resilient and effective algorithmic trading strategies.

### 3. CLER: Improving Multimodal Financial Reasoning by Cross-MLLM Error Reflection

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 36: AAAI-26 Technical Tracks 36)
- **作者**：Authors Shuangyan Deng University of Auckland Zhongsheng Wang University of Auckland Rui Mao Nanyang Technological University Ciprian Doru Giurcăneanu University of Auckland Jiamou Liu University of A
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/40303
- **摘要**：Recent advances in Multimodal Large Language Models (MLLMs) have enabled joint reasoning over financial textual and visual inputs. However, they still struggle with financial terminology, logical consistency, and numerical computations. Moreover, while commercial large models perform well on reasoning tasks, their high inference costs limit their scalable usage in real world financial applications. We thus propose a cost-effective framework, CLER, that combines contrastive retrieval with step-wise reflection to improve reasoning performance. Also, the reasoning cost is only generated in the test stage when using commercial large models. CLER leverages FinErrorSet, a dataset of 8,000+ mistake correction pairs from diverse open-source MLLMs. A fine grained retriever is trained to identify structurally relevant errors for self-correction through individual reflection. Experiments on three benchmarks show that CLER consistently outperforms other baselines. To our knowledge, CLER is the first framework to use cross-model errors for financial reasoning.

### 4. When Valid Signals Fail: Regime Boundaries Between LLM Features and RL Trading Policies

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：arXiv (arXiv cs.CL, cs.AI, cs.CE)
- **作者**：Zhengzhe Yang
- **链接**：http://arxiv.org/abs/2604.10996v1
- **摘要**：Can large language models (LLMs) generate continuous numerical features that improve reinforcement learning (RL) trading agents? We build a modular pipeline where a frozen LLM serves as a stateless feature extractor, transforming unstructured daily news and filings into a fixed-dimensional vector consumed by a downstream PPO agent. We introduce an automated prompt-optimization loop that treats the extraction prompt as a discrete hyperparameter and tunes it directly against the Information Coefficient - the Spearman rank correlation between predicted and realized returns - rather than NLP losses. The optimized prompt discovers genuinely predictive features (IC above 0.15 on held-out data). However, these valid intermediate representations do not automatically translate into downstream task performance: during a distribution shift caused by a macroeconomic shock, LLM-derived features add noise, and the augmented agent under-performs a price-only baseline. In a calmer test regime the agent recovers, yet macroeconomic state variables remain the most robust driver of policy improvement. Our findings highlight a gap between feature-level validity and policy-level robustness that parallels known challenges in transfer learning under distribution shift.

### 5. ArchetypeTrader: Reinforcement Learning for Selecting and Refining Learnable Strategic Archetypes in Quantitative Trading

- **类别**：🎯 强化学习交易
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 34: AAAI-26 Technical Tracks 34)
- **作者**：Authors Chuqiao Zong Nanyang Technological University Molei Qin Nanyang Technological University Haochong Xia Nanyang Technological University Bo An Nanyang Technological University
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/40166
- **摘要**：Quantitative trading using mathematical models and automated execution to generate trading decisions has been widely applied acorss financial markets. Recently, reinforcement learning (RL) has emerged as a promising approach for developing profitable trading strategies, especially in highly volatile markets like cryptocurrency. However, existing RL methods for cryptocurrency trading face two critical drawbacks: 1) Prior RL algorithms segment markets using handcrafted indicators (e.g., trend or volatility) to train specialized sub-policies. However, these coarse labels oversimplify market dynamics into rigid categories, biasing policies toward obvious patterns like trend-following and neglecting nuanced but lucrative opportunities. 2) Current RL methods fail to systematically use demonstration data. While some approaches ignore demonstrations altogether, others rely on “optimal” yet overly granular trajectories or human-crafted strategies, both of which can overwhelm learning and introduce significant bias, resulting in high variance and significant profit losses. To address these problems, we propose ArchetypeTrader, a novel reinforcement learning framework that automatically selects and refines data-driven trading archetypes distilled from demonstrations. The framework operates in three phases: 1) We use dynamic programming (DP) to generate representative expert trajectories and train a vector-quantized encoder-decoder architecture to distill these demonstrations into discrete, reusable strategic archetypes through self-supervised learning, capturing nuanced market-behavior patterns without human heuristics. 2) We then train an RL agent to select contextually appropriate archetypes from the learned codebook and reconstruct action sequences for the upcoming horizons, ef...

### 6. OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Based Multi-Agent Systems

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：arXiv (arXiv cs.AI, cs.SE, q-fin.TR)
- **作者**：Kun Liu, Liqun Chen
- **链接**：http://arxiv.org/abs/2604.11477v1
- **摘要**：The alignment of Multi-Agent Systems (MAS) for autonomous software engineering is constrained by evaluator epistemic uncertainty. Current paradigms, such as Reinforcement Learning from Human Feedback (RLHF) and AI Feedback (RLAIF), frequently induce model sycophancy, while execution-based environments suffer from adversarial "Test Evasion" by unconstrained agents. In this paper, we introduce an objective alignment paradigm: \textbf{Out-of-Money Reinforcement Learning (OOM-RL)}. By deploying agents into the non-stationary, high-friction reality of live financial markets, we utilize critical capital depletion as an un-hackable negative gradient. Our longitudinal 20-month empirical study (July 2024 -- February 2026) chronicles the system's evolution from a high-turnover, sycophantic baseline to a robust, liquidity-aware architecture. We demonstrate that the undeniable ontological consequences of financial loss forced the MAS to abandon overfitted hallucinations in favor of the \textbf{Strict Test-Driven Agentic Workflow (STDAW)}, which enforces a Byzantine-inspired uni-directional state lock (RO-Lock) anchored to a deterministically verified $\geq 95\%$ code coverage constraint matrix. Our results show that while early iterations suffered severe execution decay, the final OOM-RL-aligned system achieved a stable equilibrium with an annualized Sharpe ratio of 2.06 in its mature phase. We conclude that substituting subjective human preference with rigorous economic penalties provides a robust methodology for aligning autonomous agents in high-stakes, real-world environments, laying the groundwork for generalized paradigms where computational billing acts as an objective physical constraint

### 7. Kill-Chain Canaries: Stage-Level Tracking of Prompt Injection Across Attack Surfaces and Model Safety Tiers

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：arXiv (arXiv cs.CR, cs.AI, cs.LG)
- **作者**：Haochuan Kevin Wang, Zechen Zhang
- **链接**：http://arxiv.org/abs/2603.28013v3
- **摘要**：Multi-agent LLM systems are entering production -- processing documents, managing workflows, acting on behalf of users -- yet their resilience to prompt injection is still evaluated with a single binary: did the attack succeed? This leaves architects without the diagnostic information needed to harden real pipelines. We introduce a kill-chain canary methodology that tracks a cryptographic token through four stages (EXPOSED -> PERSISTED -> RELAYED -> EXECUTED) across 950 runs, five frontier LLMs, six attack surfaces, and five defense conditions. The results reframe prompt injection as a pipeline-architecture problem: every model is fully exposed, yet outcomes diverge downstream -- Claude blocks all injections at memory-write (0/164 ASR), GPT-4o-mini propagates at 53%, and DeepSeek exhibits 0%/100% across surfaces from the same model. Three findings matter for deployment: (1) write-node placement is the highest-leverage safety decision -- routing writes through a verified model eliminates propagation; (2) all four defenses fail on at least one surface due to channel mismatch alone, no adversarial adaptation required; (3) invisible whitefont PDF payloads match or exceed visible-text ASR, meaning rendered-layer screening is insufficient. These dynamics apply directly to production: institutional investors and financial firms already run NLP pipelines over earnings calls, SEC filings, and analyst reports -- the document-ingestion workflows now migrating to LLM agents. Code, run logs, and tooling are publicly released.

### 8. SkyNet: Belief-Aware Planning for Partially-Observable Stochastic Games

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：arXiv (arXiv cs.AI)
- **作者**：Adam Haile
- **链接**：http://arxiv.org/abs/2603.27751v1
- **摘要**：In 2019, Google DeepMind released MuZero, a model-based reinforcement learning method that achieves strong results in perfect-information games by combining learned dynamics models with Monte Carlo Tree Search (MCTS). However, comparatively little work has extended MuZero to partially observable, stochastic, multi-player environments, where agents must act under uncertainty about hidden state. Such settings arise not only in card games but in domains such as autonomous negotiation, financial trading, and multi-agent robotics. In the absence of explicit belief modeling, MuZero's latent encoding has no dedicated mechanism for representing uncertainty over unobserved variables.   To address this, we introduce SkyNet (Belief-Aware MuZero), which adds ego-conditioned auxiliary heads for winner prediction and rank estimation to the standard MuZero architecture. These objectives encourage the latent state to retain information predictive of outcomes under partial observability, without requiring explicit belief-state tracking or changes to the search algorithm.   We evaluate SkyNet on Skyjo, a partially observable, non-zero-sum, stochastic card game, using a decision-granularity environment, transformer-based encoding, and a curriculum of heuristic opponents with self-play. In 1000-game head-to-head evaluations at matched checkpoints, SkyNet achieves a 75.3% peak win rate against the baseline (+194 Elo, $p < 10^{-50}$). SkyNet also outperforms the baseline against heuristic opponents (0.720 vs.\ 0.466 win rate). Critically, the belief-aware model initially underperforms the baseline but decisively surpasses it once training throughput is sufficient, suggesting that belief-aware auxiliary supervision improves learned representations under partial observability, but only given a...

### 9. Adaptive Regime-Aware Stock Price Prediction Using Autoencoder-Gated Dual Node Transformers with Reinforcement Learning Control

- **类别**：🎯 强化学习交易
- **年份**：2026 | **源**：arXiv (arXiv cs.LG, cs.AI, q-fin.ST)
- **作者**：Mohammad Al Ridhawi, Mahtab Haj Ali, Hussein Al Osman
- **链接**：http://arxiv.org/abs/2603.19136v2
- **摘要**：Stock markets exhibit regime-dependent behavior where prediction models optimized for stable conditions often fail during volatile periods. Existing approaches typically treat all market states uniformly or require manual regime labeling, which is expensive and quickly becomes stale as market dynamics evolve. This paper introduces an adaptive prediction framework that adaptively identifies deviations from normal market conditions and routes data through specialized prediction pathways. The architecture consists of three components: (1) an autoencoder trained on normal market conditions that identifies anomalous regimes through reconstruction error, (2) dual node transformer networks specialized for stable and event-driven market conditions respectively, and (3) a Soft Actor-Critic reinforcement learning controller that adaptively tunes the regime detection threshold and pathway blending weights based on prediction performance feedback. The reinforcement learning component enables the system to learn adaptive regime boundaries, defining anomalies as market states where standard prediction approaches fail. Experiments on 20 S&P 500 stocks spanning 1982 to 2025 demonstrate that the proposed framework achieves 0.68% mean absolute percentage error (MAPE) for one-day predictions without the reinforcement controller and 0.59% MAPE with the full adaptive system, compared to 0.80% for the baseline integrated node transformer. Directional accuracy reaches 72% with the complete framework. The system maintains robust performance during high-volatility periods, with MAPE below 0.85% when baseline models exceed 1.5%. Ablation studies confirm that each component contributes meaningfully: autoencoder routing accounts for 36% relative MAPE degradation upon removal, followed by the SAC c...

### 10. RAmmStein: Regime Adaptation in Mean-reverting Markets with Stein Thresholds -- Optimal Impulse Control in Concentrated AMMs

- **类别**：🎯 强化学习交易
- **年份**：2026 | **源**：arXiv (arXiv cs.LG, q-fin.TR)
- **作者**：Pranay Anchuri
- **链接**：http://arxiv.org/abs/2602.19419v2
- **摘要**：Concentrated liquidity provision in decentralized exchanges presents a fundamental Impulse Control problem. Liquidity Providers (LPs) face a non-trivial trade-off between maximizing fee accrual through tight price-range concentration and minimizing the friction costs of rebalancing, including gas fees and swap slippage. Existing methods typically employ heuristic or threshold strategies that fail to account for market dynamics.   This paper formulates liquidity management as an optimal control problem and derives the corresponding Hamilton-Jacobi-Bellman quasi-variational inequality (HJB-QVI). We present an approximate solution RAmmStein, a Deep Reinforcement Learning method that incorporates the mean-reversion speed (theta) of an Ornstein-Uhlenbeck process among other features as input to the model. We demonstrate that the agent learns to separate the state space into regions of action and inaction. We further extend the framework with RAmmStein-Width, which jointly optimizes rebalancing timing and position width via a 6-action DDQN.   We evaluate the framework using high-frequency 1Hz Coinbase trade data comprising over 6.8M trades on a realistic environment (10M TVL, 1% default width). Experimental results show that RAmmStein achieves a net ROI of 1.60%, the highest among all realistic (non-omniscient) strategies, while greedy strategies lose up to -8.4% to gas costs. Notably, the agent reduces rebalancing frequency by 85% compared to greedy rebalancing. RAmmStein-Width discovers extreme parsimony on its own, executing only 9 rebalances and $40 in gas, and degrades more slowly than all active strategies at elevated gas costs. Our results demonstrate that regime-aware laziness can significantly improve capital efficiency by preserving the returns that would otherwise ...

### 11. QuantaAlpha: An Evolutionary Framework for LLM-Driven Alpha Mining

- **类别**：🔍 因子挖掘/Alpha 发现
- **年份**：2026 | **源**：arXiv (arXiv q-fin.ST, cs.AI, q-fin.CP)
- **作者**：Jun Han, Shuo Zhang, Wei Li, Zhi Yang, Yifan Dong, Tu Hu, Jialuo Yuan, Xiaomin Yu
- **链接**：http://arxiv.org/abs/2602.07085v2
- **摘要**：Financial markets are noisy and non-stationary, making alpha mining highly sensitive to noise in backtesting results and sudden market regime shifts. While recent agentic frameworks improve alpha mining automation, they often lack controllable multi-round search and reliable reuse of validated experience. To address these challenges, we propose QuantaAlpha, an evolutionary alpha mining framework that treats each end-to-end mining run as a trajectory and improves factors through trajectory-level mutation and crossover operations. QuantaAlpha localizes suboptimal steps in each trajectory for targeted revision and recombines complementary high-reward segments to reuse effective patterns, enabling structured exploration and refinement across mining iterations. During factor generation, QuantaAlpha enforces semantic consistency across the hypothesis, factor expression, and executable code, while constraining the complexity and redundancy of the generated factor to mitigate crowding. Extensive experiments on the China Securities Index 300 (CSI 300) demonstrate consistent gains over strong baseline models and prior agentic systems. When utilizing GPT-5.2, QuantaAlpha achieves an Information Coefficient (IC) of 0.1501, with an Annualized Rate of Return (ARR) of 27.75% and a Maximum Drawdown (MDD) of 7.98%. Moreover, factors mined on CSI 300 transfer effectively to the China Securities Index 500 (CSI 500) and the Standard & Poor's 500 Index (S&P 500), delivering 160% and 137% cumulative excess return over four years, respectively, which indicates strong robustness of QuantaAlpha under market distribution shifts.

### 12. Learning to Staff: Offline Reinforcement Learning and Fine-Tuned LLMs for Warehouse Staffing Optimization

- **类别**：🎯 强化学习交易
- **年份**：2026 | **源**：arXiv (arXiv cs.LG)
- **作者**：Kalle Kujanpää, Yuying Zhu, Kristina Klinkner, Shervin Malmasi
- **链接**：http://arxiv.org/abs/2603.24883v1
- **摘要**：We investigate machine learning approaches for optimizing real-time staffing decisions in semi-automated warehouse sortation systems. Operational decision-making can be supported at different levels of abstraction, with different trade-offs. We evaluate two approaches, each in a matching simulation environment. First, we train custom Transformer-based policies using offline reinforcement learning on detailed historical state representations, achieving a 2.4% throughput improvement over historical baselines in learned simulators. In high-volume warehouse operations, improvements of this size translate to significant savings. Second, we explore LLMs operating on abstracted, human-readable state descriptions. These are a natural fit for decisions that warehouse managers make using high-level operational summaries. We systematically compare prompting techniques, automatic prompt optimization, and fine-tuning strategies. While prompting alone proves insufficient, supervised fine-tuning combined with Direct Preference Optimization on simulator-generated preferences achieves performance that matches or slightly exceeds historical baselines in a hand-crafted simulator. Our findings demonstrate that both approaches offer viable paths toward AI-assisted operational decision-making. Offline RL excels with task-specific architectures. LLMs support human-readable inputs and can be combined with an iterative feedback loop that can incorporate manager preferences.

### 13. FinRpt: Dataset, Evaluation System and LLM-based Multi-agent Framework for Equity Research Report Generation

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 1: AAAI-26 Technical Tracks 1)
- **作者**：Authors Song Jin Renmin University of China Shuqi Li Renmin University of China King Abdullah University of Science and Technology Shukun Zhang Renmin University of China Rui Yan Renmin University of 
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/37014
- **摘要**：While LLMs have shown great success in financial tasks like stock prediction and question answering, their application in fully automating Equity Research Report generation remains uncharted territory. In this paper, we formulate the Equity Research Report (ERR) Generation task for the first time. To address the data scarcity and the evaluation metrics absence, we present an open-source evaluation benchmark for ERR generation - FinRpt. We frame a Dataset Construction Pipeline that integrates 7 financial data types and produces a high-quality ERR dataset automatically, which could be used for model training and evaluation. We also introduce a comprehensive evaluation system including 11 metrics to assess the generated ERRs. Moreover, we propose a multi-agent framework specifically tailored to address this task, named FinRpt-Gen, and train several LLM-based agents on the proposed datasets using Supervised Fine-Tuning and Reinforcement Learning. Experimental results indicate the data quality and metrics effectiveness of the benchmark FinRpt and the strong performance of FinRpt-Gen, showcasing their potential to drive innovation in the ERR generation field. All code and datasets are publicly available.

### 14. FactorEngine: A Program-level Knowledge-Infused Factor Mining Framework for Quantitative Investment

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：arXiv (arXiv cs.AI)
- **作者**：Qinhong Lin, Ruitao Feng, Yinglun Feng, Zhenxin Huang, Yukun Chen, Zhongliang Yang, Linna Zhou, Binjie Fei
- **链接**：http://arxiv.org/abs/2603.16365v2
- **摘要**：We study alpha factor mining, the automated discovery of predictive signals from noisy, non-stationary market data-under a practical requirement that mined factors be directly executable and auditable, and that the discovery process remain computationally tractable at scale. Existing symbolic approaches are limited by bounded expressiveness, while neural forecasters often trade interpretability for performance and remain vulnerable to regime shifts and overfitting. We introduce FactorEngine (FE), a program-level factor discovery framework that casts factors as Turing-complete code and improves both effectiveness and efficiency via three separations: (i) logic revision vs. parameter optimization, (ii) LLM-guided directional search vs. Bayesian hyperparameter search, and (iii) LLM usage vs. local computation. FE further incorporates a knowledge-infused bootstrapping module that transforms unstructured financial reports into executable factor programs through a closed-loop multi-agent extraction-verification-code-generation pipeline, and an experience knowledge base that supports trajectory-aware refinement (including learning from failures). Across extensive backtests on real-world OHLCV data, FE produces factors with substantially stronger predictive stability and portfolio impact-for example, higher IC/ICIR (and Rank IC/ICIR) and improved AR/Sharpe, than baseline methods, achieving state-of-the-art predictive and portfolio performance.

### 15. FinMMDocR: Benchmarking Financial Multimodal Reasoning with Scenario Awareness, Document Understanding, and Multi-Step Computation

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 30: AAAI-26 Technical Tracks 30)
- **作者**：Authors Zichen Tang Beijing University of Posts and Telecommunications Haihong E Beijing University of Posts and Telecommunications Rongjin Li Beijing University of Posts and Telecommunications Jiache
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/39785
- **摘要**：We introduce FinMMDocR, a novel bilingual multimodal benchmark for evaluating multimodal large language models (MLLMs) on real-world financial numerical reasoning. Compared to existing benchmarks, our work delivers three major advancements. (1) Scenario Awareness: 57.9% of 1,200 expert-annotated problems incorporate 12 types of implicit financial scenarios (e.g., Portfolio Management), challenging models to perform expert-level reasoning based on assumptions; (2) Document Understanding: 837 Chinese/English documents spanning 9 types (e.g., Company Research) average 50.8 pages with rich visual elements, significantly surpassing existing benchmarks in both breadth and depth of financial documents; (3) Multi-Step Computation: Problems demand 11-step reasoning on average (5.3 extraction + 5.7 calculation steps), with 65.0% requiring cross-page evidence (2.4 pages average). The best-performing MLLM achieves only 58.0% accuracy, and different retrieval-augmented generation (RAG) methods show significant performance variations on this task. We expect FinMMDocR to drive improvements in MLLMs and reasoning-enhanced methods on complex multimodal reasoning tasks in real-world scenarios.

### 16. Toward Expert Investment Teams:A Multi-Agent LLM System with Fine-Grained Trading Tasks

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：arXiv (arXiv cs.AI, q-fin.TR)
- **作者**：Kunihiro Miyazaki, Takanobu Kawahara, Stephen Roberts, Stefan Zohren
- **链接**：http://arxiv.org/abs/2602.23330v1
- **摘要**：The advancement of large language models (LLMs) has accelerated the development of autonomous financial trading systems. While mainstream approaches deploy multi-agent systems mimicking analyst and manager roles, they often rely on abstract instructions that overlook the intricacies of real-world workflows, which can lead to degraded inference performance and less transparent decision-making. Therefore, we propose a multi-agent LLM trading framework that explicitly decomposes investment analysis into fine-grained tasks, rather than providing coarse-grained instructions. We evaluate the proposed framework using Japanese stock data, including prices, financial statements, news, and macro information, under a leakage-controlled backtesting setting. Experimental results show that fine-grained task decomposition significantly improves risk-adjusted returns compared to conventional coarse-grained designs. Crucially, further analysis of intermediate agent outputs suggests that alignment between analytical outputs and downstream decision preferences is a critical driver of system performance. Moreover, we conduct standard portfolio optimization, exploiting low correlation with the stock index and the variance of each system's output. This approach achieves superior performance. These findings contribute to the design of agent structure and task configuration when applying LLM agents to trading systems in practical settings.

### 17. Multi-Agent Reinforcement Learning for Modeling, Simulating, and Optimizing Energy Markets

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 45: AAAI-26 Special Track AI for Social Impact I)
- **作者**：Authors Matan Levy Faculty of Electrical Engineering and Computing, Technion - Israel Institute of Technology Itay Segev Faculty of Computer Science, Technion - Israel Institute of Technology Alexande
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/41229
- **摘要**：The objective of this study is to advance the optimization of hybrid electricity markets using multi-agent reinforcement learning (MARL). The transition from centralized systems to public–private models introduces significant challenges, including the emergence of independent market players and the increasing integration of renewable energy sources (RESs). These challenges are further intensified by rapidly shifting demand patterns, driven both by energy-intensive data centers and AI inference workloads, as well as by political and societal instabilities.

To address these complexities, we develop a formal model of market participants’ behavior and propose a MARL-based framework for optimizing system operator strategies. This framework incorporates dynamic pricing and dispatch scheduling to minimize operational costs, maintain grid stability, and align market incentives. We also present a new, adaptable simulation environment compatible with state-of-the-art MARL methods. Empirical evaluations in increasingly complex scenarios demonstrate the effectiveness of our approach in capturing the dynamic and decentralized nature of modern electricity markets.

### 18. MARS: A Meta-Adaptive Reinforcement Learning Framework for Risk-Aware Multi-Agent Portfolio Management

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 24: AAAI-26 Technical Tracks 24)
- **作者**：Authors Jiayi Chen New Jersey Institute of Technology Jing Li New Jersey Institute of Technology Guiling Wang New Jersey Institute of Technology
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/39095
- **摘要**：Reinforcement Learning (RL) has shown significant promise in automated portfolio management; however, effectively balancing risk and return remains a central challenge, as many models fail to adapt to dynamically changing market conditions. We propose Meta-controlled Agents for a Risk-aware System (MARS), a novel framework addressing this through a multi-agent, risk-aware approach. MARS replaces monolithic models with a Heterogeneous Agent Ensemble, where each agent’s unique risk profile is enforced by a Safety-Critic network to span behaviors from capital preservation to aggressive growth. A high-level Meta-Adaptive Controller (MAC) dynamically orchestrates this ensemble, shifting reliance between conservative and aggressive agents to minimize drawdown during downturns while seizing opportunities in bull markets. This two-tiered structure leverages behavioral diversity rather than explicit feature engineering to ensure a disciplined portfolio robust across market regimes. Experiments on major international indexes confirm that our framework significantly reduces maximum drawdown and volatility while maintaining competitive returns.

### 19. FinMathBench: A Formula-Driven Benchmark for Evaluating LLMs’ Math Reasoning Capabilities in Finance

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：AAAI (Vol. 40 No. 37: AAAI-26 Technical Tracks 37)
- **作者**：Authors Yi He Ant Group Ping Wang Ant Group Shiqiang Xiong Ant Group Chao Chen Ant Group Haixiang Hu Ant Group
- **链接**：https://ojs.aaai.org/index.php/AAAI/article/view/40358
- **摘要**：Many existing financial math reasoning benchmarks suffer from data contamination and high manual construction costs. To address this, we propose a novel formula-driven approach to dynamically construct math reasoning benchmarks in finance. Our two-stage approach: (1) generates single-formula questions by LLMs using a "Mask-for-Solve" paradigm for ground truth answers, and (2) synthesizes multi-formula questions through hierarchical tree-based DAGs. Our approach ensures novelty (via LLMs' creativity) and controllability of difficulty (via DAG structure). Based on a self-constructed financial formula bank, we utilize the proposed method to build FinMathBench, the first formula-driven and fully LLM-generated benchmark aimed at assessing LLMs' math reasoning abilities in finance, containing 946 questions across 4 complexity levels. Evaluation results on 40 LLMs demonstrate significant accuracy drops in multi-formula questions, e.g., 72.9% (1-Formula) to 14.0% (4-Formula) for GPT-4o under Chain-of-Thought prompting. Three critical flaws of LLMs are also observed: poor direct calculation performance, bias toward frequently solved variables in formulas, and erroneous "correction" of valid but extreme financial values. These findings highlight gaps in current LLMs' domain-specific reasoning and underscore FinMathBench's value for advancing robust financial LLMs.

### 20. Shared Lexical Task Representations Explain Behavioral Variability In LLMs

- **类别**：🤖 LLM/Agent 金融应用
- **年份**：2026 | **源**：arXiv (arXiv cs.CL, cs.AI, cs.LG)
- **作者**：Zhuonan Yang, Jacob Xiaochen Li, Francisco Piedrahita Velez, Eric Todd, David Bau, Michael L. Littman, Stephen H. Bach, Ellie Pavlick
- **链接**：http://arxiv.org/abs/2604.22027v1
- **摘要**：One of the most common complaints about large language models (LLMs) is their prompt sensitivity -- that is, the fact that their ability to perform a task or provide a correct answer to a question can depend unpredictably on the way the question is posed. We investigate this variation by comparing two very different but commonly-used styles of prompting: instruction-based prompts, which describe the task in natural language, and example-based prompts, which provide in-context few-shot demonstration pairs to illustrate the task. We find that, despite large variation in performance as a function of the prompt, the model engages some common underlying mechanisms across different prompts of a task. Specifically, we identify task-specific attention heads whose outputs literally describe the task -- which we dub lexical task heads -- and show that these heads are shared across prompting styles and trigger subsequent answer production. We further find that behavioral variation between prompts can be explained by the degree to which these heads are activated, and that failures are at least sometimes due to competing task representations that dilute the signal of the target task. Our results together present an increasingly clear picture of how LLMs' internal representations can explain behavior that otherwise seems idiosyncratic to users and developers.

---

## 📚 各主题代表论文

每个主题展示 Top 5 (按年份+摘要质量)；其余在最后做 reference。


### 🤖 LLM/Agent 金融应用（360 篇）

#### 📄 Dialect vs Demographics: Quantifying LLM Bias from Implicit Linguistic Signals vs. Explicit User Profiles
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.21152v1)
- **作者**：Irti Haq, Belén Saldías
- **摘要**：As state-of-the-art Large Language Models (LLMs) have become ubiquitous, ensuring equitable performance across diverse demographics is critical. However, it remains unclear whether these disparities arise from the explicitly stated identity itself or from the way identity is signaled. In real-world interactions, users' identity is often conveyed implicitly through a complex combination of various socio-linguistic factors. This study disentangles these signals by employing a factorial design with over 24,000 responses from two open-weight LLMs (Gemma-3-12B and Qwen-3-VL-8B), comparing prompts with explicitly announced user profiles against implicit dialect signals (e.g., AAVE, Singlish) across various sensitive domains. Our results uncover a unique paradox in LLM safety where users achieve ``better'' performance by sounding like a demographic than by stating they belong to it. Explicit identity prompts activate aggressive safety filters, increasing refusal rates and reducing semantic similarity compared to our reference text for Black users. In contrast, implicit dialect cues trigger a powerful ``dialect jailbreak,'' reducing refusal probability to near zero while simultaneously ach...

#### 📄 Signal or Noise in Multi-Agent LLM-based Stock Recommendations?
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.17327v1)
- **作者**：George Fatouros, Kostas Metaxas
- **摘要**：We present the first portfolio-level validation of MarketSenseAI, a deployed multi-agent LLM equity system. All signals are generated live at each observation date, eliminating look-ahead bias. The system routes four specialist agents (News, Fundamentals, Dynamics, and Macro) through a synthesis agent that issues a monthly equity thesis and recommendation for each stock in its coverage universe, and we ask two questions: do its buy recommendations add value over both passive benchmarks and random selection, and what does the internal agent structure reveal about the source of the edge? On the S&P 500 cohort (19 months) the strong-buy equal-weight portfolio earns +2.18%/month against a passive equal-weight benchmark of +1.15% (approximating RSP), a +25.2% compound excess, and ranks at the 99.7th percentile of 10,000 Monte Carlo portfolios (p=0.003). The S&P 100 cohort (35 months) delivers a +30.5% compound excess over EQWL with consistent direction but formal significance not reached, limited by the small average selection of ~10 stocks per month. Non-negative least-squares projection of thesis embeddings onto agent embeddings reveals an adaptive-integration mechanism. Agent contrib...

#### 📄 Differential Harm Propensity in Personalized LLM Agents: The Curious Case of Mental Health Disclosure
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.16734v1)
- **作者**：Caglar Yildirim
- **摘要**：Large language models (LLMs) are increasingly deployed as tool-using agents, shifting safety concerns from harmful text generation to harmful task completion. Deployed systems often condition on user profiles or persistent memory, yet agent safety evaluations typically ignore personalization signals. To address this gap, we investigated how mental health disclosure, a sensitive and realistic user-context cue, affects harmful behavior in agentic settings. Building on the AgentHarm benchmark, we evaluated frontier and open-source LLMs on multi-step malicious tasks (and their benign counterparts) under controlled prompt conditions that vary user-context personalization (no bio, bio-only, bio+mental health disclosure) and include a lightweight jailbreak injection. Our results reveal that harmful task completion is non-trivial across models: frontier lab models (e.g., GPT 5.2, Claude Sonnet 4.5, Gemini 3-Pro) still complete a measurable fraction of harmful tasks, while an open model (DeepSeek 3.2) exhibits substantially higher harmful completion. Adding a bio-only context generally reduces harm scores and increases refusals. Adding an explicit mental health disclosure often shifts outco...

#### 📄 Tiered Super-Moore's Law: Price Evolution, Production Frontiers, and Market Competition in Large Language Model Inference Services
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.28576v1)
- **作者**：Mingdeng Du
- **摘要**：This paper provides the first systematic economic analysis of token pricing in the large language model (LLM) inference market. Assembling a novel dataset integrating OpenRouter API data (318 models), Epoch AI records (3,237 models), and 62 cross-validated milestone observations spanning 2020-2026, we document an approximately 600-fold decline in token prices and propose the "Tiered Super-Moore" hypothesis. Economy-tier models exhibit a price half-life of 1.10 years and mid-tier models 1.55 years -- both significantly faster than Moore's Law's two-year benchmark -- while flagship models display near-zero exponential fit (R^2 = 0.031) due to a reasoning premium averaging 31.5 times non-reasoning prices. A Chow structural break test identifies May 2024 as the critical market inflection point (F = 5.74, p = 0.005), marking a transition from technology-driven to competition-driven price acceleration. Cost decomposition reveals that total factor productivity residuals account for approximately 103.7% of cost reduction, with GPU hardware contributing only -0.9%, confirming that software and architectural innovation -- not hardware advances -- drive the decline. Data Envelopment Analysis ...

#### 📄 Fully Homomorphic Encryption on Llama 3 model for privacy preserving LLM inference
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.12168v1)
- **作者**：Anes Abdennebi, Nadjia Kara, Laaziz Lahlou
- **摘要**：The applications of Generative Artificial Intelligence (GenAI) and their intersections with data-driven fields, such as healthcare, finance, transportation, and information security, have led to significant improvements in service efficiency and low latency. However, this synergy raises serious concerns regarding the security of large language models (LLMs) and their potential impact on the privacy of companies and users' data. Many technology companies that incorporate LLMs in their services with a certain level of command and control bear a risk of data exposure and secret divulgence caused by insecure LLM pipelines, making them vulnerable to multiple attacks such as data poisoning, prompt injection, and model theft. Although several security techniques (input/output sanitization, decentralized learning, access control management, and encryption) were implemented to reduce this risk, there is still an imminent risk of quantum computing attacks, which are expected to break existing encryption algorithms, hence, retrieving secret keys, encrypted sensitive data, and decrypting encrypted models. In this extensive work, we integrate the Post-Quantum Cryptography (PQC) based Lattice-ba...


### 🎯 强化学习交易（297 篇）

#### 📄 ArchetypeTrader: Reinforcement Learning for Selecting and Refining Learnable Strategic Archetypes in Quantitative Trading
- **2026 | AAAI** | [link](https://ojs.aaai.org/index.php/AAAI/article/view/40166)
- **作者**：Authors Chuqiao Zong Nanyang Technological University Molei Qin Nanyang Technological University Haochong Xia Nanyang Technological University Bo An N
- **摘要**：Quantitative trading using mathematical models and automated execution to generate trading decisions has been widely applied acorss financial markets. Recently, reinforcement learning (RL) has emerged as a promising approach for developing profitable trading strategies, especially in highly volatile markets like cryptocurrency. However, existing RL methods for cryptocurrency trading face two critical drawbacks: 1) Prior RL algorithms segment markets using handcrafted indicators (e.g., trend or volatility) to train specialized sub-policies. However, these coarse labels oversimplify market dynamics into rigid categories, biasing policies toward obvious patterns like trend-following and neglecting nuanced but lucrative opportunities. 2) Current RL methods fail to systematically use demonstration data. While some approaches ignore demonstrations altogether, others rely on “optimal” yet overly granular trajectories or human-crafted strategies, both of which can overwhelm learning and introduce significant bias, resulting in high variance and significant profit losses. To address these problems, we propose ArchetypeTrader, a novel reinforcement learning framework that automatically selec...

#### 📄 Fairness under uncertainty in sequential decisions
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.21711v1)
- **作者**：Michelle Seng Ah Lee, Kirtan Padh, David Watson, Niki Kilbertus, Jatinder Singh
- **摘要**：Fair machine learning (ML) methods help identify and mitigate the risk that algorithms encode or automate social injustices. Algorithmic approaches alone cannot resolve structural inequalities, but they can support socio-technical decision systems by surfacing discriminatory biases, clarifying trade-offs, and enabling governance. Although fairness is well studied in supervised learning, many real ML applications are online and sequential, with prior decisions informing future ones. Each decision is taken under uncertainty due to unobserved counterfactuals and finite samples, with dire consequences for under-represented groups, systematically under-observed due to historical exclusion and selective feedback. A bank cannot know whether a denied loan would have been repaid, and may have less data on marginalized populations.   This paper introduces a taxonomy of uncertainty in sequential decision-making -- model, feedback, and prediction uncertainty -- providing shared vocabulary for assessing systems where uncertainty is unevenly distributed across groups. We formalize model and feedback uncertainty via counterfactual logic and reinforcement learning, and illustrate harms to decision...

#### 📄 Reinforcement learning for quantum processes with memory
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.25138v1)
- **作者**：Josep Lumbreras, Ruo Cheng Huang, Yanglin Hu, Marco Fanizza, Mile Gu
- **摘要**：In reinforcement learning, an agent interacts sequentially with an environment to maximize a reward, receiving only partial, probabilistic feedback. This creates a fundamental exploration-exploitation trade-off: the agent must explore to learn the hidden dynamics while exploiting this knowledge to maximize its target objective. While extensively studied classically, applying this framework to quantum systems requires dealing with hidden quantum states that evolve via unknown dynamics. We formalize this problem via a framework where the environment maintains a hidden quantum memory evolving via unknown quantum channels, and the agent intervenes sequentially using quantum instruments. For this setting, we adapt an optimistic maximum-likelihood estimation algorithm. We extend the analysis to continuous action spaces, allowing us to model general positive operator-valued measures (POVMs). By controlling the propagation of estimation errors through quantum channels and instruments, we prove that the cumulative regret of our strategy scales as $\widetilde{\mathcal{O}}(\sqrt{K})$ over $K$ episodes. Furthermore, via a reduction to the multi-armed quantum bandit problem, we establish inform...

#### 📄 Asset Returns, Portfolio Choice, and Proportional Wealth Taxation
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.05264v2)
- **作者**：Anders G Frøseth
- **摘要**：We analyse the effect of a proportional wealth tax on asset returns, portfolio choice, and asset pricing. The tax is levied annually on the market value of all holdings at a uniform rate. We show that such a tax is economically equivalent to the government acquiring a proportional stake in the investor's portfolio each period -- a form of risk sharing in which expected wealth and risk are reduced by the same factor, while the return per share is unaffected. This multiplicative separability drives four main results. First, the coefficient of variation of wealth is invariant to the tax rate. Second, the optimal portfolio weights -- and in particular the tangency portfolio -- are independent of the tax rate. Third, the wealth tax is orthogonal to portfolio choice: it induces a homothetic contraction of the opportunity set in the mean-standard deviation plane that preserves the Sharpe ratio of every portfolio. Fourth, both taxed and untaxed investors are willing to pay the same price per share for any asset. The results are derived first under geometric Brownian motion and then generalised to any return distribution in the location-scale family. A complementary Modigliani-Miller analys...

#### 📄 Adaptive Regime-Aware Stock Price Prediction Using Autoencoder-Gated Dual Node Transformers with Reinforcement Learning Control
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.19136v2)
- **作者**：Mohammad Al Ridhawi, Mahtab Haj Ali, Hussein Al Osman
- **摘要**：Stock markets exhibit regime-dependent behavior where prediction models optimized for stable conditions often fail during volatile periods. Existing approaches typically treat all market states uniformly or require manual regime labeling, which is expensive and quickly becomes stale as market dynamics evolve. This paper introduces an adaptive prediction framework that adaptively identifies deviations from normal market conditions and routes data through specialized prediction pathways. The architecture consists of three components: (1) an autoencoder trained on normal market conditions that identifies anomalous regimes through reconstruction error, (2) dual node transformer networks specialized for stable and event-driven market conditions respectively, and (3) a Soft Actor-Critic reinforcement learning controller that adaptively tunes the regime detection threshold and pathway blending weights based on prediction performance feedback. The reinforcement learning component enables the system to learn adaptive regime boundaries, defining anomalies as market states where standard prediction approaches fail. Experiments on 20 S&P 500 stocks spanning 1982 to 2025 demonstrate that the pr...


### 🌐 其他金融 AI（141 篇）

#### 📄 Revealing Geography-Driven Signals in Zone-Level Claim Frequency Models: An Empirical Study using Environmental and Visual Predictors
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.21893v1)
- **作者**：Sherly Alfonso-Sánchez, Cristián Bravo, Kristina G. Stankova
- **摘要**：Geographic context is often consider relevant to motor insurance risk, yet public actuarial datasets provide limited location identifiers, constraining how this information can be incorporated and evaluated in claim-frequency models. This study examines how geographic information from alternative data sources can be incorporated into actuarial models for Motor Third Party Liability (MTPL) claim prediction under such constraints.   Using the BeMTPL97 dataset, we adopt a zone-level modeling framework and evaluate predictive performance on unseen postcodes. Geographic information is introduced through two channels: environmental indicators from OpenStreetMap and CORINE Land Cover, and orthoimagery released by the Belgian National Geographic Institute for academic use. We evaluate the predictive contribution of coordinates, environmental features, and image embeddings across three baseline models: generalized linear models (GLMs), regularized GLMs, and gradient-boosted trees, while raw imagery is modeled using convolutional neural networks.   Our results show that augmenting actuarial variables with constructed geographic information improves accuracy. Across experiments, both linear a...

#### 📄 A Formal Approach to AMM Fee Mechanisms with Lean 4
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.00101v1)
- **作者**：Marco Dessalvi, Massimo Bartoletti, Alberto Lluch-Lafuente
- **摘要**：Decentralized Finance (DeFi) has revolutionized financial markets by enabling complex asset-exchange protocols without trusted intermediaries. Automated Market Makers (AMMs) are a central component of DeFi, providing the core functionality of swapping assets of different types at algorithmically computed exchange rates. Several mainstream AMM implementations are based on the constant-product model, which ensures that swaps preserve the product of the token reserves in the AMM -- up to a \emph{trading fee} used to incentivize liquidity provision. Trading fees substantially complicate the economic properties of AMMs, and for this reason some AMM models abstract them away in order to simplify the analysis. However, trading fees have a non-trivial impact on users' trading strategies, making it crucial to develop refined AMM models that precisely account for their effects. We extend a foundational model of AMMs by introducing a new parameter, the trading fee $φ\in(0,1]$, into the swap rate function. Fee amounts increase inversely proportional to $φ$. When $φ= 1$, no fee is applied and the original model is recovered. We analyze the resulting fee-adjusted model from an economic perspecti...

#### 📄 Misinformation Span Detection in Videos via Audio Transcripts
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.21767v1)
- **作者**：Breno Matos, Rennan C. Lima, Savvas Zannettou, Fabricio Benevenuto, Rodrygo L. T. Santos
- **摘要**：Online misinformation is one of the most challenging issues lately, yielding severe consequences, including political polarization, attacks on democracy, and public health risks. Misinformation manifests in any platform with a large user base, including online social networks and messaging apps. It permeates all media and content forms, including images, text, audio, and video. Distinctly, video-based misinformation represents a multifaceted challenge for fact-checkers, given the ease with which individuals can record and upload videos on various video-sharing platforms. Previous research efforts investigated detecting video-based misinformation, focusing on whether a video shares misinformation or not on a video level. While this approach is useful, it only provides a limited and non-easily interpretable view of the problem given that it does not provide an additional context of when misinformation occurs within videos and what content (i.e., claims) are responsible for the video's misinformation nature.   In this work, we attempt to bridge this research gap by creating two novel datasets that allow us to explore misinformation detection on videos via audio transcripts, focusing o...

#### 📄 The Free-Market Algorithm: Self-Organizing Optimization for Open-Ended Complex Systems
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.24559v1)
- **作者**：Martin Jaraiz
- **摘要**：We introduce the Free-Market Algorithm (FMA), a novel metaheuristic inspired by free-market economics. Unlike Genetic Algorithms, Particle Swarm Optimization, and Simulated Annealing -- which require prescribed fitness functions and fixed search spaces -- FMA uses distributed supply-and-demand dynamics where fitness is emergent, the search space is open-ended, and solutions take the form of hierarchical pathway networks. Autonomous agents discover rules, trade goods, open and close firms, and compete for demand with no centralized controller.   FMA operates through a three-layer architecture: a universal market mechanism (supply, demand, competition, selection), pluggable domain-specific behavioral rules, and domain-specific observation. The market mechanism is identical across applications; only the behavioral rules change.   Validated in two unrelated domains. In prebiotic chemistry, starting from 900 bare atoms (C, H, O, N), FMA discovers all 12 feasible amino acid formulas, all 5 nucleobases, the formose sugar chain, and Krebs cycle intermediates in under 5 minutes on a laptop -- with up to 240 independent synthesis routes per product. In macroeconomic forecasting, reading a si...

#### 📄 Financial Dynamics and Interconnected Risk of Liquid Restaking
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.03274v1)
- **作者**：Hasret Ozan Sevim, Christof Ferreira Torres
- **摘要**：Decentralized finance introduces new business models and use cases as part of digital finance. Restaking has recently emerged as a transformative mechanism in DeFi, promising extra yields but introducing complex and interconnected risks. The paper monitors the current restaking landscape, empirically analyzes the revenue drivers of a liquid restaking protocol, and conducts a technical investigation on the emitted risk arising from the interconnection between liquid restaking and other protocols. The revenue dynamics of Renzo Protocol are analyzed by employing an OLS regression model, Granger-causality and random forest feature importance tests. Our results identify that revenue is primarily predicted by the value locked in the underlying EigenLayer ecosystem, the yield of Renzo protocol's liquid restaking token and the multi-blockchain expansion of that token. The multi-blockchain expansion of the liquid restaking token presents a double-edged sword: bridging to other networks is crucial for user adoption, but it adds the bridge risks to the existing risks of restaking. We investigate the cross-contamination risk between different DeFi services and the liquid restaking protocol. By...


### 📊 波动率预测（112 篇）

#### 📄 Detecting and Explaining Unlawful Insider Trading: A Shapley Value and Causal Forest Approach to Identifying Key Drivers and Causal Relationships
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.19841v1)
- **作者**：Krishna Neupane, Igor Griva, Robert Axtell, William Kennedy, Jason Kinser
- **摘要**：Corporate insiders trade for diverse reasons, often possessing Material Non-Public Information (MNPI). Determining whether specific trades leverage MNPI is a significant challenge due to inherent complexity. This study focuses on two critical objectives: accurately detecting Unlawful Insider Trading (UIT) and identifying key features explaining classification. The analysis demonstrates how combining Shapley Values (SHAP) and Causal Forest (CF) reveals these explanatory drivers.   The findings underscore the necessity of causality in identifying and interpreting UIT, requiring the consideration of alternative scenarios and potential outcomes. Within a high-dimensional feature space, the proposed architecture integrates state-of-the-art techniques to achieve high classification accuracy. The framework provides robust feature rankings via SHAP and causal significance assessments through CF, facilitating the discovery of unique causal relationships.   Statistically significant relationships are documented between the outcome and several key features, including director status, price-to-book ratio, return, and market beta. These features significantly influence the likelihood of UIT, su...

#### 📄 GARCH-FIS: A Hybrid Forecasting Model with Dynamic Volatility-Driven Parameter Adaptation
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.14793v1)
- **作者**：Wen-Jing Li, Da-Qing Zhang
- **摘要**：This paper proposes a novel hybrid model, termed GARCH-FIS, for recursive rolling multi-step forecasting of financial time series. It integrates a Fuzzy Inference System (FIS) with a Generalized Autoregressive Conditional Heteroskedasticity (GARCH) model to jointly address nonlinear dynamics and time-varying volatility. The core innovation is a dynamic parameter adaptation mechanism for the FIS, specifically activated within the multi-step forecasting cycle. In this process, the conditional volatility estimated by a rolling window GARCH model is continuously translated into a price volatility measure. At each forecasting step, this measure, alongside the updated mean of the sliding window data -- which now incorporates the most recent predicted price -- jointly determines the parameters of the FIS membership functions for the next prediction. Consequently, the granularity of the fuzzy inference adapts as the forecast horizon extends: membership functions are automatically widened during high-volatility market regimes to bolster robustness and narrowed during stable periods to enhance precision. This constitutes a fundamental advancement over a static one-step-ahead prediction setup...

#### 📄 Temporal Coverage Bias in Financial Panel Data: A Coverage-Aware Structuring Framework with Evidence from the Dhaka Stock Exchange
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.20237v2)
- **作者**：Tashreef Muhammad
- **摘要**：A common practice in empirical finance is to construct calendar-aligned panels that implicitly treat all instruments as having existed for the full observation period. When securities with different listing histories are combined without explicit coverage constraints, price histories can be inadvertently extended before valid trading ever began. This paper formalizes this problem and proposes a coverage-aware structuring framework built around instrument-level observation windows encoded through structured metadata and an availability matrix. Applied to end-of-day data from the Dhaka Stock Exchange spanning October 2012 to January 2026 and covering 486 instruments, the framework reveals substantial distortions from naive temporal alignment. ARIMA-based experiments establish the mechanism through which padded observations corrupt return dynamics, and volatility analysis across 53 instruments shows that forward-filling alone suppresses return volatility by roughly 20% on average, with GARCH unconditional variance distortions exceeding 26% in over 90% of instruments - a lower bound, as backward extension to the panel start produces 36.6% suppression and causes GARCH non-convergence in...

#### 📄 Merton's Problem with Recursive Perturbed Utility
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.13544v1)
- **作者**：Min Dai, Yuchao Dong, Yanwei Jia, Xun Yu Zhou
- **摘要**：The classical Merton investment problem predicts deterministic, state-dependent portfolio rules; however, laboratory and field evidence suggests that individuals often prefer randomized decisions leading to stochastic and noisy choices. Fudenberg et al. (2015) develop the additive perturbed utility theory to explain the preference for randomization in the static setting, which, however, becomes ill-posed or intractable in the dynamic setting. We introduce the recursive perturbed utility (RPU), a special stochastic differential utility that incorporates an entropy-based preference for randomization into a recursive aggregator. RPU endogenizes the intertemporal trade-off between utilities from randomization and bequest via a discounting term dependent on past accumulated randomization, thereby avoiding excessive randomization and yielding a well-posed problem. In a general Markovian incomplete market with CRRA preferences, we prove that the RPU-optimal portfolio policy (in terms of the risk exposure ratio) is Gaussian and can be expressed in closed form, independent of wealth. Its variance is inversely proportional to risk aversion and stock volatility, while its mean is based on the...

#### 📄 A Novel approach to portfolio construction
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.03325v1)
- **作者**：T. Di Matteo, L. Riso, M. G. Zoia
- **摘要**：This paper proposes a machine learning-based framework for asset selection and portfolio construction, termed the Best-Path Algorithm Sparse Graphical Model (BPASGM). The method extends the Best-Path Algorithm (BPA) by mapping linear and non-linear dependencies among a large set of financial assets into a sparse graphical model satisfying a structural Markov property. Based on this representation, BPASGM performs a dependence-driven screening that removes positively or redundantly connected assets, isolating subsets that are conditionally independent or negatively correlated. This step is designed to enhance diversification and reduce estimation error in high-dimensional portfolio settings. Portfolio optimization is then conducted on the selected subset using standard mean-variance techniques. BPASGM does not aim to improve the theoretical mean-variance optimum under known population parameters, but rather to enhance realized performance in finite samples, where sample-based Markowitz portfolios are highly sensitive to estimation error. Monte Carlo simulations show that BPASGM-based portfolios achieve more stable risk-return profiles, lower realized volatility, and superior risk-ad...


### 💼 组合优化/资产配置（66 篇）

#### 📄 STRIKE: Additive Feature-Group-Aware Stacking Framework for Credit Default Prediction
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.17622v1)
- **作者**：Swattik Maiti, Ritik Pratap Singh, Fardina Fathmiul Alam
- **摘要**：Credit risk default prediction remains a cornerstone of risk management in the financial industry. The task involves estimating the likelihood that a borrower will fail to meet debt obligations, an objective critical for lending decisions, portfolio optimization, and regulatory compliance. Traditional machine learning models such as logistic regression and tree-based ensembles are widely adopted for their interpretability and strong empirical performance. However, modern credit datasets are high-dimensional, heterogeneous, and noisy, increasing overfitting risk in monolithic models and reducing robustness under distributional shift. We introduce STRIKE (Stacking via Targeted Representations of Isolated Knowledge Extractors), a feature-group-aware stacking framework for structured tabular credit risk data. Rather than training a single monolithic model on the complete dataset, STRIKE partitions the feature space into semantically coherent groups and trains independent learners within each group. This decomposition is motivated by an additive perspective on risk modeling, where distinct feature sources contribute complementary evidence that can be combined through a structured aggreg...

#### 📄 Biased Mean Quadrangle and Applications
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.26901v1)
- **作者**：Anton Malandii, Stan Uryasev
- **摘要**：This paper introduces \emph{biased mean regression}, estimating the \emph{biased mean}, i.e., $\mathbb{E}[Y] + x$, where $x \in \mathbb{R}$. The approach addresses a fundamental statistical problem that covers numerous applications. For instance, it can be used to estimate factors driving portfolio loss exceeding the expected loss by a specified amount (e.g., $ x=\$10 billion$) or to estimate factors impacting a specific excess release of radiation in the environment, where nuclear safety regulations specify different severity levels.   The estimation is performed by minimizing the so-called \emph{superexpectation error}. We establish two equivalence results that connect the method to popular paradigms: (i) biased mean regression is equivalent to quantile regression for an appropriate parameterization and is equivalent to ordinary least squares when $x=0$; (ii) in portfolio optimization, minimizing \emph{superexpectation risk}, associated with the superexpectation error, is equivalent to CVaR optimization. The approach is computationally attractive, as minimizing the superexpectation error reduces to linear programming (LP), thereby offering algorithmic and modeling advantages. It ...

#### 📄 Hyper-Adaptive Momentum Dynamics for Native Cubic Portfolio Optimization: Avoiding Quadratization Distortion in Higher-Order Cardinality-Constrained Search
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.15947v1)
- **作者**：Greg Serbarinov
- **摘要**：We study cubic cardinality-constrained portfolio optimization, a higher-order extension of the standard Markowitz formulation where three-way sector co-movement terms augment the quadratic risk-return objective. Classical heuristics like simulated annealing (SA) and tabu search require Rosenberg quadratization of these cubic interactions. This inflates the variable count from n to 5n and introduces penalty terms that substantially distort the augmented search landscape. In contrast, Hyper-Adaptive Momentum Dynamics (HAMD) operates directly on the native higher-order objective using a hybrid pipeline combining continuous Hamiltonian search, exact cardinality-preserving projection, and iterated local search (ILS). On a cubic portfolio benchmark under matched 60-second CPU budgets, HAMD achieves substantially lower decoded native cubic objective values than SA and tabu search, yielding single-seed relative improvements of 87.9%, 71.2%, 59.5%, and 46.9% at n = 200, 300, 500, and 1000. In a detailed three-seed study at n = 200, HAMD attains a median native objective of 195.65 (zero variance), while SA and tabu yield 1208.07. Decoded-feasibility analysis shows SA satisfies all exact card...

#### 📄 Money-Back Tontines for Retirement Decumulation: Neural-Network Optimization under Systematic Longevity Risk
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.16212v1)
- **作者**：German Nova Orozco, Duy-Minh Dang, Peter A. Forsyth
- **摘要**：Money-back guarantees (MBGs) are features of pooled retirement income products that address bequest concerns by ensuring the initial premium is returned through lifetime payments or, upon early death, as a death benefit to the estate. This paper studies optimal retirement decumulation in an individual tontine account with an MBG overlay under international diversification and systematic longevity risk. The retiree chooses withdrawals and asset allocation dynamically to trade off expected total withdrawals (EW) against the Conditional Value-at-Risk (CVaR) of terminal wealth, subject to realistic investment constraints. The optimization is solved under a plan-to-live convention, while stochastic mortality affects outcomes through its impact on mortality credits at the pool level. We develop a neural-network based computational approach for the resulting high-dimensional, constrained control problem. The MBG is priced ex post under the induced EW--CVaR optimal policy via a simulation-based actuarial rule that combines expected guarantee costs with a prudential tail buffer. Using long-horizon historical return data expressed in real domestic-currency terms, we find that international d...

#### 📄 Optimal Insurance Menu Design under the Expected-Value Premium Principle
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.15881v1)
- **作者**：Xia Han, Bin Li
- **摘要**：This paper studies optimal insurance design under asymmetric information in a Stackelberg framework, where a monopolistic insurer faces uncertainty about both the insured's risk attitude, captured by a risk-aversion parameter, and the insured's risk type, characterized by the loss distribution. In particular, when the risk type is unobservable, we allow the risk-aversion parameter to depend on the risk type. We construct a menu of contracts that maximizes the mean-variance utilities of both parties under the expected-value premium principle, subject to a truth-telling constraint that ensures the truthful revelation of private information. We show that when risk attitude is private information, the optimal coverage takes the form of excess-of-loss insurance with linear pricing in terms of the risk loading (defined as the premium minus the expected loss), designed to screen risk preferences. In contrast, when risk type is unobserved, we restrict the coverage function to an excess-of-loss form and derive an ordinary differential equation that characterizes the optimal risk loading. Under mild conditions, we establish the existence and uniqueness of the solution. The results show that ...


### ⚡ 订单簿/HFT/微观结构（56 篇）

#### 📄 A Hybrid Quantum-Classical Framework for Financial Volatility Forecasting Based on Quantum Circuit Born Machines
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.09789v1)
- **作者**：Yixiong Chen
- **摘要**：Accurate forecasting of financial market volatility is crucial for risk management, option pricing, and portfolio optimization. Traditional econometric models and classical machine learning methods face challenges in handling the inherent non-linear and non-stationary characteristics of financial time series. In recent years, the rapid development of quantum computing has provided a new paradigm for solving complex optimization and sampling problems. This paper proposes a novel hybrid quantum-classical computing framework aimed at combining the powerful representation capabilities of classical neural networks with the unique advantages of quantum models. For the specific task of financial market volatility forecasting, we designed and implemented a hybrid model based on this framework, which combines a Long Short-Term Memory (LSTM) network with a Quantum Circuit Born Machine (QCBM). The LSTM is responsible for extracting complex dynamic features from historical time series data, while the QCBM serves as a learnable prior module, providing the model with a high-quality prior distribution to guide the forecasting process. We evaluated the model on two real financial datasets consisti...

#### 📄 A Learnable Wavelet Transformer for Long-Short Equity Trading and Risk-Adjusted Return Optimization
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.13435v4)
- **作者**：Shuozhe Li, Du Cheng, Leqi Liu
- **摘要**：Learning profitable intraday trading policies from financial time series is challenging due to heavy noise, non-stationarity, and strong cross-sectional dependence among related assets. We propose \emph{WaveLSFormer}, a learnable wavelet-based long-short Transformer that jointly performs multi-scale decomposition and return-oriented decision learning. Unlike standard time-series forecasting that optimizes prediction error and typically requires a separate position-sizing or portfolio-construction step, our model directly outputs a market-neutral long/short portfolio and is trained end-to-end on a trading objective with risk-aware regularization. Specifically, a learnable wavelet front-end generates low-/high-frequency components via an end-to-end trained filter bank, guided by spectral regularizers that encourage stable and well-separated frequency bands. To fuse multi-scale information, we introduce a low-guided high-frequency injection (LGHI) module that refines low-frequency representations with high-frequency cues while controlling training stability. The model outputs a portfolio of long/short positions that is rescaled to satisfy a fixed risk budget and is optimized directly ...

#### 📄 Improving Machine Learning Performance with Synthetic Augmentation
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.14498v1)
- **作者**：Mel Sohm, Charles Dezons, Sami Sellami, Oscar Ninou, Axel Pincon
- **摘要**：Synthetic augmentation is increasingly used to mitigate data scarcity in financial machine learning, yet its statistical role remains poorly understood. We formalize synthetic augmentation as a modification of the effective training distribution and show that it induces a structural bias--variance trade-off: while additional samples may reduce estimation error, they may also shift the population objective whenever the synthetic distribution deviates from regions relevant under evaluation. To isolate informational gains from mechanical sample-size effects, we introduce a size-matched null augmentation and a finite-sample, non-parametric block permutation test that remains valid under weak temporal dependence.   We evaluate this framework in both controlled Markov-switching environments and real financial datasets, including high-frequency option trade data and a daily equity panel. Across generators spanning bootstrap, copula-based models, variational autoencoders, diffusion models, and TimeGAN, we vary augmentation ratio, model capacity, task type, regime rarity, and signal-to-noise. We show that synthetic augmentation is beneficial only in variance-dominant regimes, such as persis...

#### 📄 Pregeometric Origins of Liquidity Geometry in Financial Order Books
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.17245v1)
- **作者**：João P. da Cruz
- **摘要**：We propose a structural framework for the geometry of financial order books in which liquidity, supply, and demand are treated as emergent observables rather than primitive economic variables. The market is modeled as an inflationary relational system without assumed metric, temporal, or price coordinates. Observable quantities arise only through projection, implemented here via spectral embeddings of the graph Laplacian. A one-dimensional projection induces a price-like coordinate, while the projected density defines liquidity profiles around the mid price. Under a minimal single-scale hypothesis -- excluding intrinsic length scales beyond distance to the mid and finite visibility -- we show that projected supply and demand are constrained to gamma-like functional forms. In discrete data, this prediction translates into integrated-gamma cumulative profiles. We test these results using high-frequency Level~II data for several U.S. equities and find robust agreement across assets and intraday windows. Explicit comparison with alternative cumulative models using information criteria demonstrates a systematic preference for the integrated-gamma geometry. A minimal simulation of inflat...

#### 📄 The Geometry of Risk: Path-Dependent Regulation and Anticipatory Hedging via the SigSwap
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.24154v1)
- **作者**：Daniel Bloch
- **摘要**：This paper introduces a transformative framework for managing path-dependent financial risk by shifting from traditional distribution-centric models to a geometry-based approach. We propose the SigSwap as a new regulatory instrument that allows market participants to decompose complex risk into terminal price law and the underlying texture of the price path. By utilising the mathematical properties of the path-signature, we demonstrate how previously unmodellable risks, such as lead-lag dynamics and flash-crash spiralling, can be converted into transparent and linear risk factors. Central to this framework is the introduction of Signature Expected Shortfall, a risk metric designed to capture toxic path geometries that traditional methods often overlook. We also present a proactive monitoring system based on the Temporal Exposure Profile, which utilises anticipatory learning to detect potential liquidity traps and geometric decoupling before they manifest as realised volatility. The proposed methodology offers a rigorous alignment with global regulatory mandates, specifically the Fundamental Review of the Trading Book (FRTB), by providing a consistent bridge between physical stress-...


### 📈 时序模型(LSTM/RNN)（41 篇）

#### 📄 Trend-Adjusted Time Series Models with an Application to Gold Price Forecasting
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.12706v2)
- **作者**：Sina Kazemdehbashi
- **摘要**：Time series data play a critical role in various fields, including finance, healthcare, marketing, and engineering. A wide range of techniques (from classical statistical models to neural network-based approaches such as Long Short-Term Memory (LSTM)) have been employed to address time series forecasting challenges. In this paper, we reframe time series forecasting as a two-part task: (1) predicting the trend (directional movement) of the time series at the next time step, and (2) forecasting the quantitative value at the next time step. The trend can be predicted using a binary classifier, while quantitative values can be forecasted using models such as LSTM and Bidirectional Long Short-Term Memory (Bi-LSTM). Building on this reframing, we propose the Trend-Adjusted Time Series (TATS) model, which adjusts the forecasted values based on the predicted trend provided by the binary classifier. We validate the proposed approach through both theoretical analysis and empirical evaluation. The TATS model is applied to a volatile financial time series (the daily gold price) with the objective of forecasting the next days price. Experimental results demonstrate that TATS consistently outper...

#### 📄 Forecasting the Evolving Composition of Inbound Tourism Demand: A Bayesian Compositional Time Series Approach Using Platform Booking Data
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.18358v3)
- **作者**：Harrison Katz
- **摘要**：Understanding how the composition of guest origin markets evolves over time is critical for destination marketing organizations, hospitality businesses, and tourism planners. We develop and apply Bayesian Dirichlet autoregressive moving average (BDARMA) models to forecast the compositional dynamics of guest origin market shares using proprietary Airbnb booking data spanning 2017--2025 across four major destination regions. Our analysis reveals substantial pandemic-induced structural breaks in origin composition, with heterogeneous recovery patterns across markets. In our analysis, the BDARMA framework achieves the lowest forecast error for EMEA and competitive performance across destination regions, outperforming standard benchmarks including naïve forecasts, exponential smoothing, and SARIMA on log-ratio transformed data in compositionally complex markets. For EMEA destinations, BDARMA achieves 27% lower forecast error than naïve methods ($p < 0.001$), with the greatest gains where multiple origin markets compete in the 5-25% share range. By modeling compositions directly on the simplex with a Dirichlet likelihood and incorporating seasonal variation in both mean and precision par...

#### 📄 DCD: Decomposition-based Causal Discovery from Autocorrelated and Non-Stationary Temporal Data
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.01433v1)
- **作者**：Muhammad Hasan Ferdous, Md Osman Gani
- **摘要**：Multivariate time series in domains such as finance, climate science, and healthcare often exhibit long-term trends, seasonal patterns, and short-term fluctuations, complicating causal inference under non-stationarity and autocorrelation. Existing causal discovery methods typically operate on raw observations, making them vulnerable to spurious edges and misattributed temporal dependencies. We introduce a decomposition-based causal discovery framework that separates each time series into trend, seasonal, and residual components and performs component-specific causal analysis. Trend components are assessed using stationarity tests, seasonal components using kernel-based dependence measures, and residual components using constraint-based causal discovery. The resulting component-level graphs are integrated into a unified multi-scale causal structure. This approach isolates long- and short-range causal effects, reduces spurious associations, and improves interpretability. Across extensive synthetic benchmarks and real-world climate data, our framework more accurately recovers ground-truth causal structure than state-of-the-art baselines, particularly under strong non-stationarity and ...

#### 📄 Identifying dynamical network markers of financial market instability
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.21297v1)
- **作者**：Mariko I. Ito, Hiroyuki Hasada, Yudai Honma, Takaaki Ohnishi, Tsutomu Watanabe, Kazuyuki Aihara
- **摘要**：Market instability has been extensively studied using mathematical approaches to characterize complex trading dynamics and detect structural change points. This study explores the potential for early warning of market instability by applying the Dynamical Network Marker (DNM) theory to order placement and execution data from the Tokyo Stock Exchange. DNM theory identifies indicators associated with critical slowing down -- a precursor to critical transitions -- in high-dimensional systems of many interacting elements. In this study, market participants are identified using virtual server IDs from the trading system, and multivariate time series representing their trading activities are constructed. This framework treats each participant as an interacting element, thereby enabling the application of DNM theory to the resulting time series. The results suggest that early warning signals of large price movements can be detected on a daily time scale. These findings highlight the potential to develop practical DNM-based early-warning systems for large price movements by further refining forecasting horizons and integrating multiple time series capturing different aspects of trading beh...

#### 📄 Brownian ReLU(Br-ReLU): A New Activation Function for a Long-Short Term Memory (LSTM) Network
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.16446v1)
- **作者**：George Awiakye-Marfo, Elijah Agbosu, Victoria Mawuena Barns, Samuel Asante Gyamerah
- **摘要**：Deep learning models are effective for sequential data modeling, yet commonly used activation functions such as ReLU, LeakyReLU, and PReLU often exhibit gradient instability when applied to noisy, non-stationary financial time series. This study introduces BrownianReLU, a stochastic activation function induced by Brownian motion that enhances gradient propagation and learning stability in Long Short-Term Memory (LSTM) networks. Using Monte Carlo simulation, BrownianReLU provides a smooth, adaptive response for negative inputs, mitigating the dying ReLU problem. The proposed activation is evaluated on financial time series from Apple, GCB, and the S&P 500, as well as LendingClub loan data for classification. Results show consistently lower Mean Squared Error and higher $R^2$ values, indicating improved predictive accuracy and generalization. Although ROC-AUC metric is limited in classification tasks, activation choice significantly affects the trade-off between accuracy and sensitivity, with Brownian ReLU and the selected activation functions yielding practically meaningful performance.


### 🔄 Transformer 时序（40 篇）

#### 📄 ProbFM: Probabilistic Time Series Foundation Model with Uncertainty Decomposition
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.10591v1)
- **作者**：Arundeep Chinta, Lucas Vinh Tran, Jay Katukuri
- **摘要**：Time Series Foundation Models (TSFMs) have emerged as a promising approach for zero-shot financial forecasting, demonstrating strong transferability and data efficiency gains. However, their adoption in financial applications is hindered by fundamental limitations in uncertainty quantification: current approaches either rely on restrictive distributional assumptions, conflate different sources of uncertainty, or lack principled calibration mechanisms. While recent TSFMs employ sophisticated techniques such as mixture models, Student's t-distributions, or conformal prediction, they fail to address the core challenge of providing theoretically-grounded uncertainty decomposition. For the very first time, we present a novel transformer-based probabilistic framework, ProbFM (probabilistic foundation model), that leverages Deep Evidential Regression (DER) to provide principled uncertainty quantification with explicit epistemic-aleatoric decomposition. Unlike existing approaches that pre-specify distributional forms or require sampling-based inference, ProbFM learns optimal uncertainty representations through higher-order evidence learning while maintaining single-pass computational effic...

#### 📄 Reliable Grid Forecasting: State Space Models for Safety-Critical Energy Systems
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.01410v6)
- **作者**：Sunki Hong, Jisoo Lee
- **摘要**：Accurate grid load forecasting is safety-critical: under-predictions risk supply shortfalls, while symmetric error metrics can mask this operational asymmetry. We introduce an operator-legible evaluation framework -- Under-Prediction Rate (UPR), tail $\text{Reserve}_{99.5}^{\%}$ requirements, and explicit inflation diagnostics ($\text{Bias}_{24h}$/OPR) -- to quantify one-sided reliability risk beyond MAPE.   Using this framework, we evaluate five neural architectures -- two state space models (S-Mamba, PowerMamba), two Transformers (iTransformer, PatchTST), an LSTM, and a probabilistic SSM variant (Mamba-ProbTSF) -- on a weather-aligned California Independent System Operator (CAISO) dataset spanning Nov 2023--Nov 2025 (84,498 hourly records across 5 regional transmission areas) under a rolling-origin walk-forward backtest. We develop and evaluate thermal-lag-aligned weather fusion strategies matched to each architecture's inductive bias.   Our results demonstrate that standard accuracy metrics are insufficient proxies for operational safety: models with comparable MAPE can imply materially different tail reserve requirements ($\text{Reserve}_{99.5}^{\%}$). We show that explicit wea...

#### 📄 Integrating Inductive Biases in Transformers via Distillation for Financial Time Series Forecasting
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.16985v1)
- **作者**：Yu-Chen Den, Kuan-Yu Chen, Kendro Vincent, Darby Tien-Hao Chang
- **摘要**：Transformer-based models have been widely adopted for time-series forecasting due to their high representational capacity and architectural flexibility. However, many Transformer variants implicitly assume stationarity and stable temporal dynamics -- assumptions routinely violated in financial markets characterized by regime shifts and non-stationarity. Empirically, state-of-the-art time-series Transformers often underperform even vanilla Transformers on financial tasks, while simpler architectures with distinct inductive biases, such as CNNs and RNNs, can achieve stronger performance with substantially lower complexity. At the same time, no single inductive bias dominates across markets or regimes, suggesting that robust financial forecasting requires integrating complementary temporal priors. We propose TIPS (Transformer with Inductive Prior Synthesis), a knowledge distillation framework that synthesizes diverse inductive biases -- causality, locality, and periodicity -- within a unified Transformer. TIPS trains bias-specialized Transformer teachers via attention masking, then distills their knowledge into a single student model with regime-dependent alignment across inductive bi...

#### 📄 TF-CoDiT: Conditional Time Series Synthesis with Diffusion Transformers for Treasury Futures
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.11880v1)
- **作者**：Yingxiao Zhang, Jiaxin Duan, Junfu Zhang, Ke Feng
- **摘要**：Diffusion Transformers (DiT) have achieved milestones in synthesizing financial time-series data, such as stock prices and order flows. However, their performance in synthesizing treasury futures data is still underexplored. This work emphasizes the characteristics of treasury futures data, including its low volume, market dependencies, and the grouped correlations among multivariables. To overcome these challenges, we propose TF-CoDiT, the first DiT framework for language-controlled treasury futures synthesis. To facilitate low-data learning, TF-CoDiT adapts the standard DiT by transforming multi-channel 1-D time series into Discrete Wavelet Transform (DWT) coefficient matrices. A U-shape VAE is proposed to encode cross-channel dependencies hierarchically into a latent variable and bridge the latent and DWT spaces through decoding, thereby enabling latent diffusion generation. To derive prompts that cover essential conditions, we introduce the Financial Market Attribute Protocol (FinMAP) - a multi-level description system that standardizes daily$/$periodical market dynamics by recognizing 17$/$23 economic indicators from 7/8 perspectives. In our experiments, we gather four types o...

#### 📄 Financial time series augmentation using transformer based GAN architecture
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.17865v1)
- **作者**：Andrzej Podobiński, Jarosław A. Chudziak
- **摘要**：Time-series forecasting is a critical task across many domains, from engineering to economics, where accurate predictions drive strategic decisions. However, applying advanced deep learning models in challenging, volatile domains like finance is difficult due to the inherent limitation and dynamic nature of financial time series data. This scarcity often results in sub-optimal model training and poor generalization. The fundamental challenge lies in determining how to reliably augment scarce financial time series data to enhance the predictive accuracy of deep learning forecasting models. Our main contribution is a demonstration of how Generative Adversarial Networks (GANs) can effectively serve as a data augmentation tool to overcome data scarcity in the financial domain. Specifically, we show that training a Long Short-Term Memory (LSTM) forecasting model on a dataset augmented with synthetic data generated by a transformer-based GAN (TTS-GAN) significantly improves the forecasting accuracy compared to using real data alone. We confirm these results across different financial time series (Bitcoin and S\&P500 price data) and various forecasting horizons. Furthermore, we propose a ...


### 🕸 图神经网络/股票关系（34 篇）

#### 📄 A Dynamic-Causal Lens of Stock Interactions: Graph Modeling From Symbolic Movement Patterns
- **2026 | OpenReview** | [link](https://openreview.net/forum?id=JSEhNQIpr6)
- **作者**：Haotian Liu, Bowen Hu, Yadong Zhou, Yuxun Zhou
- **摘要**：In modern quantitative finance and portfolio-based investment, modeling latent interactions among stocks is paramount for prediction and decision-making on profit, risk management, hedging, etc. While previous studies have constructed complex stock graphs for applying sophisticated variants of graph neural networks (GNNs), existing graph modeling approaches still face two limitations: 1) Correlation-based statistical relationships fail to unveil nuanced stock interactions effectively and determine directional influence. 2) Rigid and static graphs overlook the evolving graph structure of stocks in volatile financial systems. In this paper, we propose a dynamic-causal graph neural network (DC-GNN) to discover causal interactions from the non-stationary price time series and dynamically model graph structures for stock movement prediction. More specifically, we identify the pattern prototypes of all directed stock pairs from long-term price movement knowledge to quantify their causal interactions. These prototypes capture the pattern-to-pattern correspondence across time series based on symbolic dynamics. By inferring real-time stock networks from the prototypes, we encapsulate neighb...

#### 📄 Forecasting Equity Correlations with Hybrid Transformer Graph Neural Network
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.04602v1)
- **作者**：Jack Fanshawe, Rumi Masih, Alexander Cameron
- **摘要**：This paper studies forward-looking stock-stock correlation forecasting for S\&P 500 constituents and evaluates whether learned correlation forecasts can improve graph-based clustering used in basket trading strategies. We cast 10-day ahead correlation prediction in Fisher-z space and train a Temporal-Heterogeneous Graph Neural Network (THGNN) to predict residual deviations from a rolling historical baseline. The architecture combines a Transformer-based temporal encoder, which captures non-stationary, complex, temporal dependencies, with an edge-aware graph attention network that propagates cross-asset information over the equity network. Inputs span daily returns, technicals, sector structure, previous correlations, and macro signals, enabling regime-aware forecasts and attention-based feature and neighbor importance to provide interpretability. Out-of-sample results from 2019-2024 show that the proposed model meaningfully reduces correlation forecasting error relative to rolling-window estimates. When integrated into a graph-based clustering framework, forward-looking correlations produce adaptable and economically meaningfully baskets, particularly during periods of market stres...

#### 📄 MaGNet: A Mamba Dual-Hypergraph Network for Stock Prediction via Temporal-Causal and Global Relational Learning
- **2025 | arXiv** | [link](http://arxiv.org/abs/2511.00085v1)
- **作者**：Peilin Tan, Chuanqi Shi, Dian Tu, Liang Xie
- **摘要**：Stock trend prediction is crucial for profitable trading strategies and portfolio management yet remains challenging due to market volatility, complex temporal dynamics and multifaceted inter-stock relationships. Existing methods struggle to effectively capture temporal dependencies and dynamic inter-stock interactions, often neglecting cross-sectional market influences, relying on static correlations, employing uniform treatments of nodes and edges, and conflating diverse relationships. This work introduces MaGNet, a novel Mamba dual-hyperGraph Network for stock prediction, integrating three key innovations: (1) a MAGE block, which leverages bidirectional Mamba with adaptive gating mechanisms for contextual temporal modeling and integrates a sparse Mixture-of-Experts layer to enable dynamic adaptation to diverse market conditions, alongside multi-head attention for capturing global dependencies; (2) Feature-wise and Stock-wise 2D Spatiotemporal Attention modules enable precise fusion of multivariate features and cross-stock dependencies, effectively enhancing informativeness while preserving intrinsic data structures, bridging temporal modeling with relational reasoning; and (3) a...

#### 📄 Crisis-Resilient Portfolio Management via Graph-based Spatio-Temporal Learning
- **2025 | arXiv** | [link](http://arxiv.org/abs/2510.20868v1)
- **作者**：Zan Li, Rui Fan
- **摘要**：Financial time series forecasting faces a fundamental challenge: predicting optimal asset allocations requires understanding regime-dependent correlation structures that transform during crisis periods. Existing graph-based spatio-temporal learning approaches rely on predetermined graph topologies--correlation thresholds, sector classifications--that fail to adapt when market dynamics shift across different crisis mechanisms: credit contagion, pandemic shocks, or inflation-driven selloffs.   We present CRISP (Crisis-Resilient Investment through Spatio-temporal Patterns), a graph-based spatio-temporal learning framework that encodes spatial relationships via Graph Convolutional Networks and temporal dynamics via BiLSTM with self-attention, then learns sparse structures through multi-head Graph Attention Networks. Unlike fixed-topology methods, CRISP discovers which asset relationships matter through attention mechanisms, filtering 92.5% of connections as noise while preserving crisis-relevant dependencies for accurate regime-specific predictions.   Trained on 2005--2021 data encompassing credit and pandemic crises, CRISP demonstrates robust generalization to 2022--2024 inflation-dri...

#### 📄 DeXposure: A Dataset and Benchmarks for Inter-protocol Credit Exposure in Decentralized Financial Networks
- **2025 | arXiv** | [link](http://arxiv.org/abs/2511.22314v1)
- **作者**：Wenbin Wu, Kejiang Qian, Alexis Lui, Christopher Jack, Yue Wu, Peter McBurney, Fengxiang He, Bryan Zhang
- **摘要**：We curate the DeXposure dataset, the first large-scale dataset for inter-protocol credit exposure in decentralized financial networks, covering global markets of 43.7 million entries across 4.3 thousand protocols, 602 blockchains, and 24.3 thousand tokens, from 2020 to 2025. A new measure, value-linked credit exposure between protocols, is defined as the inferred financial dependency relationships derived from changes in Total Value Locked (TVL). We develop a token-to-protocol model using DefiLlama metadata to infer inter-protocol credit exposure from the token's stock dynamics, as reported by the protocols. Based on the curated dataset, we develop three benchmarks for machine learning research with financial applications: (1) graph clustering for global network measurement, tracking the structural evolution of credit exposure networks, (2) vector autoregression for sector-level credit exposure dynamics during major shocks (Terra and FTX), and (3) temporal graph neural networks for dynamic link prediction on temporal graphs. From the analysis, we observe (1) a rapid growth of network volume, (2) a trend of concentration to key protocols, (3) a decline of network density (the ratio ...


### 📰 新闻/社媒情绪（34 篇）

#### 📄 Stock Market Prediction Using Node Transformer Architecture Integrated with BERT Sentiment Analysis
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.05917v2)
- **作者**：Mohammad Al Ridhawi, Mahtab Haj Ali, Hussein Al Osman
- **摘要**：Stock market prediction presents considerable challenges for investors, financial institutions, and policymakers operating in complex market environments characterized by noise, non-stationarity, and behavioral dynamics. Traditional forecasting methods, including fundamental analysis and technical indicators, often fail to capture the intricate patterns and cross-sectional dependencies inherent in financial markets. This paper presents an integrated framework combining a node transformer architecture with BERT-based sentiment analysis for stock price forecasting. The proposed model represents the stock market as a graph structure where individual stocks form nodes and edges capture relationships including sectoral affiliations, correlated price movements, and supply chain connections. A fine-tuned BERT model extracts sentiment information from social media posts and combines it with quantitative market features through attention-based fusion mechanisms. The node transformer processes historical market data while capturing both temporal evolution and cross-sectional dependencies among stocks. Experiments conducted on 20 S&P 500 stocks spanning January 1982 to March 2025 demonstrate ...

#### 📄 Beyond the Numbers: Causal Effects of Financial Report Sentiment on Bank Profitability
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.17851v1)
- **作者**：Krishna Neupane, Prem Sapkota, Ujjwal Prajapati
- **摘要**：This study establishes the causal effects of market sentiment on firm profitability, moving beyond traditional correlational analyses. It leverages a causal forest machine learning methodology to control for numerous confounding variables, enabling systematic analysis of heterogeneity and non-linearities often overlooked. A key innovation is the use of a pre-trained FinancialBERT to generate sentiment scores from quarterly reports, which are then treated as causal interventions impacting profitability dynamics like returns and volatilities. Utilizing a comprehensive dataset from NEPSE, NRB, and individual financial institutions, the research employs SHAP analysis to identify influential profit predictors. A two-pronged causal analysis further explores how sentiment's impact is conditioned by Loan Portfolio/Asset Composition and Balance Sheet Strength/Leverage. Average Treatment Effect analyses, combined with SHAP insights, reveal statistically significant causal associations between certain balance sheet and expense management variables and profitability. This advanced causal machine learning framework significantly extends existing literature, providing a more robust understanding...

#### 📄 Multimodal Proposal for an AI-Based Tool to Increase Cross-Assessment of Messages
- **2025 | arXiv** | [link](http://arxiv.org/abs/2509.03529v1)
- **作者**：Alejandro Álvarez Castro, Joaquín Ordieres-Meré
- **摘要**：Earnings calls represent a uniquely rich and semi-structured source of financial communication, blending scripted managerial commentary with unscripted analyst dialogue. Although recent advances in financial sentiment analysis have integrated multi-modal signals, such as textual content and vocal tone, most systems rely on flat document-level or sentence-level models, failing to capture the layered discourse structure of these interactions. This paper introduces a novel multi-modal framework designed to generate semantically rich and structurally aware embeddings of earnings calls, by encoding them as hierarchical discourse trees. Each node, comprising either a monologue or a question-answer pair, is enriched with emotional signals derived from text, audio, and video, as well as structured metadata including coherence scores, topic labels, and answer coverage assessments. A two-stage transformer architecture is proposed: the first encodes multi-modal content and discourse metadata at the node level using contrastive learning, while the second synthesizes a global embedding for the entire conference. Experimental results reveal that the resulting embeddings form stable, semantically...

#### 📄 Dynamic stacking ensemble learning with investor knowledge representations for stock market index prediction based on multi-source financial data
- **2025 | arXiv** | [link](http://arxiv.org/abs/2512.14042v1)
- **作者**：Ruize Gao, Mei Yang, Yu Wang, Shaoze Cui
- **摘要**：The patterns of different financial data sources vary substantially, and accordingly, investors exhibit heterogeneous cognition behavior in information processing. To capture different patterns, we propose a novel approach called the two-stage dynamic stacking ensemble model based on investor knowledge representations, which aims to effectively extract and integrate the features from multi-source financial data. In the first stage, we identify different financial data property from global stock market indices, industrial indices, and financial news based on the perspective of investors. And then, we design appropriate neural network architectures tailored to these properties to generate effective feature representations. Based on learned feature representations, we design multiple meta-classifiers and dynamically select the optimal one for each time window, enabling the model to effectively capture and learn the distinct patterns that emerge across different temporal periods. To evaluate the performance of the proposed model, we apply it to predicting the daily movement of Shanghai Securities Composite index, SZSE Component index and Growth Enterprise index in Chinese stock market....

#### 📄 Hybrid Quantum-Classical Ensemble Learning for S\&P 500 Directional Prediction
- **2025 | arXiv** | [link](http://arxiv.org/abs/2512.15738v1)
- **作者**：Abraham Itzhak Weinberg
- **摘要**：Financial market prediction is a challenging application of machine learning, where even small improvements in directional accuracy can yield substantial value. Most models struggle to exceed 55--57\% accuracy due to high noise, non-stationarity, and market efficiency. We introduce a hybrid ensemble framework combining quantum sentiment analysis, Decision Transformer architecture, and strategic model selection, achieving 60.14\% directional accuracy on S\&P 500 prediction, a 3.10\% improvement over individual models.   Our framework addresses three limitations of prior approaches. First, architecture diversity dominates dataset diversity: combining different learning algorithms (LSTM, Decision Transformer, XGBoost, Random Forest, Logistic Regression) on the same data outperforms training identical architectures on multiple datasets (60.14\% vs.\ 52.80\%), confirmed by correlation analysis ($r>0.6$ among same-architecture models). Second, a 4-qubit variational quantum circuit enhances sentiment analysis, providing +0.8\% to +1.5\% gains per model. Third, smart filtering excludes weak predictors (accuracy $<52\%$), improving ensemble performance (Top-7 models: 60.14\% vs.\ all 35 mod...


### ⚖ 风险/信用/欺诈（27 篇）

#### 📄 Risk-Based Auto-Deleveraging
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.15963v1)
- **作者**：Steven Campbell, Natascha Hey, Ciamac C. Moallemi, Marcel Nutz
- **摘要**：Auto-deleveraging (ADL) mechanisms are a critical yet understudied component of risk management on cryptocurrency futures exchanges. When available margin and other loss-absorbing resources are insufficient to cover losses following large price moves, exchanges reduce positions and socialize losses among solvent participants via rule-based ADL protocols.   We formulate ADL as an optimization problem that minimizes the exchange's risk of loss arising from future equity shortfalls. In a single-asset, isolated-margin setting, we show that under a risk-neutral expected loss objective the unique optimal policy minimizes the maximum leverage among participants. The resulting design has a transparent structure: positions are reduced first for the most highly levered accounts, and leverage is progressively equalized via a water-filling (or ``leverage-draining'') rule. This policy is distribution-free, wash-trade resistant, Sybil resistant, and path-independent. It provides a canonical and implementable benchmark for ADL design and clarifies the economic logic underlying queue-based mechanisms used in practice.   We further study the multi-asset, cross-margin setting, where the ADL problem ...

#### 📄 Option Pricing on Noisy Intermediate-Scale Quantum Computers: A Quantum Neural Network Approach
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.19832v1)
- **作者**：Sebastian Zając, Rafał Pracht
- **摘要**：In a global derivatives market with notional values in the hundreds of trillions of dollars, the accuracy and efficiency of pricing models are of fundamental importance, with direct implications for risk management, capital allocation, and regulatory compliance. In this work, we employ the Black-Scholes-Merton (BSM) framework not as an end in itself, but as a controlled benchmark environment in which to rigorously assess the capabilities of quantum machine learning methods.   We propose a fully quantum approach to option pricing based on Quantum Neural Networks (QNNs), and, to the best of our knowledge, present one of the first implementations of such a methodology on currently available quantum hardware. Specifically, we investigate whether QNNs, by exploiting the geometric structure of Hilbert space, can effectively approximate option pricing functions.   Our implementation utilizes a compact 2-qubit QNN architecture evaluated across multiple state-of-the-art quantum processors, including IBM Fez, IQM Garnet, IonQ Forte, and Rigetti Ankaa-3. This cross-platform study reveals distinct hardware-dependent performance characteristics while demonstrating that accurate pricing approxim...

#### 📄 Shifting Correlations: How Trade Policy Uncertainty Alters stock-T bill Relationships
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.25285v1)
- **作者**：Demetrio Lacava
- **摘要**：This paper examines how trade policy uncertainty influences the correlation between U.S. stock indices and short-term government bonds. The objective is to assess whether policy-related shocks, especially those linked to trade tensions, alter the traditional stock-T bill relationship and its implications for investors. We extend the Dynamic Conditional Correlation (DCC) framework by incorporating exogenous variables to account for external shocks. Three specifications are analyzed: one using the Trade Policy Uncertainty (TPU) index, one including a dummy variable reflecting presidential-cycle effects, and one combining both through an interaction term. The analysis is based on daily data for major U.S. stock indices and the 3-month Treasury bill. Results indicate that trade policy uncertainty exerts a significant effect on stock-T bill correlations. Moreover, its influence becomes stronger under specific political conditions, suggesting that political agendas can amplify the impact of trade-related shocks on financial markets. Crucially, augmenting the DCC framework with trade-policy-related variables improves also the economic relevance of correlation forecasts. Therefore, this st...

#### 📄 Adaptive VaR Control for Standardized Option Books under Marking Frictions
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.03499v1)
- **作者**：Tenghan Zhong
- **摘要**：Short-horizon risk control matters for hedging and capital allocation. Yet existing Value-at-Risk studies rarely address standardized option books or the next-day valuation frictions that arise in derivatives data. This paper develops a framework for tail-risk control in standardized option books. The analysis focuses on the next-day realized loss and combines a base conditional quantile forecast with sequential conformal recalibration for adaptive Value-at-Risk control. This design addresses two central difficulties: unstable tail-risk forecasts under changing market conditions and the practical challenge of next-day valuation when exact same-contract quotes are unavailable. It also preserves economic interpretability through standardized construction and spot hedging when needed.   Using SPX option data from 2018 to 2025, we show that the uncalibrated base model systematically underestimates downside risk across multiple standardized books. Sequential recalibration removes much of this shortfall, brings exceedance rates closer to target, and improves rolling-window tail stability, with the largest gains in the books where the raw forecast is most vulnerable. The paper also provid...

#### 📄 Embedding interpretable $\ell_1$-regression into neural networks for uncovering temporal structure in cell imaging
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.02899v2)
- **作者**：Fabian Kabus, Maren Hackenberg, Julia Hindel, Thibault Cholvin, Antje Kilias, Thomas Brox, Abhinav Valada, Marlene Bartos
- **摘要**：While artificial neural networks excel in unsupervised learning of non-sparse structure, classical statistical regression techniques offer better interpretability, in particular when sparseness is enforced by $\ell_1$ regularization, enabling identification of which factors drive observed dynamics. We investigate how these two types of approaches can be optimally combined, exemplarily considering two-photon calcium imaging data where sparse autoregressive dynamics are to be extracted. We propose embedding a vector autoregressive (VAR) model as an interpretable regression technique into a convolutional autoencoder, which provides dimension reduction for tractable temporal modeling. A skip connection separately addresses non-sparse static spatial information, selectively channeling sparse structure into the $\ell_1$-regularized VAR. $\ell_1$-estimation of regression parameters is enabled by differentiating through the piecewise linear solution path. This is contrasted with approaches where the autoencoder does not adapt to the VAR model. Having an embedded statistical model also enables a testing approach for comparing temporal sequences from the same observational unit. Additionally...


### 🛡 对抗/鲁棒性（25 篇）

#### 📄 A novel approach to trading strategy parameter optimization using double out-of-sample data and walk-forward techniques
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.10785v1)
- **作者**：Tomasz Mroziewicz, Robert Ślepaczuk
- **摘要**：This study introduces a novel approach to walk-forward optimization by parameterizing the lengths of training and testing windows. We demonstrate that the performance of a trading strategy using the Exponential Moving Average (EMA) evaluated within a walk-forward procedure based on the Robust Sharpe Ratio is highly dependent on the chosen window size. We investigated the strategy on intraday Bitcoin data at six frequencies (1 minute to 60 minutes) using 81 combinations of walk-forward window lengths (1 day to 28 days) over a 19-month training period. The two best-performing parameter sets from the training data were applied to a 21-month out-of-sample testing period to ensure data independence. The strategy was only executed once during the testing period. To further validate the framework, strategy parameters estimated on Bitcoin were applied to Binance Coin and Ethereum. Our results suggest the robustness of our custom approach. In the training period for Bitcoin, all combinations of walk-forward windows outperformed a Buy-and-Hold strategy. During the testing period, the strategy performed similarly to Buy-and-Hold but with lower drawdown and a higher Information Ratio. Similar ...

#### 📄 Budgeted Robust Intervention Design for Financial Networks with Common Asset Exposures
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.27274v1)
- **作者**：Giuseppe C. Calafiore
- **摘要**：In the context of containment of default contagion in financial networks, we here study a regulator that allocates pre-shock capital or liquidity buffers across banks connected by interbank liabilities and common external asset exposures. The regulator chooses a nonnegative buffer vector under a linear budget before asset-price shocks realize. Shocks are modeled as belonging to either an $\ell_{\infty}$ or an $\ell_{1}$ uncertainty set, and the design objective is either to enlarge the certified no-default/no-insolvency region or to minimize worst-case clearing losses at a prescribed stress radius. Four exact synthesis results are derived. The buffer that maximizes the default resilience margin is obtained from a linear program and admits a closed-form minimal-budget certificate for any target margin. The buffer that maximizes the insolvency resilience margin is computed by a single linear program. At a fixed radius, minimizing the worst-case systemic loss is again a linear program under $\ell_{\infty}$ uncertainty and a linear program with one scenario block per asset under $\ell_{1}$ uncertainty. Crucially, under $\ell_{1}$ uncertainty, exact robustness adds only one LP block per...

#### 📄 Feasibility-First Satellite Integration in Robust Portfolio Architectures
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.08721v1)
- **作者**：Roberto Garrone
- **摘要**：The integration of thematic satellite allocations into core-satellite portfolio architectures is commonly approached using factor exposures, discretionary convictions, or backtested performance, with feasibility assessed primarily through liquidity screens or market-impact considerations. While such approaches may be appropriate at institutional scale, they are ill-suited to small portfolios and robustness-oriented allocation frameworks, where dominant constraints arise not from return predictability or trading capacity, but from fixed costs, irreversibility risk, and governance complexity. This paper develops a feasibility-first, non-predictive framework for satellite integration that is explicitly scale-aware. We formalize four nested feasibility layers (physical, economic, structural, and epistemic) that jointly determine whether a satellite allocation is admissible. Physical feasibility ensures implementability under concave market-impact laws; economic feasibility suppresses noise-dominated reallocations via cost-dominance threshold constraints; structural feasibility bounds satellite size through an explicit optionality budget defined by tolerable loss under thesis failure; a...

#### 📄 MartDE: A Privacy-Preserving and Cost-Efficient Evaluation Framework for Data Marketplaces
- **2026 | AAAI** | [link](https://ojs.aaai.org/index.php/AAAI/article/view/40889)
- **作者**：Authors Xinyuan Qian University of Electronic Science and Technology of China Haoyong Wang Chinese Academy of Sciences Hangcheng Cao City University o
- **摘要**：The development of machine learning models increasingly relies on high-quality data that resides in private domains. To enable secure and value-driven data exchange under strict privacy regulations, federated learning (FL) has emerged as a key primitive by enabling the trading of model utilities instead of raw data. Among existing solutions, martFL (CCS 2023) represents the state-of-the-art FL-based data marketplace architecture, integrating privacy-preserving model evaluation and verifiable trading protocols to enable robust and fair model utility trading without revealing raw data. Despite its strengths, martFL suffers from critical weaknesses at the evaluation layer, including plaintext score exposure and unverifiable and manipulable participant selection. To address these challenges, we propose MartDE, a dedicated evaluation framework that builds model-centric data marketplaces with robust, privacy-preserving, and verifiable mechanisms. MartDE introduces encrypted utility scoring with client-side decryption to preserve score confidentiality, formally bounded anomaly filtering, adaptive participant selection based on global model performance, and commitment-based verification to...

#### 📄 RARE: Redundancy-Aware Retrieval Evaluation Framework for High-Similarity Corpora
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.19047v1)
- **作者**：Hanjun Cho, Jay-Yoon Lee
- **摘要**：Existing QA benchmarks typically assume distinct documents with minimal overlap, yet real-world retrieval-augmented generation (RAG) systems operate on corpora such as financial reports, legal codes, and patents, where information is highly redundant and documents exhibit strong inter-document similarity. This mismatch undermines evaluation validity: retrievers can be unfairly undervalued even when they retrieve documents that provide sufficient evidence, because redundancy across documents is not accounted for in evaluation. On the other hand, retrievers that perform well on standard benchmarks often generalize poorly to real-world corpora with highly similar and redundant documents. We present RARE (Redundancy-Aware Retrieval Evaluation), a framework for constructing realistic benchmarks by (i) decomposing documents into atomic facts to enable precise redundancy tracking and (ii) enhancing LLM-based data generation with CRRF. RAG benchmark data usually requires multiple quality criteria, but LLMs often yield trivial outputs. CRRF scores criteria separately and fuses decisions by rank, improving the reliability of generated data. Applying RARE to Finance, Legal, and Patent corpora...


### 📐 期权/衍生品（22 篇）

#### 📄 Topological Risk Parity
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.16773v1)
- **作者**：Revant Nayar, Dnyanesh Kulkarni, El Mehdi Ainasse
- **摘要**：We develop \emph{Topological Risk Parity} (TRP), a tree-based portfolio construction approach intended for long/short, market neutral, factor-aware portfolios. The method is motivated by the dominance of passive/factor flows that naturally create a tree-like structure in markets. We introduce two implementation variants: (i) a rooted minimum-spanning-tree allocator, and (ii) a market/sector-anchored variant referred to here as \emph{Semi-Supervised TRP}, which imposes SPY as the root node and the 11 sector ETFs as the second layer. In both cases, the key object is a sparse rooted topology extracted from a correlation-distance graph, together with a propagation law that maps signed signals into portfolio weights.   Relative to classical Hierarchical Risk Parity (HRP), TRP is non-binary and designed for signed cross-sectional signals and hedged long-short portfolios: it preserves signal direction while using return-dependence geometry to shape exposures. It accounts for the fact that there is imperfect correlation between parent and child nodes, and thus does not propagate weights entirely to the children. We can also impose economically motivated hierarchy that involves industries, ...

#### 📄 KANHedge: Efficient Hedging of High-Dimensional Options Using Kolmogorov-Arnold Network-Based BSDE Solver
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.11097v1)
- **作者**：Rushikesh Handal, Masanori Hirano
- **摘要**：High-dimensional option pricing and hedging present significant challenges in quantitative finance, where traditional PDE-based methods struggle with the curse of dimensionality. The BSDE framework offers a computationally efficient alternative to PDE-based methods, and recently proposed deep BSDE solvers, generally utilizing conventional Multi-Layer Perceptrons (MLPs), build upon this framework to provide a scalable alternative to numerical BSDE solvers. In this research, we show that although such MLP-based deep BSDEs demonstrate promising results in option pricing, there remains room for improvement regarding hedging performance. To address this issue, we introduce KANHedge, a novel BSDE-based hedger that leverages Kolmogorov-Arnold Networks (KANs) within the BSDE framework. Unlike conventional MLP approaches that use fixed activation functions, KANs employ learnable B-spline activation functions that provide enhanced function approximation capabilities for continuous derivatives. We comprehensively evaluate KANHedge on both European and American basket options across multiple dimensions and market conditions. Our experimental results demonstrate that while KANHedge and MLP achi...

#### 📄 Optimal strategy and deep hedging for share repurchase programs
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.18686v1)
- **作者**：Stefano Corti, Roberto Daluiso, Andrea Pallavicini
- **摘要**：In recent decades, companies have frequently adopted share repurchase programs to return capital to shareholders or for other strategic purposes, instructing investment banks to rapidly buy back shares on their behalf. When the executing institution is allowed to hedge its exposure, it encounters several challenges due to the intrinsic features of the product. Moreover, contractual clauses or market regulations on trading activity may make it infeasible to rely on Greeks. In this work, we address the hedging of these products by developing a machine-learning framework that determines the optimal execution of the buyback while explicitly accounting for the bank's actual trading capabilities. This unified treatment of execution and hedging yields substantial performance improvements, resulting in an optimized policy that provides a feasible and realistic hedging approach. The pricing of these programs can be framed in terms of the discount that banks offer to the client on the price at which the shares are delivered. Since, in our framework, risk measures serve as objective functions, we exploit the concept of indifference pricing to compute this discount, thereby capturing the actua...

#### 📄 Adaptively trained Physics-informed Radial Basis Function Neural Networks for Solving Multi-asset Option Pricing Problems
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.12704v1)
- **作者**：Yan Ma, Yumeng Ren
- **摘要**：The present study investigates the numerical solution of Black-Scholes partial differential equation (PDE) for option valuation with multiple underlying assets. We develop a physics-informed (PI) machine learning algorithm based on a radial basis function neural network (RBFNN) that concurrently optimizes the network architecture and predicts the target option price. The physics-informed radial basis function neural network (PIRBFNN) combines the strengths of the traditional radial basis function collocation method and the physics-informed neural network machine learning approach to effectively solve PDE problems in the financial context. By employing a PDE residual-based technique to adaptively refine the distribution of hidden neurons during the training process, the PIRBFNN facilitates accurate and efficient handling of multidimensional option pricing models featuring non-smooth payoff conditions. The validity of the proposed method is demonstrated through a set of experiments encompassing a single-asset European put option, a double-asset exchange option, and a four-asset basket call option.

#### 📄 Was Benoit Mandelbrot a hedgehog or a fox?
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.01122v1)
- **作者**：Rosario N. Mantegna
- **摘要**：Benoit Mandelbrot's scientific legacy spans an extraordinary range of disciplines, from linguistics and fluid turbulence to cosmology and finance, suggesting the intellectual temperament of a "fox" in Isaiah Berlin's famous dichotomy of thinkers. This essay argues, however, that Mandelbrot was, at heart, a "hedgehog": a thinker unified by a single guiding principle. Across his diverse pursuits, the concept of scaling -- manifested in self-similarity, power laws, fractals, and multifractals -- served as the central idea that structured his work. By tracing the continuity of this scaling paradigm through his contributions to mathematics, physics, and economics, the paper reveals a coherent intellectual trajectory masked by apparent eclecticism. Mandelbrot's enduring insight in the modeling of natural and social phenomena can be understood through the lens of the geometry and statistics of scale invariance.


### 🌊 市场状态/Regime（22 篇）

#### 📄 Bayesian Robust Financial Trading with Adversarial Synthetic Market Data
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.17008v1)
- **作者**：Haochong Xia, Simin Li, Ruixiao Xu, Zhixia Zhang, Hongxiang Wang, Zhiqian Liu, Teng Yao Long, Molei Qin
- **摘要**：Algorithmic trading relies on machine learning models to make trading decisions. Despite strong in-sample performance, these models often degrade when confronted with evolving real-world market regimes, which can shift dramatically due to macroeconomic changes-e.g., monetary policy updates or unanticipated fluctuations in participant behavior. We identify two challenges that perpetuate this mismatch: (1) insufficient robustness in existing policy against uncertainties in high-level market fluctuations, and (2) the absence of a realistic and diverse simulation environment for training, leading to policy overfitting. To address these issues, we propose a Bayesian Robust Framework that systematically integrates a macro-conditioned generative model with robust policy learning. On the data side, to generate realistic and diverse data, we propose a macro-conditioned GAN-based generator that leverages macroeconomic indicators as primary control variables, synthesizing data with faithful temporal, cross-instrument, and macro correlations. On the policy side, to learn robust policy against market fluctuations, we cast the trading process as a two-player zero-sum Bayesian Markov game, wherei...

#### 📄 Flow Taxes, Stock Taxes, and Portfolio Choice: A Generalised Neutrality Result
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.15974v2)
- **作者**：Anders G Frøseth
- **摘要**：A proportional wealth tax - a levy on the stock of wealth - preserves portfolio neutrality by acting as a uniform drift shift in the Fokker-Planck equation for wealth dynamics. We extend this result to the full system of ownership taxes (eierkostnader) that a shareholder faces: a corporate tax on gross profits, a capital income tax on the risk-free return, a dividend and capital gains tax on the excess return, and a wealth tax on net assets. Each tax modifies the drift of the wealth process in a distinct way - multiplicative rescaling, constant shift, or regime-dependent compression - while leaving the diffusion coefficient unchanged. We show that the combined system preserves portfolio neutrality under three conditions: (i) the capital income tax rate equals the corporate tax rate, (ii) the shielding rate equals the risk-free rate, and (iii) the wealth tax assessment is uniform across assets. When these conditions hold, the after-tax excess return is a uniform rescaling of the pre-tax excess return by the factor $(1-τ_c)(1-τ_d)$, and the drift-shift symmetry of the wealth-tax-only case generalises to a drift-shift-and-rescale symmetry. We classify the distortions that arise when e...

#### 📄 The Temporal Markov Transition Field
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.08803v1)
- **作者**：Michael Leznik
- **摘要**：The Markov Transition Field (MTF), introduced by Wang and Oates (2015), encodes a time series as a two-dimensional image by mapping each pair of time steps to the transition probability between their quantile states, estimated from a single global transition matrix. This construction is efficient when the transition dynamics are stationary, but produces a misleading representation when the process changes regime over time: the global matrix averages across regimes and the resulting image loses all information about \emph{when} each dynamical regime was active. In this paper we introduce the \emph{Temporal Markov Transition Field} (TMTF), an extension that partitions the series into $K$ contiguous temporal chunks, estimates a separate local transition matrix for each chunk, and assembles the image so that each row reflects the dynamics local to its chunk rather than the global average. The resulting $T \times T$ image has $K$ horizontal bands of distinct texture, each encoding the transition dynamics of one temporal segment. We develop the formal definition, establish the key structural properties of the representation, work through a complete numerical example that makes the distin...

#### 📄 Optimal Parlay Wagering and Whitrow Asymptotics: A State-Price and Implicit-Cash Treatment
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.26620v1)
- **作者**：Christopher D. Long
- **摘要**：For independent multi-outcome events under multiplicative parlay pricing, we give a short exact proof of the optimal Kelly strategy using the implicit-cash viewpoint. The proof is entirely eventwise. One first solves each event in isolation. The full simultaneous optimizer over the entire menu of singles, doubles, triples, and higher parlays is then obtained by taking the outer product of the one-event Kelly strategies. Equivalently, the optimal terminal wealth factorizes across events. This yields an immediate active-leg criterion: a parlay is active if and only if each of its legs is active in the corresponding one-event problem. The result recovers, in a more transparent state-price form, the log-utility equivalence between simultaneous multibetting and sequential Kelly betting.   We then study what is lost when one forbids parlays and allows only singles. In a low-edge regime and on a fixed active support, the exact parlay optimizer supplies the natural reference point. The singles-only problem is a first-order truncation of the factorized wealth formula. A perturbative expansion shows that the growth-rate loss from forbidding parlays is $\OO(\eps^4)$, while the optimal singles...

#### 📄 STN-GPR: A Singularity Tensor Network Framework for Efficient Option Pricing
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.26318v1)
- **作者**：Dominic Gribben, Carolina Allende, Alba Villarino, Aser Cortines, Mazen Ali, Román Orús, Pascal Oswald, Noureddine Lehdili
- **摘要**：We develop a tensor-network surrogate for option pricing, targeting large-scale portfolio revaluation problems arising in market risk management (e.g., VaR and Expected Shortfall computations). The method involves representing high-dimensional price surfaces in tensor-train (TT) form using TT-cross approximation, constructing the surrogate directly from black-box price evaluations without materializing the full training tensor. For inference, we use a Laplacian kernel and derive TT representations of the kernel matrix and its closed-form inverse in the noise-free setting, enabling TT-based Gaussian process regression without dense matrix factorization or iterative linear solves. We found that hyperparameter optimization consistently favors a large kernel length-scale and show that in this regime the GPR predictor reduces to multilinear interpolation for off-grid inputs; we also derive a low-rank TT representation for this limit. We evaluate the approach on five-asset basket options over an eight dimensional parameter space (asset spot levels, strike, interest rate, and time to maturity). For European geometric basket puts, the tensor surrogate achieves lower test error at shorter t...


### 🧪 回测/市场模拟（20 篇）

#### 📄 Systemic Risk and Default Cascades in Global Equity Markets: A Network and Tail-Risk Approach Based on the Gai Kapadia Framework
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.19796v1)
- **作者**：Ana Isabel Castillo Pereda
- **摘要**：This study extends the Gai-Kapadia framework, originally developed for interbank contagion, to assess systemic risk and default cascades in global equity markets. We analyze a 30 asset network comprising Brazilian and developed market equities over the period 2015-2026, constructing exposure based financial networks from price co-movements. Threshold filtering (theta = 0.3 and theta = 0.5) is applied to isolate significant interconnections.   Cascade dynamics are analyzed through a combination of deterministic propagation and stochastic Monte Carlo simulations (n = 1000) under varying shock intensities. The results show that the system exhibits strong global resilience, with a negligible probability of large scale failure, while maintaining localized vulnerability within highly clustered subnetworks. In particular, shocks lead to an average of 1.0 failed asset for single shocks and 2.0 for simultaneous shocks, indicating limited propagation below a critical threshold.   Network analysis reveals a clear structural asymmetry: Brazilian assets display high clustering (Ci approx 0.8-1.0) and dense connectivity, which amplifies local shock propagation, whereas developed market assets ex...

#### 📄 Manipulation in Prediction Markets: An Agent-based Modeling Experiment
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.20452v1)
- **作者**：Bridget Smart, Ebba Mark, Anne Bastian, Josefina Waugh
- **摘要**：Prediction markets mobilize financial incentives to forecast binary event outcomes through the aggregation of dispersed beliefs and heterogeneous information. Their growing popularity and demonstrated predictive accuracy in political elections have raised speculation and concern regarding their susceptibility to manipulation and the potential consequences for democratic processes. Using agent-based simulations combined with an analytic characterization of price dynamics, we study how high-budget agents can introduce price distortions in prediction markets. We explore the persistence and stability of these distortions in the presence of herding or stubborn agents, and analyze how agent expertise affects market-price variance. Firstly we propose an agent-based model of a prediction market in which bettors with heterogeneous expertise, noisy private information, variable learning rates and budgets observe the evolution of public opinion on a binary election outcome to inform their betting strategies in the market. The model exhibits stability across a broad parameter space, with complex agent behaviors and price interactions producing self-regulatory price discovery. Second, using thi...

#### 📄 Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.21017v1)
- **作者**：Open-H-Embodiment Consortium,  :, Nigel Nelson, Juo-Tung Chen, Jesse Haworth, Xinhao Chen, Lukas Zbinden, Dianye Huang
- **摘要**：Autonomous medical robots hold promise to improve patient outcomes, reduce provider workload, democratize access to care, and enable superhuman precision. However, autonomous medical robotics has been limited by a fundamental data problem: existing medical robotic datasets are small, single-embodiment, and rarely shared openly, restricting the development of foundation models that the field needs to advance. We introduce Open-H-Embodiment, the largest open dataset of medical robotic video with synchronized kinematics to date, spanning more than 49 institutions and multiple robotic platforms including the CMR Versius, Intuitive Surgical's da Vinci, da Vinci Research Kit (dVRK), Rob Surgical BiTrack, Virtual Incision's MIRA, Moon Surgical Maestro, and a variety of custom systems, spanning surgical manipulation, robotic ultrasound, and endoscopy procedures. We demonstrate the research enabled by this dataset through two foundation models. GR00T-H is the first open foundation vision-language-action model for medical robotics, which is the only evaluated model to achieve full end-to-end task completion on a structured suturing benchmark (25% of trials vs. 0% for all others) and achieves...

#### 📄 Cosmological analysis of the DESI DR1 Lyman alpha 1D power spectrum
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.21432v1)
- **作者**：J. Chaves-Montero, A. Font-Ribera, P. McDonald, E. Armengaud, D. Chebat, C. Garcia-Quintero, N. G. Karaçaylı, C. Ravoux
- **摘要**：We present the cosmological analysis of the one-dimensional Lyman-$α$ flux power spectrum from the first data release of the Dark Energy Spectroscopic Instrument (DESI). We capture the dependence of the signal on cosmology and intergalactic medium physics using an emulator trained on a cosmological suite of hydrodynamical simulations, and we correct its predictions for the impact of astrophysical contaminants and systematics, many of these not considered in previous analyses. We employ this framework to constrain the amplitude and logarithmic slope of the linear matter power spectrum at $k_\star=0.009\,\mathrm{km^{-1}s}$ and redshift $z=3$, obtaining $Δ^2_\star=0.379\pm0.032$ and $n_\star=-2.309\pm0.019$. The robustness of these constraints is validated through the analysis of mocks and a large number of alternative data analysis variations, with cosmological parameters kept blinded throughout the validation process. We then combine our results with constraints from DESI BAO and temperature, polarization, and lensing measurements from Planck, ACT, and SPT-3G to set constraints on $Λ$CDM extensions. While our measurements do not significantly tighten the limits on the sum of neutrin...

#### 📄 Bayesian Sparsity Modeling of Shared Neural Response in Functional Magnetic Resonance Imaging Data
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.21676v1)
- **作者**：Spencer Wadsworth, Nabin Koirala, Nicole Landi, Ofer Harel
- **摘要**：Detecting shared neural activity from functional magnetic resonance imaging (fMRI) across individuals exposed to the same stimulus can reveal synchronous brain responses, functional roles of regions, and potential clinical biomarkers. Intersubject correlation (ISC) is the main method for identifying voxelwise shared responses and per-subject variability, but it relies on heavy data summarization and thousands of regional tests, leading to poor uncertainty quantification and multiple testing issues. ISC also does not directly estimate a shared neural response (SNR) function. We propose a model-based alternative applicable to both task-based and naturalistic fMRI that simultaneously identifies spatial regions of shared activity and estimates the SNR function. The model combines sparse Gaussian process estimation of the response function with a Bayesian sparsity prior inspired by the horseshoe prior to detect voxel activation. A spatially structured extension encourages neighboring voxels to exhibit similar activation patterns. We examine the model's properties, evaluate performance via simulations, and analyze two real-world fMRI datasets, including one task-based and one naturalisti...


### 🎨 多模态融合（16 篇）

#### 📄 Investing Is Compression
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.10758v3)
- **作者**：Oscar Stiffelman
- **摘要**：In 1956 John Kelly wrote a paper at Bell Labs describing the relationship between gambling and Information Theory. What came to be known as the Kelly Criterion is both an objective and a closed-form solution to sizing wagers when odds and edge are known. Samuelson argued it was arbitrary and subjective, and successfully kept it out of mainstream economics. Luckily it lived on in computer science, mostly because of Tom Cover's work at Stanford. He showed that it is the uniquely optimal way to invest: it maximizes long-term wealth, minimizes the risk of ruin, and is competitively optimal in a game-theoretic sense, even over the short term.   One of Cover's most surprising contributions to portfolio theory was the universal portfolio. Related to universal compression in information theory, it performs asymptotically as well as the best constant-rebalanced portfolio in hindsight. I borrow a trick from that algorithm to show that Kelly's objective, even in the general form, factors the investing problem into three terms: a money term, an entropy term, and a divergence term. The only way to maximize growth is to minimize divergence which measures the difference between our distribution a...

#### 📄 Trading in CEXs and DEXs with Priority Fees and Stochastic Delays
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.10798v2)
- **作者**：Philippe Bergault, Yadh Hafsi, Leandro Sánchez-Betancourt
- **摘要**：We develop a mixed control framework that combines absolutely continuous controls with impulse interventions subject to stochastic execution delays. The model extends current impulse control formulations by allowing (i) the controller to choose the mean of the stochastic delay of their impulses, and allowing (ii) for multiple pending orders, so that several impulses can be submitted and executed asynchronously at random times. The framework is motivated by an optimal trading problem between centralized (CEX) and decentralized (DEX) exchanges. In DEXs, traders control the distribution of the execution delay through the priority fee paid, introducing a fundamental trade-off between delays, uncertainty, and costs. We study the optimal trading problem of an agent exploiting trading signals in CEXs and DEXs. From a mathematical perspective, we derive the associated dynamic programming principle of this new class of impulse control problems, and establish the viscosity properties of the corresponding quasi-variational inequalities. From a financial perspective, our model provides insights on how to carry out execution across CEXs and DEXs, highlighting how traders manage latency risk opt...

#### 📄 COTTA: Context-Aware Transfer Adaptation for Trajectory Prediction in Autonomous Driving
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.00402v1)
- **作者**：Seohyoung Park, Jaeyeol Lim, Seoyoung Ju, Kyeonghun Kim, Nam-Joon Kim, Hyuk-Jae Lee
- **摘要**：Developing robust models to accurately predict the trajectories of surrounding agents is fundamental to autonomous driving safety. However, most public datasets, such as the Waymo Open Motion Dataset and Argoverse, are collected in Western road environments and do not reflect the unique traffic patterns, infrastructure, and driving behaviors of other regions, including South Korea. This domain discrepancy leads to performance degradation when state-of-the-art models trained on Western data are deployed in different geographic contexts. In this work, we investigate the adaptability of Query-Centric Trajectory Prediction (QCNet) when transferred from U.S.-based data to Korean road environments. Using a Korean autonomous driving dataset, we compare four training strategies: zero-shot transfer, training from scratch, full fine-tuning, and encoder freezing. Experimental results demonstrate that leveraging pretrained knowledge significantly improves prediction performance. Specifically, selectively fine-tuning the decoder while freezing the encoder yields the best trade-off between accuracy and training efficiency, reducing prediction error by over 66% compared to training from scratch. ...

#### 📄 Is an investor stolen their profits by mimic investors? Investigated by an agent-based model
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.03671v1)
- **作者**：Takanobu Mizuta, Isao Yagi
- **摘要**：Some investors say increasing investors with the same strategy decreasing their profits per an investor. On the other hand, some investors using technical analysis used to use same strategy and parameters with other investors, and say that it is better. Those argues are conflicted each other because one argues using with same strategy decreases profits but another argues it increase profits. However, those arguments have not been investigated yet. In this study, the agent-based artificial financial market model(ABAFMM) was built by adding "additional agents"(AAs) that includes additional fundamental agents (AFAs) and additional technical agents (ATAs) to the prior model. The AFAs(ATAs) trade obeying simple fundamental(technical) strategy having only the one parameter. We investigated earnings of AAs when AAs increased. We found that in the case with increasing AFAs, market prices are made stable that leads to decrease their profits. In the case with increasing ATAs, market prices are made unstable that leads to gain their profits more.

#### 📄 An Approach Towards Developing Relationally Intelligent Multimodal Framework for Stock Movement Prediction (Student Abstract)
- **2026 | AAAI** | [link](https://ojs.aaai.org/index.php/AAAI/article/view/42266)
- **作者**：Authors Manali Patel Sardar Vallabhbhai National Institute of Technology Krupa Jariwala Sardar Vallabhbhai National Institute of Technology Chiranjoy 
- **摘要**：The dependency of stock prices on a multitude of factors
makes the task of prediction exceedingly challenging. Given
the volatile nature of stock data, it is imperative to
integrate multiple sources of information to accurately
encompass the various factors that influence market trends.
To capture these complex dynamics, several multimodal
methodologies have been proposed, integrating market data,
technical indicators, and textual information. However, it
is claimed that these coarse-grained information sources do
not offer a holistic view of the market. Furthermore, these
sources are stock-specific and do not elucidate the
interconnections between various stocks. To address this
deficiency, we propose a multimodal approach that
incorporates this relational aspect alongside fine-grained
information sources. The applicability of our framework is
underscored by empirical results, which demonstrate the
superiority of our approach.


### 🔍 因子挖掘/Alpha 发现（14 篇）

#### 📄 AlphaPROBE: Alpha Mining via Principled Retrieval and On-graph biased evolution
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.11917v1)
- **作者**：Taian Guo, Haiyang Shen, Junyu Luo, Binqi Chen, Hongjun Ding, Jinsheng Huang, Luchen Liu, Yun Ma
- **摘要**：Extracting signals through alpha factor mining is a fundamental challenge in quantitative finance. Existing automated methods primarily follow two paradigms: Decoupled Factor Generation, which treats factor discovery as isolated events, and Iterative Factor Evolution, which focuses on local parent-child refinements. However, both paradigms lack a global structural view, often treating factor pools as unstructured collections or fragmented chains, which leads to redundant search and limited diversity. To address these limitations, we introduce AlphaPROBE (Alpha Mining via Principled Retrieval and On-graph Biased Evolution), a framework that reframes alpha mining as the strategic navigation of a Directed Acyclic Graph (DAG). By modeling factors as nodes and evolutionary links as edges, AlphaPROBE treats the factor pool as a dynamic, interconnected ecosystem. The framework consists of two core components: a Bayesian Factor Retriever that identifies high-potential seeds by balancing exploitation and exploration through a posterior probability model, and a DAG-aware Factor Generator that leverages the full ancestral trace of factors to produce context-aware, nonredundant optimizations. ...

#### 📄 QuantaAlpha: An Evolutionary Framework for LLM-Driven Alpha Mining
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.07085v2)
- **作者**：Jun Han, Shuo Zhang, Wei Li, Zhi Yang, Yifan Dong, Tu Hu, Jialuo Yuan, Xiaomin Yu
- **摘要**：Financial markets are noisy and non-stationary, making alpha mining highly sensitive to noise in backtesting results and sudden market regime shifts. While recent agentic frameworks improve alpha mining automation, they often lack controllable multi-round search and reliable reuse of validated experience. To address these challenges, we propose QuantaAlpha, an evolutionary alpha mining framework that treats each end-to-end mining run as a trajectory and improves factors through trajectory-level mutation and crossover operations. QuantaAlpha localizes suboptimal steps in each trajectory for targeted revision and recombines complementary high-reward segments to reuse effective patterns, enabling structured exploration and refinement across mining iterations. During factor generation, QuantaAlpha enforces semantic consistency across the hypothesis, factor expression, and executable code, while constraining the complexity and redundancy of the generated factor to mitigate crowding. Extensive experiments on the China Securities Index 300 (CSI 300) demonstrate consistent gains over strong baseline models and prior agentic systems. When utilizing GPT-5.2, QuantaAlpha achieves an Informati...

#### 📄 FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.14670v1)
- **作者**：Yanlong Wang, Jian Xu, Hongkang Zhang, Shao-Lun Huang, Danny Dongning Sun, Xiao-Ping Zhang
- **摘要**：Formulaic alpha factor mining is a critical yet challenging task in quantitative investment, characterized by a vast search space and the need for domain-informed, interpretable signals. However, finding novel signals becomes increasingly difficult as the library grows due to high redundancy. We propose FactorMiner, a lightweight and flexible self-evolving agent framework designed to navigate this complex landscape through continuous knowledge accumulation. FactorMiner combines a Modular Skill Architecture that encapsulates systematic financial evaluation into executable tools with a structured Experience Memory that distills historical mining trials into actionable insights (successful patterns and failure constraints). By instantiating the Ralph Loop paradigm -- retrieve, generate, evaluate, and distill -- FactorMiner iteratively uses memory priors to guide exploration, reducing redundant search while focusing on promising directions. Experiments on multiple datasets across different assets and Markets show that FactorMiner constructs a diverse library of high-quality factors with competitive performance, while maintaining low redundancy among factors as the library scales. Overa...

#### 📄 Alpha Discovery via Grammar-Guided Learning and Search
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.22119v1)
- **作者**：Han Yang, Dong Hao, Zhuohan Wang, Qi Shi, Xingtong Li
- **摘要**：Automatically discovering formulaic alpha factors is a central problem in quantitative finance. Existing methods often ignore syntactic and semantic constraints, relying on exhaustive search over unstructured and unbounded spaces. We present AlphaCFG, a grammar-based framework for defining and discovering alpha factors that are syntactically valid, financially interpretable, and computationally efficient. AlphaCFG uses an alpha-oriented context-free grammar to define a tree-structured, size-controlled search space, and formulates alpha discovery as a tree-structured linguistic Markov decision process, which is then solved using a grammar-aware Monte Carlo Tree Search guided by syntax-sensitive value and policy networks. Experiments on Chinese and U.S. stock market datasets show that AlphaCFG outperforms state-of-the-art baselines in both search efficiency and trading profitability. Beyond trading strategies, AlphaCFG serves as a general framework for symbolic factor discovery and refinement across quantitative finance, including asset pricing and portfolio construction.

#### 📄 Understanding the Long-Only Minimum Variance Portfolio
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.07692v1)
- **作者**：Nick L. Gunther, Alec N. Kercheval, Ololade Sowunmi
- **摘要**：For a covariance matrix coming from a factor model of returns, we investigate the relationship between the long-only global minimum variance portfolio and the asset exposures to the factors. In the case of a 1-factor model, we provide a rigorous and explicit description of the long-only solution in terms of the parameters of the covariance matrix. For $q>1$ factors, we provide a description of the long-only portfolio in geometric terms. The results are illustrated with empirical daily returns of US stocks.


### 📑 财报/披露文本分析（9 篇）

#### 📄 Global Persistence, Local Residual Structure: Forecasting Heterogeneous Investment Panels
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.09821v1)
- **作者**：Oleg Roshka
- **摘要**：On a 93-actor quarterly panel mixing macro indicators, institutional data, and firm-level investment ratios, global factor augmentation degrades prediction for actor subgroups whose dynamics are misrepresented by the shared basis. A two-stage architecture -- global pooled AR(1) for shared persistence, block-specific local models for residual dynamics -- improves full-panel out-of-sample $R^2$ from 0.630 to 0.677 ($Δ= +0.047$, CI $[+0.036, +0.058]$, 10/10 windows, placebo $p \leq 0.001$). A held-out decade test -- block partition frozen on 2005--2014 data, evaluated on unseen 2015--2024 windows -- confirms the gain ($Δ= +0.050$, 10/10). Dropping the tech/health block eliminates roughly 72\% of the gain, making it the primary driver; rank-matched decomposition confirms this reflects a genuine cross-sector co-movement factor, not a rank-capacity artefact. Among the linear estimators tested, the gain is architectural rather than methodological; per-actor gradient boosting with the same block decomposition ($R^2 = 0.657$) does not close the gap, showing the advantage combines block-specific estimation with low-rank factor extraction. The gain arises only on heterogeneous mixed-type pane...

#### 📄 Extracting key insights from earnings call transcript via information-theoretic contrastive learning
- **2025 | OpenReview** | [link](https://openreview.net/forum?id=4GmTSLbjH5)
- **作者**：Yanlong Huang, Wenxin Tai, Fan Zhou, Qiang Gao, Ting Zhong, Kunpeng Zhang
- **摘要**：Earnings conference calls provide critical insights into a company’s financial health, future outlook, and strategic direction. Traditionally, analysts manually analyze these lengthy transcripts to extract key information, a process that is both time-consuming and prone to bias and error. To address this, text mining tools, particularly extractive summarization, are increasingly being used to automatically extract key insights, aiming to standardize the analysis process and improve efficiency. Extractive summarization automates the selection of the most informative sentences, offering a promising solution for transcript analysis. However, existing extractive summarization techniques face several challenges, such as the lack of labeled training data, difficulties in incorporating domain-specific knowledge, and inefficiencies in handling large-scale datasets. In this work, we introduce ECT-SKIE, an information-theoretic, self-supervised approach for extracting key insights from earnings call transcripts. We leverage variational information bottleneck theory to extract insights in parallel, significantly accelerating the process. In addition, we propose a structure-aware contrastive l...

#### 📄 MiMIC: Multi-Modal Indian Earnings Calls Dataset to Predict Stock Prices
- **2025 | arXiv** | [link](http://arxiv.org/abs/2504.09257v1)
- **作者**：Sohom Ghosh, Arnab Maji, Sudip Kumar Naskar
- **摘要**：Predicting stock market prices following corporate earnings calls remains a significant challenge for investors and researchers alike, requiring innovative approaches that can process diverse information sources. This study investigates the impact of corporate earnings calls on stock prices by introducing a multi-modal predictive model. We leverage textual data from earnings call transcripts, along with images and tables from accompanying presentations, to forecast stock price movements on the trading day immediately following these calls. To facilitate this research, we developed the MiMIC (Multi-Modal Indian Earnings Calls) dataset, encompassing companies representing the Nifty 50, Nifty MidCap 50, and Nifty Small 50 indices. The dataset includes earnings call transcripts, presentations, fundamentals, technical indicators, and subsequent stock prices. We present a multimodal analytical framework that integrates quantitative variables with predictive signals derived from textual and visual modalities, thereby enabling a holistic approach to feature representation and analysis. This multi-modal approach demonstrates the potential for integrating diverse information sources to enhan...

#### 📄 An Automated LLM-based Pipeline for Asset-Level Database Creation to Assess Deforestation Impact
- **2025 | arXiv** | [link](http://arxiv.org/abs/2505.05494v1)
- **作者**：Avanija Menon, Ovidiu Serban
- **摘要**：The European Union Deforestation Regulation (EUDR) requires companies to prove their products do not contribute to deforestation, creating a critical demand for precise, asset-level environmental impact data. Current databases lack the necessary detail, relying heavily on broad financial metrics and manual data collection, which limits regulatory compliance and accurate environmental modeling. This study presents an automated, end-to-end data extraction pipeline that uses LLMs to create, clean, and validate structured databases, specifically targeting sectors with a high risk of deforestation. The pipeline introduces Instructional, Role-Based, Zero-Shot Chain-of-Thought (IRZ-CoT) prompting to enhance data extraction accuracy and a Retrieval-Augmented Validation (RAV) process that integrates real-time web searches for improved data reliability. Applied to SEC EDGAR filings in the Mining, Oil & Gas, and Utilities sectors, the pipeline demonstrates significant improvements over traditional zero-shot prompting approaches, particularly in extraction accuracy and validation coverage. This work advances NLP-driven automation for regulatory compliance, CSR (Corporate Social Responsibility)...

#### 📄 Agentic Retrieval of Topics and Insights from Earnings Calls
- **2025 | arXiv** | [link](http://arxiv.org/abs/2507.07906v1)
- **作者**：Anant Gupta, Rajarshi Bhowmik, Geoffrey Gunow
- **摘要**：Tracking the strategic focus of companies through topics in their earnings calls is a key task in financial analysis. However, as industries evolve, traditional topic modeling techniques struggle to dynamically capture emerging topics and their relationships. In this work, we propose an LLM-agent driven approach to discover and retrieve emerging topics from quarterly earnings calls. We propose an LLM-agent to extract topics from documents, structure them into a hierarchical ontology, and establish relationships between new and existing topics through a topic ontology. We demonstrate the use of extracted topics to infer company-level insights and emerging trends over time. We evaluate our approach by measuring ontology coherence, topic evolution accuracy, and its ability to surface emerging financial trends.


### 🎲 生成模型/合成数据（7 篇）

#### 📄 Prediction Arena: Benchmarking AI Models on Real-World Prediction Markets
- **2026 | arXiv** | [link](http://arxiv.org/abs/2604.07355v1)
- **作者**：Jaden Zhang, Gardenia Liu, Oliver Johansson, Hileamlak Yitayew, Kamryn Ohly, Grace Li
- **摘要**：We introduce Prediction Arena, a benchmark for evaluating AI models' predictive accuracy and decision-making by enabling them to trade autonomously on live prediction markets with real capital. Unlike synthetic benchmarks, Prediction Arena tests models in environments where trades execute on actual exchanges (Kalshi and Polymarket), providing objective ground truth that cannot be gamed or overfitted. Each model operates as an independent agent starting with $10,000, making autonomous decisions every 15-45 minutes. Over a 57-day longitudinal evaluation (January 12 to March 9, 2026), we track two cohorts: six frontier models in live trading (Cohort 1, full period) and four next-generation models in paper trading (Cohort 2, 3-day preliminary). For Cohort 1, final Kalshi returns range from -16.0% to -30.8%. Our analysis identifies a clear performance hierarchy: initial prediction accuracy and the ability to capitalize on correct predictions are the main drivers, while research volume shows no correlation with outcomes. A striking cross-platform contrast emerges from parallel Polymarket live trading: Cohort 1 models averaged only -1.1% on Polymarket vs. -22.6% on Kalshi, with grok-4-20-...

#### 📄 Dynamic Synthetic Controls vs. Panel-Aware Double Machine Learning for Geo-Level Marketing Impact Estimation
- **2025 | arXiv** | [link](http://arxiv.org/abs/2508.20335v1)
- **作者**：Sang Su Lee, Vineeth Loganathan, Vijay Raghavan
- **摘要**：Accurately quantifying geo-level marketing lift in two-sided marketplaces is challenging: the Synthetic Control Method (SCM) often exhibits high power yet systematically under-estimates effect size, while panel-style Double Machine Learning (DML) is seldom benchmarked against SCM. We build an open, fully documented simulator that mimics a typical large-scale geo roll-out: N_unit regional markets are tracked for T_pre weeks before launch and for a further T_post-week campaign window, allowing all key parameters to be varied by the user and probe both families under five stylized stress tests: 1) curved baseline trends, 2) heterogeneous response lags, 3) treated-biased shocks, 4) a non-linear outcome link, and 5) a drifting control group trend.   Seven estimators are evaluated: three standard Augmented SCM (ASC) variants and four panel-DML flavors (TWFE, CRE/Mundlak, first-difference, and within-group). Across 100 replications per scenario, ASC models consistently demonstrate severe bias and near-zero coverage in challenging scenarios involving nonlinearities or external shocks. By contrast, panel-DML variants dramatically reduce this bias and restore nominal 95%-CI coverage, proving...

#### 📄 The "double" square-root law: Evidence for the mechanical origin of market impact using Tokyo Stock Exchange data
- **2025 | arXiv** | [link](http://arxiv.org/abs/2502.16246v2)
- **作者**：Guillaume Maitrier, Grégoire Loeper, Kiyoshi Kanazawa, Jean-Philippe Bouchaud
- **摘要**：Understanding the impact of trades on prices is a crucial question for both academic research and industry practice. It is well established that impact follows a square-root impact as a function of traded volume. However, the microscopic origin of such a law remains elusive: empirical studies are particularly challenging due to the anonymity of orders in public data. Indeed, there is ongoing debate about whether price impact has a mechanical origin or whether it is primarily driven by information, as suggested by many economic theories. In this paper, we revisit this question using a very detailed dataset provided by the Japanese stock exchange, containing the trader IDs for all orders sent to the exchange between 2012 and 2018. Our central result is that such a law has in fact microscopic roots and applies already at the level of single child orders, provided one waits long enough for the market to "digest" them. The mesoscopic impact of metaorders arises from a "double" square-root effect: square-root in volume of individual impact, followed by an inverse square-root decay as a function of time. Since market orders are anonymous, we expect and indeed find that these results apply...

#### 📄 Causal Interventions in Bond Multi-Dealer-to-Client Platforms
- **2025 | arXiv** | [link](http://arxiv.org/abs/2506.18147v2)
- **作者**：Paloma Marín, Sergio Ardanza-Trevijano, Javier Sabio
- **摘要**：The digitalization of financial markets has shifted trading from voice to electronic channels, with Multi-Dealer-to-Client (MD2C) platforms now enabling clients to request quotes (RfQs) for financial instruments like bonds from multiple dealers simultaneously. In this competitive landscape, dealers cannot see each other's prices, making a rigorous analysis of the negotiation process crucial to ensure their profitability. This article introduces a novel general framework for analyzing the RfQ process using probabilistic graphical models and causal inference. Within this framework, we explore different inferential questions that are relevant for dealers participating in MD2C platforms, such as the computation of optimal prices, estimating potential revenues and the identification of clients that might be interested in trading the dealer's axes. We then move into analyzing two different approaches for model specification: a generative model built on the work of (Fermanian, Guéant, \& Pu, 2017); and discriminative models utilizing machine learning techniques. Our results show that generative models can match the predictive accuracy of leading discriminative algorithms such as LightGBM ...

#### 📄 Copyright and Competition: Estimating Supply and Demand with Unstructured Data
- **2025 | arXiv** | [link](http://arxiv.org/abs/2501.16120v2)
- **作者**：Sukjin Han, Kyungho Lee
- **摘要**：We study the competitive and welfare effects of copyright in creative industries in the face of cost-reducing technologies such as generative artificial intelligence. Creative products often feature unstructured attributes (e.g., images and text) that are complex and high-dimensional. To address this challenge, we study a stylized design product -- fonts -- using data from the world's largest font marketplace. We construct neural network embeddings to quantify unstructured attributes and measure visual similarity in a manner consistent with human perception. Spatial regression and event-study analyses demonstrate that competition is local in the visual characteristics space. Building on this evidence, we develop a structural model of supply and demand that incorporates embeddings and captures product positioning under copyright-based similarity constraints. Our estimates reveal consumers' heterogeneous design preferences and producers' cost-effective mimicry advantages. Counterfactual analyses show that copyright protection can raise consumer welfare by encouraging product relocation, and that the optimal policy depends on the interaction between copyright and cost-reducing technol...


### ₿ 加密货币/区块链（7 篇）

#### 📄 Do Whitepaper Claims Predict Market Behavior? Evidence from Cryptocurrency Factor Analysis
- **2026 | arXiv** | [link](http://arxiv.org/abs/2601.20336v4)
- **作者**：Murad Farzulla
- **摘要**：This study investigates whether cryptocurrency whitepaper narratives align with empirically observed market factor structure. We construct a pipeline combining zero-shot NLP classification of 38 whitepapers across 10 semantic categories with CP tensor decomposition of hourly market data (49 assets, 17,543 timestamps). Using Procrustes rotation and Tucker's congruence coefficient (phi), we find weak alignment between claims and market statistics (phi = 0.246, p = 0.339) and between claims and latent factors (phi = 0.058, p = 0.751). A methodological validation comparison (statistics versus factors, both derived from market data) achieves significance (p < 0.001), confirming the pipeline detects real structure. The null result indicates whitepaper narratives do not meaningfully predict market factor structure, with implications for narrative economics and investor decision-making. Entity-level analysis reveals specialized tokens (XMR, CRV, YFI) show stronger narrative-market correspondence than broad infrastructure tokens.

#### 📄 Predicting the success of new crypto-tokens: the Pump.fun case
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.14860v1)
- **作者**：Giulio Marino, Manuel Naviglio, Francesco Tarantelli, Fabrizio Lillo
- **摘要**：We study the dynamics of token launched on Pump.fun, a Solana-based launchpad platform, to identify the determinants of the token success. Pump.fun employs a bonding curve mechanism to bootstrap initial liquidity possibly leading to graduation to the on-chain market, which can be seen as a token success. We build predictive models of the probability of graduation conditional on the current amount of Solana locked in the bonding curve and a set of explanatory variables that capture structural and behavioral aspects of the launch process. Conditioning the graduation probability on these variables significantly improves its predictive power, providing insights into early-stage market behavior, speculative and manipulative dynamics, and the informational efficiency of bonding-curve-based token launches.

#### 📄 Market Inefficiency in Cryptoasset Markets
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.20771v2)
- **作者**：Joel Hasbrouck, Julian Ma, Fahad Saleh, Caspar Schwarz-Schilling
- **摘要**：We demonstrate market inefficiency in cryptoasset markets. Our approach examines investments that share a dominant risk factor but differ in their exposure to a secondary risk. We derive equilibrium restrictions that must hold regardless of how investors price either risk. Our empirical results strongly reject these necessary equilibrium restrictions. The rejection implies market inefficiency that cannot be attributed to mispriced risk, suggesting the presence of frictions that impede capital reallocation.

#### 📄 Anomaly prediction in XRP price with topological features
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.18021v2)
- **作者**：Illia Donhauzer, Pierluigi Cesana, Tomoyuki Shirai, Yuichi Ikeda
- **摘要**：The aim of this research is to study XRP cryptoasset price dynamics, with a particular focus on forecasting atypical price movements. Recent studies suggest that topological properties of transaction graphs are highly informative for understanding cryptocurrency price behavior. In this work, we show that specific topological properties of the XRP transaction graphs provide important information about extreme XRP price surges, and can be used for more competitive prediction of anomalous price dynamics.

#### 📄 Informer in Algorithmic Investment Strategies on High Frequency Bitcoin Data
- **2025 | arXiv** | [link](http://arxiv.org/abs/2503.18096v1)
- **作者**：Filip Stefaniuk, Robert Ślepaczuk
- **摘要**：The article investigates the usage of Informer architecture for building automated trading strategies for high frequency Bitcoin data. Three strategies using Informer model with different loss functions: Root Mean Squared Error (RMSE), Generalized Mean Absolute Directional Loss (GMADL) and Quantile loss, are proposed and evaluated against the Buy and Hold benchmark and two benchmark strategies based on technical indicators. The evaluation is conducted using data of various frequencies: 5 minute, 15 minute, and 30 minute intervals, over the 6 different periods. Although the Informer-based model with Quantile loss did not outperform the benchmark, two other models achieved better results. The performance of the model using RMSE loss worsens when used with higher frequency data while the model that uses novel GMADL loss function is benefiting from higher frequency data and when trained on 5 minute interval it beat all the other strategies on most of the testing periods. The primary contribution of this study is the application and assessment of the RMSE, GMADL, and Quantile loss functions with the Informer model to forecast future returns, subsequently using these forecasts to develop...


### 📐 统计套利/均值回归（5 篇）

#### 📄 Pairs Trading Using a Novel Graphical Matching Approach
- **2024 | arXiv** | [link](http://arxiv.org/abs/2403.07998v1)
- **作者**：Khizar Qureshi, Tauhid Zaman
- **摘要**：Pairs trading, a strategy that capitalizes on price movements of asset pairs driven by similar factors, has gained significant popularity among traders. Common practice involves selecting highly cointegrated pairs to form a portfolio, which often leads to the inclusion of multiple pairs sharing common assets. This approach, while intuitive, inadvertently elevates portfolio variance and diminishes risk-adjusted returns by concentrating on a small number of highly cointegrated assets. Our study introduces an innovative pair selection method employing graphical matchings designed to tackle this challenge. We model all assets and their cointegration levels with a weighted graph, where edges signify pairs and their weights indicate the extent of cointegration. A portfolio of pairs is a subgraph of this graph. We construct a portfolio which is a maximum weighted matching of this graph to select pairs which have strong cointegration while simultaneously ensuring that there are no shared assets within any pair of pairs. This approach ensures each asset is included in just one pair, leading to a significantly lower variance in the matching-based portfolio compared to a baseline approach tha...

#### 📄 Market information of the fractional stochastic regularity model
- **2024 | arXiv** | [link](http://arxiv.org/abs/2409.07159v3)
- **作者**：Daniele Angelini, Matthieu Garcin
- **摘要**：The Fractional Stochastic Regularity Model (FSRM) is an extension of Black-Scholes model describing the multifractal nature of prices. It is based on a multifractional process with a random Hurst exponent $H_t$, driven by a fractional Ornstein-Uhlenbeck (fOU) process. When the regularity parameter $H_t$ is equal to $1/2$, the efficient market hypothesis holds, but when $H_t\neq 1/2$ past price returns contain some information on a future trend or mean-reversion of the log-price process. In this paper, we investigate some properties of the fOU process and, thanks to information theory and Shannon's entropy, we determine theoretically the serial information of the regularity process $H_t$ of the FSRM, giving some insight into one's ability to forecast future price increments and to build statistical arbitrages with this model.

#### 📄 ESG driven pairs algorithm for sustainable trading: Analysis from the Indian market
- **2024 | arXiv** | [link](http://arxiv.org/abs/2401.14761v1)
- **作者**：Eeshaan Dutta, Sarthak Diwan, Siddhartha P. Chakrabarty
- **摘要**：This paper proposes an algorithmic trading framework integrating Environmental, Social, and Governance (ESG) ratings with a pairs trading strategy. It addresses the demand for socially responsible investment solutions by developing a unique algorithm blending ESG data with methods for identifying co-integrated stocks. This allows selecting profitable pairs adhering to ESG principles. Further, it incorporates technical indicators for optimal trade execution within this sustainability framework. Extensive back-testing provides evidence of the model's effectiveness, consistently generating positive returns exceeding conventional pairs trading strategies, while upholding ESG principles. This paves the way for a transformative approach to algorithmic trading, offering insights for investors, policymakers, and academics.

#### 📄 Statistical Arbitrage in Rank Space
- **2024 | arXiv** | [link](http://arxiv.org/abs/2410.06568v1)
- **作者**：Y. -F. Li, G. Papanicolaou
- **摘要**：Equity market dynamics are conventionally investigated in name space where stocks are indexed by company names. In contrast, by indexing stocks based on their ranks in capitalization, we gain a different perspective of market dynamics in rank space. Here, we demonstrate the superior performance of statistical arbitrage in rank space over name space, driven by a robust market representation and enhanced mean-reverting properties of residual returns in rank space. Our statistical arbitrage algorithm features an intraday rebalancing mechanism for effective conversion between portfolios in name and rank space. We explore statistical arbitrage with and without neural networks in both name and rank space and show that the portfolios obtained in rank space with neural networks significantly outperform those in name space.

#### 📄 An Application of the Ornstein-Uhlenbeck Process to Pairs Trading
- **2024 | arXiv** | [link](http://arxiv.org/abs/2412.12458v1)
- **作者**：Jirat Suchato, Sean Wiryadi, Danran Chen, Ava Zhao, Michael Yue
- **摘要**：We conduct a preliminary analysis of a pairs trading strategy using the Ornstein-Uhlenbeck (OU) process to model stock price spreads. We compare this approach to a naive pairs trading strategy that uses a rolling window to calculate mean and standard deviation parameters. Our findings suggest that the OU model captures signals and trends effectively but underperforms the naive model on a risk-return basis, likely due to non-stationary pairs and parameter tuning limitations.


### 💡 可解释性（3 篇）

#### 📄 Beyond Prompting: An Autonomous Framework for Systematic Factor Investing via Agentic AI
- **2026 | arXiv** | [link](http://arxiv.org/abs/2603.14288v2)
- **作者**：Allen Yikuan Huang, Zheqi Fan
- **摘要**：This paper develops an autonomous framework for systematic factor investing via agentic AI. Rather than relying on sequential manual prompts, our approach operationalizes the model as a self-directed engine that endogenously formulates interpretable trading signals. To mitigate data snooping biases, this closed-loop system imposes strict empirical discipline through out-of-sample validation and economic rationale requirements. Applying this methodology to the U.S. equity market, we document that long-short portfolios formed on the simple linear combination of signals deliver an annualized Sharpe ratio of 3.11 and a return of 59.53%. Finally, our empirics demonstrate that self-evolving AI offers a scalable and interpretable paradigm.

#### 📄 Stochastic Discount Factors with Cross-Asset Spillovers
- **2026 | arXiv** | [link](http://arxiv.org/abs/2602.20856v1)
- **作者**：Doron Avramov, Xin He
- **摘要**：This paper develops a unified framework that links firm-level predictive signals, cross-asset spillovers, and the stochastic discount factor (SDF). Signals and spillovers are jointly estimated by maximizing the Sharpe ratio, yielding an interpretable SDF that both ranks characteristic relevance and uncovers the direction of predictive influence across assets. Out-of-sample, the SDF consistently outperforms self-predictive and expected-return benchmarks across investment universes and market states. The inferred information network highlights large, low-turnover firms as net transmitters. The framework offers a clear, economically grounded view of the informational architecture underlying cross-sectional return dynamics.

#### 📄 A Comprehensive Sustainable Framework for Machine Learning and Artificial Intelligence
- **2024 | arXiv** | [link](http://arxiv.org/abs/2407.12445v1)
- **作者**：Roberto Pagliari, Peter Hill, Po-Yu Chen, Maciej Dabrowny, Tingsheng Tan, Francois Buet-Golfouse
- **摘要**：In financial applications, regulations or best practices often lead to specific requirements in machine learning relating to four key pillars: fairness, privacy, interpretability and greenhouse gas emissions. These all sit in the broader context of sustainability in AI, an emerging practical AI topic. However, although these pillars have been individually addressed by past literature, none of these works have considered all the pillars. There are inherent trade-offs between each of the pillars (for example, accuracy vs fairness or accuracy vs privacy), making it even more important to consider them together. This paper outlines a new framework for Sustainable Machine Learning and proposes FPIG, a general AI pipeline that allows for these critical topics to be considered simultaneously to learn the trade-offs between the pillars better. Based on the FPIG framework, we propose a meta-learning algorithm to estimate the four key pillars given a dataset summary, model architecture, and hyperparameters before model training. This algorithm allows users to select the optimal model architecture for a given dataset and a given set of user requirements on the pillars. We illustrate the trade...


---

## 💎 散户实操要点（融合 AAAI + arXiv 共识）

### A. 你应该立刻试的 3 件事

**1. LLM 做新闻+财报情绪分析（最低门槛、最大杠杆）**
- 现在的 LLM（GPT-4o / Claude / Qwen2.5）在金融文本理解上已经超过专门训练的 FinBERT
- 给 LLM 喂当天的新闻稿/财报通话/SEC 文件，要求结构化输出：
  - 标的代码列表
  - 情绪极性（-1 到 +1）
  - 事件类型（财报、并购、政策、产品发布、诉讼）
  - 信心度（0-1）
  - 短期方向预期（涨/跌/中性）
- 把这些当作日级别特征喂给 XGBoost / LightGBM 配合价格特征做方向预测
- **多篇 AAAI/arXiv 论文反复验证：news + price 融合显著优于纯 price**

**2. 用预训练 Transformer 时序模型做收益率分布预测**
- 推荐: PatchTST / Autoformer / Informer (开源 GitHub 现成)
- 关键技巧：**不要预测下一个收盘价**，预测**未来 N 天收益率的分布**（quantile forecast）
- 用 quantile 计算：上行概率、95% VaR、最大可能收益

**3. 多策略组合 + 元控制器**
- 学界趋势：单一模型在不同 regime 下都不稳定
- 实操：跑 3-5 个不同思路的策略（动量、反转、事件、宏观、套利），每天根据近期 regime 让一个高层模型选择当前权重
- AAAI 26 多篇论文（MARS、ArchetypeTrader）都在做这事——但你可以用简单加权

### B. 你应该警惕的 5 个陷阱（论文里反复警告）

**1. Look-ahead bias（前瞻偏差）**：用了未来信息做特征，回测虚高
- 例：用 t+1 收盘价计算 t 时刻的指标，看似高 sharpe 实则作弊
- 修复：所有特征只能用 ≤t-1 的数据，时间戳严格对齐

**2. Survivorship bias（存活者偏差）**：只用现存股票做训练
- 例：用 S&P500 当前成分股回测 10 年，**忽略了被剔除/退市的差股**
- 修复：用历史成分股快照、包含已退市标的的数据库

**3. Transaction cost 严重低估**
- 学术回测平均假设 5bps 成本，实际散户经常 15-50bps
- **特别是高频策略**：成本会吃掉 80%+ 的纸面利润

**4. Regime sensitivity（regime 敏感性）**
- 2019 训练的模型在 2020 COVID 全部失效
- 2021 训练的模型在 2022 加息周期全部失效
- 论文 OOS（样本外）测试通常只覆盖训练集后 6-12 月，但**真实部署期是无限期**
- 修复：滚动训练 + 关键经济事件触发的强制重训练

**5. Overfitting（特别是因子挖掘）**
- 暴力搜索 1000 个因子，挑最好的，看似 sharpe 5+
- 修复：Bonferroni 校正、out-of-sample 必须独立、跨市场跨时段验证

### C. 不该做的事（论文也反复警示）

- **不要用 RL 直接预测明天收盘价**——OOS 表现差
- **不要相信单一论文的 Sharpe**——除非有第三方独立复现
- **不要 leverage 学术策略**——学术回测忽略 margin call、流动性约束
- **不要把 LLM 输出的'交易建议'直接执行**——LLM 还没有 actor-level 的真实金融问责机制

---

## 🔬 关键论文方法论拆解

挑 5 篇代表性论文做方法论级别的拆解（其余的看上面 Top 20 + 主题节）。

### LLM Agent 代表论文

**Navigating the Alpha Jungle: An LLM-Powered MCTS Framework for Formulaic Alpha Factor Mining** (2026, AAAI)

- 链接：https://ojs.aaai.org/index.php/AAAI/article/view/37069
- 摘要：Alpha factor mining is pivotal in quantitative investment for identifying predictive signals from complex financial data. While traditional formulaic alpha mining relies on human expertise, contemporary automated methods, such as those based on genetic programming or reinforcement learning, often struggle with search inefficiency or yield alpha factors that are difficult to interpret. This paper introduces a novel framework that integrates Large Language Models (LLMs) with Monte Carlo Tree Search (MCTS) to overcome these limitations. Our framework leverages the LLM's instruction-following and reasoning capability to iteratively generate and refine symbolic alpha formulas within an MCTS-driven exploration. A key innovation is the guidance of MCTS exploration by rich, quantitative feedback from financial backtesting of each candidate factor, enabling efficient navigation of the vast search space. Furthermore, a frequent subtree avoidance mechanism is introduced to enhance search diversity and prevent formulaic homogenization, further improving performance. Experimental results on real-world stock market data demonstrate that our LLM-based framework outperforms existing methods by mining alphas with superior predictive accuracy and trading performance. The resulting formulas are also more amenable to human interpretation, establishing a more effective and efficient paradigm for formulaic alpha mining.

### RL Trading 代表论文

**An Interactive Simulation Framework by Ensemble Imitation Learning Agents for Training Robust Trading Policies** (2026, AAAI)

- 链接：https://ojs.aaai.org/index.php/AAAI/article/view/41493
- 摘要：The reliable deployment of reinforcement learning (RL) for real-world algorithmic trading is critically hindered by the ``simulation-to-reality gap.'' Standard industry backtesting on static historical data ignores market impact—the feedback loop where an agent's trades influence price dynamics—leading to strategies that are fragile and untrustworthy in live markets. To solve this significant problem, we present a novel and emerging application of AI: a framework for building an interactive, responsive market simulator. Our system first uses imitation learning (IL) to automatically train an ensemble of agents, each learning a distinct trading strategy from a different historical market regime (e.g., bull, bear). This creates a data-driven proxy for a diverse population of real-world traders. We then deploy an innovative Action Synthesis Network to synthesize the actions of this ensemble, generating a realistic, synthetic price trajectory that endogenously models the market's reaction to trades. This interactive environment is then used to train a final RL policy. We evaluate our system on NASDAQ-100 (QQQ) data, and the results demonstrate strong potential for deployment. The RL policy trained in our responsive simulator achieves significantly more robust performance, exhibiting superior downside protection during market downturns compared to various traditional baselines. This application provides a scalable and technically sound methodology for building more realistic traini

### Alpha Mining 代表论文

**SkyNet: Belief-Aware Planning for Partially-Observable Stochastic Games** (2026, arXiv)

- 链接：http://arxiv.org/abs/2603.27751v1
- 摘要：In 2019, Google DeepMind released MuZero, a model-based reinforcement learning method that achieves strong results in perfect-information games by combining learned dynamics models with Monte Carlo Tree Search (MCTS). However, comparatively little work has extended MuZero to partially observable, stochastic, multi-player environments, where agents must act under uncertainty about hidden state. Such settings arise not only in card games but in domains such as autonomous negotiation, financial trading, and multi-agent robotics. In the absence of explicit belief modeling, MuZero's latent encoding has no dedicated mechanism for representing uncertainty over unobserved variables.   To address this, we introduce SkyNet (Belief-Aware MuZero), which adds ego-conditioned auxiliary heads for winner prediction and rank estimation to the standard MuZero architecture. These objectives encourage the latent state to retain information predictive of outcomes under partial observability, without requiring explicit belief-state tracking or changes to the search algorithm.   We evaluate SkyNet on Skyjo, a partially observable, non-zero-sum, stochastic card game, using a decision-granularity environment, transformer-based encoding, and a curriculum of heuristic opponents with self-play. In 1000-game head-to-head evaluations at matched checkpoints, SkyNet achieves a 75.3% peak win rate against the baseline (+194 Elo, $p < 10^{-50}$). SkyNet also outperforms the baseline against heuristic opponent

### Graph 代表论文

**Kill-Chain Canaries: Stage-Level Tracking of Prompt Injection Across Attack Surfaces and Model Safety Tiers** (2026, arXiv)

- 链接：http://arxiv.org/abs/2603.28013v3
- 摘要：Multi-agent LLM systems are entering production -- processing documents, managing workflows, acting on behalf of users -- yet their resilience to prompt injection is still evaluated with a single binary: did the attack succeed? This leaves architects without the diagnostic information needed to harden real pipelines. We introduce a kill-chain canary methodology that tracks a cryptographic token through four stages (EXPOSED -> PERSISTED -> RELAYED -> EXECUTED) across 950 runs, five frontier LLMs, six attack surfaces, and five defense conditions. The results reframe prompt injection as a pipeline-architecture problem: every model is fully exposed, yet outcomes diverge downstream -- Claude blocks all injections at memory-write (0/164 ASR), GPT-4o-mini propagates at 53%, and DeepSeek exhibits 0%/100% across surfaces from the same model. Three findings matter for deployment: (1) write-node placement is the highest-leverage safety decision -- routing writes through a verified model eliminates propagation; (2) all four defenses fail on at least one surface due to channel mismatch alone, no adversarial adaptation required; (3) invisible whitefont PDF payloads match or exceed visible-text ASR, meaning rendered-layer screening is insufficient. These dynamics apply directly to production: institutional investors and financial firms already run NLP pipelines over earnings calls, SEC filings, and analyst reports -- the document-ingestion workflows now migrating to LLM agents. Code, run lo

### Multimodal 代表论文

**CLER: Improving Multimodal Financial Reasoning by Cross-MLLM Error Reflection** (2026, AAAI)

- 链接：https://ojs.aaai.org/index.php/AAAI/article/view/40303
- 摘要：Recent advances in Multimodal Large Language Models (MLLMs) have enabled joint reasoning over financial textual and visual inputs. However, they still struggle with financial terminology, logical consistency, and numerical computations. Moreover, while commercial large models perform well on reasoning tasks, their high inference costs limit their scalable usage in real world financial applications. We thus propose a cost-effective framework, CLER, that combines contrastive retrieval with step-wise reflection to improve reasoning performance. Also, the reasoning cost is only generated in the test stage when using commercial large models. CLER leverages FinErrorSet, a dataset of 8,000+ mistake correction pairs from diverse open-source MLLMs. A fine grained retriever is trained to identify structurally relevant errors for self-correction through individual reflection. Experiments on three benchmarks show that CLER consistently outperforms other baselines. To our knowledge, CLER is the first framework to use cross-model errors for financial reasoning.


---

## 📁 数据文件

- `aaai_papers_full.json` — AAAI 完整数据（97 篇）
- `arxiv_papers.json` — arXiv 完整数据（723 篇 2024+）
- 本文档 `AAAI_量化交易论文总结.md`

---

## 📋 完整论文清单（按年份 + 主题）

**仅列标题、年份、链接，作快速浏览参考**。要看摘要去上面的对应主题节或两个 JSON 文件。

### 2026 (499 篇)

**🤖 LLM/Agent 金融应用**：
- [AAAI] MARS: A Meta-Adaptive Reinforcement Learning Framework for Risk-Aware Multi-Agent Portfolio Management → https://ojs.aaai.org/index.php/AAAI/article/view/39095
- [AAAI] Navigating the Alpha Jungle: An LLM-Powered MCTS Framework for Formulaic Alpha Factor Mining → https://ojs.aaai.org/index.php/AAAI/article/view/37069
- [AAAI] Semantics-Preserving Adversarial Attacks on Event-Driven Stock Prediction Models → https://ojs.aaai.org/index.php/AAAI/article/view/41099
- [AAAI] CLER: Improving Multimodal Financial Reasoning by Cross-MLLM Error Reflection → https://ojs.aaai.org/index.php/AAAI/article/view/40303
- [AAAI] FinMathBench: A Formula-Driven Benchmark for Evaluating LLMs’ Math Reasoning Capabilities in Finance → https://ojs.aaai.org/index.php/AAAI/article/view/40358
- [AAAI] FinMMDocR: Benchmarking Financial Multimodal Reasoning with Scenario Awareness, Document Understanding, and Multi-Step Computation → https://ojs.aaai.org/index.php/AAAI/article/view/39785
- [AAAI] Multi-Agent Reinforcement Learning for Modeling, Simulating, and Optimizing Energy Markets → https://ojs.aaai.org/index.php/AAAI/article/view/41229
- [AAAI] FinRpt: Dataset, Evaluation System and LLM-based Multi-agent Framework for Equity Research Report Generation → https://ojs.aaai.org/index.php/AAAI/article/view/37014
- [arXiv] When Quotes Crumble: Detecting Transient Mechanical Liquidity Erosion in Limit Order Books → http://arxiv.org/abs/2604.21993v1
- [arXiv] AEL: Agent Evolving Learning for Open-Ended Environments → http://arxiv.org/abs/2604.21725v1
- [arXiv] ChatGPT as a Time Capsule: The Limits of Price Discovery → http://arxiv.org/abs/2604.21433v1
- [arXiv] Ideological Bias in LLMs' Economic Causal Reasoning → http://arxiv.org/abs/2604.21334v1
- [arXiv] Dialect vs Demographics: Quantifying LLM Bias from Implicit Linguistic Signals vs. Explicit User Profiles → http://arxiv.org/abs/2604.21152v1
- [arXiv] MGDA-Decoupled: Geometry-Aware Multi-Objective Optimisation for DPO-based LLM Alignment → http://arxiv.org/abs/2604.20685v1
- [arXiv] A Hierarchical MARL-Based Approach for Coordinated Retail P2P Trading and Wholesale Market Participation of DERs → http://arxiv.org/abs/2604.20586v1
- [arXiv] On the Quantization Robustness of Diffusion Language Models in Coding Benchmarks → http://arxiv.org/abs/2604.20079v1
- [arXiv] Information Aggregation with AI Agents → http://arxiv.org/abs/2604.20050v1
- [arXiv] From Signal Degradation to Computation Collapse: Uncovering the Two Failure Modes of LLM Quantization → http://arxiv.org/abs/2604.19884v1
- [arXiv] Time Series Augmented Generation for Financial Applications → http://arxiv.org/abs/2604.19633v1
- [arXiv] Cross-Stock Predictability via LLM-Augmented Semantic Networks → http://arxiv.org/abs/2604.19476v1
- [arXiv] If you're waiting for a sign... that might not be it! Mitigating Trust Boundary Confusion from Visual Injections on Vision-Language Agentic  → http://arxiv.org/abs/2604.19844v1
- [arXiv] Rethinking Scale: Deployment Trade-offs of Small Language Models under Agent Paradigms → http://arxiv.org/abs/2604.19299v1
- [arXiv] CHICO-Agent: An LLM Agent for the Cross-layer Optimization of 2.5D and 3D Chiplet-based Systems → http://arxiv.org/abs/2604.18764v1
- [arXiv] Dissecting AI Trading: Behavioral Finance and Market Bubbles → http://arxiv.org/abs/2604.18373v1
- [arXiv] MFMDQwen: Multilingual Financial Misinformation Detection Based on Large Language Model → http://arxiv.org/abs/2604.18272v1
- [arXiv] Privacy-Preserving Product-Quantized Approximate Nearest Neighbor Search Framework for Large-scale Datasets via A Hybrid of Fully Homomorphi → http://arxiv.org/abs/2604.17816v1
- [arXiv] Bridging the Reasoning Gap in Vietnamese with Small Language Models via Test-Time Scaling → http://arxiv.org/abs/2604.17794v1
- [arXiv] Representation-Guided Parameter-Efficient LLM Unlearning → http://arxiv.org/abs/2604.17396v1
- [arXiv] AutoSearch: Adaptive Search Depth for Efficient Agentic RAG via Reinforcement Learning → http://arxiv.org/abs/2604.17337v1
- [arXiv] Signal or Noise in Multi-Agent LLM-based Stock Recommendations? → http://arxiv.org/abs/2604.17327v1
- *(+110 篇省略)*

**🎯 强化学习交易**：
- [AAAI] MetaTrader: Learning to Generalize RL Trading Policies Beyond Offline Data → https://ojs.aaai.org/index.php/AAAI/article/view/40027
- [AAAI] ArchetypeTrader: Reinforcement Learning for Selecting and Refining Learnable Strategic Archetypes in Quantitative Trading → https://ojs.aaai.org/index.php/AAAI/article/view/40166
- [AAAI] An Interactive Simulation Framework by Ensemble Imitation Learning Agents for Training Robust Trading Policies → https://ojs.aaai.org/index.php/AAAI/article/view/41493
- [AAAI] Inferring Heterogeneous Private Valuations from Offline Market Data via Entropic Risk-Sensitive Utility Maximization → https://ojs.aaai.org/index.php/AAAI/article/view/38822
- [arXiv] Liquidity provision in CLMMs: evidence from transactions data → http://arxiv.org/abs/2604.22069v1
- [arXiv] StructMem: Structured Memory for Long-Horizon Behavior in LLMs → http://arxiv.org/abs/2604.21748v1
- [arXiv] Fairness under uncertainty in sequential decisions → http://arxiv.org/abs/2604.21711v1
- [arXiv] Temporally Extended Mixture-of-Experts Models → http://arxiv.org/abs/2604.20156v1
- [arXiv] Testing replication for an agent-based model of market fragmentation and latency arbitrage → http://arxiv.org/abs/2604.20067v1
- [arXiv] Probabilistic Forecasting for Day-ahead Electricity Prices, Battery Trading Strategies and the Economic Evaluation of Predictive Accuracy → http://arxiv.org/abs/2604.19580v1
- [arXiv] SAHM: A Benchmark for Arabic Financial and Shari'ah-Compliant Reasoning → http://arxiv.org/abs/2604.19098v1
- [arXiv] Fisher Decorator: Refining Flow Policy via A Local Transport Map → http://arxiv.org/abs/2604.17919v1
- [arXiv] Climate Risk Stress Testing in California: A Geospatial Framework for Banking and Climate-Exposed Sectors → http://arxiv.org/abs/2604.16716v1
- [arXiv] Risk-Sensitive Investment Management via Free Energy-Entropy Duality → http://arxiv.org/abs/2604.15463v1
- [arXiv] When Missing Becomes Structure: Intent-Preserving Policy Completion from Financial KOL Discourse → http://arxiv.org/abs/2604.14333v2
- [arXiv] Risk-Constrained Kelly for Mutually Exclusive Outcomes: CRRA Support Invariance and Logarithmic One-Dimensional Calibration → http://arxiv.org/abs/2604.11577v1
- [arXiv] Temperature Anomalies and Climate Physical Risk in Portfolio Construction → http://arxiv.org/abs/2604.11143v1
- [arXiv] On the Structure of Risk Contribution: A Leave-One-Out Decomposition into Inherent and Correlation Risk → http://arxiv.org/abs/2604.10375v1
- [arXiv] Credit-Budgeted ICPC-Style Coding: When Agents Must Pay for Every Decision → http://arxiv.org/abs/2604.10182v1
- [arXiv] When AAA Satisfies Nothing: Impossibility Theorems for Structured Credit Ratings → http://arxiv.org/abs/2604.20877v1
- [arXiv] From Perception to Autonomous Computational Modeling: A Multi-Agent Approach → http://arxiv.org/abs/2604.06788v2
- [arXiv] Heterogeneous Mixture-of-Experts for Energy-Efficient Multimodal ISAC in Highly Mobile Networks → http://arxiv.org/abs/2604.06697v1
- [arXiv] Transfer Learning for Loan Recovery Prediction under Distribution Shifts with Heterogeneous Feature Spaces → http://arxiv.org/abs/2604.02832v2
- [arXiv] Hedging market risk and uncertainty via a robust portfolio approach → http://arxiv.org/abs/2604.02126v1
- [arXiv] Reinforcement Learning for Speculative Trading under Exploratory Framework → http://arxiv.org/abs/2604.02035v1
- [arXiv] ClawSafety: "Safe" LLMs, Unsafe Agents → http://arxiv.org/abs/2604.01438v2
- [arXiv] Common Risk Factors in Decentralized AI Subnets → http://arxiv.org/abs/2603.29751v1
- [arXiv] Be Water: An Evolutionary Proof for Trend-Following → http://arxiv.org/abs/2603.29593v1
- [arXiv] Realistic Market Impact Modeling for Reinforcement Learning Trading Environments → http://arxiv.org/abs/2603.29086v2
- [arXiv] Model Predictive Control For Trade Execution → http://arxiv.org/abs/2603.28898v1
- *(+70 篇省略)*

**🌐 其他金融 AI**：
- [arXiv] Revealing Geography-Driven Signals in Zone-Level Claim Frequency Models: An Empirical Study using Environmental and Visual Predictors → http://arxiv.org/abs/2604.21893v1
- [arXiv] Modeling dependency between operational risk losses and macroeconomic variables using Hidden Markov Models → http://arxiv.org/abs/2604.21734v1
- [arXiv] CoFEE: Reasoning Control for LLM-Based Feature Discovery → http://arxiv.org/abs/2604.21584v1
- [arXiv] Relative Principals, Pluralistic Alignment, and the Structural Value Alignment Problem → http://arxiv.org/abs/2604.20805v1
- [arXiv] Contagion or Macroeconomic Fluctuations? Identifiability in Aggregated Default Data → http://arxiv.org/abs/2604.18118v1
- [arXiv] A Herding-Based Model of Technological Transfer and Economic Convergence: Evidence from Central and Eastern Europe → http://arxiv.org/abs/2604.11413v1
- [arXiv] Climate-Aware Copula Models for Sovereign Rating Migration Risk → http://arxiv.org/abs/2604.07567v1
- [arXiv] Ranking Metrics: Extending Acceptability and Performance Indexes → http://arxiv.org/abs/2604.16438v1
- [arXiv] $α$-robust utility maximization with intractable claims: A quantile optimization approach → http://arxiv.org/abs/2604.04649v1
- [arXiv] SuperLocalMemory V3.3: The Living Brain -- Biologically-Inspired Forgetting, Cognitive Quantization, and Multi-Channel Retrieval for Zero-LL → http://arxiv.org/abs/2604.04514v1
- [arXiv] Concave Continuation: Linking Routing to Arbitrage → http://arxiv.org/abs/2604.02909v1
- [arXiv] Financial Anomaly Detection for the Canadian Market → http://arxiv.org/abs/2604.02549v1
- [arXiv] Interpretable Deep Reinforcement Learning for Element-level Bridge Life-cycle Optimization → http://arxiv.org/abs/2604.02528v1
- [arXiv] Paper Reconstruction Evaluation: Evaluating Presentation and Hallucination in AI-written Papers → http://arxiv.org/abs/2604.01128v1
- [arXiv] AlphaLab: Autonomous Multi-Agent Research Across Optimization Domains with Frontier LLMs → http://arxiv.org/abs/2604.08590v1
- [arXiv] Building evidence-based knowledge bases from full-text literature for disease-specific biomedical reasoning → http://arxiv.org/abs/2603.28325v3
- [arXiv] Nonlinear Factor Decomposition via Kolmogorov-Arnold Networks: A Spectral Approach to Asset Return Analysis → http://arxiv.org/abs/2603.28257v1
- [arXiv] Capital-Allocation-Induced Risk Sharing → http://arxiv.org/abs/2603.26491v1
- [arXiv] The Free-Market Algorithm: Self-Organizing Optimization for Open-Ended Complex Systems → http://arxiv.org/abs/2603.24559v1
- [arXiv] Adapting Altman's bankruptcy prediction model to the compositional data methodology → http://arxiv.org/abs/2603.24215v1
- [arXiv] Ordering results for extreme claim amounts based on random number of claims → http://arxiv.org/abs/2603.24640v1
- [arXiv] Mean Field Equilibrium Asset Pricing Models With Exponential Utility → http://arxiv.org/abs/2603.22058v1
- [arXiv] Financial Dynamics and Interconnected Risk of Liquid Restaking → http://arxiv.org/abs/2604.03274v1
- [arXiv] Connecting Distributed Ledgers: Surveying Novel Interoperability Solutions in On-chain Finance → http://arxiv.org/abs/2603.21797v1
- [arXiv] A Modular LLM Framework for Explainable Price Outlier Detection → http://arxiv.org/abs/2603.20636v1
- [arXiv] Outperforming a Benchmark with $α$-Bregman Wasserstein divergence → http://arxiv.org/abs/2603.20580v1
- [arXiv] Dynamic Pareto Optima in Multi-Period Pure-Exchange Economies → http://arxiv.org/abs/2603.19414v1
- [arXiv] Discrimination-insensitive pricing → http://arxiv.org/abs/2603.16720v2
- [arXiv] Heterogeneous Returns and Wealth Tax Neutrality: A Fokker-Planck Framework → http://arxiv.org/abs/2603.16006v2
- [arXiv] Some general results on risk budgeting portfolios → http://arxiv.org/abs/2603.15511v1
- *(+42 篇省略)*

**📊 波动率预测**：
- [arXiv] Structural Dynamics of G5 Stock Markets During Exogenous Shocks: A Random Matrix Theory-Based Complexity Gap Approach → http://arxiv.org/abs/2604.19107v1
- [arXiv] Broken Symmetry, Conservation Law, and Scaling in Accumulated Stock Returns -- a Modified Jones-Faddy Skew t-Distribution Perspective → http://arxiv.org/abs/2604.15519v1
- [arXiv] The Acoustic Camouflage Phenomenon: Re-evaluating Speech Features for Financial Risk Prediction → http://arxiv.org/abs/2604.14619v1
- [arXiv] When Forecast Accuracy Fails: Rank Correlation and Decision Quality in Multi-Market Battery Storage Optimization → http://arxiv.org/abs/2604.12082v1
- [arXiv] Risk-Sensitive Specialist Routing for Volatility Forecasting → http://arxiv.org/abs/2604.10402v3
- [arXiv] Reliability-Aware ETF Tail-Risk Monitoring → http://arxiv.org/abs/2604.08765v2
- [arXiv] Measuring Strategy-Decay Risk: Minimum Regime Performance and the Durability of Systematic Investing → http://arxiv.org/abs/2604.08356v1
- [arXiv] SBBTS: A Unified Schrödinger-Bass Framework for Synthetic Financial Time Series → http://arxiv.org/abs/2604.07159v1
- [arXiv] Asset allocation using a Markov process of clustered efficient frontier coefficients states → http://arxiv.org/abs/2604.03946v1
- [arXiv] On options-driven realized volatility forecasting: Information gains via rough volatility model → http://arxiv.org/abs/2604.02743v3
- [arXiv] Do Prediction Markets Forecast Cryptocurrency Volatility? Evidence from Kalshi Macro Contracts → http://arxiv.org/abs/2604.01431v1
- [arXiv] Option Pricing on Automated Market Maker Tokens → http://arxiv.org/abs/2603.29763v1
- [arXiv] Modeling and Forecasting Tail Risk Spillovers: A Component-Based CAViaR Approach → http://arxiv.org/abs/2603.25217v1
- [arXiv] Proxy-Reliance Control in Conformal Recalibration of One-Sided Value-at-Risk → http://arxiv.org/abs/2603.22569v1
- [arXiv] Flexible Information Acquisition in the Kyle Model → http://arxiv.org/abs/2603.21842v1
- [arXiv] Mislearning of Factor Risk Premia under Structural Breaks: A Misspecified Bayesian Learning Framework → http://arxiv.org/abs/2603.21672v3
- [arXiv] If Not Now, Then When? Model Risk in the Optimal Exercise of American Options → http://arxiv.org/abs/2603.19984v1
- [arXiv] ARTEMIS: A Neuro Symbolic Framework for Economically Constrained Market Dynamics → http://arxiv.org/abs/2603.18107v1
- [arXiv] Multivariate GARCH and portfolio variance prediction: A forecast reconciliation perspective → http://arxiv.org/abs/2603.17463v2
- [arXiv] GARCH-FIS: A Hybrid Forecasting Model with Dynamic Volatility-Driven Parameter Adaptation → http://arxiv.org/abs/2603.14793v1
- [arXiv] Entropic signatures of market response under concentrated policy communication → http://arxiv.org/abs/2603.12040v1
- [arXiv] Hybrid Hidden Markov Model for Modeling Equity Excess Growth Rate Dynamics: A Discrete-State Approach with Jump-Diffusion → http://arxiv.org/abs/2603.10202v2
- [arXiv] Competition between DEXs through Dynamic Fees → http://arxiv.org/abs/2603.09669v1
- [arXiv] Nonconcave Portfolio Choice under Smooth Ambiguity → http://arxiv.org/abs/2603.08552v1
- [arXiv] Temporal Coverage Bias in Financial Panel Data: A Coverage-Aware Structuring Framework with Evidence from the Dhaka Stock Exchange → http://arxiv.org/abs/2603.20237v2
- [arXiv] Joint Return and Risk Modeling with Deep Neural Networks for Portfolio Construction → http://arxiv.org/abs/2603.19288v1
- [arXiv] An Interpretable Generative Framework for Anomaly Detection in High-Dimensional Financial Time Series → http://arxiv.org/abs/2603.07864v1
- [arXiv] Dynamic Tracking Error and the Total Portfolio Approach → http://arxiv.org/abs/2603.03213v1
- [arXiv] Range-Based Volatility Estimators for Monitoring Market Stress: Evidence from Local Food Price Data → http://arxiv.org/abs/2603.02898v1
- [arXiv] Same Error, Different Function: The Optimizer as an Implicit Prior in Financial Time Series → http://arxiv.org/abs/2603.02620v1
- *(+19 篇省略)*

**💼 组合优化/资产配置**：
- [AAAI] PortfolioPilot: An Agentic Platform for Financial Portfolio Management Algorithm Development and Evaluation → https://ojs.aaai.org/index.php/AAAI/article/view/42396
- [arXiv] STRIKE: Additive Feature-Group-Aware Stacking Framework for Credit Default Prediction → http://arxiv.org/abs/2604.17622v1
- [arXiv] Optimal Insurance Menu Design under the Expected-Value Premium Principle → http://arxiv.org/abs/2604.15881v1
- [arXiv] Lambda R{é}nyi entropic value-at-risk → http://arxiv.org/abs/2604.10657v1
- [arXiv] Multi periods mean-DCVaR optimization: a Recursive Neural Network resolution → http://arxiv.org/abs/2604.14439v1
- [arXiv] Forecasting Tangency Portfolios and Investing in the Minimum Euclidean Distance Portfolio to Maximize Out-of-Sample Sharpe Ratios → http://arxiv.org/abs/2604.03948v1
- [arXiv] Portfolio Optimization Proxies under Label Scarcity and Regime Shifts via Bayesian and Deterministic Students under Semi-Supervised Sandwich → http://arxiv.org/abs/2604.14206v1
- [arXiv] Scalable Mean-Variance Portfolio Optimization via Subspace Embeddings and GPU-Friendly Nesterov-Accelerated Projected Gradient → http://arxiv.org/abs/2604.02917v1
- [arXiv] The Self Driving Portfolio: Agentic Architecture for Institutional Asset Management → http://arxiv.org/abs/2604.02279v1
- [arXiv] The Risk Quadrangle in Optimization: An Overview with Recent Results and Extensions → http://arxiv.org/abs/2603.27370v1
- [arXiv] Biased Mean Quadrangle and Applications → http://arxiv.org/abs/2603.26901v1
- [arXiv] Semi-Static Variance-Optimal Hedging of Covariance Risk in Multi-Asset Derivatives → http://arxiv.org/abs/2603.25320v1
- [arXiv] Hyper-Adaptive Momentum Dynamics for Native Cubic Portfolio Optimization: Avoiding Quadratization Distortion in Higher-Order Cardinality-Con → http://arxiv.org/abs/2603.15947v1
- [arXiv] Pools as Portfolios: Observed arbitrage efficiency & LVR analysis of dynamic weight AMMs → http://arxiv.org/abs/2602.22069v1
- [arXiv] Entropy Regularization under Bayesian Drift Uncertainty → http://arxiv.org/abs/2602.16862v2
- [arXiv] Money-Back Tontines for Retirement Decumulation: Neural-Network Optimization under Systematic Longevity Risk → http://arxiv.org/abs/2602.16212v1
- [arXiv] Constrained Portfolio Optimization via Quantum Approximate Optimization Algorithm (QAOA) with XY-Mixers and Trotterized Initialization: A Hy → http://arxiv.org/abs/2602.14827v1
- [arXiv] Sustainable Investment: ESG Impacts on Large Portfolio → http://arxiv.org/abs/2602.14439v1
- [arXiv] Neural Nonlinear Shrinkage of Covariance Matrices for Minimum Variance Portfolio Optimization → http://arxiv.org/abs/2601.15597v1
- [arXiv] Enhancing Portfolio Optimization with Deep Learning Insights → http://arxiv.org/abs/2601.07942v1
- [arXiv] FlashFolio: A GPU-Accelerated Solver for Portfolio Optimization → http://arxiv.org/abs/2604.22625v1

**⚡ 订单簿/HFT/微观结构**：
- [arXiv] Early Detection of Latent Microstructure Regimes in Limit Order Books → http://arxiv.org/abs/2604.20949v1
- [arXiv] Bond Market Making with a Hit-Ratio Target → http://arxiv.org/abs/2604.20406v1
- [arXiv] Spurious Predictability in Financial Machine Learning → http://arxiv.org/abs/2604.15531v1
- [arXiv] Interpretable Systematic Risk around the Clock → http://arxiv.org/abs/2604.13458v1
- [arXiv] Mandatory Disclosure in Oligopolistic Market Making → http://arxiv.org/abs/2604.10194v1
- [arXiv] What Happens When Institutional Liquidity Enters Prediction Markets: Identification, Measurement, and a Synthetic Proof of Concept → http://arxiv.org/abs/2604.10005v2
- [arXiv] Forecasting duration in high-frequency financial data using a self-exciting flexible residual point process → http://arxiv.org/abs/2604.00346v1
- [arXiv] Forecast collapse of transformer-based models under squared loss in financial time series → http://arxiv.org/abs/2604.00064v1
- [arXiv] The Geometry of Risk: Path-Dependent Regulation and Anticipatory Hedging via the SigSwap → http://arxiv.org/abs/2603.24154v1
- [arXiv] Bridging the Reality Gap in Limit Order Book Simulation → http://arxiv.org/abs/2603.24137v1
- [arXiv] ReLaMix: Residual Latency-Aware Mixing for Delay-Robust Financial Time-Series Forecasting → http://arxiv.org/abs/2603.20869v1
- [arXiv] Information Propagation Across Investor Types: Transfer Entropy Networks in the Korean Equity Market → http://arxiv.org/abs/2603.20271v1
- [arXiv] An operator-level ARCH Model → http://arxiv.org/abs/2603.10272v2
- [arXiv] A Hybrid Quantum-Classical Framework for Financial Volatility Forecasting Based on Quantum Circuit Born Machines → http://arxiv.org/abs/2603.09789v1
- [arXiv] Extreme Value Analysis for Finite, Multivariate and Correlated Systems with Finance as an Example → http://arxiv.org/abs/2603.05260v1
- [arXiv] TradeFM: A Generative Foundation Model for Trade-flow and Market Microstructure → http://arxiv.org/abs/2602.23784v1
- [arXiv] Explainable Patterns in Cryptocurrency Microstructure → http://arxiv.org/abs/2602.00776v1
- [arXiv] Directional Liquidity and Geometric Shear in Pregeometric Order Books → http://arxiv.org/abs/2601.19369v1
- [arXiv] Pregeometric Origins of Liquidity Geometry in Financial Order Books → http://arxiv.org/abs/2601.17245v1
- [arXiv] A Learnable Wavelet Transformer for Long-Short Equity Trading and Risk-Adjusted Return Optimization → http://arxiv.org/abs/2601.13435v4
- [arXiv] Improving Machine Learning Performance with Synthetic Augmentation → http://arxiv.org/abs/2604.14498v1

**🌊 市场状态/Regime**：
- [arXiv] Evaluating Structured Strategy Backtests: Peer Benchmarks, Regime Timing, and Live Performance → http://arxiv.org/abs/2604.18821v1
- [arXiv] The Virtue of Sparsity in Complexity → http://arxiv.org/abs/2604.17166v1
- [arXiv] Against a Universal Trading Strategy: No-Arbitrage, No-Free-Lunch, and Adversarial Cantor Diagonalization → http://arxiv.org/abs/2604.13334v1
- [arXiv] Bridging Stochastic Control and Deep Hedging: Structural Priors for No-Transaction Band Networks → http://arxiv.org/abs/2603.29994v1
- [arXiv] Optimal Parlay Wagering and Whitrow Asymptotics: A State-Price and Implicit-Cash Treatment → http://arxiv.org/abs/2603.26620v1
- [arXiv] Robust Investment-Driven Insurance Pricing under Correlation Ambiguity → http://arxiv.org/abs/2603.18969v1
- [arXiv] Flow Taxes, Stock Taxes, and Portfolio Choice: A Generalised Neutrality Result → http://arxiv.org/abs/2603.15974v2
- [arXiv] E-TRENDS: Enhanced LSTM Trend Forecasting for Equities → http://arxiv.org/abs/2603.14453v1
- [arXiv] Spectral Portfolio Theory: From SGD Weight Matrices to Wealth Dynamics → http://arxiv.org/abs/2603.09006v2
- [arXiv] Uncertainty-Gated Generative Modeling → http://arxiv.org/abs/2603.07753v1
- [arXiv] Coupled Supply and Demand Forecasting in Platform Accommodation Markets → http://arxiv.org/abs/2603.00422v2
- [arXiv] When Fusion Helps and When It Breaks: View-Aligned Robustness in Same-Source Financial Imaging → http://arxiv.org/abs/2602.11020v2
- [arXiv] Bayesian Robust Financial Trading with Adversarial Synthetic Market Data → http://arxiv.org/abs/2601.17008v1
- [arXiv] STN-GPR: A Singularity Tensor Network Framework for Efficient Option Pricing → http://arxiv.org/abs/2603.26318v1
- [arXiv] Three-Body Barrier Dynamics of Double-Alpha Decay in Heavy Nuclei → http://arxiv.org/abs/2602.09480v1
- [arXiv] The Temporal Markov Transition Field → http://arxiv.org/abs/2603.08803v1

**⚖ 风险/信用/欺诈**：
- [arXiv] Vault as a credit instrument → http://arxiv.org/abs/2604.17579v2
- [arXiv] A Counterfactual Diagnostic Framework for Explaining KS Deterioration in Credit Risk Model Validation → http://arxiv.org/abs/2604.11561v1
- [arXiv] Adaptive VaR Control for Standardized Option Books under Marking Frictions → http://arxiv.org/abs/2604.03499v1
- [arXiv] Shifting Correlations: How Trade Policy Uncertainty Alters stock-T bill Relationships → http://arxiv.org/abs/2603.25285v1
- [arXiv] Environmental CVA with K-Robust Wrong-Way Risk → http://arxiv.org/abs/2603.23842v2
- [arXiv] Risk-Based Auto-Deleveraging → http://arxiv.org/abs/2603.15963v1
- [arXiv] Fast Times, Slow Times: Timescale Separation in Financial Timeseries Data → http://arxiv.org/abs/2601.11201v1
- [arXiv] Option Pricing on Noisy Intermediate-Scale Quantum Computers: A Quantum Neural Network Approach → http://arxiv.org/abs/2604.19832v1
- [arXiv] Lévy-Flow Models: Heavy-Tail-Aware Normalizing Flows for Financial Risk Management → http://arxiv.org/abs/2604.00195v1
- [arXiv] Embedding interpretable $\ell_1$-regression into neural networks for uncovering temporal structure in cell imaging → http://arxiv.org/abs/2603.02899v2
- [arXiv] Reliable Real-Time Value at Risk Estimation via Quantile Regression Forest with Conformal Calibration → http://arxiv.org/abs/2602.01912v1
- [arXiv] Constrained Policy Optimization with Cantelli-Bounded Value-at-Risk → http://arxiv.org/abs/2601.22993v2

**🛡 对抗/鲁棒性**：
- [AAAI] MartDE: A Privacy-Preserving and Cost-Efficient Evaluation Framework for Data Marketplaces → https://ojs.aaai.org/index.php/AAAI/article/view/40889
- [arXiv] RARE: Redundancy-Aware Retrieval Evaluation Framework for High-Similarity Corpora → http://arxiv.org/abs/2604.19047v1
- [arXiv] Budgeted Robust Intervention Design for Financial Networks with Common Asset Exposures → http://arxiv.org/abs/2603.27274v1
- [arXiv] Optimal Hedge Ratio for Delta-Neutral Liquidity Provision under Liquidation Constraints → http://arxiv.org/abs/2603.19716v1
- [arXiv] Autodeleveraging as Online Learning → http://arxiv.org/abs/2602.15182v1
- [arXiv] A novel approach to trading strategy parameter optimization using double out-of-sample data and walk-forward techniques → http://arxiv.org/abs/2602.10785v1
- [arXiv] Comparing Mixture, Box, and Wasserstein Ambiguity Sets in Distributionally Robust Asset Liability Management → http://arxiv.org/abs/2602.08228v1
- [arXiv] Continual Quantum Architecture Search with Tensor-Train Encoding: Theory and Applications to Signal Processing → http://arxiv.org/abs/2601.06392v1
- [arXiv] The GT-Score: A Robust Objective Function for Reducing Overfitting in Data-Driven Trading Strategies → http://arxiv.org/abs/2602.00080v1
- [arXiv] Feasibility-First Satellite Integration in Robust Portfolio Architectures → http://arxiv.org/abs/2601.08721v1
- [arXiv] A Quantum Reservoir Computing Approach to Quantum Stock Price Forecasting in Quantum-Invested Markets → http://arxiv.org/abs/2602.13094v1

**🧪 回测/市场模拟**：
- [arXiv] Post-Screening Portfolio Selection → http://arxiv.org/abs/2604.17593v1
- [arXiv] Systemic Risk and Default Cascades in Global Equity Markets: A Network and Tail-Risk Approach Based on the Gai Kapadia Framework → http://arxiv.org/abs/2604.19796v1
- [arXiv] Sequential Audit Sampling with Statistical Guarantees → http://arxiv.org/abs/2604.06116v1
- [arXiv] Survivorship Bias in Emerging Market Small-Cap Indices: Evidence from India's NIFTY Smallcap 250 → http://arxiv.org/abs/2603.19380v1
- [arXiv] Manipulation in Prediction Markets: An Agent-based Modeling Experiment → http://arxiv.org/abs/2601.20452v1
- [arXiv] Low-energy 17O(n,g)18O reaction within the microscopic potential model and its role for the weak r-process → http://arxiv.org/abs/2601.22234v1
- [arXiv] Compliance Moral Hazard and the Backfiring Mandate → http://arxiv.org/abs/2604.21789v1
- [arXiv] Bayesian Sparsity Modeling of Shared Neural Response in Functional Magnetic Resonance Imaging Data → http://arxiv.org/abs/2604.21676v1
- [arXiv] Open-H-Embodiment: A Large-Scale Dataset for Enabling Foundation Models in Medical Robotics → http://arxiv.org/abs/2604.21017v1
- [arXiv] Passive Variable Impedance For Shared Control → http://arxiv.org/abs/2604.20557v1
- [arXiv] Cosmological analysis of the DESI DR1 Lyman alpha 1D power spectrum → http://arxiv.org/abs/2601.21432v1

**🔄 Transformer 时序**：
- [arXiv] The CTLNet for Shanghai Composite Index Prediction → http://arxiv.org/abs/2604.16835v1
- [arXiv] Multimodal Forecasting for Commodity Prices Using Spectrogram-Based and Time Series Representations → http://arxiv.org/abs/2603.27321v1
- [arXiv] Integrating Inductive Biases in Transformers via Distillation for Financial Time Series Forecasting → http://arxiv.org/abs/2603.16985v1
- [arXiv] A Controlled Comparison of Deep Learning Architectures for Multi-Horizon Financial Forecasting: Evidence from 918 Experiments → http://arxiv.org/abs/2603.16886v1
- [arXiv] Financial time series augmentation using transformer based GAN architecture → http://arxiv.org/abs/2602.17865v1
- [arXiv] TF-CoDiT: Conditional Time Series Synthesis with Diffusion Transformers for Treasury Futures → http://arxiv.org/abs/2601.11880v1
- [arXiv] ProbFM: Probabilistic Time Series Foundation Model with Uncertainty Decomposition → http://arxiv.org/abs/2601.10591v1
- [arXiv] Reliable Grid Forecasting: State Space Models for Safety-Critical Energy Systems → http://arxiv.org/abs/2601.01410v6
- [arXiv] StretchTime: Adaptive Time Series Forecasting via Symplectic Attention → http://arxiv.org/abs/2602.08983v1
- [arXiv] From Hawkes Processes to Attention: Time-Modulated Mechanisms for Event Sequences → http://arxiv.org/abs/2601.09220v2

**📐 期权/衍生品**：
- [arXiv] Pricing and Hedging Financial Derivatives in Merger\&Acquisition Deals with Price Impact → http://arxiv.org/abs/2604.21581v1
- [arXiv] Topological Risk Parity → http://arxiv.org/abs/2604.16773v1
- [arXiv] Target Weight Mechanism doesn't make delta hedge easier → http://arxiv.org/abs/2604.16467v1
- [arXiv] Was Benoit Mandelbrot a hedgehog or a fox? → http://arxiv.org/abs/2602.01122v1
- [arXiv] Optimal strategy and deep hedging for share repurchase programs → http://arxiv.org/abs/2601.18686v1
- [arXiv] Adaptively trained Physics-informed Radial Basis Function Neural Networks for Solving Multi-asset Option Pricing Problems → http://arxiv.org/abs/2601.12704v1
- [arXiv] KANHedge: Efficient Hedging of High-Dimensional Options Using Kolmogorov-Arnold Network-Based BSDE Solver → http://arxiv.org/abs/2601.11097v1

**🎨 多模态融合**：
- [AAAI] An Approach Towards Developing Relationally Intelligent Multimodal Framework for Stock Movement Prediction (Student Abstract) → https://ojs.aaai.org/index.php/AAAI/article/view/42266
- [arXiv] Investing Is Compression → http://arxiv.org/abs/2604.10758v3
- [arXiv] COTTA: Context-Aware Transfer Adaptation for Trajectory Prediction in Autonomous Driving → http://arxiv.org/abs/2604.00402v1
- [arXiv] Caratheodory II: The Geometry of Financial Irreversibility → http://arxiv.org/abs/2603.09966v1
- [arXiv] Is an investor stolen their profits by mimic investors? Investigated by an agent-based model → http://arxiv.org/abs/2603.03671v1
- [arXiv] Trading in CEXs and DEXs with Priority Fees and Stochastic Delays → http://arxiv.org/abs/2602.10798v2

**📈 时序模型(LSTM/RNN)**：
- [arXiv] Identifying dynamical network markers of financial market instability → http://arxiv.org/abs/2604.21297v1
- [arXiv] Forecasting the Evolving Composition of Inbound Tourism Demand: A Bayesian Compositional Time Series Approach Using Platform Booking Data → http://arxiv.org/abs/2602.18358v3
- [arXiv] Brownian ReLU(Br-ReLU): A New Activation Function for a Long-Short Term Memory (LSTM) Network → http://arxiv.org/abs/2601.16446v1
- [arXiv] Trend-Adjusted Time Series Models with an Application to Gold Price Forecasting → http://arxiv.org/abs/2601.12706v2
- [arXiv] Quantum Classical Ridgelet Neural Network For Time Series Model → http://arxiv.org/abs/2601.03654v1
- [arXiv] DCD: Decomposition-based Causal Discovery from Autocorrelated and Non-Stationary Temporal Data → http://arxiv.org/abs/2602.01433v1

**🔍 因子挖掘/Alpha 发现**：
- [arXiv] Understanding the Long-Only Minimum Variance Portfolio → http://arxiv.org/abs/2603.07692v1
- [arXiv] FactorMiner: A Self-Evolving Agent with Skills and Experience Memory for Financial Alpha Discovery → http://arxiv.org/abs/2602.14670v1
- [arXiv] QuantaAlpha: An Evolutionary Framework for LLM-Driven Alpha Mining → http://arxiv.org/abs/2602.07085v2
- [arXiv] Alpha Discovery via Grammar-Guided Learning and Search → http://arxiv.org/abs/2601.22119v1
- [arXiv] AlphaPROBE: Alpha Mining via Principled Retrieval and On-graph biased evolution → http://arxiv.org/abs/2602.11917v1

**₿ 加密货币/区块链**：
- [arXiv] Anomaly prediction in XRP price with topological features → http://arxiv.org/abs/2603.18021v2
- [arXiv] Market Inefficiency in Cryptoasset Markets → http://arxiv.org/abs/2602.20771v2
- [arXiv] Predicting the success of new crypto-tokens: the Pump.fun case → http://arxiv.org/abs/2602.14860v1
- [arXiv] Do Whitepaper Claims Predict Market Behavior? Evidence from Cryptocurrency Factor Analysis → http://arxiv.org/abs/2601.20336v4

**💡 可解释性**：
- [arXiv] Beyond Prompting: An Autonomous Framework for Systematic Factor Investing via Agentic AI → http://arxiv.org/abs/2603.14288v2
- [arXiv] Stochastic Discount Factors with Cross-Asset Spillovers → http://arxiv.org/abs/2602.20856v1

**📰 新闻/社媒情绪**：
- [arXiv] Stock Market Prediction Using Node Transformer Architecture Integrated with BERT Sentiment Analysis → http://arxiv.org/abs/2603.05917v2
- [arXiv] Beyond the Numbers: Causal Effects of Financial Report Sentiment on Bank Profitability → http://arxiv.org/abs/2602.17851v1

**🕸 图神经网络/股票关系**：
- [arXiv] Forecasting Equity Correlations with Hybrid Transformer Graph Neural Network → http://arxiv.org/abs/2601.04602v1
- [OpenReview] A Dynamic-Causal Lens of Stock Interactions: Graph Modeling From Symbolic Movement Patterns → https://openreview.net/forum?id=JSEhNQIpr6

**📑 财报/披露文本分析**：
- [arXiv] Global Persistence, Local Residual Structure: Forecasting Heterogeneous Investment Panels → http://arxiv.org/abs/2604.09821v1

**🎲 生成模型/合成数据**：
- [arXiv] Prediction Arena: Benchmarking AI Models on Real-World Prediction Markets → http://arxiv.org/abs/2604.07355v1

### 2025 (515 篇)

**🤖 LLM/Agent 金融应用**：
- [arXiv] PriceSeer: Evaluating Large Language Models in Real-Time Stock Prediction → http://arxiv.org/abs/2601.06088v1
- [arXiv] A Test of Lookahead Bias in LLM Forecasts → http://arxiv.org/abs/2512.23847v1
- [arXiv] Alpha-R1: Alpha Screening with LLM Reasoning via Reinforcement Learning → http://arxiv.org/abs/2512.23515v1
- [arXiv] Quantitative Financial Modeling for Sri Lankan Markets: Approach Combining NLP, Clustering and Time-Series Forecasting → http://arxiv.org/abs/2512.20216v1
- [arXiv] Adaptive Financial Sentiment Analysis for NIFTY 50 via Instruction-Tuned LLMs , RAG and Reinforcement Learning Approaches → http://arxiv.org/abs/2512.20082v2
- [arXiv] Financial News Summarization: Can extractive methods still offer a true alternative to LLMs? → http://arxiv.org/abs/2512.08764v1
- [arXiv] Unveiling Hedge Funds: Topic Modeling and Sentiment Correlation with Fund Performance → http://arxiv.org/abs/2512.06620v1
- [arXiv] Fine-tuning of lightweight large language models for sentiment classification on heterogeneous financial textual data → http://arxiv.org/abs/2512.00946v1
- [arXiv] Financial Text Classification Based On rLoRA Finetuning On Qwen3-8B model → http://arxiv.org/abs/2512.00630v1
- [arXiv] Re(Visiting) Time Series Foundation Models in Finance → http://arxiv.org/abs/2511.18578v1
- [arXiv] MoMoE: A Mixture of Expert Agent Model for Financial Sentiment Analysis → http://arxiv.org/abs/2511.13983v1
- [arXiv] GroupSHAP-Guided Integration of Financial News Keywords and Technical Indicators for Stock Price Prediction → http://arxiv.org/abs/2510.23112v3
- [arXiv] News-Aware Direct Reinforcement Trading for Financial Markets → http://arxiv.org/abs/2510.19173v1
- [arXiv] BondBERT: What we learn when assigning sentiment in the bond market → http://arxiv.org/abs/2511.01869v2
- [arXiv] Exploring the Synergy of Quantitative Factors and Newsflow Representations from Large Language Models for Stock Return Prediction → http://arxiv.org/abs/2510.15691v3
- [arXiv] Integrating Large Language Models and Reinforcement Learning for Sentiment-Driven Quantitative Trading → http://arxiv.org/abs/2510.10526v1
- [arXiv] Predicting Stock Price Movement with LLM-Enhanced Tweet Emotion Analysis → http://arxiv.org/abs/2510.03633v1
- [arXiv] Extracting the Structure of Press Releases for Predicting Earnings Announcement Returns → http://arxiv.org/abs/2509.24254v2
- [arXiv] GRAB: A Risk Taxonomy--Grounded Benchmark for Unsupervised Topic Discovery in Financial Disclosures → http://arxiv.org/abs/2509.21698v1
- [arXiv] DeltaHedge: A Multi-Agent Framework for Portfolio Options Optimization → http://arxiv.org/abs/2509.12753v1
- [arXiv] FinSentLLM: Multi-LLM and Structured Semantic Signals for Enhanced Financial Sentiment Forecasting → http://arxiv.org/abs/2509.12638v1
- [arXiv] Analogy-Driven Financial Chain-of-Thought (AD-FCoT): A Prompting Approach for Financial Sentiment Analysis → http://arxiv.org/abs/2509.12611v1
- [arXiv] Trading-R1: Financial Trading with LLM Reasoning via Reinforcement Learning → http://arxiv.org/abs/2509.11420v1
- [arXiv] Mamba Outpaces Reformer in Stock Prediction with Sentiments from Top Ten LLMs → http://arxiv.org/abs/2510.01203v1
- [arXiv] When FinTech Meets Privacy: Securing Financial LLMs with Differential Private Fine-Tuning → http://arxiv.org/abs/2509.08995v1
- [arXiv] A Role-Aware Multi-Agent Framework for Financial Education Question Answering with LLMs → http://arxiv.org/abs/2509.09727v1
- [arXiv] Methodological Insights into Structural Causal Modelling and Uncertainty-Aware Forecasting for Economic Indicators → http://arxiv.org/abs/2509.07036v2
- [arXiv] Can News Predict the Direction of Oil Price Volatility? A Language Model Approach with SHAP Explanations → http://arxiv.org/abs/2508.20707v1
- [arXiv] TULIP: Adapting Open-Source Large Language Models for Underrepresented Languages and Specialized Financial Tasks → http://arxiv.org/abs/2508.16243v1
- [arXiv] RicciFlowRec: A Geometric Root Cause Recommender Using Ricci Curvature on Financial Graphs → http://arxiv.org/abs/2508.09334v1
- *(+100 篇省略)*

**🎯 强化学习交易**：
- [AAAI] Logic-Q: Improving Deep Reinforcement Learning-based Quantitative Trading via Program Sketch-based Tuning → https://ojs.aaai.org/index.php/AAAI/article/view/34045
- [AAAI] Augmented Lagrangian Risk-constrained Reinforcement Learning for Portfolio Optimization (Student Abstract) → https://ojs.aaai.org/index.php/AAAI/article/view/35252
- [AAAI] AlphaForge: A Framework to Mine and Dynamically Combine Formulaic Alpha Factors → https://ojs.aaai.org/index.php/AAAI/article/view/33365
- [AAAI] Dynamic Graph Learning with Static Relations for Credit Risk Assessment → https://ojs.aaai.org/index.php/AAAI/article/view/33433
- [arXiv] Integrated Prediction and Multi-period Portfolio Optimization → http://arxiv.org/abs/2512.11273v2
- [arXiv] The Red Queen's Trap: Limits of Deep Evolution in High-Frequency Trading → http://arxiv.org/abs/2512.15732v1
- [arXiv] Multi-Modal Opinion Integration for Financial Sentiment Analysis using Cross-Modal Attention → http://arxiv.org/abs/2512.03464v1
- [arXiv] Reinforcement Learning for Portfolio Optimization with a Financial Goal and Defined Time Horizons → http://arxiv.org/abs/2511.18076v1
- [arXiv] Hybrid LSTM and PPO Networks for Dynamic Portfolio Optimization → http://arxiv.org/abs/2511.17963v1
- [arXiv] Reinforcement Learning in Queue-Reactive Models: Application to Optimal Execution → http://arxiv.org/abs/2511.15262v1
- [arXiv] A FEDformer-Based Hybrid Framework for Anomaly Detection and Risk Forecasting in Financial Time Series → http://arxiv.org/abs/2511.12951v1
- [arXiv] Cryptocurrency Portfolio Management with Reinforcement Learning: Soft Actor--Critic and Deep Deterministic Policy Gradient Algorithms → http://arxiv.org/abs/2511.20678v1
- [arXiv] A Hybrid Deep Learning based Carbon Price Forecasting Framework with Structural Breakpoints Detection and Signal Denoising → http://arxiv.org/abs/2511.04988v2
- [arXiv] When AI Trading Agents Compete: Adverse Selection of Meta-Orders by Reinforcement Learning-Based Market Making → http://arxiv.org/abs/2510.27334v1
- [arXiv] RL-Exec: Impact-Aware Reinforcement Learning for Opportunistic Optimal Liquidation, Outperforms TWAP and a Book-Liquidity VWAP on BTC-USD Re → http://arxiv.org/abs/2511.07434v1
- [arXiv] Right Place, Right Time: Market Simulation-based RL for Execution Optimisation → http://arxiv.org/abs/2510.22206v1
- [arXiv] Diffusion-Augmented Reinforcement Learning for Robust Portfolio Optimization under Stress Scenarios → http://arxiv.org/abs/2510.07099v1
- [arXiv] Tail-Safe Hedging: Explainable Risk-Sensitive Reinforcement Learning with a White-Box CBF--QP Safety Layer in Arbitrage-Free Markets → http://arxiv.org/abs/2510.04555v1
- [arXiv] FR-LUX: Friction-Aware, Regime-Conditioned Policy Optimization for Implementable Portfolio Management → http://arxiv.org/abs/2510.02986v1
- [arXiv] Conditional Risk Minimization with Side Information: A Tractable, Universal Optimal Transport Framework → http://arxiv.org/abs/2509.23128v1
- [arXiv] Dynamic Lagging for Time-Series Forecasting in E-Commerce Finance: Mitigating Information Loss with A Hybrid ML Architecture → http://arxiv.org/abs/2509.20244v1
- [arXiv] Meta-Learning Reinforcement Learning for Crypto-Return Prediction → http://arxiv.org/abs/2509.09751v2
- [arXiv] Quantum-Enhanced Forecasting for Deep Reinforcement Learning in Algorithmic Trading → http://arxiv.org/abs/2509.09176v2
- [arXiv] Nested Optimal Transport Distances → http://arxiv.org/abs/2509.06702v1
- [arXiv] FinXplore: An Adaptive Deep Reinforcement Learning Framework for Balancing and Discovering Investment Opportunities → http://arxiv.org/abs/2509.10531v1
- [arXiv] FinFlowRL: An Imitation-Reinforcement Learning Framework for Adaptive Stochastic Control in Finance → http://arxiv.org/abs/2510.15883v1
- [arXiv] QTMRL: An Agent for Quantitative Trading Decision-Making Based on Multi-Indicator Guided Reinforcement Learning → http://arxiv.org/abs/2508.20467v2
- [arXiv] Comparing Normalization Methods for Portfolio Optimization with Reinforcement Learning → http://arxiv.org/abs/2508.03910v1
- [arXiv] CTBench: Cryptocurrency Time Series Generation Benchmark → http://arxiv.org/abs/2508.02758v1
- [arXiv] Learning from Expert Factors: Trajectory-level Reward Shaping for Formulaic Alpha Mining → http://arxiv.org/abs/2507.20263v1
- *(+86 篇省略)*

**📊 波动率预测**：
- [arXiv] Synthetic Financial Data Generation for Enhanced Financial Modelling → http://arxiv.org/abs/2512.21791v1
- [arXiv] Covariance-Aware Simplex Projection for Cardinality-Constrained Portfolio Optimization → http://arxiv.org/abs/2512.19986v1
- [arXiv] Stochastic Volatility Modelling with LSTM Networks: A Hybrid Approach for S&P 500 Index Volatility Forecasting → http://arxiv.org/abs/2512.12250v1
- [arXiv] Weak Relation Enforcement for Kinematic-Informed Long-Term Stock Prediction with Artificial Neural Networks → http://arxiv.org/abs/2511.10494v1
- [arXiv] Data-Efficient Realized Volatility Forecasting with Vision Transformers → http://arxiv.org/abs/2511.03046v1
- [arXiv] ProteuS: A Generative Approach for Simulating Concept Drift in Financial Markets → http://arxiv.org/abs/2509.11844v1
- [arXiv] The Sound of Risk: A Multimodal Physics-Informed Acoustic Model for Forecasting Market Volatility and Enhancing Market Interpretability → http://arxiv.org/abs/2508.18653v1
- [arXiv] RegimeNAS: Regime-Aware Differentiable Architecture Search With Theoretical Guarantees for Financial Trading → http://arxiv.org/abs/2508.11338v1
- [arXiv] A diffusion-based generative model for financial time series via geometric Brownian motion → http://arxiv.org/abs/2507.19003v1
- [arXiv] Time Series Foundation Models for Multivariate Financial Time Series Forecasting → http://arxiv.org/abs/2507.07296v1
- [arXiv] Deep Learning Enhanced Multi-Day Turnover Quantitative Trading Algorithm for Chinese A-Share Market → http://arxiv.org/abs/2506.06356v1
- [arXiv] Modeling Regime Structure and Informational Drivers of Stock Market Volatility via the Financial Chaos Index → http://arxiv.org/abs/2504.18958v1
- [arXiv] Adapting to the Unknown: Robust Meta-Learning for Zero-Shot Financial Time Series Forecasting → http://arxiv.org/abs/2504.09664v2
- [arXiv] Forecasting VIX using interpretable Kolmogorov-Arnold networks → http://arxiv.org/abs/2502.00980v1
- [arXiv] Forecasting S&P 500 Using LSTM Models → http://arxiv.org/abs/2501.17366v1
- [arXiv] CryptoMamba: Leveraging State Space Models for Accurate Bitcoin Price Prediction → http://arxiv.org/abs/2501.01010v2
- [arXiv] Towards a fast and robust deep hedging approach → http://arxiv.org/abs/2504.16436v1
- [arXiv] CoFinDiff: Controllable Financial Diffusion Model for Time Series Generation → http://arxiv.org/abs/2503.04164v1
- [arXiv] Stochastic factors can matter: improving robust growth under ergodicity → http://arxiv.org/abs/2512.24906v1
- [arXiv] Time-Varying Factor-Augmented Models for Volatility Forecasting → http://arxiv.org/abs/2508.01880v3
- [arXiv] DeepSVM: Learning Stochastic Volatility Models with Physics-Informed Deep Operator Networks → http://arxiv.org/abs/2512.07162v1
- [arXiv] Deep Learning-Enhanced Calibration of the Heston Model: A Unified Framework → http://arxiv.org/abs/2510.24074v2
- [arXiv] Towards Fast Option Pricing PDE Solvers Powered by PIELM → http://arxiv.org/abs/2510.04322v1
- [arXiv] Applying Informer for Option Pricing: A Transformer-Based Approach → http://arxiv.org/abs/2506.05565v1
- [arXiv] Mathematical Modeling of Option Pricing with an Extended Black-Scholes Framework → http://arxiv.org/abs/2504.03175v2
- [arXiv] Bayesian Modeling for Uncertainty Management in Financial Risk Forecasting and Compliance → http://arxiv.org/abs/2512.15739v1
- [arXiv] Macroeconomic Forecasting for the G7 countries under Uncertainty Shocks → http://arxiv.org/abs/2510.23347v1
- [arXiv] Extending the application of dynamic Bayesian networks in calculating market risk: Standard and stressed expected shortfall → http://arxiv.org/abs/2512.12334v1
- [arXiv] Valuation of Exotic Options and Counterparty Games Based on Conditional Diffusion → http://arxiv.org/abs/2509.13374v1
- [arXiv] Advancing Exchange Rate Forecasting: Leveraging Machine Learning and AI for Enhanced Accuracy in Global Financial Markets → http://arxiv.org/abs/2506.09851v2
- *(+14 篇省略)*

**🌐 其他金融 AI**：
- [AAAI] Decentralized Convergence to Equilibrium Prices in Trading Networks → https://ojs.aaai.org/index.php/AAAI/article/view/33532
- [AAAI] Langevin Multiplicative Weights Update with Applications in Polynomial Portfolio Management → https://ojs.aaai.org/index.php/AAAI/article/view/33220
- [AAAI] Constrained Offline Black-Box Optimization via Risk Evaluation and Management → https://ojs.aaai.org/index.php/AAAI/article/view/34470
- [arXiv] "It Looks All the Same to Me": Cross-index Training for Long-term Financial Series Prediction → http://arxiv.org/abs/2511.08658v1
- [arXiv] A Mathematical Theory of Top-$k$ Sparse Attention via Total Variation Distance → http://arxiv.org/abs/2512.07647v1
- [arXiv] Variational Polya Tree → http://arxiv.org/abs/2510.22651v1
- [arXiv] A Mixed-Methods Analysis of Repression and Mobilization in Bangladesh's July Revolution Using Machine Learning and Statistical Modeling → http://arxiv.org/abs/2510.06264v1
- [arXiv] VAR-MATH: Probing True Mathematical Reasoning in LLMS via Symbolic Multi-Instance Benchmarks → http://arxiv.org/abs/2507.12885v3
- [arXiv] Privacy Attacks on Image AutoRegressive Models → http://arxiv.org/abs/2502.02514v5
- [arXiv] Unified Royer law revision for alpha-decay half-lives: shell corrections, pairing,and orbital-angular-momentum → http://arxiv.org/abs/2512.22057v1
- [arXiv] Enhancement of Alpha Decay due to Medium Effects → http://arxiv.org/abs/2510.22194v1
- [arXiv] Nonlocality Effect in the Tunneling of Alpha Radioactivity with the Aid of Machine Learning → http://arxiv.org/abs/2510.18199v2
- [arXiv] Role of universal function of the nuclear proximity potential: A systematic study on the alpha-decay of heavy/super-heavy nuclei and α-induc → http://arxiv.org/abs/2510.02764v1
- [arXiv] The nuclear surface diffuseness effects on the alpha decay of heavy and super heavy nuclei → http://arxiv.org/abs/2509.01343v1
- [arXiv] Flow-dependent tagging of $^{214}$Pb decays in the LZ dark matter detector → http://arxiv.org/abs/2508.19117v1
- [arXiv] Deformed magic numbers at $N=$178 and $Z=$120, 124 in the 112 $\leq N \leq $ 190 superheavy region from Skyrme mean-field calculations → http://arxiv.org/abs/2506.02684v1
- [arXiv] The candidates of 2$α$ condensate around the 16O nucleus studied by the real-time evolution method → http://arxiv.org/abs/2505.04975v1
- [arXiv] Systematic calculation on alpha decay and cluster radioactivity of superheavy nuclei → http://arxiv.org/abs/2503.10987v1
- [arXiv] The disclosure of information about the range of asset value in market → http://arxiv.org/abs/2511.11405v2
- [arXiv] Regulation or Competition:Major-Minor Optimal Liquidation across Dark and Lit Pools → http://arxiv.org/abs/2509.03916v1
- [arXiv] The asymmetrical Acquisition of information about the range of asset value in market → http://arxiv.org/abs/2508.09615v1
- [arXiv] Position building in competition is a game with incomplete information → http://arxiv.org/abs/2501.01241v2
- [arXiv] Entrepreneurial Motivations and ESG Performance Evidence from Automobile Companies Listed on the Chinese Stock Exchange → http://arxiv.org/abs/2503.21828v1
- [arXiv] WallStreetFeds: Client-Specific Tokens as Investment Vehicles in Federated Learning → http://arxiv.org/abs/2506.20518v1
- [arXiv] Low-Order Flow Reconstruction and Uncertainty Quantification in Disturbed Aerodynamics Using Sparse Pressure Measurements → http://arxiv.org/abs/2501.03406v1
- [arXiv] Sparse Latent Factor Forecaster (SLFF) with Iterative Inference for Transparent Multi-Horizon Commodity Futures Prediction → http://arxiv.org/abs/2505.06795v5
- [arXiv] The Challenger: When Do New Data Sources Justify Switching Machine Learning Models? → http://arxiv.org/abs/2512.18390v1
- [arXiv] Tests of Evolving Dark Energy with Geometric Probes of the Late-Time Universe → http://arxiv.org/abs/2509.26480v2
- [arXiv] Detecting Statistically Significant Fairness Violations in Recidivism Forecasting Algorithms → http://arxiv.org/abs/2511.11575v1
- [arXiv] PanelMatch: Matching Methods for Causal Inference with Time-Series Cross-Section Data → http://arxiv.org/abs/2503.02073v2
- *(+8 篇省略)*

**📈 时序模型(LSTM/RNN)**：
- [arXiv] Times2D: Multi-Period Decomposition and Derivative Mapping for General Time Series Forecasting → http://arxiv.org/abs/2504.00118v1
- [AAAI] Transfer Learning in Financial Time Series with Gramian Angular Field (Student Abstract) → https://ojs.aaai.org/index.php/AAAI/article/view/35272
- [arXiv] Orchestration Framework for Financial Agents: From Algorithmic Trading to Agentic Trading → http://arxiv.org/abs/2512.02227v1
- [arXiv] Towards Causal Market Simulators → http://arxiv.org/abs/2511.04469v4
- [arXiv] Fiaingen: A financial time series generative method matching real-world data quality → http://arxiv.org/abs/2510.01169v2
- [arXiv] Scaling Law for Large-Scale Pre-Training Using Chaotic Time Series and Predictability in Financial Time Series → http://arxiv.org/abs/2509.04921v1
- [arXiv] Diffusion Generative Models Meet Compressed Sensing, with Applications to Imaging and Finance → http://arxiv.org/abs/2509.03898v2
- [arXiv] FinCast: A Foundation Model for Financial Time-Series Forecasting → http://arxiv.org/abs/2508.19609v1
- [arXiv] Deep Learning-Based Financial Time Series Forecasting via Sliding Window and Variational Mode Decomposition → http://arxiv.org/abs/2508.12565v2
- [arXiv] Forecasting Nigerian Equity Stock Returns Using Long Short-Term Memory Technique → http://arxiv.org/abs/2507.01964v1
- [arXiv] On Multivariate Financial Time Series Classification → http://arxiv.org/abs/2504.17664v2
- [arXiv] HQNN-FSP: A Hybrid Classical-Quantum Neural Network for Regression-Based Financial Stock Market Prediction → http://arxiv.org/abs/2503.15403v1
- [arXiv] FinTSB: A Comprehensive and Practical Benchmark for Financial Time Series Forecasting → http://arxiv.org/abs/2502.18834v1
- [arXiv] Analysis of Contagion in China's Stock Market: A Hawkes Process Perspective → http://arxiv.org/abs/2512.08000v1
- [arXiv] Tensor dynamic conditional correlation model: A new way to pursuit "Holy Grail of investing" → http://arxiv.org/abs/2502.13461v1
- [arXiv] Machine Learning vs. Randomness: Challenges in Predicting Binary Options Movements → http://arxiv.org/abs/2511.15960v1
- [arXiv] Ada-MoGE: Adaptive Mixture of Gaussian Expert Model for Time Series Forecasting → http://arxiv.org/abs/2512.02061v1
- [arXiv] DeltaLag: Learning Dynamic Lead-Lag Patterns in Financial Markets → http://arxiv.org/abs/2511.00390v1
- [arXiv] Ensembled Direct Multi-Step forecasting methodology with comparison on macroeconomic and financial data → http://arxiv.org/abs/2509.13945v2
- [arXiv] Enhancing Forecasting with a 2D Time Series Approach for Cohort-Based Data → http://arxiv.org/abs/2508.15369v1
- [arXiv] Towards Measuring and Modeling Geometric Structures in Time Series Forecasting via Image Modality → http://arxiv.org/abs/2507.23253v1
- [arXiv] Timing is Important: Risk-aware Fund Allocation based on Time-Series Forecasting → http://arxiv.org/abs/2505.24835v3
- [arXiv] An Open-Source and Reproducible Implementation of LSTM and GRU Networks for Time Series Forecasting → http://arxiv.org/abs/2504.18185v1
- [arXiv] The Economic Impact of DeFi Crime Events on Decentralized Autonomous Organizations (DAOs) → http://arxiv.org/abs/2510.00669v1
- [arXiv] ReTimeCausal: EM-Augmented Additive Noise Models for Interpretable Causal Discovery in Irregular Time Series → http://arxiv.org/abs/2507.03310v1
- [arXiv] An Attention-based Feature Memory Design for Energy-Efficient Continual Learning → http://arxiv.org/abs/2510.04660v2

**💼 组合优化/资产配置**：
- [arXiv] Rough Path Signatures: Learning Neural RDEs for Portfolio Optimization → http://arxiv.org/abs/2510.10728v3
- [arXiv] Bayesian Portfolio Optimization by Predictive Synthesis → http://arxiv.org/abs/2510.07180v1
- [arXiv] Toward Quantum Utility in Finance: A Robust Data-Driven Algorithm for Asset Clustering → http://arxiv.org/abs/2509.07766v2
- [arXiv] Finance-Grounded Optimization For Algorithmic Trading → http://arxiv.org/abs/2509.04541v2
- [arXiv] Adaptive Multi-task Learning for Multi-sector Portfolio Optimization → http://arxiv.org/abs/2507.16433v2
- [arXiv] Kernel Learning for Mean-Variance Trading Strategies → http://arxiv.org/abs/2507.10701v1
- [arXiv] Beating the Best Constant Rebalancing Portfolio in Long-Term Investment: A Generalization of the Kelly Criterion and Universal Learning Algo → http://arxiv.org/abs/2507.05994v1
- [arXiv] skfolio: Portfolio Optimization in Python → http://arxiv.org/abs/2507.04176v2
- [arXiv] A Scalable Gradient-Based Optimization Framework for Sparse Minimum-Variance Portfolio Selection → http://arxiv.org/abs/2505.10099v1
- [arXiv] Latent Variable Estimation in Bayesian Black-Litterman Models → http://arxiv.org/abs/2505.02185v1
- [arXiv] Diffusion Factor Models: Generating High-Dimensional Returns with Factor Structure → http://arxiv.org/abs/2504.06566v5
- [arXiv] Why risk matters for protein binder design → http://arxiv.org/abs/2504.00146v2
- [arXiv] A Framework for Finding Local Saddle Points in Two-Player Zero-Sum Black-Box Games → http://arxiv.org/abs/2503.18224v1
- [arXiv] Decision by Supervised Learning with Deep Ensembles: A Practical Framework for Robust Portfolio Optimization → http://arxiv.org/abs/2503.13544v7
- [arXiv] Optimization Method of Multi-factor Investment Model Driven by Deep Learning for Risk Control → http://arxiv.org/abs/2507.00332v1
- [arXiv] Basis Immunity: Isotropy as a Regularizer for Uncertainty → http://arxiv.org/abs/2511.13334v1
- [arXiv] Deep Declarative Risk Budgeting Portfolios → http://arxiv.org/abs/2504.19980v1
- [arXiv] Hierarchical Minimum Variance Portfolios: A Theoretical and Algorithmic Approach → http://arxiv.org/abs/2503.12328v1
- [arXiv] Diffolio: A Diffusion Model for Multivariate Probabilistic Financial Time-Series Forecasting and Portfolio Construction → http://arxiv.org/abs/2511.07014v2
- [arXiv] Dependency Network-Based Portfolio Design with Forecasting and VaR Constraints → http://arxiv.org/abs/2507.20039v1
- [arXiv] Boltzmann convolutions and Welford mean-variance layers with an application to time series forecasting and classification → http://arxiv.org/abs/2503.04956v1
- [OpenReview] Comparing Transformer Models for Stock Selection in Quantitative Trading → https://openreview.net/forum?id=wRMZNkW8gL
- [OpenReview] Factor-Based Conditional Diffusion Model for Portfolio Optimization → https://openreview.net/forum?id=v8EGREhyLF

**⚡ 订单簿/HFT/微观结构**：
- [arXiv] RefineBridge: Generative Bridge Models Improve Financial Forecasting by Foundation Models → http://arxiv.org/abs/2512.21572v2
- [arXiv] KANFormer for Predicting Fill Probabilities via Survival Analysis in Limit Order Books → http://arxiv.org/abs/2512.05734v1
- [arXiv] Detecting Multilevel Manipulation from Limit Order Book via Cascaded Contrastive Representation Learning → http://arxiv.org/abs/2508.17086v2
- [arXiv] DiffVolume: Diffusion Models for Volume Generation in Limit Order Books → http://arxiv.org/abs/2508.08698v1
- [arXiv] ByteGen: A Tokenizer-Free Generative Model for Orderbook Events in Byte Space → http://arxiv.org/abs/2508.02247v2
- [arXiv] A Comparative Analysis of Statistical and Machine Learning Models for Outlier Detection in Bitcoin Limit Order Books → http://arxiv.org/abs/2507.14960v1
- [arXiv] HAELT: A Hybrid Attentive Ensemble Learning Transformer Framework for High-Frequency Stock Price Forecasting → http://arxiv.org/abs/2506.13981v1
- [arXiv] Exploring Microstructural Dynamics in Cryptocurrency Limit Order Books: Better Inputs Matter More Than Stacking Another Hidden Layer → http://arxiv.org/abs/2506.05764v2
- [arXiv] TIP-Search: Time-Predictable Inference Scheduling for Market Prediction under Uncertain Load → http://arxiv.org/abs/2506.08026v2
- [arXiv] An Efficient deep learning model to Predict Stock Price Movement Based on Limit Order Book → http://arxiv.org/abs/2505.22678v1
- [arXiv] Trading Under Uncertainty: A Distribution-Based Strategy for Futures Markets Using FutureQuant Transformer → http://arxiv.org/abs/2505.05595v1
- [arXiv] Deep Learning Models Meet Financial Data Modalities → http://arxiv.org/abs/2504.13521v2
- [arXiv] TRADES: Generating Realistic Market Simulations with Diffusion Models → http://arxiv.org/abs/2502.07071v3
- [arXiv] Optimal Signal Extraction from Order Flow: A Matched Filter Perspective on Normalization and Market Microstructure → http://arxiv.org/abs/2512.18648v3
- [arXiv] AutoQuant: An Auditable Expert-System Framework for Execution-Constrained Auto-Tuning in Cryptocurrency Perpetual Futures → http://arxiv.org/abs/2512.22476v1
- [arXiv] Option market making with hedging-induced market impact → http://arxiv.org/abs/2511.02518v1
- [arXiv] Optimal Execution under Liquidity Uncertainty → http://arxiv.org/abs/2506.11813v2
- [arXiv] BEAT: Balanced Frequency Adaptive Tuning for Long-Term Time-Series Forecasting → http://arxiv.org/abs/2501.19065v2
- [arXiv] Meta-Learning the Optimal Mixture of Strategies for Online Portfolio Selection → http://arxiv.org/abs/2505.03659v2
- [OpenReview] LOBERT: Generative AI Foundation Model for Limit Order Book Messages → https://openreview.net/forum?id=2nDHY6gAlp
- [OpenReview] Prospects of Imitating Trading Agents in the Stock Market → https://openreview.net/forum?id=pk8w9VMUjg
- [OpenReview] LOBBen-TM: A Benchmark Study of Limit Order Book Prediction with Temporal Modeling → https://openreview.net/forum?id=CYT5zrOfK5

**🔄 Transformer 时序**：
- [AAAI] DHMoE: Diffusion Generated Hierarchical Multi-Granular Expertise for Stock Prediction → https://ojs.aaai.org/index.php/AAAI/article/view/33250
- [arXiv] Smart Timing for Mining: A Deep Learning Framework for Bitcoin Hardware ROI Prediction → http://arxiv.org/abs/2512.05402v1
- [arXiv] Multi-period Learning for Financial Time Series Forecasting → http://arxiv.org/abs/2511.08622v2
- [arXiv] On Evaluating Loss Functions for Stock Ranking: An Empirical Analysis With Transformer Model → http://arxiv.org/abs/2510.14156v1
- [arXiv] Quantum Adaptive Self-Attention for Financial Rebalancing: An Empirical Study on Automated Market Makers in Decentralized Finance → http://arxiv.org/abs/2509.16955v1
- [arXiv] Increase Alpha: Performance and Risk of an AI-Driven Trading Framework → http://arxiv.org/abs/2509.16707v2
- [arXiv] time2time: Causal Intervention in Hidden States to Simulate Rare Events in Time Series Foundation Models → http://arxiv.org/abs/2509.05801v2
- [arXiv] Alternative Loss Function in Evaluation of Transformer Models → http://arxiv.org/abs/2507.16548v2
- [arXiv] Transformer Encoder and Multi-features Time2Vec for Financial Prediction → http://arxiv.org/abs/2504.13801v2
- [arXiv] An Advanced Ensemble Deep Learning Framework for Stock Price Prediction Using VAE, Transformer, and LSTM Model → http://arxiv.org/abs/2503.22192v1
- [arXiv] Solving Optimal Execution Problems via In-Context Operator Networks → http://arxiv.org/abs/2501.15106v2
- [arXiv] Quantum and Classical Machine Learning in Decentralized Finance: Comparative Evidence from Multi-Asset Backtesting of Automated Market Maker → http://arxiv.org/abs/2510.15903v1
- [arXiv] Hydra: Dual Exponentiated Memory for Multivariate Time Series Analysis → http://arxiv.org/abs/2511.00989v1
- [arXiv] Abstain Mask Retain Core: Time Series Prediction by Adaptive Masking Loss with Representation Consistency → http://arxiv.org/abs/2510.19980v1
- [arXiv] WDformer: A Wavelet-based Differential Transformer Model for Time Series Forecasting → http://arxiv.org/abs/2509.25231v1
- [arXiv] Bridging Short- and Long-Term Dependencies: A CNN-Transformer Hybrid for Financial Time Series Forecasting → http://arxiv.org/abs/2504.19309v1
- [arXiv] A Novel Hybrid Approach Using an Attention-Based Transformer + GRU Model for Predicting Cryptocurrency Prices → http://arxiv.org/abs/2504.17079v2
- [arXiv] Automatic selection of the best neural architecture for time series forecasting → http://arxiv.org/abs/2501.12215v2
- [arXiv] WaveletDiff: Multilevel Wavelet Diffusion For Time Series Generation → http://arxiv.org/abs/2510.11839v2
- [arXiv] Optimizing In-Context Learning for Efficient Full Conformal Prediction → http://arxiv.org/abs/2509.01840v3

**🕸 图神经网络/股票关系**：
- [arXiv] MaGNet: A Mamba Dual-Hypergraph Network for Stock Prediction via Temporal-Causal and Global Relational Learning → http://arxiv.org/abs/2511.00085v1
- [arXiv] Crisis-Resilient Portfolio Management via Graph-based Spatio-Temporal Learning → http://arxiv.org/abs/2510.20868v1
- [arXiv] Structure Over Signal: A Globalized Approach to Multi-relational GNNs for Stock Prediction → http://arxiv.org/abs/2510.10775v1
- [arXiv] Stock Prediction via a Dual Relation Fusion Network incorporating Static and Dynamic Relations → http://arxiv.org/abs/2510.10695v1
- [arXiv] NGAT: A Node-level Graph Attention Network for Long-term Stock Prediction → http://arxiv.org/abs/2507.02018v1
- [arXiv] Trading Graph Neural Network → http://arxiv.org/abs/2504.07923v1
- [arXiv] \textsc{Perseus}: Tracing the Masterminds Behind Cryptocurrency Pump-and-Dump Schemes → http://arxiv.org/abs/2503.01686v1
- [arXiv] A Distillation-based Future-aware Graph Neural Network for Stock Trend Prediction → http://arxiv.org/abs/2502.10776v1
- [arXiv] Chinese Stock Prediction Based on a Multi-Modal Transformer Framework: Macro-Micro Information Fusion → http://arxiv.org/abs/2501.16621v1
- [arXiv] Stock Market Telepathy: Graph Neural Networks Predicting the Secret Conversations between MINT and G7 Countries → http://arxiv.org/abs/2506.01945v1
- [arXiv] Graph Learning for Foreign Exchange Rate Prediction and Statistical Arbitrage → http://arxiv.org/abs/2508.14784v1
- [arXiv] Gated Fusion Enhanced Multi-Scale Hierarchical Graph Convolutional Network for Stock Movement Prediction → http://arxiv.org/abs/2511.01570v1
- [arXiv] FinMamba: Market-Aware Graph Enhanced Multi-Level Mamba for Stock Movement Prediction → http://arxiv.org/abs/2502.06707v1
- [arXiv] DeXposure: A Dataset and Benchmarks for Inter-protocol Credit Exposure in Decentralized Financial Networks → http://arxiv.org/abs/2511.22314v1
- [arXiv] Stock Price Prediction Using a Hybrid LSTM-GNN Model: Integrating Time-Series and Graph-Based Analysis → http://arxiv.org/abs/2502.15813v1
- [arXiv] Multi-Head Spectral-Adaptive Graph Anomaly Detection → http://arxiv.org/abs/2512.22291v1
- [OpenReview] Toward the next generation of stock movement prediction: GenAI-based multimodal stock movement prediction model → https://openreview.net/forum?id=bdTkeEpoxx

**📰 新闻/社媒情绪**：
- [arXiv] Comparative Evaluation of Embedding Representations for Financial News Sentiment Analysis → http://arxiv.org/abs/2512.13749v2
- [arXiv] Diagram-to-Circuit QNLP for Financial Sentiment Analysis → http://arxiv.org/abs/2511.18804v2
- [arXiv] From News to Returns: A Granger-Causal Hypergraph Transformer on the Sphere → http://arxiv.org/abs/2510.04357v1
- [arXiv] Multimodal Proposal for an AI-Based Tool to Increase Cross-Assessment of Messages → http://arxiv.org/abs/2509.03529v1
- [arXiv] Rough kernel hedging → http://arxiv.org/abs/2501.09683v2
- [arXiv] Hybrid Quantum-Classical Ensemble Learning for S\&P 500 Directional Prediction → http://arxiv.org/abs/2512.15738v1
- [arXiv] Dynamic stacking ensemble learning with investor knowledge representations for stock market index prediction based on multi-source financial → http://arxiv.org/abs/2512.14042v1
- [arXiv] Investigating the effectiveness of multimodal data in forecasting SARS-COV-2 case surges → http://arxiv.org/abs/2505.22688v2
- [arXiv] Detecting Linguistic Diversity on Social Media → http://arxiv.org/abs/2502.21224v1
- [arXiv] HINTS: Extraction of Human Insights from Time-Series Without External Sources → http://arxiv.org/abs/2512.23755v1
- [arXiv] Advanced Stock Market Prediction Using Long Short-Term Memory Networks: A Comprehensive Deep Learning Framework → http://arxiv.org/abs/2505.05325v1
- [arXiv] Investor Sentiment and Market Movements: A Granger Causality Perspective → http://arxiv.org/abs/2510.15915v1
- [arXiv] Contrastive Similarity Learning for Market Forecasting: The ContraSim Framework → http://arxiv.org/abs/2502.16023v1
- [OpenReview] An investigation into correlations between financial sentiment and prices in financial markets → https://openreview.net/forum?id=X0YJPKhz46

**⚖ 风险/信用/欺诈**：
- [AAAI] Adaptive Merchant-Centric Risk Control via Unbiased Decision-Making and Dynamic Optimization in E-Commerce → https://ojs.aaai.org/index.php/AAAI/article/view/35142
- [arXiv] Topology of Currencies: Persistent Homology for FX Co-movements: A Comparative Clustering Study → http://arxiv.org/abs/2510.19306v1
- [arXiv] A Projection-Based ARIMA Framework for Nonlinear Dynamics in Macroeconomic and Financial Time Series: Closed-Form Estimation and Rolling-Win → http://arxiv.org/abs/2507.07469v3
- [arXiv] Transfer Learning for High-dimensional Reduced Rank Time Series Models → http://arxiv.org/abs/2504.15691v1
- [arXiv] Time-varying Factor Augmented Vector Autoregression with Grouped Sparse Autoencoder → http://arxiv.org/abs/2503.04386v1
- [arXiv] Universal Approximation of Visual Autoregressive Transformers → http://arxiv.org/abs/2502.06167v1
- [arXiv] Circuit Complexity Bounds for Visual Autoregressive Model → http://arxiv.org/abs/2501.04299v1
- [arXiv] Not All Factors Crowd Equally: Modeling, Measuring, and Trading on Alpha Decay → http://arxiv.org/abs/2512.11913v2
- [arXiv] Standard and stressed value at risk forecasting using dynamic Bayesian networks → http://arxiv.org/abs/2512.05661v1
- [arXiv] Grad: Guided Relation Diffusion Generation for Graph Augmentation in Graph Fraud Detection → http://arxiv.org/abs/2512.18133v1
- [arXiv] Rethinking Contrastive Learning in Graph Anomaly Detection: A Clean-View Perspective → http://arxiv.org/abs/2505.18002v1
- [arXiv] Early-MFC: Enhanced Flow Correlation Attacks on Tor via Multi-view Triplet Networks with Early Network Traffic → http://arxiv.org/abs/2503.16847v1

**📐 期权/衍生品**：
- [arXiv] A Topological Approach to Parameterizing Deep Hedging Networks → http://arxiv.org/abs/2510.16938v1
- [arXiv] Deep Hedging of Green PPAs in Electricity Markets → http://arxiv.org/abs/2503.13056v1
- [arXiv] The Relative Entropy of Expectation and Price → http://arxiv.org/abs/2502.08613v8
- [arXiv] Selective Forgetting in Option Calibration: An Operator-Theoretic Gauss-Newton Framework → http://arxiv.org/abs/2511.14980v1
- [arXiv] Error Propagation in Dynamic Programming: From Stochastic Control to Option Pricing → http://arxiv.org/abs/2509.20239v1
- [arXiv] Error Analysis of Deep PDE Solvers for Option Pricing → http://arxiv.org/abs/2505.05121v1
- [arXiv] Deep Learning vs. Black-Scholes: Option Pricing Performance on Brazilian Petrobras Stocks → http://arxiv.org/abs/2504.20088v1
- [arXiv] Signature approach for pricing and hedging path-dependent options with frictions → http://arxiv.org/abs/2511.23295v1
- [arXiv] Scalable Principal-Agent Contract Design via Gradient-Based Optimization → http://arxiv.org/abs/2510.21177v1
- [arXiv] Monotone tail functions: definitions, properties, and application to risk-reducing strategies → http://arxiv.org/abs/2508.12608v1
- [arXiv] ZKProphet: Understanding Performance of Zero-Knowledge Proofs on GPUs → http://arxiv.org/abs/2509.22684v1
- [arXiv] A GenAI System for Improved FAIR Independent Biological Database Integration → http://arxiv.org/abs/2506.17934v1

**🛡 对抗/鲁棒性**：
- [arXiv] Targeted Manipulation: Slope-Based Attacks on Financial Time-Series Data → http://arxiv.org/abs/2511.19330v1
- [arXiv] FinTSBridge: A New Evaluation Suite for Real-world Financial Prediction with Advanced Time Series Models → http://arxiv.org/abs/2503.06928v2
- [arXiv] Distributional Adversarial Attacks and Training in Deep Hedging → http://arxiv.org/abs/2508.14757v2
- [arXiv] Robust and Efficient Deep Hedging via Linearized Objective Neural Network → http://arxiv.org/abs/2502.17757v1
- [arXiv] Option Pricing Using Ensemble Learning → http://arxiv.org/abs/2506.05799v1
- [arXiv] Adaptive Sample-Level Framework Motivated by Distributionally Robust Optimization with Variance-Based Radius Assignment for Enhanced Neural  → http://arxiv.org/abs/2511.05568v1
- [arXiv] Non-Stationary Time Series Forecasting Based on Fourier Analysis and Cross Attention Mechanism → http://arxiv.org/abs/2505.06917v1
- [arXiv] Time-Series Forecasting via Topological Information Supervised Framework with Efficient Topological Feature Learning → http://arxiv.org/abs/2503.23757v2
- [arXiv] Robust Causal Discovery in Real-World Time Series with Power-Laws → http://arxiv.org/abs/2507.12257v3
- [arXiv] Dynamic Sparse Causal-Attention Temporal Networks for Interpretable Causality Discovery in Multivariate Time Series → http://arxiv.org/abs/2507.09439v1

**🎨 多模态融合**：
- [arXiv] Integration of LSTM Networks in Random Forest Algorithms for Stock Market Trading Predictions → http://arxiv.org/abs/2512.02036v1
- [arXiv] The Invisible Handshake: Tacit Collusion between Adaptive Market Agents → http://arxiv.org/abs/2510.15995v2
- [arXiv] How Patterns Dictate Learnability in Sequential Data → http://arxiv.org/abs/2510.10744v1
- [arXiv] CSMD: Curated Multimodal Dataset for Chinese Stock Analysis → http://arxiv.org/abs/2511.01318v1
- [arXiv] The local Gaussian correlation networks among return tails in the Chinese stock market → http://arxiv.org/abs/2510.21165v1
- [arXiv] Force Matching with Relativistic Constraints: A Physics-Inspired Approach to Stable and Efficient Generative Modeling → http://arxiv.org/abs/2502.08150v1
- [arXiv] The Meta-Learning Gap: Combining Hydra and Quant for Large-Scale Time Series Classification → http://arxiv.org/abs/2512.06666v1
- [OpenReview] FinCall-Surprise: A Large Scale Multi-modal Benchmark for Earning Surprise Prediction → https://openreview.net/forum?id=8R8qiM7CwZ

**🔍 因子挖掘/Alpha 发现**：
- [AAAI] FactorGCL: A Hypergraph-Based Factor Model with Temporal Residual Contrastive Learning for Stock Returns Prediction → https://ojs.aaai.org/index.php/AAAI/article/view/31993
- [arXiv] Feature Optimization for Time Series Forecasting via Novel Randomized Uphill Climbing → http://arxiv.org/abs/2505.03805v1
- [arXiv] Learning Universal Multi-level Market Irrationality Factors to Improve Stock Return Forecasting → http://arxiv.org/abs/2502.04737v1
- [arXiv] Multilayer Perceptron Neural Network Models in Asset Pricing: An Empirical Study on Large-Cap US Stocks → http://arxiv.org/abs/2505.01921v2
- [arXiv] Asset Pricing in Pre-trained Transformer → http://arxiv.org/abs/2505.01575v2
- [arXiv] Causal Inference in Financial Event Studies → http://arxiv.org/abs/2511.15123v1

**🌊 市场状态/Regime**：
- [arXiv] Information-Theoretic Quality Metric of Low-Dimensional Embeddings → http://arxiv.org/abs/2512.23981v2
- [arXiv] KASPER: Kolmogorov Arnold Networks for Stock Prediction and Explainable Regimes → http://arxiv.org/abs/2507.18983v1
- [arXiv] Improving Bayesian Optimization for Portfolio Management with an Adaptive Scheduling → http://arxiv.org/abs/2504.13529v3
- [arXiv] Algorithmic Aspects of Strategic Trading → http://arxiv.org/abs/2502.07606v2

**📑 财报/披露文本分析**：
- [arXiv] Agentic Retrieval of Topics and Insights from Earnings Calls → http://arxiv.org/abs/2507.07906v1
- [arXiv] MiMIC: Multi-Modal Indian Earnings Calls Dataset to Predict Stock Prices → http://arxiv.org/abs/2504.09257v1
- [arXiv] An Automated LLM-based Pipeline for Asset-Level Database Creation to Assess Deforestation Impact → http://arxiv.org/abs/2505.05494v1
- [OpenReview] Extracting key insights from earnings call transcript via information-theoretic contrastive learning → https://openreview.net/forum?id=4GmTSLbjH5

**🎲 生成模型/合成数据**：
- [arXiv] Dynamic Synthetic Controls vs. Panel-Aware Double Machine Learning for Geo-Level Marketing Impact Estimation → http://arxiv.org/abs/2508.20335v1
- [arXiv] The "double" square-root law: Evidence for the mechanical origin of market impact using Tokyo Stock Exchange data → http://arxiv.org/abs/2502.16246v2
- [arXiv] Copyright and Competition: Estimating Supply and Demand with Unstructured Data → http://arxiv.org/abs/2501.16120v2
- [arXiv] Causal Interventions in Bond Multi-Dealer-to-Client Platforms → http://arxiv.org/abs/2506.18147v2

**🧪 回测/市场模拟**：
- [arXiv] Joint Bidding on Intraday and Frequency Containment Reserve Markets → http://arxiv.org/abs/2510.03209v1
- [arXiv] A Fast and Effective Solution to the Problem of Look-ahead Bias in LLMs → http://arxiv.org/abs/2512.06607v1
- [arXiv] Data-Driven Prediction of Dynamic Interactions Between Robot Appendage and Granular Material → http://arxiv.org/abs/2506.10875v1

**₿ 加密货币/区块链**：
- [arXiv] Informer in Algorithmic Investment Strategies on High Frequency Bitcoin Data → http://arxiv.org/abs/2503.18096v1
- [arXiv] Slow is Fast! Dissecting Ethereum's Slow Liquidity Drain Scams → http://arxiv.org/abs/2503.04850v3

### 2024 (344 篇)

**🤖 LLM/Agent 金融应用**：
- [arXiv] TradingAgents: Multi-Agents LLM Financial Trading Framework → http://arxiv.org/abs/2412.20138v7
- [OpenReview] Sentiment trading with large language models → https://openreview.net/forum?id=47pcnKq9Mn
- [arXiv] SILC-EFSA: Self-aware In-context Learning Correction for Entity-level Financial Sentiment Analysis → http://arxiv.org/abs/2412.19140v1
- [arXiv] FinLoRA: Finetuning Quantized Financial Large Language Models Using Low-Rank Adaptation → http://arxiv.org/abs/2412.11378v2
- [arXiv] A Report on Financial Regulations Challenge at COLING 2025 → http://arxiv.org/abs/2412.11159v2
- [arXiv] FinGPT: Enhancing Sentiment-Based Stock Movement Prediction with Dissemination-Aware and Context-Enriched LLMs → http://arxiv.org/abs/2412.10823v2
- [arXiv] Financial Sentiment Analysis: Leveraging Actual and Synthetic Data for Supervised Fine-tuning → http://arxiv.org/abs/2412.09859v1
- [arXiv] Innovative Sentiment Analysis and Prediction of Stock Price Using FinBERT, GPT-4 and Logistic Regression: A Data-Driven Approach → http://arxiv.org/abs/2412.06837v1
- [arXiv] Thai Financial Domain Adaptation of THaLLE -- Technical Report → http://arxiv.org/abs/2411.18242v1
- [arXiv] FinRobot: AI Agent for Equity Research and Valuation with Large Language Models → http://arxiv.org/abs/2411.08804v1
- [arXiv] Optimal Execution with Reinforcement Learning → http://arxiv.org/abs/2411.06389v2
- [OpenReview] Golden Touchstone: A Comprehensive Bilingual Benchmark for Evaluating Financial Large Language Models → https://openreview.net/forum?id=85xhI902JR
- [arXiv] Enhancing Investment Analysis: Optimizing AI-Agent Collaboration in Financial Research → http://arxiv.org/abs/2411.04788v1
- [arXiv] FinBERT-BiLSTM: A Deep Learning Model for Predicting Volatile Cryptocurrency Market Prices Using Market Sentiment Dynamics → http://arxiv.org/abs/2411.12748v1
- [arXiv] Evaluating Company-specific Biases in Financial Sentiment Analysis using Large Language Models → http://arxiv.org/abs/2411.00420v1
- [arXiv] Enhancing literature review with LLM and NLP methods. Algorithmic trading case → http://arxiv.org/abs/2411.05013v1
- [OpenReview] Customized FinGPT Search Agents Using Foundation Models → https://openreview.net/forum?id=SF0RByqSRc
- [arXiv] Aligning LLMs with Human Instructions and Stock Market Feedback in Financial Sentiment Analysis → http://arxiv.org/abs/2410.14926v1
- [arXiv] FLAG: Financial Long Document Classification via AMR-based GNN → http://arxiv.org/abs/2410.02024v3
- [arXiv] Financial Sentiment Analysis on News and Reports Using Large Language Models and FinBERT → http://arxiv.org/abs/2410.01987v1
- [arXiv] Evaluating the performance of state-of-the-art esg domain-specific pre-trained large language models in text classification against existing → http://arxiv.org/abs/2410.00207v1
- [arXiv] A Multisource Fusion Framework for Cryptocurrency Price Movement Prediction → http://arxiv.org/abs/2409.18895v2
- [arXiv] Enhancing Financial Sentiment Analysis with Expert-Designed Hint → http://arxiv.org/abs/2409.17448v1
- [arXiv] SARF: Enhancing Stock Market Prediction with Sentiment-Augmented Random Forest → http://arxiv.org/abs/2410.07143v1
- [arXiv] Enhancing TinyBERT for Financial Sentiment Analysis Using GPT-Augmented FinBERT Distillation → http://arxiv.org/abs/2409.18999v1
- [arXiv] Automate Strategy Finding with LLM in Quant Investment → http://arxiv.org/abs/2409.06289v4
- [arXiv] Stock Price Responses to Firm-Level News in Supply Chain Networks → http://arxiv.org/abs/2409.06255v5
- [arXiv] StockTime: A Time Series Specialized Large Language Model Architecture for Stock Price Prediction → http://arxiv.org/abs/2409.08281v1
- [arXiv] Optimizing Performance: How Compact Models Match or Exceed GPT's Classification Capabilities through Fine-Tuning → http://arxiv.org/abs/2409.11408v1
- [arXiv] Open-FinLLMs: Open Multimodal Large Language Models for Financial Applications → http://arxiv.org/abs/2408.11878v3
- *(+60 篇省略)*

**🎯 强化学习交易**：
- [AAAI] EarnHFT: Efficient Hierarchical Reinforcement Learning for High Frequency Trading → https://ojs.aaai.org/index.php/AAAI/article/view/29384
- [AAAI] Risk-Conditioned Reinforcement Learning: A Generalized Approach for Adapting to Varying Risk Measures → https://ojs.aaai.org/index.php/AAAI/article/view/29589
- [arXiv] Minimal Batch Adaptive Learning Policy Engine for Real-Time Mid-Price Forecasting in High-Frequency Trading → http://arxiv.org/abs/2412.19372v2
- [arXiv] Multimodal Deep Reinforcement Learning for Portfolio Optimization → http://arxiv.org/abs/2412.17293v1
- [arXiv] Guided Learning: Lubricating End-to-End Modeling for Multi-stage Decision-making → http://arxiv.org/abs/2411.10496v1
- [arXiv] Robot See, Robot Do: Imitation Reward for Noisy Financial Environments → http://arxiv.org/abs/2411.08637v1
- [arXiv] A Random Forest approach to detect and identify Unlawful Insider Trading → http://arxiv.org/abs/2411.13564v1
- [arXiv] A Survey of Financial AI: Architectures, Advances and Open Challenges → http://arxiv.org/abs/2411.12747v1
- [arXiv] Leveraging Fundamental Analysis for Stock Trend Prediction for Profit → http://arxiv.org/abs/2410.03913v1
- [arXiv] Dynamic Portfolio Rebalancing: A Hybrid new Model Using GNNs and Pathfinding for Cost Efficiency → http://arxiv.org/abs/2410.01864v1
- [arXiv] Autoregressive Policy Optimization for Constrained Allocation Tasks → http://arxiv.org/abs/2409.18735v1
- [arXiv] MCI-GRU: Stock Prediction Model Based on Multi-Head Cross-Attention and Improved GRU → http://arxiv.org/abs/2410.20679v3
- [arXiv] QuantFactor REINFORCE: Mining Steady Formulaic Alpha Factors with Variance-bounded REINFORCE → http://arxiv.org/abs/2409.05144v3
- [arXiv] Reinforcement Learning Pair Trading: A Dynamic Scaling approach → http://arxiv.org/abs/2407.16103v2
- [arXiv] Dynamic Pricing in Securities Lending Market: Application in Revenue Optimization for an Agent Lender Portfolio → http://arxiv.org/abs/2407.13687v4
- [OpenReview] MacroHFT: Memory Augmented Context-aware Reinforcement Learning On High Frequency Trading → https://openreview.net/forum?id=l3sujW5Lu8
- [OpenReview] MOT: A Mixture of Actors Reinforcement Learning Method by Optimal Transport for Algorithmic Trading → https://openreview.net/forum?id=Ul6Zh96072
- [arXiv] Tackling Decision Processes with Non-Cumulative Objectives using Reinforcement Learning → http://arxiv.org/abs/2405.13609v3
- [arXiv] Portfolio Management using Deep Reinforcement Learning → http://arxiv.org/abs/2405.01604v1
- [arXiv] Deep Limit Order Book Forecasting → http://arxiv.org/abs/2403.09267v4
- [arXiv] Advancing Investment Frontiers: Industry-grade Deep Reinforcement Learning for Portfolio Optimization → http://arxiv.org/abs/2403.07916v1
- [arXiv] Combining Transformer based Deep Reinforcement Learning with Black-Litterman Model for Portfolio Optimization → http://arxiv.org/abs/2402.16609v1
- [arXiv] Beyond Expectations: Learning with Stochastic Dominance Made Practical → http://arxiv.org/abs/2402.02698v2
- [arXiv] Learning the Market: Sentiment-Based Ensemble Trading Agents → http://arxiv.org/abs/2402.01441v2
- [arXiv] A New Way: Kronecker-Factored Approximate Curvature Deep Hedging and its Benefits → http://arxiv.org/abs/2411.15002v1
- [arXiv] Deep Hedging Bermudan Swaptions → http://arxiv.org/abs/2411.10079v1
- [arXiv] Deep Hedging with Market Impact → http://arxiv.org/abs/2402.13326v2
- [arXiv] Enhanced Momentum with Momentum Transformers → http://arxiv.org/abs/2412.12516v1
- [arXiv] Exploiting Risk-Aversion and Size-dependent fees in FX Trading with Fitted Natural Actor-Critic → http://arxiv.org/abs/2410.23294v1
- [arXiv] A Financial Time Series Denoiser Based on Diffusion Model → http://arxiv.org/abs/2409.02138v1
- *(+51 篇省略)*

**🌐 其他金融 AI**：
- [arXiv] Parameters Optimization of Pair Trading Algorithm → http://arxiv.org/abs/2412.12555v1
- [arXiv] A new Input Convex Neural Network with application to options pricing → http://arxiv.org/abs/2411.12854v1
- [arXiv] Distilled Decoding 1: One-step Sampling of Image Auto-regressive Models with Flow Matching → http://arxiv.org/abs/2412.17153v3
- [arXiv] Granger Causality Detection with Kolmogorov-Arnold Networks → http://arxiv.org/abs/2412.15373v1
- [arXiv] Superheavy Magic Nuclei: Ground-State Properties, Bubble Structure and α-Decay Chains → http://arxiv.org/abs/2410.15157v1
- [arXiv] Alpha decay law of excited nuclei and its role in stellar decay rates → http://arxiv.org/abs/2409.06761v1
- [arXiv] Correlation between alpha-decay half-lives and symmetry energy → http://arxiv.org/abs/2407.19647v2
- [arXiv] Alpha-decay from $^{44}$Ti: Microscopic alpha half-life calculation using normalized spectroscopic factor → http://arxiv.org/abs/2407.18025v1
- [arXiv] $ {}^{164} \mathrm{Pb} $: A possible heaviest $ N = Z $ doubly magic nucleus → http://arxiv.org/abs/2405.12095v2
- [arXiv] Alpha radioactivity deep-underground as a probe of axion dark matter → http://arxiv.org/abs/2404.18993v2
- [arXiv] Cluster radioactivity preformation probability of trans-lead nuclei in the scheme of NpNn → http://arxiv.org/abs/2403.04450v1
- [arXiv] Relativistic mean-field study of alpha decay in superheavy isotopes with 100 \texorpdfstring{$\leq$ Z $\leq$}-120 → http://arxiv.org/abs/2403.02748v1
- [arXiv] Beyond the Alphabet: Deep Signal Embedding for Enhanced DNA Clustering → http://arxiv.org/abs/2410.06188v2
- [arXiv] Assets Forecasting with Feature Engineering and Transformation Methods for LightGBM → http://arxiv.org/abs/2501.07580v1
- [arXiv] Engineering Carbon Credits Towards A Responsible FinTech Era: The Practices, Implications, and Future → http://arxiv.org/abs/2501.14750v2
- [arXiv] Trading with propagators and constraints: applications to optimal execution and battery storage → http://arxiv.org/abs/2409.12098v1
- [arXiv] Optimal position-building strategies in competition → http://arxiv.org/abs/2409.03586v2
- [arXiv] The Mariana Environmental Disaster and its Labor Market Effects → http://arxiv.org/abs/2405.15862v1
- [arXiv] Application and practice of AI technology in quantitative investment → http://arxiv.org/abs/2404.18184v1
- [arXiv] Dynamic Analyses of Contagion Risk and Module Evolution on the SSE A-Shares Market Based on Minimum Information Entropy → http://arxiv.org/abs/2403.19439v1
- [arXiv] From Logistic Regression to the Perceptron Algorithm: Exploring Gradient Descent with Large Step Sizes → http://arxiv.org/abs/2412.08424v1
- [arXiv] One-Step Forward and Backtrack: Overcoming Zig-Zagging in Loss-Aware Quantization Training → http://arxiv.org/abs/2401.16760v1
- [arXiv] Denoising ESG: quantifying data uncertainty from missing data with Machine Learning and prediction intervals → http://arxiv.org/abs/2407.20047v1
- [arXiv] The Generalization Error of Supervised Machine Learning Algorithms → http://arxiv.org/abs/2411.12030v2
- [arXiv] Revaluation of the lower critical field in superconducting H$_3$S and LaH$_{10}$ (Nature Comm. 13, 3194, 2022) → http://arxiv.org/abs/2408.12675v1
- [arXiv] Modeling Performance of Data Collection Systems for High-Energy Physics → http://arxiv.org/abs/2407.00123v1
- [arXiv] Stripping Quantum Decision Diagrams of their Identity → http://arxiv.org/abs/2406.11959v1
- [arXiv] A Spatio-Temporal Approach with Self-Corrective Causal Inference for Flight Delay Prediction → http://arxiv.org/abs/2407.15185v1
- [arXiv] A Pretraining-Finetuning Computational Framework for Material Homogenization → http://arxiv.org/abs/2404.07943v2
- [OpenReview] Analyzing $D^\alpha$ seeding for $k$-means → https://openreview.net/forum?id=b9uHveqszc
- *(+1 篇省略)*

**💼 组合优化/资产配置**：
- [arXiv] MILLION: A General Multi-Objective Framework with Controllable Risk for Portfolio Management → http://arxiv.org/abs/2412.03038v1
- [arXiv] AI-Powered Energy Algorithmic Trading: Integrating Hidden Markov Models with Neural Networks → http://arxiv.org/abs/2407.19858v7
- [arXiv] Contrastive Learning of Asset Embeddings from Financial Time Series → http://arxiv.org/abs/2407.18645v1
- [arXiv] Hopfield Networks for Asset Allocation → http://arxiv.org/abs/2407.17645v1
- [arXiv] Robust portfolio optimization for recommender systems considering uncertainty of estimated statistics → http://arxiv.org/abs/2406.10250v2
- [arXiv] Autonomous Sparse Mean-CVaR Portfolio Optimization → http://arxiv.org/abs/2405.08047v1
- [arXiv] Efficient Automatic Tuning for Data-driven Model Predictive Control via Meta-Learning → http://arxiv.org/abs/2404.00232v1
- [arXiv] FDR-Controlled Portfolio Optimization for Sparse Financial Index Tracking → http://arxiv.org/abs/2401.15139v2
- [arXiv] Temporal Representation Learning for Stock Similarities and Its Applications in Investment Management → http://arxiv.org/abs/2407.13751v1
- [arXiv] Application of Black-Litterman Bayesian in Statistical Arbitrage → http://arxiv.org/abs/2406.06706v1
- [arXiv] A Markowitz Approach to Managing a Dynamic Basket of Moving-Band Statistical Arbitrages → http://arxiv.org/abs/2412.02660v1
- [arXiv] Mean-Variance Portfolio Selection in Long-Term Investments with Unknown Distribution: Online Estimation, Risk Aversion under Ambiguity, and  → http://arxiv.org/abs/2406.13486v2
- [arXiv] Sparse Portfolio Selection via Topological Data Analysis based Clustering → http://arxiv.org/abs/2401.16920v2
- [arXiv] Schur Complementary Allocation: A Unification of Hierarchical Risk Parity and Minimum Variance Portfolios → http://arxiv.org/abs/2411.05807v1
- [arXiv] Transforming Investment Strategies and Strategic Decision-Making: Unveiling a Novel Methodology for Enhanced Performance and Risk Management → http://arxiv.org/abs/2405.01892v1
- [arXiv] Can Generalized Extreme Value Model Fit the Real Stocks → http://arxiv.org/abs/2412.06226v1
- [OpenReview] A Fully Analog Pipeline for Portfolio Optimization → https://openreview.net/forum?id=mtkbTUVaV1
- [OpenReview] Advancing Portfolio Optimization: Hybrid Relaxation and Heuristic Approaches for Cardinality-Constrained MIQP Problems → https://openreview.net/forum?id=C9pndmSjg6
- [OpenReview] A Mayfly algorithm for cardinality constrained portfolio optimization → https://openreview.net/forum?id=wWiDV66Pt5
- [OpenReview] Cardinality Constrained Portfolio Optimization via Alternating Direction Method of Multipliers → https://openreview.net/forum?id=2O5Ni9ZXZY
- [OpenReview] Enhancing mean–variance portfolio optimization through GANs-based anomaly detection → https://openreview.net/forum?id=dfkRS9XAUN
- [OpenReview] Short-term Portfolio Optimization using Doubly Regularized Exponential Growth Rate → https://openreview.net/forum?id=IPmKkXAT6E

**📊 波动率预测**：
- [AAAI] MASTER: Market-Guided Stock Transformer for Stock Price Forecasting → https://ojs.aaai.org/index.php/AAAI/article/view/27767
- [AAAI] From GARCH to Neural Network for Volatility Forecast → https://ojs.aaai.org/index.php/AAAI/article/view/29643
- [arXiv] AMA-LSTM: Pioneering Robust and Fair Financial Audio Analysis for Stock Volatility Prediction → http://arxiv.org/abs/2407.18324v1
- [arXiv] Fast Deep Hedging with Second-Order Optimization → http://arxiv.org/abs/2410.22568v1
- [arXiv] Enhancing Deep Hedging of Options with Implied Volatility Surface Feedback Information → http://arxiv.org/abs/2407.21138v2
- [arXiv] Is the difference between deep hedging and delta hedging a statistical arbitrage? → http://arxiv.org/abs/2407.14736v3
- [arXiv] Finding Moving-Band Statistical Arbitrages via Convex-Concave Optimization → http://arxiv.org/abs/2402.08108v1
- [arXiv] Finance-Informed Neural Network: Learning the Geometry of Option Pricing → http://arxiv.org/abs/2412.12213v2
- [arXiv] A time-stepping deep gradient flow method for option pricing in (rough) diffusion models → http://arxiv.org/abs/2403.00746v2
- [arXiv] Deep Learning-Based Electricity Price Forecast for Virtual Bidding in Wholesale Electricity Market → http://arxiv.org/abs/2412.00062v1
- [arXiv] Utilizing RNN for Real-time Cryptocurrency Price Prediction and Trading Strategy Optimization → http://arxiv.org/abs/2411.05829v1
- [arXiv] Deep Generative Modeling for Financial Time Series with Application in VaR: A Comparative Review → http://arxiv.org/abs/2401.10370v1
- [arXiv] Volatility-Volume Order Slicing via Statistical Analysis → http://arxiv.org/abs/2412.12482v1
- [arXiv] Uncertain Regulations, Definite Impacts: The Impact of the US Securities and Exchange Commission's Regulatory Interventions on Crypto Assets → http://arxiv.org/abs/2412.02452v1
- [arXiv] Analyst Reports and Stock Performance: Evidence from the Chinese Market → http://arxiv.org/abs/2411.08726v2
- [arXiv] MIGA: Mixture-of-Experts with Group Aggregation for Stock Market Prediction → http://arxiv.org/abs/2410.02241v1
- [arXiv] Navigating Market Turbulence: Insights from Causal Network Contagion Value at Risk → http://arxiv.org/abs/2402.06032v1
- [OpenReview] Can GANs Learn the Stylized Facts of Financial Time Series? → https://openreview.net/forum?id=Qlg9Nd4Sdy
- [OpenReview] [Q3: Extreme market conditions] We have added experimental results to demonstrate FINCON's robust performance during periods of significant  → https://openreview.net/forum?id=w8InKmaChX

**📰 新闻/社媒情绪**：
- [arXiv] Assessing the Robustness of LLM-based NLP Software via Automated Testing → http://arxiv.org/abs/2412.21016v2
- [arXiv] Composing Ensembles of Instrument-Model Pairs for Optimizing Profitability in Algorithmic Trading → http://arxiv.org/abs/2411.13559v1
- [arXiv] Modeling News Interactions and Influence for Financial Market Prediction → http://arxiv.org/abs/2410.10614v1
- [arXiv] MANA-Net: Mitigating Aggregated Sentiment Homogenization with News Weighting for Enhanced Market Prediction → http://arxiv.org/abs/2409.05698v1
- [arXiv] Instruction-Guided Bullet Point Summarization of Long Financial Earnings Call Transcripts → http://arxiv.org/abs/2405.06669v1
- [arXiv] Multi-Task Learning for Features Extraction in Financial Annual Reports → http://arxiv.org/abs/2404.05281v1
- [arXiv] EFSA: Towards Event-Level Financial Sentiment Analysis → http://arxiv.org/abs/2404.08681v2
- [arXiv] Enhancement of price trend trading strategies via image-induced importance weights → http://arxiv.org/abs/2408.08483v1
- [arXiv] A Hybrid Deep Learning Framework for Stock Price Prediction Considering the Investor Sentiment of Online Forum Enhanced by Popularity → http://arxiv.org/abs/2405.10584v1
- [arXiv] Prioritizing Investments in Cybersecurity: Empirical Evidence from an Event Study on the Determinants of Cyberattack Costs → http://arxiv.org/abs/2402.04773v1
- [arXiv] Trust Dynamics and Market Behavior in Cryptocurrency: A Comparative Study of Centralized and Decentralized Exchanges → http://arxiv.org/abs/2404.17227v2
- [OpenReview] From attention to profit: quantitative trading strategy based on transformer → https://openreview.net/forum?id=AMrOGR8rns
- [OpenReview] Financial Sentiment Analysis: Techniques and Applications → https://openreview.net/forum?id=CFNmRsC7hs
- [OpenReview] Review on Enhacing Sentiment Analysis for Financial Markets → https://openreview.net/forum?id=SFBfqdOYuP
- [OpenReview] Promising Approach to Financial Sentiment Analysis Using RNNs and Word Embeddings → https://openreview.net/forum?id=MCh36mS8L8
- [OpenReview] [Proposal-ML]Enhancing Sentiment Analysis in Financial Markets Using RNNs and Word Embeddings → https://openreview.net/forum?id=Xky6NFYjzc
- [OpenReview] Explainable Stock Price Movement Prediction using Contrastive Learning → https://openreview.net/forum?id=osIUxmvLDr
- [OpenReview] Stock Movement Prediction with Multimodal Stable Fusion via Gated Cross-Attention Mechanism → https://openreview.net/forum?id=cQkR3xDjEW

**🕸 图神经网络/股票关系**：
- [AAAI] ECHO-GL: Earnings Calls-Driven Heterogeneous Graph Learning for Stock Movement Prediction → https://ojs.aaai.org/index.php/AAAI/article/view/29305
- [AAAI] CI-STHPAN: Pre-trained Attention Network for Stock Selection with Channel-Independent Spatio-Temporal Hypergraph → https://ojs.aaai.org/index.php/AAAI/article/view/28770
- [AAAI] MDGNN: Multi-Relational Dynamic Graph Neural Network for Comprehensive and Dynamic Stock Investment Prediction → https://ojs.aaai.org/index.php/AAAI/article/view/29381
- [arXiv] Stock Type Prediction Model Based on Hierarchical Graph Neural Network → http://arxiv.org/abs/2412.06862v1
- [arXiv] Clustering Time Series Data with Gaussian Mixture Embeddings in a Graph Autoencoder Framework → http://arxiv.org/abs/2411.16972v1
- [arXiv] Double-Path Adaptive-correlation Spatial-Temporal Inverted Transformer for Stock Time Series Forecasting → http://arxiv.org/abs/2409.15662v1
- [arXiv] LSR-IGRU: Stock Trend Prediction Based on Long Short-Term Relationships and Improved GRU → http://arxiv.org/abs/2409.08282v3
- [arXiv] MTRGL:Effective Temporal Correlation Discerning through Multi-modal Temporal Relational Graph Learning → http://arxiv.org/abs/2401.14199v2
- [arXiv] Time-Varying Graph Learning for Data with Heavy-Tailed Distribution → http://arxiv.org/abs/2501.00606v1
- [arXiv] Multi-relational Graph Diffusion Neural Network with Parallel Retention for Stock Trends Classification → http://arxiv.org/abs/2401.05430v1
- [arXiv] Dynamic Graph Representation with Contrastive Learning for Financial Market Prediction: Integrating Temporal Evolution and Static Relations → http://arxiv.org/abs/2412.04034v1
- [OpenReview] A Motif-Based Graph Convolution Network for Stock Trend Prediction → https://openreview.net/forum?id=XyYIdLXHua
- [OpenReview] Phrase-Aware Financial Sentiment Analysis Based on Constituent Syntax → https://openreview.net/forum?id=vp9OpSqcr7
- [OpenReview] MERGE: Multi-view Relationship Graph Network for Event-Driven Stock Movement Prediction → https://openreview.net/forum?id=p6hBIFNfQ0
- [OpenReview] A Dynamic Dual-Graph Neural Network for Stock Price Movement Prediction → https://openreview.net/forum?id=4YkCYPkYdB

**⚡ 订单簿/HFT/微观结构**：
- [arXiv] Market Making without Regret → http://arxiv.org/abs/2411.13993v2
- [arXiv] High resolution microprice estimates from limit orderbook data using hyperdimensional vector Tsetlin Machines → http://arxiv.org/abs/2411.13594v1
- [arXiv] Limit Order Book Simulation and Trade Evaluation with $K$-Nearest-Neighbor Resampling → http://arxiv.org/abs/2409.06514v1
- [arXiv] HLOB -- Information Persistence and Structure in Limit Order Books → http://arxiv.org/abs/2405.18938v3
- [arXiv] Automated Market Making and Decentralized Finance → http://arxiv.org/abs/2407.16885v1
- [arXiv] A theory of passive market impact → http://arxiv.org/abs/2412.07461v1
- [arXiv] Optimal Execution under Incomplete Information → http://arxiv.org/abs/2411.04616v1
- [arXiv] Data-driven measures of high-frequency trading → http://arxiv.org/abs/2405.08101v3
- [arXiv] High-Frequency Options Trading | With Portfolio Optimization → http://arxiv.org/abs/2408.08866v1
- [OpenReview] Neural Marked Hawkes Process for Limit Order Book Modeling → https://openreview.net/forum?id=tlgh6NGDv4
- [OpenReview] Long short-term temporal fusion transformer for short-term forecasting of limit order book in China markets → https://openreview.net/forum?id=gswCmaMDlR
- [OpenReview] A Benchmark Study For Limit Order Book (LOB) Models and Time Series Forecasting Models on LOB Data → https://openreview.net/forum?id=MhD9rLeU31
- [OpenReview] Thermodynamic Analysis of Financial Markets: Measuring Order Book Dynamics with Temperature and Entropy → https://openreview.net/forum?id=tZruVmQN4D

**🔄 Transformer 时序**：
- [arXiv] Hidformer: Transformer-Style Neural Network in Stock Price Forecasting → http://arxiv.org/abs/2412.19932v1
- [arXiv] Trading through Earnings Seasons using Self-Supervised Contrastive Representation Learning → http://arxiv.org/abs/2409.17392v1
- [arXiv] Evaluating Named Entity Recognition: A comparative analysis of mono- and multilingual transformer models on a novel Brazilian corporate earn → http://arxiv.org/abs/2403.12212v2
- [arXiv] MLP, XGBoost, KAN, TDNN, and LSTM-GRU Hybrid RNN with Attention for SPX and NDX European Call Option Pricing → http://arxiv.org/abs/2409.06724v3
- [arXiv] Enhancing Risk Assessment in Transformers with Loss-at-Risk Functions → http://arxiv.org/abs/2411.02558v1
- [arXiv] Explaining the Model, Protecting Your Data: Revealing and Mitigating the Data Privacy Risks of Post-Hoc Model Explanations via Membership In → http://arxiv.org/abs/2407.17663v1
- [arXiv] tsGT: Stochastic Time Series Modeling With Transformer → http://arxiv.org/abs/2403.05713v3
- [arXiv] Hedge Fund Portfolio Construction Using PolyModel Theory and iTransformer → http://arxiv.org/abs/2408.03320v3
- [OpenReview] StockQM: A Cross-Frequency Dataset for Stock Prediction and a New Stock Prediction Model → https://openreview.net/forum?id=98c6gelRnn
- [OpenReview] Time Series Anomaly Detection Leveraging MSE Feedback with AutoEncoder and RNN → https://openreview.net/forum?id=tNHluL0FLd

**📈 时序模型(LSTM/RNN)**：
- [arXiv] Supervised Autoencoders with Fractionally Differentiated Features and Triple Barrier Labelling Enhance Predictions on Noisy Data → http://arxiv.org/abs/2411.12753v2
- [arXiv] A Stock Price Prediction Approach Based on Time Series Decomposition and Multi-Scale CNN using OHLCT Images → http://arxiv.org/abs/2410.19291v2
- [arXiv] Detecting and Triaging Spoofing using Temporal Convolutional Networks → http://arxiv.org/abs/2403.13429v1
- [arXiv] Pricing American Options using Machine Learning Algorithms → http://arxiv.org/abs/2409.03204v1
- [arXiv] Neural Network Learning of Black-Scholes Equation for Option Pricing → http://arxiv.org/abs/2405.05780v1
- [arXiv] Time series generation for option pricing on quantum computers using tensor network → http://arxiv.org/abs/2402.17148v2
- [arXiv] GDP nowcasting with large-scale inter-industry payment data in real time -- A network approach → http://arxiv.org/abs/2411.02029v1
- [OpenReview] Time-Causal VAE: Robust Financial Time Series Generator → https://openreview.net/forum?id=No385565BR
- [OpenReview] Representation learning for financial time series forecasting → https://openreview.net/forum?id=qU1GtrDDst

**🧪 回测/市场模拟**：
- [arXiv] Experimental Analysis of Deep Hedging Using Artificial Market Simulations for Underlying Asset Simulators → http://arxiv.org/abs/2404.09462v1
- [arXiv] Predicting Market Trends with Enhanced Technical Indicator Integration and Classification Models → http://arxiv.org/abs/2410.06935v2
- [arXiv] Practical Marketplace Optimization at Uber Using Causally-Informed Machine Learning → http://arxiv.org/abs/2407.19078v1
- [arXiv] Primary activity measurement of an Am-241 solution using microgram inkjet gravimetry and decay energy spectrometry → http://arxiv.org/abs/2411.02565v3
- [arXiv] Penalized Sparse Covariance Regression with High Dimensional Covariates → http://arxiv.org/abs/2410.04028v1
- [OpenReview] Benchmarking Machine Learning Methods for Stock Prediction → https://openreview.net/forum?id=bsXxNkhvm6

**📐 统计套利/均值回归**：
- [arXiv] An Application of the Ornstein-Uhlenbeck Process to Pairs Trading → http://arxiv.org/abs/2412.12458v1
- [arXiv] Pairs Trading Using a Novel Graphical Matching Approach → http://arxiv.org/abs/2403.07998v1
- [arXiv] ESG driven pairs algorithm for sustainable trading: Analysis from the Indian market → http://arxiv.org/abs/2401.14761v1
- [arXiv] Statistical Arbitrage in Rank Space → http://arxiv.org/abs/2410.06568v1
- [arXiv] Market information of the fractional stochastic regularity model → http://arxiv.org/abs/2409.07159v3

**🛡 对抗/鲁棒性**：
- [AAAI] Market-GAN: Adding Control to Financial Market Data Generation with Semantic Context → https://ojs.aaai.org/index.php/AAAI/article/view/29531
- [arXiv] A Comprehensive Analysis of Machine Learning Models for Algorithmic Trading of Bitcoin → http://arxiv.org/abs/2407.18334v1
- [arXiv] Risk Management with Feature-Enriched Generative Adversarial Networks (FE-GAN) → http://arxiv.org/abs/2411.15519v1
- [arXiv] AI in ESG for Financial Institutions: An Industrial Survey → http://arxiv.org/abs/2403.05541v1

**📑 财报/披露文本分析**：
- [AAAI] Explainable Earnings Call Representation Learning (Student Abstract) → https://ojs.aaai.org/index.php/AAAI/article/view/30454
- [OpenReview] A QA Dataset for Analyzing Earnings Call Transcripts → https://openreview.net/forum?id=7MPIepD2c8
- [OpenReview] Co-Trained Retriever-Generator Framework for Question Generation in Earnings Calls → https://openreview.net/forum?id=uQi2JWxHgV
- [OpenReview] ConEC: Earnings Call Dataset with Real-world Contexts for Benchmarking Contextual Speech Recognition → https://openreview.net/forum?id=1WqIb2QVbq

**🔍 因子挖掘/Alpha 发现**：
- [arXiv] Blending Ensemble for Classification with Genetic-algorithm generated Alpha factors and Sentiments (GAS) → http://arxiv.org/abs/2411.03035v1
- [arXiv] KAN based Autoencoders for Factor Models → http://arxiv.org/abs/2408.02694v1
- [arXiv] Alpha Mining and Enhancing via Warm Start Genetic Programming for Quantitative Investment → http://arxiv.org/abs/2412.00896v1

**⚖ 风险/信用/欺诈**：
- [arXiv] Jump Diffusion-Informed Neural Networks with Transfer Learning for Accurate American Option Pricing under Data Scarcity → http://arxiv.org/abs/2409.18168v1
- [arXiv] A Personal data Value at Risk Approach → http://arxiv.org/abs/2411.03217v2
- [arXiv] The Blockchain Risk Parity Line: Moving From The Efficient Frontier To The Final Frontier Of Investments → http://arxiv.org/abs/2407.09536v1

**📐 期权/衍生品**：
- [arXiv] A deep implicit-explicit minimizing movement method for option pricing in jump-diffusion models → http://arxiv.org/abs/2401.06740v2
- [arXiv] AI Diffusion to Low- and Middle Income Countries; A Blessing or a Curse? → http://arxiv.org/abs/2405.20399v3
- [arXiv] rECGnition_v1.0: Arrhythmia detection using cardiologist-inspired multi-modal architecture incorporating demographic attributes in ECG → http://arxiv.org/abs/2410.18985v1

**🌊 市场状态/Regime**：
- [arXiv] Representation Learning for Regime detection in Block Hierarchical Financial Markets → http://arxiv.org/abs/2410.22346v1
- [arXiv] Portfolio Stress Testing and Value at Risk (VaR) Incorporating Current Market Conditions → http://arxiv.org/abs/2409.18970v1

**🎨 多模态融合**：
- [arXiv] A multi-factor market-neutral investment strategy for New York Stock Exchange equities → http://arxiv.org/abs/2412.12350v1
- [OpenReview] DeepAR-Attention probabilistic prediction for stock price series → https://openreview.net/forum?id=toP8E3vAOk

**🎲 生成模型/合成数据**：
- [arXiv] End-to-End Policy Learning of a Statistical Arbitrage Autoencoder Architecture → http://arxiv.org/abs/2402.08233v1
- [arXiv] Causal Inference in Finance: An Expertise-Driven Model for Instrument Variables Identification and Interpretation → http://arxiv.org/abs/2411.17542v1

**💡 可解释性**：
- [arXiv] A Comprehensive Sustainable Framework for Machine Learning and Artificial Intelligence → http://arxiv.org/abs/2407.12445v1

**₿ 加密货币/区块链**：
- [OpenReview] Athena: Smart order routing on centralized crypto exchanges using a unified order book → https://openreview.net/forum?id=U2yVLHGbOa

