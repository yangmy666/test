"""单独重试视频 #8 (insaneoo) 的评论抓取，并 merge 进现有 dy_a_comments.json。"""
import sys, time, json
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from connect import attach
from dy_comments_full import EXTRACT_JS, wait_for_comments, scroll_comment_list

V8_URL = 'https://www.douyin.com/video/7633649287998017161'
V8_LABEL = '#8 insaneoo - 听说今天大盘不好 我不知道啊🧐'

def main():
    out = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/dy_a_comments.json', encoding='utf-8'))

    with attach() as (pw, browser, ctx):
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        for attempt in range(3):
            try:
                print(f'尝试 {attempt+1}: {V8_URL}', file=sys.stderr)
                page.goto(V8_URL, wait_until='domcontentloaded', timeout=30000)
                count = wait_for_comments(page, max_seconds=30)
                if count == 0:
                    print('  无评论', file=sys.stderr); time.sleep(5); continue
                count = scroll_comment_list(page, max_iter=50)
                ext = page.evaluate(EXTRACT_JS)
                print(f'  阶段1: 主 {len(ext["main"])} 子 {len(ext["sub"])}', file=sys.stderr)
                # 展开
                btn = page.locator('button.comment-reply-expand-btn')
                bn = btn.count()
                print(f'  阶段2: {bn} 按钮', file=sys.stderr)
                clicked = 0
                for bi in range(bn):
                    try:
                        b = btn.nth(bi)
                        if not b.is_visible(timeout=400): continue
                        b.scroll_into_view_if_needed(timeout=2000)
                        b.click(timeout=3000)
                        clicked += 1
                        time.sleep(0.4)
                    except: pass
                time.sleep(2)
                for r in range(5):
                    btn2 = page.locator('button.comment-reply-expand-btn')
                    nc = btn2.count()
                    if nc == 0: break
                    rc = 0
                    for bi in range(nc):
                        try:
                            b = btn2.nth(bi)
                            if not b.is_visible(timeout=400): continue
                            b.click(timeout=3000); rc += 1
                            time.sleep(0.3)
                        except: pass
                    time.sleep(1.4)
                    if rc == 0: break
                ext = page.evaluate(EXTRACT_JS)
                seen = set(); deduped = []
                for c in ext['main'] + ext['sub']:
                    k = (c.get('author') or '', (c.get('text') or '')[:100], c.get('is_sub'))
                    if k in seen: continue
                    seen.add(k); deduped.append(c)
                main_n = sum(1 for c in deduped if not c['is_sub'])
                sub_n = sum(1 for c in deduped if c['is_sub'])
                print(f'  最终: 主 {main_n} + 子 {sub_n} = {len(deduped)}', file=sys.stderr)
                out[V8_URL] = {'label': V8_LABEL, 'main_count': main_n, 'sub_count': sub_n,
                               'total_count': len(deduped), 'comments': deduped}
                break
            except Exception as e:
                print(f'  失败: {str(e)[:120]}', file=sys.stderr)
                time.sleep(5)

    with open('C:/Users/yang/desktop/test_project/browser-cli/dy_a_comments.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    g_main = sum(d.get('main_count', 0) for d in out.values())
    g_sub = sum(d.get('sub_count', 0) for d in out.values())
    print(f'\n更新后总计: 主 {g_main} + 子 {g_sub} = {g_main+g_sub}', file=sys.stderr)

if __name__ == '__main__':
    main()
