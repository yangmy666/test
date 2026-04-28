"""TikTok 评论全量抓取器（含子回复）— 参数化、可复用。

匿名状态可用：先点 [data-e2e="comment-icon"] 唤出评论侧栏，再滚动+展开子回复。

用法：
    python tt_comments_full.py <input.json> <output.json>

input.json 格式：[{"label": "...", "url": "https://www.tiktok.com/@x/video/123"}, ...]
output.json：键为 url，值含 main_count, sub_count, total_count, comments[]
"""
import sys, time, json
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from connect import attach

# 抓取所有评论（主+子）。TikTok 主楼用 data-e2e="comment-level-1"，子回复用 comment-level-2。
# 兼容老版本，也接 [data-e2e="comment-item"]。
EXTRACT_JS = r"""
() => {
  // TikTok 结构：[data-e2e="comment-level-1"] 是文本 span，要往上找 DivCommentItemWrapper
  function findWrapper(node) {
    let p = node.parentElement;
    for (let i = 0; i < 5 && p; i++) {
      const c = (typeof p.className === 'string') ? p.className : '';
      if (/DivCommentItemWrapper|CommentItemContainer/.test(c)) return p;
      p = p.parentElement;
    }
    return node.parentElement?.parentElement || node.parentElement;
  }

  function parseLikes(s) {
    if (!s) return 0;
    const m = s.match(/^([\d.]+)\s*([KMW万千BMG])?$/i);
    if (!m) return 0;
    let n = parseFloat(m[1]);
    const u = (m[2] || '').toUpperCase();
    if (u === 'K') n *= 1000;
    else if (u === 'M') n *= 1000000;
    else if (u === 'W' || s.endsWith('万')) n *= 10000;
    else if (u === 'B' || s.endsWith('B')) n *= 1000000000;
    return Math.round(n);
  }

  function parseItem(textNode, level) {
    const wrap = findWrapper(textNode);
    const text = (textNode.innerText || textNode.textContent || '').trim();
    if (!text) return null;
    if (!wrap) return {author: '', text, time_str: '', likes: 0, level};

    // 作者：包装内第一个 a[href*="/@"]
    const authorA = wrap.querySelector('a[href*="/@"]');
    const author = authorA?.innerText?.trim() || authorA?.textContent?.trim() || '';

    // 容器全文形如 "<author> <text> <time> 回复 <likes>" — 用结构解析
    const allText = (wrap.innerText || wrap.textContent || '').replace(/\s+/g, ' ').trim();

    // 时间：天前 / 小时前 / 分钟前 / X-X / YYYY-X-X / ago
    let time_str = '';
    const tm = allText.match(/(\d+\s*(?:分钟|小时|天|周|月|年)前|刚刚|昨天|前天|\d+\s*(?:minute|hour|day|week|month|year)s?\s+ago|hace\s+\d+|\d{1,2}-\d{1,2}|\d{4}-\d{1,2}-\d{1,2})/);
    if (tm) time_str = tm[1].trim();

    // 点赞：在容器里找最后一个纯数字（紧跟"回复"/"Reply"之后）
    let likes = 0;
    // 策略：找 "回复" 后的下一个数字 token
    const after = allText.split(/回复|Reply/i);
    if (after.length > 1) {
      const tail = after[after.length - 1].trim();
      const ln = tail.match(/^\s*([\d.]+\s*[KMW万千]?)/i);
      if (ln) likes = parseLikes(ln[1].replace(/\s/g,''));
    }
    if (!likes) {
      // fallback: 找容器内独立的数字 span
      for (const s of wrap.querySelectorAll('span, p, div')) {
        if (s.children.length > 0) continue;
        const t = (s.innerText || s.textContent || '').trim();
        if (/^\d+(\.\d+)?[KMW万千]?$/i.test(t) && t.length < 8 && !/前/.test(t)) {
          likes = parseLikes(t);
          if (likes > 0) break;
        }
      }
    }
    return {author, text, time_str, likes, level};
  }

  const mainSpans = Array.from(document.querySelectorAll('[data-e2e="comment-level-1"], [data-e2e="comment-item"]'));
  const subSpans = Array.from(document.querySelectorAll('[data-e2e="comment-level-2"], [data-e2e="comment-reply-item"]'));
  return {
    main: mainSpans.map(it => parseItem(it, 1)).filter(c => c && c.text.length > 1),
    sub:  subSpans.map(it => parseItem(it, 2)).filter(c => c && c.text.length > 1),
  };
}
"""

