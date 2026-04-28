"""通过 DOM (深度穿透 shadow DOM) 抓 Top 10 视频评论。绕开 API 的 412 限流。"""
import sys, json, time, re
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from connect import attach

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
  const threads = [];
  let idx = 0;
  for (const el of walk(document.body)) {
    if (++idx > 200000) break;
    if (el.tagName?.toLowerCase() === 'bili-comment-thread-renderer') {
      const txt = deepText(el).replace(/\s+/g, ' ').trim();
      threads.push(txt);
    }
  }
  return threads;
}
"""

# 解析 deepText 输出为结构化数据
DATE_RE = re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}|\d{2}-\d{2}\s+\d{2}:\d{2}|\d+\s*(小时|分钟|天)前|刚刚)')
SUB_RE  = re.compile(r'共(\d+)条回复')

def parse_thread(s: str) -> dict:
    """形如：'<uname> [置顶 ...] <content> <date> [<likes>] 回复 [共N条回复，点击查看]'"""
    if not s: return {}
    # 取出"共N条回复"
    sub = 0
    m = SUB_RE.search(s)
    if m:
        sub = int(m.group(1))
        s = s[:m.start()].rstrip(' ，,。.')
    # 找时间戳
    dm = DATE_RE.search(s)
    ts = dm.group(0) if dm else ''
    pre = s[:dm.start()].strip() if dm else s.strip()
    post = s[dm.end():].strip() if dm else ''
    # post 形如 "72 回复" 或 "回复"
    likes = 0
    lm = re.match(r'(\d+)', post)
    if lm: likes = int(lm.group(1))
    # pre = "<uname> [置顶 ...省略...] <content>"
    # 用户名 = 第一个空格前的 token（很多用户名含空格，不可靠）
    # 改用：拿前 30 字符作为用户名候选，剩下作为正文。
    # 实际：B站结构是 <uname> 后面紧跟 [置顶/up主等标签] 再是正文
    # 简单切分：第一个空格前为 uname
    parts = pre.split(' ', 1)
    uname = parts[0] if parts else ''
    rest = parts[1] if len(parts) > 1 else ''
    # 去除 "置顶" 标签 + UP 主自顶 (作者名重复)
    rest = re.sub(r'^置顶\s+', '', rest).strip()
    # 如果 rest 又以同一个 uname 开头（B站 UP 自评机制），去掉
    if rest.startswith(uname + ' '):
        rest = rest[len(uname)+1:].strip()
    return {
        'uname': uname,
        'content': rest,
        'time': ts,
        'like': likes,
        'sub_count': sub,
        'raw_len': len(s),
    }

def main():
    d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/bili_us_stocks_top10.json', encoding='utf-8'))
    top10 = d['top10']

    out = []
    with attach() as (pw, browser, ctx):
        # 用现有 tab，避免 new_page 导致 B 站不给加载评论
        page = ctx.pages[0]
        for i, v in enumerate(top10, 1):
            t0 = time.time()
            print(f"\n[{i}/10] {v['title'][:55]}", file=sys.stderr)
            try:
                page.goto(v['url'], wait_until='domcontentloaded', timeout=30000)
            except Exception as e:
                print(f"  导航失败: {e}", file=sys.stderr); continue
            time.sleep(3.5)
            # 滚到评论区
            page.evaluate("""() => {
              const el = document.querySelector('bili-comments');
              if (el) el.scrollIntoView({behavior:'instant', block:'start'});
            }""")
            time.sleep(2)

            seen_count = -1
            stable = 0
            max_scrolls = 60
            for sc in range(max_scrolls):
                page.evaluate("window.scrollBy(0, 1200)")
                time.sleep(1.1)
                threads = page.evaluate(EXTRACT_JS)
                cur = len(threads)
                if cur == seen_count:
                    stable += 1
                    if stable >= 5:
                        break
                else:
                    stable = 0
                seen_count = cur

            # 最终一次提取
            threads = page.evaluate(EXTRACT_JS)
            print(f"  抓到 {len(threads)} 条主楼，{sc+1} 次滚动，耗时 {time.time()-t0:.1f}s", file=sys.stderr)

            parsed = []
            for s in threads:
                p = parse_thread(s)
                if p.get('content') is not None:
                    parsed.append(p)

            out.append({
                'rank': i,
                'bv': v['bv'],
                'title': v['title'],
                'author': v['author'],
                'play_count': v['play_count'],
                'date': v['date'],
                'url': v['url'],
                'top_level_count': len(parsed),
                'comments': parsed,
            })
            time.sleep(1.5)
        # 不关闭用户已有的 tab

    out_path = 'C:/Users/yang/desktop/test_project/browser-cli/bili_us_stocks_comments.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'videos': out}, f, ensure_ascii=False, indent=2)
    total = sum(v['top_level_count'] for v in out)
    sub_total = sum(c.get('sub_count', 0) for v in out for c in v['comments'])
    print(f"\n总抓取主楼 {total} 条 (子回复另计 ~{sub_total})，输出 {out_path}", file=sys.stderr)

if __name__ == '__main__':
    main()
