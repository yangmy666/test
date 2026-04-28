"""B 站搜索：近 3 天 A 股相关视频，按播放量排序。"""
import sys, time, json, re
from urllib.parse import quote
from datetime import datetime

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

KEYWORDS = [
    "A股",
    "A股大盘",
    "A股复盘",
    "A股分析",
    "上证指数",
    "上证",
    "沪指",
    "创业板",
    "科创板",
    "沪深300",
    "中证500",
    "涨停",
    "跌停",
    "北向资金",
    "茅台",
    "宁德时代",
    "比亚迪",
    "板块轮动",
    "国企改革",
]

now = int(time.time())
three_days_ago = now - 3 * 86400

EXTRACT_JS = r"""
() => {
  const cards = document.querySelectorAll('div.bili-video-card');
  return Array.from(cards).map(c => {
    const titleEl = c.querySelector('.bili-video-card__info--tit');
    const title = titleEl?.title?.trim() || titleEl?.innerText?.trim();
    const link = c.querySelector('a[href*="/video/"]');
    const stats = Array.from(c.querySelectorAll('.bili-video-card__stats--item'))
      .map(s => s.innerText.trim());
    const owner = c.querySelector('.bili-video-card__info--author')?.innerText?.trim();
    const dateText = c.querySelector('.bili-video-card__info--date')?.innerText?.trim();
    const duration = c.querySelector('.bili-video-card__stats__duration')?.innerText?.trim();
    return {
      title: title?.slice(0, 200),
      url: link?.href,
      author: owner?.slice(0, 80),
      play_text: stats[0] || '',
      danmu_text: stats[1] || '',
      date: dateText,
      duration,
    };
  }).filter(c => c.title);
}
"""

def parse_play_count(s: str) -> int:
    if not s: return 0
    s = s.strip().replace(',', '')
    m = re.search(r'(\d+(?:\.\d+)?)\s*(万|亿)?', s)
    if not m: return 0
    n = float(m.group(1)); unit = m.group(2)
    if unit == '万': n *= 10000
    elif unit == '亿': n *= 100000000
    return int(n)

def extract_bv(url: str) -> str:
    m = re.search(r'/video/(BV[\w]+)', url or '')
    return m.group(1) if m else ''

def main():
    t0 = time.time()
    all_videos = {}
    with attach() as (pw, browser, ctx):
        page = ctx.pages[0]  # 用现有 tab，避免 new_page 反爬
        for kw in KEYWORDS:
            kw_t0 = time.time()
            url = (f"https://search.bilibili.com/video?keyword={quote(kw)}"
                   f"&order=click&pubtime_begin_s={three_days_ago}&pubtime_end_s={now}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                time.sleep(2.8)
                for _ in range(2):
                    page.evaluate("window.scrollBy(0, 1800)")
                    time.sleep(0.6)
                videos = page.evaluate(EXTRACT_JS)
            except Exception as e:
                print(f"  [{kw}] 失败: {str(e)[:100]}", file=sys.stderr); continue

            added = 0
            for v in videos:
                bv = extract_bv(v.get('url'))
                if not bv: continue
                v['play_count'] = parse_play_count(v.get('play_text', ''))
                v['bv'] = bv
                v['matched_keyword'] = kw
                if bv not in all_videos or v['play_count'] > all_videos[bv].get('play_count', 0):
                    all_videos[bv] = v
                    added += 1
            print(f"  [{kw}] +{added}, 总 {len(all_videos)}, {time.time()-kw_t0:.1f}s", file=sys.stderr)

    videos = sorted(all_videos.values(), key=lambda v: v['play_count'], reverse=True)
    out_path = "C:/Users/yang/desktop/test_project/browser-cli/bili_a_search.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "fetched_at": datetime.now().isoformat(),
            "window_days": 3,
            "total": len(videos),
            "videos": videos,
        }, f, ensure_ascii=False, indent=2)

    print(f"\n=== 总抓 {len(videos)} 条，按播放量 Top 25 ===")
    for v in videos[:25]:
        print(f"  {v['play_count']:>8}  {v['title'][:60]}")
        print(f"           {v['author']} | {v['date']} | {v['url']}")
    print(f"\n耗时 {time.time()-t0:.1f}s, 输出 {out_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