def dismiss_overlays(page):
    """关闭可能挡住操作的弹层（登录提示、cookie、follow promp 等）。"""
    page.evaluate(r"""() => {
      // 按 Esc 关弹层
      document.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape',code:'Escape',keyCode:27,which:27}));
      // 找各种关闭按钮
      const closeBtns = document.querySelectorAll('[aria-label*="close" i], [aria-label*="关闭"], [data-e2e*="close"], button[class*="close"], [class*="ModalCloseButton"], [class*="close-button"]');
      closeBtns.forEach(b => { try { b.click(); } catch(e) {} });
    }""")

def open_comment_panel(page, max_seconds=25):
    """点击评论图标唤出评论侧栏。匿名状态必须做这一步。多种 selector 重试。"""
    deadline = time.time() + max_seconds
    selectors = [
        '[data-e2e="comment-icon"]',
        '[data-e2e="comment-count"]',
        'button[aria-label*="omment"]',  # comment / Comment
        'button[aria-label*="评论"]',
    ]
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        # 先看评论是否已渲染
        cnt = page.evaluate('document.querySelectorAll(\'[data-e2e="comment-level-1"], [data-e2e="comment-item"]\').length')
        if cnt > 0: return cnt
        # 关弹层
        try: dismiss_overlays(page)
        except: pass
        # 滚一下确保元素可见
        try:
            page.evaluate("window.scrollBy(0, 100); window.scrollBy(0, -100);")
        except: pass
        # 依次试 selector
        clicked = False
        for sel in selectors:
            try:
                loc = page.locator(sel).first
                if loc.count() == 0: continue
                # scroll into view
                try: loc.scroll_into_view_if_needed(timeout=1000)
                except: pass
                if not loc.is_visible(timeout=800): continue
                loc.click(timeout=2500, force=False)
                clicked = True
                break
            except Exception: pass
        if not clicked:
            # 强力 fallback：JS click 所有可能的评论按钮
            try:
                page.evaluate(r"""() => {
                  const sels = ['[data-e2e="comment-icon"]','[data-e2e="comment-count"]','button[aria-label*="omment"]','button[aria-label*="评论"]'];
                  for (const sel of sels) {
                    const el = document.querySelector(sel);
                    if (el) { el.click(); el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window})); break; }
                  }
                }""")
            except: pass
        time.sleep(2)
    return 0

def scroll_comment_panel(page, max_iter=60):
    """滚动评论侧栏加载更多。"""
    prev = 0; stable = 0
    for _ in range(max_iter):
        page.evaluate("""() => {
          const sels = ['[data-e2e="comment-list"]', '[class*="CommentListContainer"]', '[class*="DivCommentListContainer"]'];
          for (const sel of sels) {
            const el = document.querySelector(sel);
            if (el) {
              let target = el;
              while (target && target.scrollHeight <= target.clientHeight + 10) target = target.parentElement;
              if (target) target.scrollBy(0, 1500);
            }
          }
          window.scrollBy(0, 600);
        }""")
        time.sleep(0.7)
        cur = page.evaluate('document.querySelectorAll(\'[data-e2e="comment-level-1"], [data-e2e="comment-item"]\').length')
        if cur == prev:
            stable += 1
            if stable >= 5: return cur
        else: stable = 0
        prev = cur
    return prev

def expand_sub_replies(page, max_rounds=12):
    """循环点击 '查看 N 条回复' 展开子回复。"""
    total_clicked = 0
    for _ in range(max_rounds):
        # 找所有展开子回复的按钮
        clicked = 0
        # 多种 selector：button/div/span 含"查看"或"View"或"View more replies"
        candidates = page.evaluate(r"""() => {
          if (!window.__tt_clicked) window.__tt_clicked = new WeakSet();
          const out = [];
          const root = document.body;
          for (const el of root.querySelectorAll('button, div, span, p')) {
            if (window.__tt_clicked.has(el)) continue;
            if (el.children.length > 1) continue;
            const t = (el.innerText || el.textContent || '').trim();
            if (!t || t.length > 50) continue;
            if (!/查看\s*\d+\s*条回复|view\s+\d+\s+repl|更多回复|展开\s*\d+|see\s+more/i.test(t)) continue;
            out.push(t);
            if (out.length >= 30) break;
          }
          return out.length;
        }""")
        if not candidates: break
        # 实际点击：用 Playwright 真鼠标
        for kw in ['查看', 'view', '更多回复', '展开', 'See more']:
            try:
                btns = page.get_by_text(kw, exact=False)
                # 限点击数量避免无限
                for i in range(min(20, btns.count())):
                    try:
                        b = btns.nth(i)
                        if not b.is_visible(timeout=400): continue
                        txt = b.text_content() or ''
                        # 二次过滤：长度短 + 含"回复"或"repl"
                        if len(txt) > 50: continue
                        if not any(k in txt.lower() for k in ['回复', 'repl', '更多', 'more']): continue
                        b.click(timeout=2500)
                        clicked += 1
                        time.sleep(0.4)
                    except Exception: pass
            except Exception: pass
        if clicked == 0: break
        total_clicked += clicked
        time.sleep(1.5)
    return total_clicked

