"""B 站评论完整抓取（主楼 + 子回复 + 楼中楼）：
1. 滚到底加载所有主楼
2. 点击每个 "共 N 条回复，点击查看" 展开子回复
3. 滚动以触发分页
4. 提取 main + sub renderers，去重并解析

支持参数：python bili_comments_full.py <input_top10.json> <output.json>
"""
import sys, json, time, re
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from connect import attach

INPUT = sys.argv[1] if len(sys.argv) > 1 else 'C:/Users/yang/desktop/test_project/browser-cli/bili_a_top10.json'
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else 'C:/Users/yang/desktop/test_project/browser-cli/bili_a_comments.json'

# JS：抽取所有主楼+子楼的 deepText
EXTRACT_JS = r"""
() => {
  const SKIP = new Set(['STYLE','SCRIPT','SVG','BILI-AVATAR',
    'BILI-COMMENT-USER-SAILING-CARD','BILI-COMMENT-PICTURES-RENDERER',
    'BILI-COMMENT-USER-MEDAL','BILI-COMMENT-MENU']);
  function deepText(node, visited) {
    if (!node) return '';
    if (visited.has(node)) return '';
    visited.add(node);
    if (node.nodeType === 3) return node.textContent;
    if (SKIP.has(node.tagName)) return '';
    let s = '';
    if (node.shadowRoot) for (const c of node.shadowRoot.childNodes) s += deepText(c, visited);
    for (const c of (node.childNodes || [])) s += deepText(c, visited);
    return s;
  }
  function* walk(root, vis) {
    if (vis.has(root)) return;
    vis.add(root);
    yield root;
    if (root.shadowRoot) for (const c of root.shadowRoot.querySelectorAll('*')) {
      if (!vis.has(c)) yield* walk(c, vis);
    }
    for (const c of (root.children || [])) {
      if (!vis.has(c)) yield* walk(c, vis);
    }
  }
  const main = [];
  const sub = [];
  const seenEl = new Set();
  for (const el of walk(document.body, new Set())) {
    const t = el.tagName?.toLowerCase();
    if (t === 'bili-comment-thread-renderer') {
      if (seenEl.has(el)) continue;
      seenEl.add(el);
      main.push(deepText(el, new Set()).replace(/\s+/g,' ').trim());
    } else if (t === 'bili-comment-reply-renderer') {
      if (seenEl.has(el)) continue;
      seenEl.add(el);
      sub.push(deepText(el, new Set()).replace(/\s+/g,' ').trim());
    }
  }
  return {main, sub};
}
"""

# JS：找所有 "共N条回复" 点击目标（穿透 shadow DOM），返回点击数
# 通用点击器：找 <bili-text-button> 包含目标文本，跟踪已点过的按钮
CLICK_BY_TEXT_JS = r"""
(targetTextRegexStr) => {
  const re = new RegExp(targetTextRegexStr);
  const SKIP = new Set(['STYLE','SCRIPT','SVG']);
  function* walk(root, vis) {
    if (vis.has(root)) return;
    vis.add(root); yield root;
    if (root.shadowRoot) for (const c of root.shadowRoot.querySelectorAll('*')) if (!vis.has(c)) yield* walk(c, vis);
    for (const c of (root.children || [])) if (!vis.has(c)) yield* walk(c, vis);
  }
  if (!window.__bili_clicked) window.__bili_clicked = new WeakSet();
  let clicked = 0;
  for (const el of walk(document.body, new Set())) {
    if (SKIP.has(el.tagName)) continue;
    if (el.tagName !== 'BILI-TEXT-BUTTON') continue;
    if (window.__bili_clicked.has(el)) continue;
    const txt = (el.innerText || el.textContent || '').trim();
    if (!txt || txt.length > 40) continue;
    if (!re.test(txt)) continue;
    try {
      el.click();
      el.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true, view:window}));
      window.__bili_clicked.add(el);
      clicked++;
    } catch (e) {}
  }
  return clicked;
}
"""

DATE_RE = re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}|\d{2}-\d{2}\s+\d{2}:\d{2}|\d+\s*(小时|分钟|天)前|刚刚)')
SUB_RE = re.compile(r'共(\d+)条回复')

def parse(s, is_sub=False):
    if not s: return {}
    sub = 0
    m = SUB_RE.search(s)
    if m:
        sub = int(m.group(1))
        s = s[:m.start()].rstrip(' ，,。.')
    dm = DATE_RE.search(s)
    ts = dm.group(0) if dm else ''
    pre = s[:dm.start()].strip() if dm else s.strip()
    post = s[dm.end():].strip() if dm else ''
    likes = 0
    lm = re.match(r'(\d+)', post)
    if lm: likes = int(lm.group(1))
    parts = pre.split(' ', 1)
    uname = parts[0] if parts else ''
    rest = parts[1] if len(parts) > 1 else ''
    rest = re.sub(r'^置顶\s+', '', rest).strip()
    if rest.startswith(uname + ' '):
        rest = rest[len(uname)+1:].strip()
    return {
        'uname': uname,
        'content': rest,
        'time': ts,
        'like': likes,
        'sub_count_meta': sub,
        'is_sub': is_sub,
    }

