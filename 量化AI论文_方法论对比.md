# 量化 AI 论文 · 方法论横向对比

_对 1358 篇 2024+ 论文摘要的统计分析 | 完成于 2026-04-27_

> 这份分析告诉你：当代量化 AI 论文用什么数据、和什么 baseline 比、报告什么指标。
> 是研究**学界共识与盲区**的最直接窗口。

---

## 📊 数据集使用频次（Top 25）

| # | 数据集 | 论文数 | 解读 |
|---:|---|---:|---|
| 1 | Crypto | 73 | |
| 2 | S&P 500 | 57 | |
| 3 | Bitcoin | 45 | |
| 4 | Chinese 市场 | 38 | |
| 5 | Earnings call 转录 | 22 | |
| 6 | Ethereum | 17 | |
| 7 | NASDAQ-100 | 10 | |
| 8 | Twitter | 10 | |
| 9 | SEC 文件 | 9 | |
| 10 | Dow Jones | 6 | |
| 11 | CSI300 | 6 | |
| 12 | A-share (中国 A 股) | 5 | |
| 13 | Binance | 5 | |
| 14 | 波动率曲面 | 5 | |
| 15 | LOBSTER (LOB 数据) | 5 | |
| 16 | NYSE | 4 | |
| 17 | FI-2010 | 4 | |
| 18 | Yahoo Finance | 3 | |
| 19 | Reddit/WSB | 2 | |
| 20 | CSI500 | 2 | |
| 21 | SPX 期权 | 1 | |
| 22 | AlphaVantage | 1 | |
| 23 | Coinbase | 1 | |
| 24 | CRSP 数据库 | 1 | |
| 25 | Reuters | 1 | |

**关键观察**：
- 最常用 5 个数据集：Crypto, S&P 500, Bitcoin, Chinese 市场, Earnings call 转录
- **散户能拿到**：S&P 500、NASDAQ-100、Yahoo Finance、Twitter — 这些是免费/低门槛
- **散户拿不到**：CRSP、Compustat、WRDS、Bloomberg、LOBSTER — 这些机构数据需付费
- **中国数据**：CSI 300/800、A-share 论文不少，Tushare/Akshare 是免费方案

---

## 🧪 Baseline 使用频次（Top 25）

| # | Baseline | 引用次数 |
|---:|---|---:|
| 1 | Transformer baseline | 111 |
| 2 | LSTM | 83 |
| 3 | FinBERT | 69 |
| 4 | Markowitz/MV | 40 |
| 5 | Llama | 32 |
| 6 | BERT | 32 |
| 7 | GPT-3/4 | 27 |
| 8 | PPO | 19 |
| 9 | Random Forest | 19 |
| 10 | Black-Scholes | 18 |
| 11 | XGBoost | 18 |
| 12 | MLP | 18 |
| 13 | GARCH | 17 |
| 14 | GPT-4o | 15 |
| 15 | ARIMA | 14 |
| 16 | Buy & Hold | 14 |
| 17 | GRU | 13 |
| 18 | Claude | 12 |
| 19 | CNN | 11 |
| 20 | DDPG | 7 |
| 21 | A2C/A3C | 5 |
| 22 | LightGBM | 5 |
| 23 | PatchTST | 5 |
| 24 | Informer | 5 |
| 25 | SAC | 3 |

**关键观察**：
- 时序基线主流：LSTM、Transformer、GRU、ARIMA
- ML 基线主流：XGBoost、LightGBM、Random Forest
- RL 主流算法：PPO、DDPG、SAC、DQN
- LLM 基线已经进入：FinBERT 是文本任务标配，GPT-3/4 / Claude 在新论文里
- 经济模型基线：Black-Scholes（期权）、Markowitz/MV（组合）、GARCH（波动率）

---

## 📐 评估指标使用频次（Top 15）

