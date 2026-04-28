"""TikTok 美股多语言搜索 — API 抓包版（匿名）。
监听 TikTok 搜索 API 响应，提取 aweme_id / title / author / create_time / digg_count 等完整元数据。
"""
import sys, time, json, re
from urllib.parse import quote
from datetime import datetime

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

KEYWORDS = [
    "us stocks", "stock market", "investing", "wall street", "trading",
    "$NVDA", "$TSLA", "$SPY", "NASDAQ", "S&P 500",
    "美股", "纳斯达克",
    "米国株", "アメリカ株",
    "미국주식",
    "bolsa eeuu", "acciones americanas",
    "US Aktien",
    "ações americanas",
    "bourse américaine",
]

SEARCH_URL_TPL = 'https://www.tiktok.com/search?q={kw}&publish_time=ONE_WEEK'

def extract_videos_from_obj(obj, keyword):
    """从 TikTok API JSON 响应里提取视频元数据。"""
    out = []
    if not isinstance(obj, dict): return out
    # TikTok 的搜索响应通常 data 是数组，每项有 item 或 type/aweme_info
    candidates = []
    if 'data' in obj and isinstance(obj['data'], list):
        candidates = obj['data']
    elif 'item_list' in obj:
        candidates = obj['item_list']
    elif 'aweme_list' in obj:
        candidates = obj['aweme_list']
    for c in candidates:
        info = c.get('item') or c.get('aweme_info') or c.get('aweme') or c
        if not isinstance(info, dict): continue
        aid = info.get('id') or info.get('aweme_id')
        if not aid: continue
        stats = info.get('stats') or info.get('statistics') or {}
        author = info.get('author') or {}
        author_name = author.get('uniqueId') or author.get('unique_id') or author.get('nickname')
        create_time = info.get('createTime') or info.get('create_time') or 0
        out.append({
            'aweme_id': str(aid),
            'url': f'https://www.tiktok.com/@{author_name}/video/{aid}' if author_name else f'https://www.tiktok.com/video/{aid}',
            'title': (info.get('desc') or '').strip().replace('\n',' '),
            'author': author_name,
            'author_nickname': author.get('nickname'),
            'digg_count': stats.get('diggCount') or stats.get('digg_count', 0),
            'comment_count': stats.get('commentCount') or stats.get('comment_count', 0),
            'share_count': stats.get('shareCount') or stats.get('share_count', 0),
            'play_count': stats.get('playCount') or stats.get('play_count', 0),
            'create_time': create_time,
            'create_time_str': datetime.fromtimestamp(create_time).isoformat() if create_time else None,
            'age_h': (time.time() - create_time) / 3600 if create_time else None,
            'matched_keyword': keyword,
        })
    return out

def main():
    t0 = time.time()
    all_videos = {}
    seen_urls_per_kw = []

    with attach() as (pw, browser, ctx):
        page = ctx.pages[0]

        for kw in KEYWORDS:
            kw_t0 = time.time()
            api_bodies = []
            api_urls = []

            def on_response(resp):
                u = resp.url
                if '/api/search/' in u or 'search/general' in u or 'search/item' in u:
                    api_urls.append(u[:200])
                    try: api_bodies.append(resp.text())
                    except Exception: pass

            page.on('response', on_response)

            try:
                url = SEARCH_URL_TPL.format(kw=quote(kw))
                page.goto(url, wait_until='domcontentloaded', timeout=25000)
                time.sleep(4)
                # 滚一些以触发懒加载
                prev = 0; stable = 0
                for sc in range(15):
                    page.evaluate("window.scrollBy(0, 1800)")
                    time.sleep(0.7)
                    cur = page.evaluate('document.querySelectorAll(\'[data-e2e="search_top-item"]\').length')
                    if cur == prev:
                        stable += 1
                        if stable >= 3: break
                    else: stable = 0
                    prev = cur
            except Exception as e:
                print(f"  [{kw}] goto 失败: {str(e)[:120]}", file=sys.stderr)
                page.remove_listener('response', on_response)
                continue

            page.remove_listener('response', on_response)

            videos_from_kw = []
            for body in api_bodies:
                try:
                    obj = json.loads(body)
                    videos_from_kw.extend(extract_videos_from_obj(obj, kw))
                except json.JSONDecodeError:
                    pass

            added = 0
            for v in videos_from_kw:
                if v['aweme_id'] in all_videos: continue
                all_videos[v['aweme_id']] = v
                added += 1
            print(f"  [{kw}] 卡片 {prev}, API {len(api_bodies)}, 视频 {len(videos_from_kw)}, +{added}, 总 {len(all_videos)} ({time.time()-kw_t0:.1f}s)",
                  file=sys.stderr)
            seen_urls_per_kw.append({'kw': kw, 'api_urls': api_urls[:3]})

    videos = list(all_videos.values())
    # 按 age_h 过滤 3 天内
    filtered = [v for v in videos if v.get('age_h') is not None and v['age_h'] <= 72]
    filtered.sort(key=lambda v: v.get('digg_count', 0), reverse=True)

    out_path = "C:/Users/yang/desktop/test_project/browser-cli/tt_us_search.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({
            'fetched_at': datetime.now().isoformat(),
            'total_3d': len(filtered),
            'total_all': len(videos),
            'videos_3d': filtered,
            'videos_all': videos,
            'api_url_samples': seen_urls_per_kw[:3],
        }, f, ensure_ascii=False, indent=2)

    print(f"\n3 天内: {len(filtered)} / 总 {len(videos)}, 耗时 {time.time()-t0:.1f}s", file=sys.stderr)
    print("\n=== Top 25 (3 天内, 按点赞) ===")
    for i, v in enumerate(filtered[:25], 1):
        ts = v.get('create_time_str','?')[:16]
        print(f"{i:2}. 赞{v['digg_count']:>6} 评{v['comment_count']:>4}  [{ts}]  {v['title'][:55]}")
        print(f"     ↳ {v['author']}  {v['url']}")

if __name__ == '__main__':
    main()
