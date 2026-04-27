"""B 站搜索：灵笼/玲珑第三季发布时间。"""
import sys, time, json
from urllib.parse import quote

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

KEYWORDS = [
    "灵笼第三季",
    "灵笼第3季",
    "灵笼3",
    "灵笼 第三季 发布",
    "玲珑第3季",
    "玲珑第三季",
    "灵笼 季更",
]

EXTRACT_JS = r"""
() => {
  const cards = document.querySelectorAll('div.bili-video-card');
  return Array.from(cards).slice(0, 25).map(c => {
    const titleEl = c.querySelector('.bili-video-card__info--tit, h3.bili-video-card__info--tit');
    const title = titleEl?.title || titleEl?.textContent?.trim() || c.querySelector('a')?.title;
    const link = c.querySelector('a[href*="/video/"]');
    const owner = c.querySelector('.bili-video-card__info--owner, .bili-video-card__info--author')?.textContent?.trim();
    const dateEl = c.querySelector('.bili-video-card__info--date');
    return {
      title: title?.slice(0, 200),
      url: link?.href,
      author: owner?.slice(0, 50),
      date: dateEl?.textContent?.trim(),
    };
  }).filter(c => c.title);
}
"""

results = []
seen = set()
with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    for kw in KEYWORDS:
        url = f"https://search.bilibili.com/video?keyword={quote(kw)}&order=pubdate"
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(2.5)
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(1)
        videos = page.evaluate(EXTRACT_JS)
        added = 0
        for v in videos:
            u = v.get("url")
            if not u or u in seen: continue
            seen.add(u)
            v["kw"] = kw
            results.append(v)
            added += 1
        print(f"  [{kw}] +{added}", file=sys.stderr)
    page.close()

# 按"含'第三季'/'3'/'更新'/'发布'/'2026'"过滤
print(f"\n总抓 {len(results)} 个视频")
print("\n=== 含'第三季'/'第 3 季'/'灵笼 3' 关键词 ===")
for v in results:
    t = v.get("title", "").lower()
    if any(k in t for k in ["第三季", "第3季", "三季", "s3", "灵笼3", "灵笼 3"]):
        print(f"  [{v.get('date','')}] {v.get('title','')[:120]}")
        print(f"    {v.get('author','')} | {v['url']}")

print("\n=== 时间相关（pv/预告/官宣/发布/2026/2025）===")
for v in results:
    t = v.get("title", "").lower()
    if any(k in t for k in ["预告","官宣","发布","上线","定档","pv","2026","2025"]) and "灵笼" in t:
        print(f"  [{v.get('date','')}] {v.get('title','')[:120]}")
        print(f"    {v['url']}")

print("\n=== 全部前 30（最新）===")
results.sort(key=lambda x: x.get("date") or "", reverse=True)
for v in results[:30]:
    print(f"  [{v.get('date','')}] {v.get('title','')[:100]}")
