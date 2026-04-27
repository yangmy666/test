# 美股新闻情绪结构化提取（Claude API）

完全自动化的新闻情绪 pipeline——从 Yahoo Finance 抓新闻 → Claude 提取结构化情绪 → 聚合成可读报告。

## 📦 文件

- `fetch_news.py` — 从 Yahoo Finance RSS 抓 14 个标的（Mag 7 + 半导体 + 指数 + 银行）的最新新闻
- `extract_sentiment.py` — 用 Claude Opus 4.7 + Pydantic 结构化输出做情绪提取
- `aggregate.py` — 聚合分析：按标的/事件/方向，输出 markdown 报告
- `news_raw.json` — 步骤 1 输出（已生成，**203 条**）
- `news_analyzed.json` — 步骤 2 输出（待跑）
- `sentiment_report.md` — 步骤 3 输出（待跑）

## 🚀 用法

### 1. 设置 Claude API Key

PowerShell:
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

bash:
```bash
export ANTHROPIC_API_KEY='sk-ant-...'
```

如果你没有 key：去 https://console.anthropic.com/ 创建。

### 2. 跑流程

```bash
cd C:/Users/yang/desktop/test_project/news-sentiment

# Step 1（已经跑过了）：抓最新新闻
python fetch_news.py

# Step 2：Claude 提取（这步要钱，但很便宜——见下面成本估算）
python extract_sentiment.py

# 想先小规模测试？限制 10 条
LIMIT=10 python extract_sentiment.py

# Step 3：聚合 + 写报告
python aggregate.py
```

## 💰 成本估算

- 输入 prompt（系统提示 + 新闻）：~600 tokens（其中 ~500 是缓存的系统提示）
- 输出（结构化 JSON）：~200 tokens
- Claude Opus 4.7：$5/M input + $25/M output

每条新闻约：
- 第 1 条（缓存写）：500 × 1.25 + 100 + 200 × 25 = $0.0083
- 后续条（缓存读）：500 × 0.1 + 100 + 200 × 25 = $0.0058

**203 条新闻总成本：**
- Claude Opus 4.7（默认，最准）: ~$1.20
- Claude Sonnet 4.6（推荐性价比）: ~$0.72
- Claude Haiku 4.5（最便宜，结构化任务够用）: ~$0.24

**先小规模 + 用 Haiku 试一下：**
```bash
LIMIT=10 CLAUDE_MODEL=claude-haiku-4-5 python extract_sentiment.py
```

10 条 × Haiku 大概 1 美分。先验证 pipeline 跑通，再决定要不要全跑 + 用什么模型。

## 🎯 为什么这套设计

按 AAAI/arXiv 论文综述里多次验证的结论：
1. **新闻+价格融合显著优于纯价格**（论文佐证：FinAgent, MountainLion, ECHO-GL）
2. **结构化输出 > 自由文本**（学术 FinLLM 用 Pydantic/JSON Schema 做下游建模）
3. **Prompt caching 是必备的**：系统提示重复 → 90% 折扣
4. **置信度 + 时间窗口 → 风险加权**：不是所有信号同等重要

## 🔧 后续扩展

输出 `news_analyzed.json` 可以直接喂给：
- **XGBoost / LightGBM**：把 sentiment、confidence、event_type one-hot 当特征 + 价格特征做方向预测
- **每日定时任务**：cron + Telegram bot 推送高置信度信号
- **回测**：按 horizon 字段分组，计算每个方向预期对应的次日 / 5日 / 4周收益
