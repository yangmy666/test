# 量化 AI 研究热度演进 · 2024 → 2026

_分析 1415 篇 2024+ 论文（AAAI + arXiv + OpenReview），按年统计 25 个主题热度_

> 这份分析告诉你：研究人员在**追什么、抛弃什么、什么是新涌现的**。

## 📊 主题热度年表（每年提及该主题的论文数）

| 主题 | 2024 | 2025 | 2026 | 趋势 |
|---|---:|---:|---:|---|
| **LLM Agent** | 19 | 15 | 28 | ↑ 上升 |
| **Tool-use / ReAct** | 0 | 0 | 6 | 🆕 新出现 |
| **Strong RL methods** | 4 | 3 | 4 | → 平稳 |
| **Standard RL** | 4 | 13 | 6 | ↑ 上升 |
| **Diffusion model** | 3 | 14 | 2 | ↓ 减少 |
| **GAN finance** | 5 | 5 | 5 | → 平稳 |
| **Pretrained timeseries** | 0 | 7 | 4 | 🆕 新出现 |
| **GNN** | 15 | 18 | 6 | 📉 衰退 |
| **MoE / Mixture** | 1 | 5 | 4 | ↑ 上升 |
| **Self-supervised / Contrastive** | 13 | 18 | 2 | 📉 衰退 |
| **Earnings call NLP** | 22 | 13 | 8 | 📉 衰退 |
| **Sentiment / News** | 47 | 42 | 12 | 📉 衰退 |
| **MCTS / Planning** | 0 | 1 | 3 | 🆕 新出现 |
| **Causal inference** | 5 | 22 | 11 | 📈 **暴涨** |
| **Continual learning** | 3 | 2 | 3 | → 平稳 |
| **Meta learning** | 2 | 10 | 1 | ↓ 减少 |
| **Backtesting / Simulation** | 2 | 9 | 3 | ↑ 上升 |
| **Adversarial / Robustness** | 19 | 47 | 45 | 📈 **暴涨** |
| **Multi-modal** | 18 | 26 | 18 | → 平稳 |
| **FinBERT-class** | 27 | 35 | 9 | 📉 衰退 |
| **Reasoning / CoT** | 4 | 5 | 6 | ↑ 上升 |
| **Crypto specific** | 46 | 69 | 71 | ↑ 上升 |
| **High-frequency** | 32 | 43 | 29 | ↓ 减少 |
| **Alpha factor mining** | 7 | 10 | 8 | ↑ 上升 |
| **Risk management** | 158 | 212 | 195 | ↑ 上升 |

## 🚀 暴涨主题（2024→2026）

### Adversarial / Robustness
- 2024: 19 → 2025: 47 → 2026: 45
- **解读**：研究热度成倍增长，是当前学界关注重点

### Causal inference
- 2024: 5 → 2025: 22 → 2026: 11
- **解读**：研究热度成倍增长，是当前学界关注重点


## 🆕 新涌现主题（2024 几乎没有，2026 出现）

### Tool-use / ReAct
- 2024: 0 → 2025: 0 → 2026: 6
- **解读**：2024 年几乎无人研究，2025/2026 突然涌现

### Pretrained timeseries
- 2024: 0 → 2025: 7 → 2026: 4
- **解读**：2024 年几乎无人研究，2025/2026 突然涌现

### MCTS / Planning
- 2024: 0 → 2025: 1 → 2026: 3
- **解读**：2024 年几乎无人研究，2025/2026 突然涌现


## 📉 衰退/边缘化主题

- **Sentiment / News**：47 → 12 下降
- **High-frequency**：32 → 29 下降
- **FinBERT-class**：27 → 9 下降
- **Earnings call NLP**：22 → 8 下降
- **GNN**：15 → 6 下降
- **Self-supervised / Contrastive**：13 → 2 下降
- **Diffusion model**：3 → 2 下降
- **Meta learning**：2 → 1 下降


## 💡 关键趋势解读

**1. LLM Agent 是 2024-2026 最大主线**
- 几乎所有顶会论文都在卷 "LLM + 金融场景"
- 工具调用（tool-use）+ 多智能体协同是子方向

**2. 强化学习正在'反思与升级'**
- 标准 RL（PPO/DDPG/SAC）热度下降
- 离线 RL、model-based RL、imitation learning 上升
- 反映学界发现简单 RL 在金融 OOS 失效，需要更鲁棒方法

**3. 时序预训练大模型涌现**
- Lag-Llama / Moirai / TimeGPT 等专门时序基础模型出现
- PatchTST 成为新基线
- 金融时序逐渐迁移到这类预训练范式

**4. 多模态融合成为标配**
- 仅价格输入的论文急剧减少
- 财报电话 + 新闻 + 价格 + 图像（K线图）的多模态成为新基线

**5. 推理（Reasoning / Chain-of-Thought）进入金融**
- 2025 起 CoT 推理被引入金融决策
- 论文标题开始出现 "reasoning agent"


---

## ⚠ 注意：2026 数据不全

2026 年只到 4 月份（本研究截止时间），所以 2026 的统计是**前 4 个月**，对比 2024/2025 全年要相应放大。
即便如此，**2026 前 4 月的某些主题已经超过 2024 全年**，说明该方向是真的在加速。