def main():
    if len(sys.argv) < 3:
        print(__doc__, file=sys.stderr); sys.exit(1)
    input_path, output_path = sys.argv[1], sys.argv[2]
    with open(input_path, encoding='utf-8') as f:
        videos = json.load(f)

    out = {}
    t0 = time.time()
    with attach() as (pw, browser, ctx):
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for i, v in enumerate(videos, 1):
            label = v.get('label','')
            url = v['url']
            v_t0 = time.time()
            print(f"\n[{i}/{len(videos)}] {label[:55]}", file=sys.stderr)
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                time.sleep(2)
                # 立刻暂停视频，避免 auto-advance 摧毁 page context
                try:
                    page.evaluate("""() => {
                      document.querySelectorAll('video').forEach(v => {
                        try { v.pause(); v.muted = true; v.loop = true; } catch(e) {}
                      });
                    }""")
                except Exception: pass
                time.sleep(2)
                # 1) 唤出评论
                count = open_comment_panel(page, max_seconds=20)
                if count == 0:
                    print(f"  ⚠ 评论未渲染 ({time.time()-v_t0:.1f}s)", file=sys.stderr)
                    out[url] = {'label': label, 'main_count': 0, 'sub_count': 0, 'total_count': 0, 'comments': [], 'error': 'no comments'}
                    time.sleep(3); continue
                print(f"  阶段1 评论唤出: {count}", file=sys.stderr)
                # 2) 滚动加载
                count = scroll_comment_panel(page, max_iter=80)
                ext = page.evaluate(EXTRACT_JS)
                print(f"  阶段2 滚动后: 主 {len(ext['main'])} 子 {len(ext['sub'])}", file=sys.stderr)
                # 3) 展开子回复
                page.evaluate("window.__tt_clicked = new WeakSet()")
                clicked = expand_sub_replies(page, max_rounds=10)
                ext = page.evaluate(EXTRACT_JS)
                print(f"  阶段3 展开 {clicked}: 主 {len(ext['main'])} 子 {len(ext['sub'])}", file=sys.stderr)
                # 4) 再滚一次以触发新加载
                scroll_comment_panel(page, max_iter=15)
                ext = page.evaluate(EXTRACT_JS)
                # 去重
                seen = set(); deduped = []
                for c in ext['main'] + ext['sub']:
                    k = (c.get('author') or '', (c.get('text') or '')[:100], c.get('level'))
                    if k in seen: continue
                    seen.add(k); deduped.append(c)
                main_n = sum(1 for c in deduped if c['level'] == 1)
                sub_n = sum(1 for c in deduped if c['level'] == 2)
                print(f"  最终: 主 {main_n} + 子 {sub_n} = {len(deduped)} ({time.time()-v_t0:.1f}s)", file=sys.stderr)
                out[url] = {'label': label, 'main_count': main_n, 'sub_count': sub_n,
                            'total_count': len(deduped), 'comments': deduped}
                time.sleep(2)
            except Exception as e:
                print(f"  ✗ 失败: {str(e)[:150]}", file=sys.stderr)
                out[url] = {'label': label, 'comments': [], 'error': str(e)[:200]}
                time.sleep(4)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    g_main = sum(d.get('main_count', 0) for d in out.values())
    g_sub = sum(d.get('sub_count', 0) for d in out.values())
    success = sum(1 for d in out.values() if d.get('total_count', 0) > 0)
    print(f"\n完成: {time.time()-t0:.1f}s | {success}/{len(videos)} 成功 | 主 {g_main} + 子 {g_sub} = {g_main+g_sub} | {output_path}", file=sys.stderr)

if __name__ == '__main__':
    main()
