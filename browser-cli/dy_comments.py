"""抖音视频评论抓取器（改进版）。

用法：python dy_comments.py <input.json> <output.json>

重点改进：
- 推荐用 modal_id URL（搜索页弹出模式），直接 /video/ URL 抗爬更严
- 等评论区出现的最大耐心改为 30s，分多轮尝试触发懒加载
- 用 [data-e2e="comment-item"] 是稳定的，但内部用 [class*="C7LroK_h"] 抓正文以避免误抓用户名
"""
import sys
import time
import json

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach


# 提取：作者 + 正文 + 时间·地区 + 点赞
# 关键策略：
#  - 作者：第一个 a[href*="/user/"]
#  - 正文：div.C7LroK_h（这个类比较稳定，是评论文字外框）
#    备份：找位置在 author 后、time 前的最大文本 span
#  - 时间地区：含"前·"或"前"的纯文本 span
#  - 点赞：紧挨"分享"按钮的纯数字 span
EXTRACT_JS = r"""
() => {
  const items = document.querySelectorAll('[data-e2e="comment-item"]');
  return Array.from(items).map(it => {
    const authorA = it.querySelector('a[href*="/user/"]');
    const author = authorA?.textContent?.trim() || null;

    // 正文：优先用类名 C7LroK_h（评论文字容器）
    let text = '';
    const textBox = it.querySelector('[class*="C7LroK_h"], [class*="comment-content"]');
    if (textBox) {
      text = textBox.textContent.trim();
    }

    // 时间·地区
    let time_loc = '';
    for (const s of it.querySelectorAll('span')) {
      const t = s.textContent.trim();
      if (s.children.length === 0 && /(分钟|小时|天|周|月|年)前/.test(t) && t.length < 40) {
        time_loc = t;
        break;
      }
    }

    // 点赞：找 stats container 内的纯数字
    let likes = '';
    const stats = it.querySelector('[class*="comment-item-stats"]');
    if (stats) {
      for (const s of stats.querySelectorAll('span, p')) {
        const t = s.textContent.trim();
        if (s.children.length === 0 && /^\d+$/.test(t) && t.length < 8) {
          likes = t;
          break;
        }
      }
    }

    return { author, text, time_loc, likes };
  }).filter(c => c.text && c.text.length > 1);
}
"""


def wait_for_comments(page, max_seconds=20):
    """耐心等评论区出现，分阶段触发懒加载。"""
    deadline = time.time() + max_seconds
    while time.time() < deadline:
        # 触发评论加载：先大滚动让 video player 走，再回到 800px 触发 IntersectionObserver
        page.evaluate(
            """
            () => {
              window.scrollTo(0, 0);
              setTimeout(() => window.scrollTo(0, 1500), 100);
              setTimeout(() => window.scrollTo(0, 700), 400);
              setTimeout(() => window.scrollTo(0, 1200), 800);
            }
            """
        )
        time.sleep(1.5)
        cur = page.evaluate("document.querySelectorAll('[data-e2e=\"comment-item\"]').length")
        if cur > 0:
            return cur
    return 0


def scroll_comment_list(page, max_iter=40):
    """滚动评论区容器持续加载。"""
    prev_count, stable = 0, 0
    for _ in range(max_iter):
        page.evaluate(
            """
            () => {
              const list = document.querySelector('[data-e2e="comment-list"]');
              if (list) {
                let target = list;
                while (target && target.scrollHeight <= target.clientHeight) target = target.parentElement;
                if (target) target.scrollBy(0, 1500);
              }
              window.scrollBy(0, 500);
            }
            """
        )
        time.sleep(0.55)
        cur = page.evaluate("document.querySelectorAll('[data-e2e=\"comment-item\"]').length")
        if cur == prev_count:
            stable += 1
            if stable >= 5:
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
                # 等评论区出现 - 给足耐心
                count = wait_for_comments(page, max_seconds=25)
                if count == 0:
                    print(f"  ⚠ 25s 后仍无评论 ({time.time()-v_t0:.1f}s)", file=sys.stderr)
                    out[url] = {"label": label, "comments": [], "error": "comments did not appear"}
                    # 间隔 5s 避免反爬连环触发
                    time.sleep(5)
                    continue
                # 滚动加载更多
                count = scroll_comment_list(page)
                comments = page.evaluate(EXTRACT_JS)
                print(f"  ✓ {count} 条容器, {len(comments)} 条文本 ({time.time()-v_t0:.1f}s)", file=sys.stderr)
                out[url] = {"label": label, "comment_count": len(comments), "comments": comments}
                time.sleep(3)  # 视频间间隔
            except Exception as e:
                print(f"  ✗ 失败: {str(e)[:120]}", file=sys.stderr)
                out[url] = {"label": label, "comments": [], "error": str(e)[:200]}
                time.sleep(5)
        page.close()

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    total = sum(d.get("comment_count", 0) for d in out.values())
    success = sum(1 for d in out.values() if d.get("comment_count", 0) > 0)
    print(f"\n完成: {time.time()-t0:.1f}s | {success}/{len(videos)} 成功 | 共 {total} 条评论 | {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
