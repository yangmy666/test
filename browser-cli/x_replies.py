"""X 推文回复抓取器。

用法：python x_replies.py <input.json> <output.json>

策略：
- 进入 /status/<id> 页面
- 第一个 article[data-testid="tweet"] 是原推（跳过）
- 后续 article 是回复
- 滚动加载更多
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
  const tweets = document.querySelectorAll('article[data-testid="tweet"]');
  // 第一条是原推，跳过
  return Array.from(tweets).slice(1).map(t => {
    const userName = t.querySelector('[data-testid="User-Name"]')?.textContent || '';
    const text = t.querySelector('[data-testid="tweetText"]')?.textContent || '';
    const stats = {};
    ['reply','retweet','like'].forEach(k => {
      const el = t.querySelector('[data-testid="' + k + '"]');
      stats[k] = el?.textContent.trim() || '';
    });
    const viewA = Array.from(t.querySelectorAll('a')).find(a => a.href.includes('/analytics'));
    const views = viewA?.textContent.trim() || '';
    const timeEl = t.querySelector('time');
    return {
      author: userName.slice(0, 150),
      text: text.slice(0, 800),
      reply: stats.reply,
      retweet: stats.retweet,
      like: stats.like,
      views: views,
      time: timeEl?.getAttribute('datetime'),
    };
  }).filter(c => c.text);
}
"""


def scroll_replies(page, max_iter=30):
    prev_count, stable = 0, 0
    for _ in range(max_iter):
        page.evaluate("window.scrollBy(0, 2500)")
        time.sleep(0.6)
        cur = page.evaluate("document.querySelectorAll('article[data-testid=\"tweet\"]').length")
        if cur == prev_count:
            stable += 1
            if stable >= 4:
                return cur
        else:
            stable = 0
        prev_count = cur
    return prev_count


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
            v_t0 = time.time()
            print(f"\n[{i}/{len(videos)}] {label}", file=sys.stderr)
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(3)
                try:
                    page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
                except Exception:
                    print(f"  原推未加载", file=sys.stderr)
                    out[url] = {"label": label, "comments": [], "error": "tweet not loaded"}
                    continue
                count = scroll_replies(page)
                replies = page.evaluate(EXTRACT_JS)
                print(f"  {count} 条 article (含原推), 提取 {len(replies)} 条回复 ({time.time()-v_t0:.1f}s)", file=sys.stderr)
                out[url] = {"label": label, "comment_count": len(replies), "comments": replies}
                time.sleep(2)
            except Exception as e:
                print(f"  失败: {str(e)[:120]}", file=sys.stderr)
                out[url] = {"label": label, "comments": [], "error": str(e)[:200]}
                time.sleep(3)
        page.close()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    total = sum(d.get("comment_count", 0) for d in out.values())
    success = sum(1 for d in out.values() if d.get("comment_count", 0) > 0)
    print(f"\n完成: {time.time()-t0:.1f}s | {success}/{len(videos)} 成功 | 共 {total} 条 | {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
