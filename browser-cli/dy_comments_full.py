"""抖音评论全量抓取（主楼 + 子回复）。

策略：
1. 打开视频 URL，等评论加载
2. 滚动评论列表加载所有主楼
3. 点击每个 "展开 N 条回复" 展开子回复
4. 在每个展开的楼里继续点击"查看 N 条回复"做分页
5. 抓 [data-e2e="comment-item"] (主楼) + [data-e2e="reply-item"]/[data-e2e="comment-reply-item"] (子回复)
"""
import sys, time, json
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from connect import attach

INPUT = sys.argv[1] if len(sys.argv) > 1 else 'C:/Users/yang/desktop/test_project/browser-cli/dy_a_top10_input.json'
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else 'C:/Users/yang/desktop/test_project/browser-cli/dy_a_comments.json'

# 抓取主楼 + 子楼。子回复也用 data-e2e="comment-item"，但嵌在 .replyContainer 里
EXTRACT_JS = r"""
() => {
  function isInReplyContainer(el) {
    let p = el.parentElement;
    while (p) {
      const c = (typeof p.className === 'string') ? p.className : '';
      if (/replyContainer/.test(c)) return true;
      p = p.parentElement;
    }
    return false;
  }

  function parseItem(it, isSub) {
    const authorA = it.querySelector('a[href*="/user/"]');
    const author = authorA?.textContent?.trim() || null;
    let text = '';
    const textBox = it.querySelector('[class*="C7LroK_h"], [class*="comment-content"], span[class*="content"]');
    if (textBox) text = textBox.textContent.trim();
    if (!text) {
      let best = '';
      for (const s of it.querySelectorAll('span')) {
        if (s.children.length > 1) continue;
        const t = s.textContent.trim();
        if (t.length > best.length && t.length < 800) best = t;
      }
      text = best;
    }
    let time_loc = '';
    for (const s of it.querySelectorAll('span')) {
      const t = s.textContent.trim();
      if (s.children.length === 0 && /(分钟|小时|天|周|月|年)前/.test(t) && t.length < 40) {
        time_loc = t; break;
      }
    }
    let likes = 0;
    const stats = it.querySelector('[class*="comment-item-stats"], [class*="reply-stats"]');
    if (stats) {
      for (const s of stats.querySelectorAll('span, p')) {
        const t = s.textContent.trim();
        if (s.children.length === 0 && /^\d+$/.test(t) && t.length < 8) {
          likes = parseInt(t); break;
        }
      }
    }
    return {author, text, time_loc, likes, is_sub: isSub};
  }

  const all = Array.from(document.querySelectorAll('[data-e2e="comment-item"]'));
  const main = [], sub = [];
  for (const it of all) {
    const isSub = isInReplyContainer(it);
    const p = parseItem(it, isSub);
    if (!p.text || p.text.length <= 1) continue;
    if (isSub) sub.push(p); else main.push(p);
  }
  return {main, sub};
}
"""

# 点击展开子回复：直接定位 button.comment-reply-expand-btn（实际处理 click 的元素）
CLICK_EXPAND_REPLIES_JS = r"""
() => {
  if (!window.__dy_clicked) window.__dy_clicked = new WeakSet();
  let clicked = 0;
  const root = document.querySelector('[data-e2e="comment-list"]') || document.body;
  // 主"展开 N 条回复"按钮
  for (const btn of root.querySelectorAll('button.comment-reply-expand-btn, button[class*="reply-expand"], button[class*="reply-show"]')) {
    if (window.__dy_clicked.has(btn)) continue;
    const t = (btn.innerText || btn.textContent || '').trim();
    if (!t) continue;
    if (!/展开\s*\d+\s*条回复|查看\s*\d+\s*条回复|更多回复/.test(t)) continue;
    try {
      btn.click();
      window.__dy_clicked.add(btn);
      clicked++;
    } catch (e) {}
  }
  return clicked;
}
"""

# 点击 "查看更多回复" / 楼中楼分页（在已展开的子回复列表里）
CLICK_MORE_REPLIES_JS = r"""
() => {
  if (!window.__dy_clicked_more) window.__dy_clicked_more = new WeakSet();
  let clicked = 0;
  const root = document.querySelector('[data-e2e="comment-list"]') || document.body;
  for (const el of root.querySelectorAll('button, span[class*="reply-show"], div[class*="reply-show"], span[class*="more"]')) {
    if (window.__dy_clicked_more.has(el)) continue;
    if (el.children.length > 1) continue;
    const t = (el.innerText || el.textContent || '').trim();
    if (!t || t.length > 30) continue;
    if (!/查看更多|更多回复|查看\s*\d+\s*条|展开\s*\d+/.test(t)) continue;
    try {
      el.click();
      window.__dy_clicked_more.add(el);
      clicked++;
    } catch (e) {}
  }
  return clicked;
}
"""

def wait_for_comments(page, max_seconds=25):
    deadline = time.time() + max_seconds
    while time.time() < deadline:
        page.evaluate("""() => {
          window.scrollTo(0, 0);
          setTimeout(() => window.scrollTo(0, 1500), 100);
          setTimeout(() => window.scrollTo(0, 700), 400);
        }""")
        time.sleep(1.4)
        cur = page.evaluate('document.querySelectorAll(\'[data-e2e="comment-item"]\').length')
        if cur > 0: return cur
    return 0