def main():
    d = json.load(open(INPUT, encoding='utf-8'))
    top10 = d['top10']

    out = []
    with attach() as (pw, browser, ctx):
        page = ctx.pages[0]
        for i, v in enumerate(top10, 1):
            t0 = time.time()
            print(f"\n[{i}/{len(top10)}] {v['title'][:55]}", file=sys.stderr)
            try:
                page.goto(v['url'], wait_until='domcontentloaded', timeout=30000)
            except Exception as e:
                print(f"  导航失败: {e}", file=sys.stderr); continue
            time.sleep(3.5)
            page.evaluate("""() => {
              const el = document.querySelector('bili-comments');
              if (el) el.scrollIntoView({behavior:'instant', block:'start'});
            }""")
            time.sleep(2)

            # === 阶段 1：滚到底加载所有主楼 ===
            seen = -1; stable = 0
            for sc in range(60):
                page.evaluate("window.scrollBy(0, 1200)")
                time.sleep(1.0)
                ext = page.evaluate(EXTRACT_JS)
                cur = len(ext['main'])
                if cur == seen:
                    stable += 1
                    if stable >= 5: break
                else:
                    stable = 0
                seen = cur
            main_loaded = seen
            print(f"  阶段1: 主楼 {main_loaded} 条，{sc+1} 次滚动 ({time.time()-t0:.1f}s)", file=sys.stderr)

            # === 阶段 2：展开子回复（点 "点击查看"） ===
            for round_n in range(15):
                clicked = page.evaluate(CLICK_BY_TEXT_JS, '点击查看')
                if clicked == 0: break
                time.sleep(1.4)
                ext = page.evaluate(EXTRACT_JS)
                print(f"  阶段2-r{round_n+1}: 点击查看 +{clicked}, 主{len(ext['main'])} 子{len(ext['sub'])}", file=sys.stderr)

            # === 阶段 3：分页"查看更多 N 条" ===
            for round_n in range(15):
                more = page.evaluate(CLICK_BY_TEXT_JS, '查看更多|查看 ?\\d+ ?条|更多回复')
                if more == 0: break
                time.sleep(1.3)
                ext = page.evaluate(EXTRACT_JS)
                print(f"  阶段3-r{round_n+1}: 查看更多 +{more}, 主{len(ext['main'])} 子{len(ext['sub'])}", file=sys.stderr)

            # 最终提取
            ext = page.evaluate(EXTRACT_JS)
            main_texts = ext['main']
            sub_texts = ext['sub']
            print(f"  最终: 主{len(main_texts)} 子{len(sub_texts)}, 总耗时 {time.time()-t0:.1f}s", file=sys.stderr)

            # 解析 + 去重
            parsed = []
            seen_keys = set()
            for s in main_texts:
                p = parse(s, is_sub=False)
                if not p.get('content'): continue
                k = (p['uname'], p['content'][:100], False)
                if k in seen_keys: continue
                seen_keys.add(k); parsed.append(p)
            for s in sub_texts:
                p = parse(s, is_sub=True)
                if not p.get('content'): continue
                k = (p['uname'], p['content'][:100], True)
                if k in seen_keys: continue
                seen_keys.add(k); parsed.append(p)

            main_cnt = sum(1 for p in parsed if not p['is_sub'])
            sub_cnt = sum(1 for p in parsed if p['is_sub'])
            print(f"  去重后：主 {main_cnt} + 子 {sub_cnt} = {len(parsed)} 条", file=sys.stderr)

            out.append({
                'rank': i, 'bv': v['bv'], 'title': v['title'], 'author': v['author'],
                'play_count': v['play_count'], 'date': v['date'], 'url': v['url'],
                'main_count': main_cnt, 'sub_count': sub_cnt, 'total_count': len(parsed),
                'comments': parsed,
            })
            time.sleep(1.5)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump({'videos': out}, f, ensure_ascii=False, indent=2)
    g_main = sum(v['main_count'] for v in out)
    g_sub = sum(v['sub_count'] for v in out)
    print(f"\n总主 {g_main} + 子 {g_sub} = {g_main+g_sub} 条，{OUTPUT}", file=sys.stderr)

if __name__ == '__main__':
    main()
