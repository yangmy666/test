"""找艺画开天官方账号 + 检查最近动态。"""
import sys, time, json
from urllib.parse import quote

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

with attach() as (pw, browser, ctx):
    page = ctx.new_page()

    # 1. 搜索艺画开天的用户主页
    page.goto("https://search.bilibili.com/upuser?keyword=%E8%89%BA%E7%94%BB%E5%BC%80%E5%A4%A9", wait_until="domcontentloaded", timeout=20000)
    time.sleep(3)
    page.evaluate("window.scrollBy(0, 500)")
    time.sleep(1.5)

    users = page.evaluate(r"""() => {
      const cards = document.querySelectorAll('.user-list .user-item, [class*="user-item"], .bili-user-item');
      const allLinks = Array.from(document.querySelectorAll('a[href*="space.bilibili.com"]')).slice(0, 10).map(a => ({
        href: a.href,
        text: a.textContent.trim().slice(0, 60)
      }));
      return { allLinks };
    }""")
    print("UP 主搜索结果:")
    print(json.dumps(users, ensure_ascii=False, indent=2)[:2000])

    page.close()
