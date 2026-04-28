"""探测抖音视频页评论区子回复结构和展开按钮。"""
import sys, time
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

URL = 'https://www.douyin.com/video/7633026723517845934'  # #1 5044 likes

PROBE = r"""
() => {
  const sels = {
    'comment-item': '[data-e2e="comment-item"]',
    'reply-item': '[data-e2e="reply-item"]',
    'comment-reply-item': '[data-e2e="comment-reply-item"]',
    'comment-list': '[data-e2e="comment-list"]',
  };
  const out = {counts: {}, expandSamples: []};
  for (const [k, s] of Object.entries(sels)) {
    out.counts[k] = document.querySelectorAll(s).length;
  }
  // 找展开按钮：包含 "条回复" / "展开" 等
  const items = document.querySelectorAll('[data-e2e="comment-item"]');
  for (const it of Array.from(items).slice(0, 20)) {
    const buttons = it.querySelectorAll('span, div, button');
    for (const b of buttons) {
      if (b.children.length > 1) continue;
      const t = (b.innerText || b.textContent || '').trim();
      if (!t) continue;
      if (/展开\d*条回复|展开 \d+ 条回复|查看\d+条回复|更多回复|条回复$/.test(t) && t.length < 30) {
        out.expandSamples.push({tag: b.tagName, cls: (b.className || '').slice(0, 80), text: t});
        break;
      }
    }
    if (out.expandSamples.length >= 5) break;
  }
  return out;
}
"""

with attach() as (pw, browser, ctx):
    page = ctx.pages[0]
    page.goto(URL, wait_until='domcontentloaded', timeout=25000)
    time.sleep(4)
    # 滚动以触发评论加载
    for _ in range(8):
        page.evaluate("window.scrollBy(0, 1000)")
        time.sleep(0.7)
    info = page.evaluate(PROBE)
    import json
    print(json.dumps(info, ensure_ascii=False, indent=2))
