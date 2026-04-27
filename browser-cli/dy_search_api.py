"""通过抓包 Douyin 搜索 API 拿到 aweme_id + 所有元数据。

API: /aweme/v1/web/general/search/stream/
返回 NDJSON 流，每条带 status_code/data/aweme_info。

输出：Top N 视频带 aweme_id, 视频 URL, 标题, 作者, 点赞, 时长, 发布时间。
"""
import sys
import time
import json
import re
from datetime import datetime

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

TODAY = datetime(2026, 4, 27)


def parse_ndjson_chunks(body):
    """API 用 chunked transfer，body 是 [length]\\n[json]\\n 重复。"""
    items = []
    pos = 0
    while pos < len(body):
        # 跳过空白和长度行
        nl = body.find("\n", pos)
        if nl == -1:
            break
        # 长度行可能是十六进制，跳过到下一行
        line = body[pos:nl].strip()
        if line and re.match(r"^[\da-fA-F]+$", line):
            pos = nl + 1
            continue
        # 试图作为 JSON 解析
        try:
            obj = json.loads(line)
            items.append(obj)
            pos = nl + 1
        except json.JSONDecodeError:
            # 多行 JSON
            for end in range(nl + 1, len(body)):
                if body[end] == "\n":
                    try:
                        obj = json.loads(body[pos:end])
                        items.append(obj)
                        pos = end + 1
                        break
                    except json.JSONDecodeError:
                        continue
            else:
                break
    return items


def extract_videos(api_objects):
    """从 API 响应里提取视频元数据。"""
    out = []
    seen = set()
    for obj in api_objects:
        if not isinstance(obj, dict) or "data" not in obj:
            continue
        for item in obj["data"]:
            info = item.get("aweme_info") or item.get("aweme")
            if not info:
                continue
            aid = info.get("aweme_id")
            if not aid or aid in seen:
                continue
            seen.add(aid)
            stats = info.get("statistics") or {}
            video = info.get("video") or {}
            author = info.get("author") or {}
            duration = video.get("duration", 0)  # ms
            create_time = info.get("create_time", 0)
            out.append(
                {
                    "aweme_id": aid,
                    "url": f"https://www.douyin.com/video/{aid}",
                    "modal_url": f"https://www.douyin.com/search/%E7%BE%8E%E8%82%A1?modal_id={aid}",
                    "title": (info.get("desc") or "").strip().replace("\n", " "),
                    "author": author.get("nickname"),
                    "author_id": author.get("short_id"),
                    "digg_count": stats.get("digg_count", 0),
                    "comment_count": stats.get("comment_count", 0),
                    "share_count": stats.get("share_count", 0),
                    "duration_sec": round(duration / 1000) if duration else None,
                    "create_time": create_time,
                    "create_time_str": datetime.fromtimestamp(create_time).isoformat() if create_time else None,
                    "age_h": (time.time() - create_time) / 3600 if create_time else None,
                }
            )
    return out


def main():
    t0 = time.time()
    api_bodies = []

    with attach() as (pw, browser, ctx):
        page = next((p for p in ctx.pages if "douyin.com/search" in p.url), None)
        if page is None:
            page = ctx.new_page()

        def on_response(resp):
            url = resp.url
            if "general/search/stream" in url or "general/search/single" in url:
                try:
                    api_bodies.append(resp.text())
                except Exception:
                    pass

        page.on("response", on_response)

        url = "https://www.douyin.com/search/%E7%BE%8E%E8%82%A1?publish_time=7&sort_type=2"
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(3)

        # 滚动直到加载完毕
        prev = 0
        stable = 0
        for i in range(40):
            page.evaluate("window.scrollBy(0, 1800)")
            time.sleep(0.6)
            cur = page.evaluate("document.querySelectorAll('div.search-result-card').length")
            if cur == prev:
                stable += 1
                if stable >= 5:
                    break
            else:
                stable = 0
            prev = cur

    print(f"  抓到 {prev} 张卡片 + {len(api_bodies)} 个 API 响应", file=sys.stderr)

    # 解析所有 API 响应
    all_objs = []
    for body in api_bodies:
        all_objs.extend(parse_ndjson_chunks(body))
    print(f"  解析出 {len(all_objs)} 个 API 数据对象", file=sys.stderr)

    videos = extract_videos(all_objs)
    print(f"  提取出 {len(videos)} 个唯一视频", file=sys.stderr)

    # 过滤 3 天 + 排序
    filtered = [v for v in videos if v["age_h"] is not None and v["age_h"] <= 72]
    filtered.sort(key=lambda x: x["digg_count"], reverse=True)

    print(f"  3 天内: {len(filtered)} 个, 总耗时 {time.time()-t0:.1f}s", file=sys.stderr)

    out_path = "C:/Users/yang/desktop/test_project/browser-cli/dy_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    print(f"  已存到 {out_path}", file=sys.stderr)

    # 输出 Top 10 简表
    print(json.dumps(filtered[:10], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
