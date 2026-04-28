"""抖音 A 股近 3 天视频聚合搜索（多关键词 + API 抓包）。"""
import sys, time, json, re
from urllib.parse import quote
from datetime import datetime

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

KEYWORDS = [
    "A股",
    "A股复盘",
    "A股大盘",
    "上证指数",
    "沪指",
    "沪深300",
    "创业板",
    "涨停",
    "北向资金",
    "一季报",
]

def parse_ndjson(body):
    items = []; pos = 0
    while pos < len(body):
        nl = body.find("\n", pos)
        if nl == -1: break
        line = body[pos:nl].strip()
        if line and re.match(r"^[\da-fA-F]+$", line):
            pos = nl + 1; continue
        try:
            items.append(json.loads(line)); pos = nl + 1
        except json.JSONDecodeError:
            for end in range(nl + 1, len(body)):
                if body[end] == "\n":
                    try:
                        items.append(json.loads(body[pos:end])); pos = end + 1; break
                    except json.JSONDecodeError: continue
            else: break
    return items

def extract_videos(api_objects, keyword):
    out = []
    for obj in api_objects:
        if not isinstance(obj, dict) or "data" not in obj: continue
        for item in obj["data"]:
            info = item.get("aweme_info") or item.get("aweme")
            if not info: continue
            aid = info.get("aweme_id")
            if not aid: continue
            stats = info.get("statistics") or {}
            video = info.get("video") or {}
            author = info.get("author") or {}
            duration = video.get("duration", 0)
            create_time = info.get("create_time", 0)
            out.append({
                "aweme_id": aid,
                "url": f"https://www.douyin.com/video/{aid}",
                "modal_url": f"https://www.douyin.com/search/{quote(keyword)}?modal_id={aid}",
                "title": (info.get("desc") or "").strip().replace("\n", " "),
                "author": author.get("nickname"),
                "author_id": author.get("short_id"),
                "digg_count": stats.get("digg_count", 0),
                "comment_count": stats.get("comment_count", 0),
                "share_count": stats.get("share_count", 0),
                "play_count": stats.get("play_count", 0),
                "duration_sec": round(duration / 1000) if duration else None,
                "create_time": create_time,
                "create_time_str": datetime.fromtimestamp(create_time).isoformat() if create_time else None,
                "age_h": (time.time() - create_time) / 3600 if create_time else None,
                "matched_keyword": keyword,
            })
    return out

def main():
    t0 = time.time()
    all_videos = {}  # aweme_id -> video

    with attach() as (pw, browser, ctx):
        page = ctx.pages[0]  # 现有 tab
        api_bodies_per_kw = {}

        for kw in KEYWORDS:
            kw_t0 = time.time()
            api_bodies = []

            def on_response(resp):
                url = resp.url
                if "general/search/stream" in url or "general/search/single" in url:
                    try: api_bodies.append(resp.text())
                    except Exception: pass

            page.on("response", on_response)

            try:
                url = f"https://www.douyin.com/search/{quote(kw)}?publish_time=7&sort_type=2"
                page.goto(url, wait_until="domcontentloaded", timeout=25000)
                time.sleep(3)
                prev = 0; stable = 0
                for i in range(20):
                    page.evaluate("window.scrollBy(0, 1800)")
                    time.sleep(0.55)
                    cur = page.evaluate("document.querySelectorAll('div.search-result-card').length")
                    if cur == prev:
                        stable += 1
                        if stable >= 4: break
                    else: stable = 0
                    prev = cur
            except Exception as e:
                print(f"  [{kw}] 失败: {str(e)[:100]}", file=sys.stderr)
                page.remove_listener("response", on_response)
                continue

            page.remove_listener("response", on_response)

            all_objs = []
            for body in api_bodies:
                all_objs.extend(parse_ndjson(body))
            videos = extract_videos(all_objs, kw)

            added = 0
            for v in videos:
                if v["aweme_id"] not in all_videos:
                    all_videos[v["aweme_id"]] = v
                    added += 1
            print(f"  [{kw}] {prev} 卡片, {len(api_bodies)} API响应, {len(videos)} 视频, 新增 {added}, 总 {len(all_videos)} ({time.time()-kw_t0:.1f}s)",
                  file=sys.stderr)

    # 过滤 3 天内 + 按点赞数排序
    videos = list(all_videos.values())
    filtered = [v for v in videos if v["age_h"] is not None and v["age_h"] <= 72]
    filtered.sort(key=lambda x: x["digg_count"], reverse=True)

    out_path = "C:/Users/yang/desktop/test_project/browser-cli/dy_a_search.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"fetched_at": datetime.now().isoformat(),
                   "total": len(filtered), "videos": filtered}, f, ensure_ascii=False, indent=2)

    print(f"\n3 天内: {len(filtered)} / 总 {len(videos)}, 耗时 {time.time()-t0:.1f}s", file=sys.stderr)
    print("\n=== Top 25（按点赞）===")
    for i, v in enumerate(filtered[:25], 1):
        print(f"{i:2}. 赞{v['digg_count']:>6} 评{v['comment_count']:>4}  {v['title'][:60]}")
        print(f"     ↳ {v['author']} | {v['create_time_str']} | {v['url']}")

if __name__ == "__main__":
    main()
