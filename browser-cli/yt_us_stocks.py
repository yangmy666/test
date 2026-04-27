"""三天内 YouTube 全站美股视频按播放量 Top N。

策略：多语言多关键词搜索 → 去重合并 → 美股相关性过滤 → 72h 过滤 → 播放量排序。
"""
import sys
import time
import json
import re
from urllib.parse import quote

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

KEYWORDS = [
    # 中文
    "美股", "美股财报", "美股分析",
    "纳斯达克", "标普500",
    "特斯拉财报", "英伟达",
    # 英文
    "US stocks", "stock market today", "Wall Street",
    "S&P 500", "NASDAQ today",
    "Tesla earnings", "NVIDIA stock",
    "Mag 7 earnings", "Fed",
]

US_STOCK_RE = re.compile(
    r"(美股|纳斯达克|标普|道琼|美国股|美联储|特斯拉|英伟达|苹果|谷歌|微软|亚马逊|"
    r"Meta|Tesla|NVIDIA|Apple|Google|Microsoft|Amazon|S&P|SP500|NASDAQ|Nasdaq|"
    r"Wall Street|US stock|stock market|Mag 7|magnificent 7|Fed |Powell|earnings|"
    r"TSLA|NVDA|AAPL|GOOG|MSFT|AMZN|META|AMD|INTC|TSM|UNH|PLTR|OKLO|"
    r"道琼斯|纳指|纳指100|QQQ|SPY)",
    re.IGNORECASE,
)


def parse_views(s):
    if not s:
        return 0
    s = s.replace(",", "").replace("，", "")
    m = re.search(r"([\d.]+)\s*([万亿])", s)
    if m:
        n = float(m.group(1))
        return int(n * (10000 if m.group(2) == "万" else 100000000))
    m = re.search(r"([\d.]+)\s*([KMB])", s, re.IGNORECASE)
    if m:
        n = float(m.group(1))
        unit = m.group(2).upper()
        mult = {"K": 1000, "M": 1000000, "B": 1000000000}[unit]
        return int(n * mult)
    m = re.search(r"([\d.]+)", s)
    return int(float(m.group(1))) if m else 0


def parse_age_hours(s):
    if not s:
        return None
    s = s.lower()
    if any(x in s for x in ["分钟", "minute", " min"]):
        m = re.search(r"(\d+)", s); return float(m.group(1)) / 60 if m else None
    if any(x in s for x in ["小时", "小時", "hour", " hr"]):
        m = re.search(r"(\d+)", s); return float(m.group(1)) if m else None
    if any(x in s for x in ["天", "day"]):
        m = re.search(r"(\d+)", s); return float(m.group(1)) * 24 if m else None
    if any(x in s for x in ["周", "week"]):
        m = re.search(r"(\d+)", s); return float(m.group(1)) * 168 if m else None
    return None


t0 = time.time()
all_videos = {}

with attach() as (pw, browser, ctx):
    page = ctx.new_page()

    for kw in KEYWORDS:
        kw_t0 = time.time()
        url = f"https://www.youtube.com/results?search_query={quote(kw)}&sp=CAISBAgCEAE%253D"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_selector("ytd-video-renderer", timeout=8000)
        except Exception as e:
            print(f"  [跳过] {kw}: {e}", file=sys.stderr)
            continue

        for _ in range(4):
            page.evaluate("window.scrollBy(0, 3000)")
            time.sleep(0.35)

        raw = page.evaluate(
            """
            () => Array.from(document.querySelectorAll('ytd-video-renderer')).map(v => {
              const t = v.querySelector('a#video-title');
              const c = v.querySelector('ytd-channel-name a');
              const m = v.querySelectorAll('#metadata-line span');
              const d = v.querySelector('ytd-thumbnail-overlay-time-status-renderer span, .badge-shape-wiz__text');
              return {
                title: t?.title || t?.textContent?.trim(),
                url: t?.href,
                channel: c?.textContent?.trim(),
                views: m[0]?.textContent?.trim(),
                uploaded: m[1]?.textContent?.trim(),
                duration: d?.textContent?.trim(),
              };
            })
            """
        )

        added = 0
        for v in raw:
            if not v["url"] or not v["title"]:
                continue
            mid = re.search(r"v=([^&]+)", v["url"])
            if not mid:
                continue
            vid = mid.group(1)
            if vid in all_videos:
                continue
            all_videos[vid] = v
            added += 1

        print(f"  {kw}: +{added} ({time.time()-kw_t0:.1f}s, 累计 {len(all_videos)})", file=sys.stderr)

    page.close()

filtered = []
for vid, v in all_videos.items():
    age = parse_age_hours(v.get("uploaded"))
    views = parse_views(v.get("views"))
    if age is None or age > 72:
        continue
    text = f"{v.get('title','')} {v.get('channel','')}"
    if not US_STOCK_RE.search(text):
        continue
    v["view_n"] = views
    v["age_h"] = age
    filtered.append(v)

filtered.sort(key=lambda x: x["view_n"], reverse=True)

print(
    f"\n总耗时: {time.time()-t0:.1f}s | 唯一视频: {len(all_videos)} | 美股相关+3天内: {len(filtered)}",
    file=sys.stderr,
)

print(json.dumps(filtered[:20], ensure_ascii=False, indent=2))
