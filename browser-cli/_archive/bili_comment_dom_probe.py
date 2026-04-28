"""探测 B站视频页评论 DOM 结构（含 shadow DOM）。"""
import sys, time
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

URL = 'https://www.bilibili.com/video/BV1YCovBFE88/'  # 巴菲特五次关键操作

PROBE_JS = r"""
() => {
  // 找出所有 bili-comment-renderer，看其 shadowRoot 内结构
  function* walkAll(root) {
    yield root;
    if (root.shadowRoot) for (const c of root.shadowRoot.querySelectorAll('*')) yield* walkAll(c);
    for (const c of (root.children || [])) yield* walkAll(c);
  }
  const out = {threads: []};
  let i = 0;
  for (const el of walkAll(document.body)) {
    if (++i > 50000) break;
    if (el.tagName?.toLowerCase() === 'bili-comment-thread-renderer') {
      // 直接抓 thread 自己的 innerText（深穿透 shadow DOM）
      // 但 innerText 不会穿透 shadow，得手动拼
      function gatherText(node, depth=0) {
        if (depth > 8) return '';
        let t = '';
        if (node.shadowRoot) {
          for (const c of node.shadowRoot.children) t += gatherText(c, depth+1) + '\n';
        }
        for (const c of (node.children || [])) t += gatherText(c, depth+1) + '\n';
        if (node.nodeType === 3) t += node.textContent;
        // 直接拼 innerText 也行
        if (node.tagName === 'BILI-RICH-TEXT' || node.tagName === 'SPAN' || node.tagName === 'DIV') {
          if (node.children?.length === 0 && node.textContent) {
            t += node.textContent;
          }
        }
        return t;
      }
      const allText = (el.innerText || el.textContent || '').slice(0, 0); // empty since shadow
      // 用 querySelector 试图找到用户 + 内容 + 点赞
      function pierce(root, selector) {
        const r = [];
        function walk(n) {
          if (n.shadowRoot) {
            r.push(...n.shadowRoot.querySelectorAll(selector));
            for (const c of n.shadowRoot.children) walk(c);
          }
          for (const c of (n.children||[])) walk(c);
        }
        walk(root);
        return r;
      }
      const userInfos = pierce(el, '.user-name, .name, [class*="user-name"]');
      const richTexts = pierce(el, 'bili-rich-text, [class*="content"], [class*="rich-text"]');
      const likeBtns = pierce(el, '[class*="like"]');
      out.threads.push({
        userInfos: userInfos.slice(0,3).map(u => (u.innerText || u.textContent || '').slice(0,80)),
        contents: richTexts.slice(0,3).map(c => (c.innerText || c.textContent || '').slice(0,300)),
        likes: likeBtns.slice(0,5).map(l => (l.innerText || l.textContent || '').slice(0,30)),
      });
      if (out.threads.length >= 3) break;
    }
  }
  return out;
}
"""

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    page.goto(URL, wait_until='domcontentloaded', timeout=25000)
    time.sleep(3)
    # 滚到评论区让其加载
    # 反复滚动，确保评论加载
    for _ in range(8):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(0.8)
    time.sleep(3)
    info = page.evaluate(PROBE_JS)
    page.close()
    import json
    print(json.dumps(info, ensure_ascii=False, indent=2)[:5000])
