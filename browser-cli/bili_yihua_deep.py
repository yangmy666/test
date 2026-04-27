"""深挖艺画开天官号最近动态——滚动多次抓更多。"""
import sys, time, json, re
sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

UID = "14328316"

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    page.goto(f"https://space.bilibili.com/{UID}/dynamic", wait_until="domcontentloaded", timeout=20000)
    time.sleep(5)

    # 滚多次加载更多
    for _ in range(8):
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(1.5)

    # 抓所有动态卡片中的纯文本——不靠 class，靠日期格式定位
    info = page.evaluate(r"""() => {
      // 找含日期"YYYY年MM月DD日"或"刚刚/小时前"的元素，往上找父容器
      const all = Array.from(document.querySelectorAll('*'));
      const dynPosts = [];
      const dateRe = /(\d{4}年\d{1,2}月\d{1,2}日|\d+小时前|\d+分钟前|\d+天前|刚刚|昨天|前天)/;
      for (const el of all) {
        if (el.children.length !== 0) continue;
        const t = el.textContent.trim();
        if (dateRe.test(t) && t.length < 60) {
          // 找一个含足够文本的父容器
          let parent = el.parentElement;
          for (let i = 0; i < 6 && parent; i++) {
            if (parent.textContent.length > 50) break;
            parent = parent.parentElement;
          }
          if (parent && parent.textContent.length > 30 && dynPosts.length < 30) {
            const fullText = parent.textContent.replace(/\s+/g, ' ').trim().slice(0, 600);
            dynPosts.push({ date: t, text: fullText });
          }
        }
      }
      // 去重
      const seen = new Set();
      return dynPosts.filter(p => {
        const key = p.text.slice(0, 100);
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      }).slice(0, 20);
    }""")

    print(f"找到 {len(info)} 条带日期的动态文本片段:\n")
    for p in info:
        print(f"  📅 [{p['date']}]")
        print(f"  📝 {p['text'][:280]}")
        print()

    page.close()
