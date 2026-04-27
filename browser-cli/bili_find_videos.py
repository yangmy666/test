"""通过搜索从 4 月相关高播放量视频里找出 BV 号。"""
import sys, time, json
from urllib.parse import quote

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

# 找几个我看到的关键视频
TARGETS = [
    "艺画开天 CEO 白月魁",  # 那个 CEO 亲自回应的
    "灵笼3 并非 2026",  # 9.1万播放的辟谣
    "艺画开天",  # 官方账号
    "灵笼电影官宣",
]

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    for kw in TARGETS:
        url = f"https://search.bilibili.com/video?keyword={quote(kw)}&order=click"  # 按播放量
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(2.5)
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(1)
        videos = page.evaluate(r"""() => {
          return Array.from(document.querySelectorAll('div.bili-video-card')).slice(0, 8).map(c => {
            const titleEl = c.querySelector('.bili-video-card__info--tit');
            const link = c.querySelector('a[href*="/video/"]');
            const stats = c.querySelectorAll('.bili-video-card__stats--text');
            const owner = c.querySelector('.bili-video-card__info--owner')?.textContent?.trim();
            const date = c.querySelector('.bili-video-card__info--date')?.textContent?.trim();
            return {
              title: titleEl?.title || titleEl?.textContent?.trim(),
              url: link?.href,
              author: owner?.slice(0, 50),
              date,
              views: Array.from(stats).map(s => s.textContent.trim())
            };
          });
        }""")
        print(f"\n=== {kw} ===")
        for v in videos:
            if v.get("title"):
                print(f"  [{v.get('date','')}] {v['title'][:90]}")
                print(f"    👤 {v.get('author','')} | views: {v.get('views',[])} | {v.get('url','')}")
    page.close()
