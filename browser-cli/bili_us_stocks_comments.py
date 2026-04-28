"""为 Top 10 美股视频，调用 B 站评论 API 抓取评论（带登录态 fetch）。

API:
- aid 查询: /x/web-interface/view?bvid={bv}
- 评论: /x/v2/reply/main?type=1&oid={aid}&mode=3&next={n}&ps=20  (mode=3 热度)
"""
import sys, json, time
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
from connect import attach

PAGES_PER_VIDEO = 30  # 上限页数；mode=2 按时间排序，可拉到底
PAGE_SIZE = 20

FETCH_AID_JS = """
async (bv) => {
  const r = await fetch(`https://api.bilibili.com/x/web-interface/view?bvid=${bv}`, {credentials: 'include'});
  const j = await r.json();
  return j?.data?.aid;
}
"""

# 主楼接口: /x/v2/reply
FETCH_COMMENTS_JS = """
async ({oid, pn, ps}) => {
  const url = `https://api.bilibili.com/x/v2/reply?type=1&oid=${oid}&sort=2&pn=${pn}&ps=${ps}`;
  const r = await fetch(url, {credentials: 'include'});
  const j = await r.json();
  if (j.code !== 0) return {error: j.message || j.code};
  const replies = j.data?.replies || [];
  const page = j.data?.page || {};
  return {
    page,
    total: page.acount || page.count,
    replies: replies.map(rp => ({
      rpid: rp.rpid,
      uname: rp.member?.uname,
      mid: rp.mid,
      ctime: rp.ctime,
      like: rp.like,
      reply_count: rp.rcount,
      content: rp.content?.message?.slice(0, 1500),
    })),
  };
}
"""

# 子回复（楼中楼）: /x/v2/reply/reply
FETCH_SUBREPLIES_JS = """
async ({oid, root, pn, ps}) => {
  const url = `https://api.bilibili.com/x/v2/reply/reply?type=1&oid=${oid}&root=${root}&pn=${pn}&ps=${ps}`;
  const r = await fetch(url, {credentials: 'include'});
  const j = await r.json();
  if (j.code !== 0) return {error: j.message || j.code};
  const replies = j.data?.replies || [];
  return {
    replies: replies.map(rp => ({
      rpid: rp.rpid,
      parent: rp.parent,
      root: rp.root,
      uname: rp.member?.uname,
      mid: rp.mid,
      ctime: rp.ctime,
      like: rp.like,
      content: rp.content?.message?.slice(0, 1500),
    })),
  };
}
"""

def main():
    d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/bili_us_stocks_top10.json', encoding='utf-8'))
    top10 = d['top10']

    out = []
    with attach() as (pw, browser, ctx):
        page = ctx.new_page()
        # 必须先到 b 站域下，fetch 才会带 cookie
        page.goto('https://www.bilibili.com/', wait_until='domcontentloaded', timeout=20000)
        time.sleep(1.5)

        for i, v in enumerate(top10, 1):
            print(f"\n[{i}/10] {v['title'][:50]}", file=sys.stderr)
            try:
                aid = page.evaluate(FETCH_AID_JS, v['bv'])
            except Exception as e:
                print(f"  aid 失败: {e}", file=sys.stderr); continue
            if not aid:
                print("  aid 空，跳过", file=sys.stderr); continue

            all_replies = []
            seen_rpid = set()
            total = None
            for pn in range(1, PAGES_PER_VIDEO + 1):
                try:
                    res = page.evaluate(FETCH_COMMENTS_JS, {'oid': aid, 'pn': pn, 'ps': PAGE_SIZE})
                except Exception as e:
                    print(f"  pn {pn} 异常: {e}", file=sys.stderr); break
                if res.get('error'):
                    print(f"  api 错误: {res['error']}", file=sys.stderr); break
                replies = res.get('replies', [])
                if total is None: total = res.get('total')
                added = 0
                for r in replies:
                    if r['rpid'] in seen_rpid: continue
                    seen_rpid.add(r['rpid'])
                    all_replies.append(r); added += 1
                print(f"  pn{pn}: +{added} (累计 {len(all_replies)}/{total})", file=sys.stderr)
                if added == 0 or len(replies) < PAGE_SIZE: break
                time.sleep(0.4)

            # 拉子回复
            sub_total = 0
            for r in list(all_replies):
                rc = r.get('reply_count') or 0
                if rc <= 0: continue
                for spn in range(1, 11):  # 子回复每楼最多翻 10 页 ≈ 100 条，足够覆盖绝大多数
                    try:
                        sres = page.evaluate(FETCH_SUBREPLIES_JS,
                                             {'oid': aid, 'root': r['rpid'], 'pn': spn, 'ps': PAGE_SIZE})
                    except Exception as e:
                        print(f"  子回复 root={r['rpid']} 异常: {e}", file=sys.stderr); break
                    if sres.get('error'):
                        print(f"  子回复 api 错误: {sres['error']}", file=sys.stderr); break
                    sub = sres.get('replies', [])
                    new = 0
                    for s in sub:
                        if s['rpid'] in seen_rpid: continue
                        seen_rpid.add(s['rpid'])
                        s['is_sub'] = True
                        s['parent_rpid'] = r['rpid']
                        all_replies.append(s); new += 1; sub_total += 1
                    if new == 0 or len(sub) < PAGE_SIZE: break
                    time.sleep(0.3)
            print(f"  → 子回复 +{sub_total}, 累计 {len(all_replies)}", file=sys.stderr)

            out.append({
                'rank': i,
                'bv': v['bv'],
                'aid': aid,
                'title': v['title'],
                'author': v['author'],
                'play_count': v['play_count'],
                'date': v['date'],
                'url': v['url'],
                'total_comments_in_meta': total,
                'collected_count': len(all_replies),
                'comments': all_replies,
            })
            time.sleep(0.8)
        page.close()

    out_path = 'C:/Users/yang/desktop/test_project/browser-cli/bili_us_stocks_comments.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'videos': out}, f, ensure_ascii=False, indent=2)
    total_c = sum(v['collected_count'] for v in out)
    print(f"\n总抓取 {total_c} 条评论，10 个视频，输出 {out_path}", file=sys.stderr)

if __name__ == '__main__':
    main()
