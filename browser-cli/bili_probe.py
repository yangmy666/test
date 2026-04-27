"""快速探测 B 站搜索结果 DOM。"""
import sys, time, json
sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
from connect import attach

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    # 搜"生存类游戏 2026"按最新上传
    page.goto("https://search.bilibili.com/video?keyword=%E7%94%9F%E5%AD%98%E7%B1%BB%E6%B8%B8%E6%88%8F%202026&order=pubdate", wait_until="domcontentloaded", timeout=20000)
    time.sleep(3)
    page.evaluate("window.scrollBy(0, 800)")
    time.sleep(1.5)

    info = page.evaluate("""
      () => {
        // 探测视频卡片选择器
        const candidates = [
          'div.bili-video-card',
          'div[class*="video-card"]',
          '.video-list-item',
          'a[href*="/video/BV"]',
        ];
        const counts = {};
        candidates.forEach(s => counts[s] = document.querySelectorAll(s).length);
        const card = document.querySelector('div.bili-video-card');
        if (!card) return { counts, none: true };
        return {
          counts,
          firstCardText: card.textContent.slice(0, 300),
          firstCardHTML: card.outerHTML.slice(0, 1500),
        };
      }
    """)
    print(json.dumps(info, ensure_ascii=False, indent=2)[:3500])
