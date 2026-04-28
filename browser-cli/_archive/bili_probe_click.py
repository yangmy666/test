"""探测 '共N条回复' 元素的真实结构和点击目标。"""
import sys, time
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

URL = 'https://www.bilibili.com/video/BV1iqoZBaE5Z/'

PROBE = r"""
() => {
  function* walk(root, vis) {
    if (vis.has(root)) return;
    vis.add(root); yield root;
    if (root.shadowRoot) for (const c of root.shadowRoot.querySelectorAll('*')) if (!vis.has(c)) yield* walk(c, vis);
    for (const c of (root.children || [])) if (!vis.has(c)) yield* walk(c, vis);
  }
  const out = [];
  for (const el of walk(document.body, new Set())) {
    const tag = el.tagName?.toLowerCase();
    if (!tag || tag === 'style' || tag === 'script') continue;
    const txt = (el.innerText || el.textContent || '').trim();
    if (!txt) continue;
    if (!/点击查看|查看更多/.test(txt)) continue;
    if (txt.length > 30) continue;
    const childMatches = Array.from(el.children || []).some(c => /点击查看|查看更多/.test((c.innerText||c.textContent||'')));
    if (childMatches) continue;
    out.push({
      tag, cls: (el.className && typeof el.className === 'string') ? el.className.slice(0,80) : '',
      text: txt.slice(0, 60),
      role: el.getAttribute?.('role') || '',
      cursor: getComputedStyle(el).cursor,
      hasClickAttr: el.hasAttribute?.('@click') || el.hasAttribute?.('onclick') || false,
      parentTag: el.parentElement?.tagName?.toLowerCase() || '',
      parentCls: (el.parentElement?.className && typeof el.parentElement.className === 'string') ? el.parentElement.className.slice(0,80) : '',
    });
    if (out.length >= 8) break;
  }
  return out;
}
"""

with attach() as (pw, browser, ctx):
    page = ctx.pages[0]
    page.goto(URL, wait_until='domcontentloaded', timeout=30000)
    time.sleep(3)
    page.evaluate("""() => { const el = document.querySelector('bili-comments'); if (el) el.scrollIntoView();}""")
    time.sleep(2)
    for _ in range(15):
        page.evaluate("window.scrollBy(0,1000)")
        time.sleep(0.6)
    info = page.evaluate(PROBE)
    import json
    print(json.dumps(info, ensure_ascii=False, indent=2))
