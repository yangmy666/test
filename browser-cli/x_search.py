"""X (Twitter) 美股推文聚合搜索（按浏览量排序）。

- 多关键词搜索（中英混合）
- 用 since:YYYY-MM-DD 操作符过滤近 3 天
- 按 views 降序
"""
import sys
import time
import json
import re
from datetime import datetime, timedelta
from urllib.parse import quote

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

TODAY = datetime(2026, 4, 27)
THREE_DAYS_AGO = (TODAY - timedelta(days=3)).strftime("%Y-%m-%d")

KEYWORDS = [
    "美股",
    "纳斯达克",
    "特斯拉",
    "英伟达",
    "Mag 7 earnings",
    "Tesla earnings",
    "$TSLA",
    "$NVDA",
    "$SPY",
    "$QQQ",
    "Fed Powell",
    "stock market",
]

EXTRACT_JS = """
() => {
  const tweets = document.querySelectorAll('article[data-testid="tweet"]');
  return Array.from(tweets).map(t => {
    const userName = t.querySelector('[data-testid="User-Name"]')?.textContent || '';
    const text = t.querySelector('[data-testid="tweetText"]')?.textContent || '';
    const stats = {};
    ['reply','retweet','like','bookmark'].forEach(k => {
      const el = t.querySelector('[data-testid="' + k + '"]');
      stats[k] = el?.textContent.trim() || '';
    });
    // 浏览量：找 /analytics 的链接
    const viewA = Array.from(t.querySelectorAll('a')).find(a => a.href.includes('/analytics'));
    const viewsText = viewA?.textContent.trim() || '';
    const viewsLabel = viewA?.getAttribute('aria-label') || '';
    const timeEl = t.querySelector('time');
    const statusLink = t.querySelector('a[href*="/status/"]');
    return {
      userName: userName.slice(0, 200),
      text: text.slice(0, 1000),
      reply: stats.reply,
      retweet: stats.retweet,
      like: stats.like,
      views_text: viewsText,
      views_label: viewsLabel,
      time_iso: timeEl?.getAttribute('datetime'),
      status_url: statusLink?.href,
    };
  });
}
"""


def parse_count(s):
    """e.g. '1,941' -> 1941, '1.2K' -> 1200, '5万' -> 50000"""
    if not s:
        return 0
    s = str(s).strip().replace(",", "").replace("，", "")
    m = re.match(r"^([\d.]+)\s*([KMBkmb万千])?", s)
    if not m:
        return 0
    n = float(m.group(1))
    u = (m.group(2) or "").upper()
    mult = {"K": 1000, "M": 1000000, "B": 1e9, "万": 10000, "千": 1000}.get(u, 1)
    return int(n * mult)


def parse_time_iso(s):
    if not s:
        return None
    try:
        # ISO format: 2026-04-27T00:27:26.000Z
        s = s.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s).replace(tzinfo=None)
        return dt
    except Exception:
        return None


def main():
    t0 = time.time()
    all_tweets = {}

    with attach() as (pw, browser, ctx):
        page = ctx.new_page()
        for kw in KEYWORDS:
            kw_t0 = time.time()
            q = f"{kw} since:{THREE_DAYS_AGO}"
            url = f"https://x.com/search?q={quote(q)}&f=top"
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(3)
                # 滚动加载多条
                for _ in range(8):
                    page.evaluate("window.scrollBy(0, 2000)")
                    time.sleep(0.7)

                tweets = page.evaluate(EXTRACT_JS)
            except Exception as e:
                print(f"  [{kw}] 失败: {str(e)[:100]}", file=sys.stderr)
                continue

            added = 0
            for t in tweets:
                surl = t.get("status_url")
                if not surl or surl in all_tweets:
                    continue
                t["views_n"] = parse_count(t.get("views_text", ""))
                t["like_n"] = parse_count(t.get("like", ""))
                t["reply_n"] = parse_count(t.get("reply", ""))
                t["retweet_n"] = parse_count(t.get("retweet", ""))
                t["time_dt"] = parse_time_iso(t.get("time_iso"))
                all_tweets[surl] = t
                added += 1
            print(f"  [{kw}] +{added} (累计 {len(all_tweets)}, {time.time()-kw_t0:.1f}s)", file=sys.stderr)

        page.close()

    # 过滤 3 天内
    filtered = []
    for url, t in all_tweets.items():
        dt = t.get("time_dt")
        if not dt:
            continue
        age_h = (TODAY - dt).total_seconds() / 3600
        if age_h > 72:
            continue
        t["age_h"] = round(age_h, 1)
        # 把 datetime 转成字符串方便序列化
        t["time_dt"] = dt.isoformat()
        filtered.append(t)

    filtered.sort(key=lambda x: x["views_n"], reverse=True)

    print(f"\n3 天内: {len(filtered)} 条 / 总: {len(all_tweets)}, 耗时 {time.time()-t0:.1f}s", file=sys.stderr)

    out_path = "C:/Users/yang/desktop/test_project/browser-cli/x_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    print(f"  存到 {out_path}", file=sys.stderr)

    # 输出 Top 10
    print(json.dumps(filtered[:10], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