def scroll_comment_list(page, max_iter=50):
    prev = 0; stable = 0
    for _ in range(max_iter):
        page.evaluate("""() => {
          const list = document.querySelector('[data-e2e="comment-list"]');
          if (list) {
            let target = list;
            while (target && target.scrollHeight <= target.clientHeight) target = target.parentElement;
            if (target) target.scrollBy(0, 1500);
          }
          window.scrollBy(0, 500);
        }""")
        time.sleep(0.6)
        cur = page.evaluate('document.querySelectorAll(\'[data-e2e="comment-item"]\').length')
        if cur == prev:
            stable += 1
            if stable >= 5: return cur
        else: stable = 0
        prev = cur
    return prev

def main():
    with open(INPUT, encoding='utf-8') as f:
        videos = json.load(f)

    out = {}
    t0 = time.time()
    with attach() as (pw, browser, ctx):
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for i, v in enumerate(videos, 1):
            label = v.get('label', '')
            url = v['url']
            v_t0 = time.time()
            print(f"\n[{i}/{len(videos)}] {label[:50]}", file=sys.stderr)
            try:
                page.goto(url, wait_until='domcontentloaded', timeout=25000)
                count = wait_for_comments(page, max_seconds=25)
                if count == 0:
                    print(f"  ⚠ 25s 后无评论 ({time.time()-v_t0:.1f}s)", file=sys.stderr)
                    out[url] = {'label': label, 'main_count': 0, 'sub_count': 0, 'comments': [], 'error': 'no comments'}
                    time.sleep(4); continue

                # 滚动加载所有主楼
                count = scroll_comment_list(page)
                ext = page.evaluate(EXTRACT_JS)
                print(f"  阶段1: 主楼 {len(ext['main'])} 条 ({time.time()-v_t0:.1f}s)", file=sys.stderr)

                # 阶段 2：用 Playwright 真鼠标点击每个 "展开N条回复" 按钮
                btn_loc = page.locator('button.comment-reply-expand-btn')
                btn_count = btn_loc.count()
                print(f"  阶段2: {btn_count} 个展开按钮", file=sys.stderr)
                clicked_count = 0
                for bi in range(btn_count):
                    try:
                        b = btn_loc.nth(bi)
                        if not b.is_visible(timeout=500):
                            continue
                        b.scroll_into_view_if_needed(timeout=2000)
                        b.click(timeout=3000, force=False)
                        clicked_count += 1
                        time.sleep(0.4)
                    except Exception as e:
                        # 按钮可能在点击过程中消失（已展开后不在），跳过
                        pass
                time.sleep(2)
                ext = page.evaluate(EXTRACT_JS)
                print(f"  阶段2: 真实点击 {clicked_count}/{btn_count}, 主{len(ext['main'])} 子{len(ext['sub'])}", file=sys.stderr)

                # 阶段 3：循环点击新出现的"展开 N 条" 或楼中楼分页（点完展开后可能再出现新按钮）
                for r in range(5):
                    btn2 = page.locator('button.comment-reply-expand-btn')
                    new_count = btn2.count()
                    if new_count == 0:
                        break
                    rc = 0
                    for bi in range(new_count):
                        try:
                            b = btn2.nth(bi)
                            if not b.is_visible(timeout=400): continue
                            b.click(timeout=3000)
                            rc += 1
                            time.sleep(0.3)
                        except: pass
                    time.sleep(1.5)
                    ext = page.evaluate(EXTRACT_JS)
                    print(f"  阶段3-r{r+1}: +{rc}, 主{len(ext['main'])} 子{len(ext['sub'])}", file=sys.stderr)
                    if rc == 0: break

                # 最终再滚一遍触发懒加载
                scroll_comment_list(page, max_iter=10)

                ext = page.evaluate(EXTRACT_JS)
                # 去重
                seen = set(); deduped = []
                for c in ext['main'] + ext['sub']:
                    k = (c.get('author') or '', (c.get('text') or '')[:100], c.get('is_sub'))
                    if k in seen: continue
                    seen.add(k); deduped.append(c)
                main_n = sum(1 for c in deduped if not c['is_sub'])
                sub_n = sum(1 for c in deduped if c['is_sub'])
                print(f"  最终去重: 主 {main_n} + 子 {sub_n} = {len(deduped)} ({time.time()-v_t0:.1f}s)", file=sys.stderr)

                out[url] = {'label': label, 'main_count': main_n, 'sub_count': sub_n,
                           'total_count': len(deduped), 'comments': deduped}
                time.sleep(2)
            except Exception as e:
                print(f"  ✗ 失败: {str(e)[:120]}", file=sys.stderr)
                out[url] = {'label': label, 'comments': [], 'error': str(e)[:200]}
                time.sleep(4)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    g_main = sum(d.get('main_count', 0) for d in out.values())
    g_sub = sum(d.get('sub_count', 0) for d in out.values())
    success = sum(1 for d in out.values() if d.get('total_count', 0) > 0)
    print(f"\n完成: {time.time()-t0:.1f}s | {success}/{len(videos)} 成功 | 主 {g_main} + 子 {g_sub} = {g_main+g_sub}", file=sys.stderr)

if __name__ == '__main__':
    main()
