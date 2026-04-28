"""点击展开按钮后，看 DOM 中实际新增的元素是什么。"""
import sys, time
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

URL = 'https://www.douyin.com/video/7633026723517845934'

with attach() as (pw, browser, ctx):
    page = ctx.pages[0]
    page.goto(URL, wait_until='domcontentloaded', timeout=25000)
    time.sleep(4)
    for _ in range(5):
        page.evaluate("window.scrollBy(0,1500)")
        time.sleep(0.6)

    # 用 Playwright locator 真实点击第一个展开按钮
    btn = page.locator('button.comment-reply-expand-btn').first
    cnt = page.locator('button.comment-reply-expand-btn').count()
    print(f'expand buttons: {cnt}')
    if cnt > 0:
        try:
            btn.scroll_into_view_if_needed(timeout=3000)
            btn.click(timeout=5000)
            print('clicked first button')
        except Exception as e:
            print(f'click failed: {e}')
        time.sleep(2.5)

    # 滚动以再触发更多内容
    for _ in range(8):
        page.evaluate("window.scrollBy(0,1500)")
        time.sleep(0.5)
    # 等等
    time.sleep(2)
    # 看 .replyContainer 里有什么
    info2 = page.evaluate(r"""() => {
      const cs = document.querySelectorAll('[class*="replyContainer"]');
      const out = [];
      for (const c of Array.from(cs).slice(0,2)) {
        // 子项数量 + 第一项 outerHTML 截断
        const children = Array.from(c.children).slice(0,3).map(ch => ({
          tag: ch.tagName,
          cls: (typeof ch.className === 'string' ? ch.className : '').slice(0, 80),
          e2e: ch.getAttribute('data-e2e') || '',
          textPreview: (ch.innerText || '').slice(0, 100),
        }));
        out.push({cls: c.className, childCount: c.children.length, children});
      }
      return out;
    }""")
    import json
    print('replyContainer probe:')
    print(json.dumps(info2, ensure_ascii=False, indent=2))
    print('\n=== full data-e2e + className ===')

    # 看 DOM 中所有 data-e2e 属性的统计
    info = page.evaluate(r"""() => {
      const counts = {};
      document.querySelectorAll('[data-e2e]').forEach(el => {
        const v = el.getAttribute('data-e2e');
        counts[v] = (counts[v] || 0) + 1;
      });
      // 也找一下"回复" / "reply" / "comment" 相关的 className
      const cls = {};
      document.querySelectorAll('div, span').forEach(el => {
        const c = (typeof el.className === 'string') ? el.className : '';
        if (c && /reply|Reply|REPLY/.test(c)) cls[c] = (cls[c] || 0) + 1;
      });
      const topCls = Object.entries(cls).sort((a,b) => b[1]-a[1]).slice(0, 15);
      return {counts, topCls};
    }""")
    import json
    print(json.dumps(info, ensure_ascii=False, indent=2))
