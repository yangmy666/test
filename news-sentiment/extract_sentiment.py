"""用 Claude API 对新闻做结构化情绪+事件提取。

设计：
- 每条新闻单独调用，但用 prompt caching 缓存系统提示（重复指令 → 90% 折扣）
- 用 messages.parse() + Pydantic 强校验输出
- 失败/限速自动重试（SDK 内置）
- 输出 JSON，每条带：tickers, sentiment, event_type, confidence, direction, horizon, reasoning
"""
import sys, json, os, time
from pathlib import Path
from typing import Literal, Optional
from pydantic import BaseModel, Field

import anthropic

sys.stdout.reconfigure(encoding="utf-8")

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("❌ 请先设置 ANTHROPIC_API_KEY 环境变量。", file=sys.stderr)
    print("   方法：在 PowerShell 里运行 $env:ANTHROPIC_API_KEY=\"sk-ant-...\"", file=sys.stderr)
    print("   或者在 bash:    export ANTHROPIC_API_KEY='sk-ant-...'", file=sys.stderr)
    sys.exit(1)


# ============ Pydantic 模型 ============
class NewsAnalysis(BaseModel):
    tickers: list[str] = Field(
        description="所有被新闻提及的标的代码（如 TSLA, NVDA, SPY），大写"
    )
    sentiment: float = Field(
        description="整体情绪极性，-1 (极度负面) 到 +1 (极度正面)，0 表示中性",
        ge=-1.0, le=1.0,
    )
    event_type: Literal[
        "earnings",        # 财报相关
        "guidance",        # 业绩指引
        "M&A",             # 并购
        "product",         # 产品发布/更新
        "policy",          # 政策/监管
        "macro",           # 宏观经济
        "lawsuit",         # 诉讼/法律
        "executive",       # 高管变动
        "analyst",         # 分析师评级
        "rumor",            # 传闻
        "technical",       # 技术分析/价格行为
        "other",
    ]
    confidence: float = Field(
        description="对方向预期的信心度，0-1",
        ge=0.0, le=1.0,
    )
    direction: Literal["up", "down", "neutral"] = Field(
        description="基于此新闻，被提及主要标的的短期价格方向预期"
    )
    horizon: Literal["intraday", "short", "medium", "long"] = Field(
        description="预期方向的有效时间窗口：intraday (当日), short (1-5天), medium (1-4周), long (>1月)"
    )
    key_facts: list[str] = Field(
        description="新闻的 1-3 个关键事实（量化数字优先），简短",
        max_items=4,
    )
    reasoning: str = Field(
        description="一句话解释为什么是这个 sentiment + direction（≤80字）",
        max_length=200,
    )


SYSTEM_PROMPT = """你是一位资深量化研究员，专门把新闻转换成可机器使用的交易信号。
对每条新闻，你必须：
1. 提取所有提及的股票代码（大写）
2. 评估情绪极性 (-1 到 +1)：注意是**对该新闻提及的标的而言的**，不是新闻本身的语调
3. 分类事件类型
4. 评估你的预测信心度 (0-1)
5. 给出短期方向预期：up / down / neutral
6. 给出预期生效的时间窗口
7. 提取 1-3 个关键量化事实（具体数字优先）
8. 用一句话解释你的判断逻辑

注意原则：
- 财报"超预期但盘后跌"→ direction=down，因为市场实际反应；不要被表面利好欺骗
- "传闻/未证实/可能"类新闻 → confidence ≤ 0.5
- 大盘指数（SPY/QQQ）的新闻 → tickers 写指数代码
- 同一新闻可能多个标的，但 direction 是对**主要标的**的判断
- 如果新闻没有交易意义（纯八卦/新闻评论），event_type="other", direction="neutral", confidence ≤ 0.3"""


def main():
    in_path = Path("C:/Users/yang/desktop/test_project/news-sentiment/news_raw.json")
    out_path = Path("C:/Users/yang/desktop/test_project/news-sentiment/news_analyzed.json")

    with open(in_path, encoding="utf-8") as f:
        news = json.load(f)

    # 限制处理量（默认全跑；可改）
    LIMIT = int(os.environ.get("LIMIT", len(news)))
    news = news[:LIMIT]

    client = anthropic.Anthropic()
    MODEL = os.environ.get("CLAUDE_MODEL", "claude-opus-4-7")
    print(f"使用模型: {MODEL} | 处理 {len(news)} 条新闻", file=sys.stderr)

    results = []
    t0 = time.time()
    n_cache_hits = 0
    n_cache_writes = 0

    for i, n in enumerate(news, 1):
        try:
            response = client.messages.parse(
                model=MODEL,
                max_tokens=1024,
                system=[
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},  # 缓存系统提示
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Ticker hint: {n['ticker']}\n\n"
                            f"Title: {n['title']}\n\n"
                            f"Description: {n['description']}\n\n"
                            f"Published: {n['published']}"
                        ),
                    }
                ],
                output_format=NewsAnalysis,
            )

            analysis = response.parsed_output
            results.append({
                **n,
                "analysis": analysis.model_dump(),
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "cache_read": response.usage.cache_read_input_tokens,
                    "cache_write": response.usage.cache_creation_input_tokens,
                },
            })
            if response.usage.cache_read_input_tokens > 0:
                n_cache_hits += 1
            if response.usage.cache_creation_input_tokens > 0:
                n_cache_writes += 1

            elapsed = time.time() - t0
            print(
                f"  [{i}/{len(news)}] {n['ticker']:5s} | "
                f"sent={analysis.sentiment:+.2f} dir={analysis.direction:7s} "
                f"conf={analysis.confidence:.2f} {analysis.event_type:10s} | "
                f"{elapsed:.0f}s",
                file=sys.stderr,
            )

            # 每 10 条保存一次（防中断丢失）
            if i % 10 == 0:
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

        except anthropic.APIStatusError as e:
            print(f"  [{i}] API 错误: {e.message[:150]}", file=sys.stderr)
            results.append({**n, "error": str(e)[:300]})
        except Exception as e:
            print(f"  [{i}] 失败: {str(e)[:150]}", file=sys.stderr)
            results.append({**n, "error": str(e)[:300]})

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - t0
    success = sum(1 for r in results if "analysis" in r)
    print(
        f"\n✅ 完成 {success}/{len(news)} 成功 | {elapsed:.0f}s | "
        f"cache 命中 {n_cache_hits} 写入 {n_cache_writes}",
        file=sys.stderr,
    )
    print(f"   保存到 {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
