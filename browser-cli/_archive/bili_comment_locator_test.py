"""测试 Playwright locator 是否能穿透 bili-comment-thread-renderer 的 shadow DOM。"""
import sys, time
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    page.goto('https://www.bilibili.com/video/BV1YCovBFE88/', wait_until='domcontentloaded', timeout=25000)
    time.sleep(3)
    for _ in range(8):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(0.6)
    time.sleep(2)

    DEEP_JS = r"""
() => {
  const SKIP_TAGS = new Set(['STYLE','SCRIPT','SVG','BILI-AVATAR','BILI-COMMENT-USER-SAILING-CARD','BILI-COMMENT-PICTURES-RENDERER','BILI-COMMENT-USER-MEDAL','BILI-COMMENT-MENU']);
  function deepText(node) {
    if (!node) return '';
    if (node.nodeType === 3) return node.textContent;
    if (SKIP_TAGS.has(node.tagName)) return '';
    let s = '';
    if (node.shadowRoot) for (const c of node.shadowRoot.childNodes) s += deepText(c);
    for (const c of (node.childNodes || [])) s += deepText(c);
    return s;
  }
  function* walk(root) {
    yield root;
    if (root.shadowRoot) for (const c of root.shadowRoot.querySelectorAll('*')) yield* walk(c);
    for (const c of (root.children || [])) yield* walk(c);
  }
  const threads = [];
  let i = 0;
  for (const el of walk(document.body)) {
    if (++i > 80000) break;
    if (el.tagName?.toLowerCase() === 'bili-comment-thread-renderer') {
      threads.push(deepText(el).replace(/\s+/g,' ').trim().slice(0,800));
      if (threads.length >= 5) break;
    }
  }
  return threads;
}
"""
    samples = page.evaluate(DEEP_JS)
    print(f'samples: {len(samples)}')
    for i, s in enumerate(samples):
        print(f'\n=== thread {i} ===')
        print(s[:500])
    page.close()
