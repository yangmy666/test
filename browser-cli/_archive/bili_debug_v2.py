"""调试视频 #2 为什么拿到 0 条评论。"""
import sys, time, json
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

URL = 'https://www.bilibili.com/video/BV1wCofB7ERY/'

EXTRACT_JS = r"""
() => {
  const SKIP_TAGS = new Set(['STYLE','SCRIPT','SVG','BILI-AVATAR',
    'BILI-COMMENT-USER-SAILING-CARD','BILI-COMMENT-PICTURES-RENDERER',
    'BILI-COMMENT-USER-MEDAL','BILI-COMMENT-MENU']);
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
  const counts = {threadRenderer:0, commentRenderer:0};
  let firstThreadText = '';
  for (const el of walk(document.body)) {
    const t = el.tagName?.toLowerCase();
    if (t === 'bili-comment-thread-renderer') {
      counts.threadRenderer++;
      if (counts.threadRenderer === 1) firstThreadText = deepText(el).slice(0,500);
    }
    if (t === 'bili-comment-renderer') counts.commentRenderer++;
  }
  // 还检查页面是否有"登录看更多"或评论被关闭
  const bodyText = document.body.innerText.slice(0, 2000);
  return {counts, firstThreadText, hasLogin: /登录后查看/.test(bodyText), title: document.title};
}
"""

with attach() as (pw, browser, ctx):
    # 用已有 tab，而不是 new_page。检查评论加载是否依赖既有 session 状态
    page = ctx.pages[0]
    print(f"existing tab: {page.url}")
    # 监听响应错误
    def on_response(resp):
        if 'reply' in resp.url or 'comment' in resp.url:
            print(f"  [resp] {resp.status} {resp.url[:120]}")
    page.on('response', on_response)
    page.goto(URL, wait_until='domcontentloaded', timeout=25000)
    print("loaded; waiting...")
    time.sleep(4)
    # 先把 bili-comments 直接滚到视野
    page.evaluate("""() => {
      const el = document.querySelector('bili-comments');
      if (el) el.scrollIntoView({behavior:'instant', block:'start'});
    }""")
    time.sleep(2)
    for i in range(20):
        page.evaluate("window.scrollBy(0, 1000)")
        time.sleep(0.8)
        info = page.evaluate(EXTRACT_JS)
        print(f"  scroll {i+1}: threads={info['counts']['threadRenderer']}")
    # 找评论区相关 DOM 元素
    comment_area_info = page.evaluate("""() => {
      // 老版评论区
      const oldArea = document.querySelector('#comment, .bb-comment, .comment-list');
      const oldCount = document.querySelectorAll('.list-item.reply-wrap, .reply-item').length;
      // 新版评论区组件
      const newArea = document.querySelector('bili-comments');
      // 看页面是否有 'iframe'
      const iframes = Array.from(document.querySelectorAll('iframe')).map(f => f.src);
      // 检查是否有"评论已关闭"
      const text = document.body.innerText;
      return {
        hasOldArea: !!oldArea,
        oldReplyCount: oldCount,
        hasNewComponent: !!newArea,
        iframes: iframes.slice(0,5),
        commentsClosed: /评论(关闭|不可见)/.test(text),
        hasLoadingHint: /加载中|Loading/i.test(text.slice(0, 5000)),
      };
    }""")
    print('\ncomment area:', json.dumps(comment_area_info, ensure_ascii=False, indent=2))
    page.close()
