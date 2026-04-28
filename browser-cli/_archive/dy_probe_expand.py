"""探测抖音"展开N条回复" 真正可点击元素的位置/父链。"""
import sys, time
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

URL = 'https://www.douyin.com/video/7633026723517845934'

PROBE = r"""
() => {
  const list = document.querySelector('[data-e2e="comment-list"]') || document.body;
  const out = [];
  for (const el of list.querySelectorAll('span')) {
    const t = (el.innerText || el.textContent || '').trim();
    if (!t) continue;
    if (!/展开\s*\d+\s*条回复/.test(t) || t.length > 30) continue;
    // 收集 6 级父链信息
    const chain = [];
    let p = el;
    for (let i = 0; i < 6 && p; i++) {
      const cs = getComputedStyle(p);
      chain.push({
        tag: p.tagName,
        cls: (p.className && typeof p.className === 'string') ? p.className.slice(0,80) : '',
        cursor: cs.cursor,
        role: p.getAttribute?.('role') || '',
        e2e: p.getAttribute?.('data-e2e') || '',
        clickAttrs: ['onclick', '@click'].filter(a => p.hasAttribute?.(a)),
      });
      p = p.parentElement;
    }
    out.push({text: t, chain});
    if (out.length >= 4) break;
  }
  return out;
}
"""

with attach() as (pw, browser, ctx):
    page = ctx.pages[0]
    page.goto(URL, wait_until='domcontentloaded', timeout=25000)
    time.sleep(4)
    for _ in range(8):
        page.evaluate("window.scrollBy(0,1000)")
        time.sleep(0.7)
    info = page.evaluate(PROBE)
    import json
    print(json.dumps(info, ensure_ascii=False, indent=2))
