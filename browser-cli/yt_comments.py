"""通用 YouTube 评论抓取器。

用法：
    python yt_comments.py <input.json> <output.json>

输入 JSON 格式：
    [
      {"label": "视频标识符（任意字符串）", "url": "https://www.youtube.com/watch?v=..."},
      ...
    ]

输出：每个视频的评论 + 元信息。

注意：
- 用 ytd-comment-thread-renderer 拿顶级评论，每条只取第一个 ytd-comment-view-model（不抓回复）
- 阶段 1 耐心滚动等评论开始加载（至多 15 次）
- 阶段 2 持续滚动直到 4 轮稳定（数量不变）
- 单视频耗时约 20-60 秒，取决于评论数量
"""
import sys
import time
import json

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

EXTRACT_JS = """
() => {
  const threads = document.querySelectorAll('ytd-comment-thread-renderer');
  return Array.from(threads).map(t => {
    const c = t.querySelector('ytd-comment-view-model');
    if (!c) return null;
    return {
      author: c.querySelector('#author-text')?.textContent?.trim(),
      text: c.querySelector('#content-text')?.textContent?.trim(),
      likes: c.querySelector('#vote-count-middle')?.textContent?.trim(),
      time: c.querySelector('#published-time-text')?.textContent?.trim(),
    };
  }).filter(c => c && c.text);
}
"""


def scrape_comments(page, url):
    page.goto(url, wait_until="domcontentloaded", timeout=20000)
    time.sleep(1.5)

    # 阶段 1：等评论开始加载
    for _ in range(15):
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(0.7)
        n = page.evaluate("document.querySelectorAll('ytd-comment-thread-renderer').length")
        if n > 0:
            break
    else:
        return []

    # 阶段 2：滚动到底
    prev_count, stable = 0, 0
    for _ in range(50):
        page.evaluate("window.scrollBy(0, 2500)")
        time.sleep(0.5)
        cur = page.evaluate("document.querySelectorAll('ytd-comment-thread-renderer').length")
        if cur == prev_count:
            stable += 1
            if stable >= 4:
                break
        else:
            stable = 0
        prev_count = cur

    return page.evaluate(EXTRACT_JS)


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    input_path, output_path = sys.argv[1], sys.argv[2]

    with open(input_path, encoding="utf-8") as f:
        videos = json.load(f)

    t0 = time.time()
    out = {}
    with attach() as (pw, browser, ctx):
        page = ctx.new_page()
        for i, v in enumerate(videos, 1):
            label, url = v["label"], v["url"]
            print(f"\n[{i}/{len(videos)}] {label}", file=sys.stderr)
            v_t0 = time.time()
            try:
                comments = scrape_comments(page, url)
            except Exception as e:
                print(f"  失败: {e}", file=sys.stderr)
                out[url] = {"label": label, "comments": [], "error": str(e)}
                continue
            print(f"  +{len(comments)} 条 ({time.time()-v_t0:.1f}s)", file=sys.stderr)
            out[url] = {"label": label, "comment_count": len(comments), "comments": comments}
        page.close()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    total = sum(d.get("comment_count", 0) for d in out.values())
    print(f"\n完成: {time.time()-t0:.1f}s | 总评论: {total} | 输出: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