| # | 指标 | 论文数 |
|---:|---|---:|
| 1 | accuracy\b | 292 |
| 2 | Sharpe[\s\-]?ratio\b | 84 |
| 3 | \bF1\b | 45 |
| 4 | \bMSE\b|Mean[\s\-]?Squared[\s\ | 29 |
| 5 | \bMAE\b|Mean[\s\-]?Absolute[\s | 26 |
| 6 | max(?:imum)?[\s\-]?drawdown\b | 25 |
| 7 | \bRMSE\b|Root[\s\-]?Mean[\s\-] | 17 |
| 8 | \bAUC\b | 14 |
| 9 | \bIC\b|Information[\s\-]?coeff | 9 |
| 10 | annualized?[\s\-]?return\b | 9 |
| 11 | \bIR\b|Information[\s\-]?ratio | 7 |
| 12 | win[\s\-]?rate\b | 4 |
| 13 | Sortino[\s\-]?ratio\b | 3 |
| 14 | \bRR\b|Realized[\s\-]?Return\b | 2 |
| 15 | Calmar[\s\-]?ratio\b | 1 |

**关键观察**：
- **金融评价 vs ML 评价并存**：很多论文同时用 Sharpe + MSE
- **散户应该优先看的**：Sharpe、Sortino、Max Drawdown、Win Rate、IC（信息系数）
- **散户应该警惕的**：仅报告 MSE/MAE/RMSE 的论文——这些点估计准确度和实盘盈利能力相关性弱

---

## 📈 论文中报告的 Sharpe 比率分布

共提取 **37** 个 Sharpe 数值。

**Top 20 最高 Sharpe**：

| Sharpe | 论文 | 链接 |
|---:|---|---|
| 12.02 | KASPER: Kolmogorov Arnold Networks for Stock Prediction and Explainable Regimes | http://arxiv.org/abs/2507.18983v1 |
| 3.76 | Crisis-Resilient Portfolio Management via Graph-based Spatio-Temporal Learning | http://arxiv.org/abs/2510.20868v1 |
| 3.11 | Beyond Prompting: An Autonomous Framework for Systematic Factor Investing via Ag | http://arxiv.org/abs/2603.14288v2 |
| 3.05 | Sentiment trading with large language models | http://arxiv.org/abs/2412.19245v1 |
| 3.05 | Enhanced Financial Sentiment Analysis and Trading Strategy Development Using Lar | https://openreview.net/forum?id=V8pWvnFm04 |
| 3.05 | Sentiment trading with large language models | https://openreview.net/forum?id=kOxr4dVrFq |
| 3.05 | Sentiment trading with large language models | https://openreview.net/forum?id=47pcnKq9Mn |
| 2.80 | NewsNet-SDF: Stochastic Discount Factor Estimation with Pretrained Language Mode | http://arxiv.org/abs/2505.06864v1 |
| 2.63 | Orchestration Framework for Financial Agents: From Algorithmic Trading to Agenti | http://arxiv.org/abs/2512.02227v1 |
| 2.43 | Autonomous Market Intelligence: Agentic AI Nowcasting Predicts Stock Returns | http://arxiv.org/abs/2601.11958v1 |
| 2.30 | Attention Factors for Statistical Arbitrage | http://arxiv.org/abs/2510.11616v1 |
| 2.13 | AEL: Agent Evolving Learning for Open-Ended Environments | http://arxiv.org/abs/2604.21725v1 |
| 2.06 | OOM-RL: Out-of-Money Reinforcement Learning Market-Driven Alignment for LLM-Base | http://arxiv.org/abs/2604.11477v1 |
| 2.00 | FinDPO: Financial Sentiment Analysis for Algorithmic Trading through Preference  | http://arxiv.org/abs/2507.18417v1 |
| 1.87 | Deep Learning Enhanced Multi-Day Turnover Quantitative Trading Algorithm for Chi | http://arxiv.org/abs/2506.06356v1 |
| 1.81 | Constrained Portfolio Optimization via Quantum Approximate Optimization Algorith | http://arxiv.org/abs/2602.14827v1 |
| 1.76 | Quantum Adaptive Self-Attention for Financial Rebalancing: An Empirical Study on | http://arxiv.org/abs/2509.16955v1 |
| 1.76 | Quantum and Classical Machine Learning in Decentralized Finance: Comparative Evi | http://arxiv.org/abs/2510.15903v1 |
| 1.50 | Transforming Japan Real Estate | http://arxiv.org/abs/2405.20715v1 |
| 1.40 | Can Blindfolded LLMs Still Trade? An Anonymization-First Framework for Portfolio | http://arxiv.org/abs/2603.17692v1 |

**Bottom 10 最低 Sharpe**：

| Sharpe | 论文 | 链接 |
|---:|---|---|
| 1.01 | Long-only cryptocurrency portfolio management by ranking the assets: a neural ne | http://arxiv.org/abs/2512.08124v1 |
| 0.94 | Deep Reinforcement Learning in Factor Investment | http://arxiv.org/abs/2509.16206v1 |
| 0.91 | Joint Return and Risk Modeling with Deep Neural Networks for Portfolio Construct | http://arxiv.org/abs/2603.19288v1 |
| 0.90 | Transforming Japan Real Estate | http://arxiv.org/abs/2405.20715v1 |
| 0.77 | AI-Powered Energy Algorithmic Trading: Integrating Hidden Markov Models with Neu | http://arxiv.org/abs/2407.19858v7 |
| 0.59 | Quantum-Assisted Optimal Rebalancing with Uncorrelated Asset Selection for Algor | http://arxiv.org/abs/2603.16904v1 |
| 0.57 | Quantum-Assisted Optimal Rebalancing with Uncorrelated Asset Selection for Algor | http://arxiv.org/abs/2603.16904v1 |
| 0.33 | Interpretable Hypothesis-Driven Trading:A Rigorous Walk-Forward Validation Frame | http://arxiv.org/abs/2512.12924v1 |
| 0.22 | Not All Factors Crowd Equally: Modeling, Measuring, and Trading on Alpha Decay | http://arxiv.org/abs/2512.11913v2 |
| 0.04 | A New Way: Kronecker-Factored Approximate Curvature Deep Hedging and its Benefit | http://arxiv.org/abs/2411.15002v1 |

**统计**：
- 平均：1.96
- 中位数：1.50
- 最高：12.02
- 最低：0.04

⚠️ **重要警告**：论文报告的 Sharpe 是**回测/模拟值**，不是实盘成绩。学界发表偏向（publication bias）会让高 Sharpe 论文更容易被接收，所以中位数都偏高。**实盘 Sharpe > 1.5 已经是优秀策略**。

---

## 🎯 散户实操方案（基于横向对比）

**第一步：选择你能负担的数据**
- 美股：Yahoo Finance（免费）/ Polygon.io（$30/月起）/ AlphaVantage（免费有限）
- A 股：Tushare Pro（按月订阅）/ Akshare（免费）
- 加密：Binance API（免费）/ CoinGecko
- 文本：手动爬+LLM 处理（最便宜的 alternative data）

**第二步：用最广泛使用的 baseline 起步**
- 时序：LightGBM / XGBoost（特征工程友好）
- 文本：直接调 GPT-4o / Claude API（不再训练 FinBERT）
- 强化学习：先别做（论文 OOS 失效率高）

**第三步：用学术评价指标验证**
- 必报：Sharpe、Max Drawdown、年化收益、胜率
- 建议报：Sortino、Calmar、IC、IR、滚动 Sharpe
- 别只看：MSE/RMSE/Accuracy

**第四步：警惕你看到的高 Sharpe**
- 训练集 Sharpe 5+ → 几乎肯定过拟合
- 测试集 Sharpe 2-3 → 看测试集时间是否含大事件（COVID、加息周期）
- 真实 Sharpe（部署后）≈ 测试集 Sharpe × 0.3-0.5

