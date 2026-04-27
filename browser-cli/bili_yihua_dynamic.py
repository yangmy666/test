"""读艺画开天官号最近的动态和视频。"""
import sys, time, json
sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

UID = "14328316"

with attach() as (pw, browser, ctx):
    page = ctx.new_page()

    # 1. 投稿视频
    print("=== 视频投稿 ===")
    page.goto(f"https://space.bilibili.com/{UID}/upload/video", wait_until="domcontentloaded", timeout=20000)
    time.sleep(4)
    page.evaluate("window.scrollBy(0, 800)")
    time.sleep(1.5)
    videos = page.evaluate(r"""() => {
      const items = document.querySelectorAll('.bili-video-card, [class*="video-card"], .small-item, .list-item');
      const results = [];
      // 也找通用 a 链接
      const links = document.querySelectorAll('a[href*="/video/BV"]');
      const seen = new Set();
      for (const a of links) {
        const bv = a.href.match(/BV[a-zA-Z0-9]+/)?.[0];
        if (!bv || seen.has(bv)) continue;
        seen.add(bv);
        const card = a.closest('.bili-video-card, [class*="video-card"], .small-item, .list-item') || a;
        const text = card.textContent.trim().slice(0, 200);
        if (results.length < 20) results.push({ bv, href: a.href, text });
      }
      return results;
    }""")
    for v in videos[:15]:
        print(f"  · {v['text'][:120]}")
        print(f"    {v['href']}")

    # 2. 动态
    print("\n=== 动态 ===")
    page.goto(f"https://space.bilibili.com/{UID}/dynamic", wait_until="domcontentloaded", timeout=20000)
    time.sleep(5)
    page.evaluate("window.scrollBy(0, 1500)")
    time.sleep(2)
    dynamics = page.evaluate(r"""() => {
      // 动态卡片
      const cards = document.querySelectorAll('.bili-dyn-list .bili-dyn-list__item, [class*="dyn-card"], .list-item');
      const results = [];
      for (const c of cards) {
        const text = c.textContent.trim().slice(0, 500);
        if (text && results.length < 15) results.push({ text });
      }
      // 备份：通用文本扫描
      if (results.length === 0) {
        const all = document.querySelectorAll('*');
        for (const e of all) {
          const t = e.textContent;
          if (e.children.length === 1 && t && t.length > 30 && t.length < 500 && /灵笼|第三季|2026|大电影/.test(t)) {
            results.push({ text: t.slice(0, 300) });
            if (results.length >= 10) break;
          }
        }
      }
      return results;
    }""")
    if dynamics:
        for d in dynamics:
            print(f"  · {d['text'][:300]}")
    else:
        print("  (没拿到动态内容)")

    page.close()
