"""读 B 站视频描述 + 评论（含 shadow DOM）。"""
import sys, time, json
sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

VIDEOS = [
    ("辟谣派 sharp动漫", "https://www.bilibili.com/video/BV1qQdzBjEnv/"),
    ("辟谣派 老何不姓何", "https://www.bilibili.com/video/BV1vzd9BDECw/"),
    ("中性 苏夜漫剪", "https://www.bilibili.com/video/BV1nNDQBBE8B/"),
    ("定档派 拿真心换伤心", "https://www.bilibili.com/video/BV1m3d6BYETx/"),
    ("定档派 -小刘漫剪-", "https://www.bilibili.com/video/BV1QqQ3B7Ei8/"),
    ("定档派 鹅厂3.25亿", "https://www.bilibili.com/video/BV1AJDrBEEB5/"),
    ("电影官宣", "https://www.bilibili.com/video/BV1vedSBBEz4/"),
]

EXTRACT_JS = r"""
() => {
  // 描述
  const descEl = document.querySelector('.basic-desc-info, #v_desc');
  const desc = descEl?.textContent?.trim() || '';

  // 评论：shadow DOM 内 bili-comments 下的 bili-comment-thread-renderer
  const commentsRoot = document.querySelector('bili-comments');
  const comments = [];
  if (commentsRoot && commentsRoot.shadowRoot) {
    // bili-comments -> shadowRoot -> bili-comment-thread-renderer (or nested)
    const findThreads = (root) => {
      const threads = root.querySelectorAll('bili-comment-thread-renderer');
      const result = [];
      threads.forEach(t => {
        if (t.shadowRoot) {
          // 评论内容在 shadow 中再找
          const contentEl = t.shadowRoot.querySelector('bili-rich-text, .reply-content');
          let text = '';
          if (contentEl?.shadowRoot) {
            text = contentEl.shadowRoot.textContent.trim();
          } else if (contentEl) {
            text = contentEl.textContent.trim();
          } else {
            text = t.shadowRoot.textContent.trim();
          }
          // 找点赞数
          const likeEl = t.shadowRoot.querySelector('.reply-action-counter, [class*="like"]');
          const likes = likeEl?.textContent?.trim() || '';
          result.push({ text: text.slice(0, 400), likes });
        }
      });
      return result;
    };
    comments.push(...findThreads(commentsRoot.shadowRoot));
  }

  return {
    title: document.title,
    desc: desc.slice(0, 1000),
    commentCount: comments.length,
    comments: comments.slice(0, 10)
  };
}
"""

results = []
with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    for label, url in VIDEOS:
        print(f"\n=== {label} ===", file=sys.stderr)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(4)
            # 滚到评论区触发懒加载
            for _ in range(3):
                page.evaluate("window.scrollBy(0, 1500)")
                time.sleep(1)
            data = page.evaluate(EXTRACT_JS)
            results.append({"label": label, "url": url, **data})
            print(f"标题: {data['title'][:80]}", file=sys.stderr)
            print(f"描述: {data['desc'][:300]}", file=sys.stderr)
            print(f"评论 ({data['commentCount']}):", file=sys.stderr)
            for c in data['comments'][:6]:
                print(f"  · {c['text'][:150]}", file=sys.stderr)
        except Exception as e:
            print(f"  失败: {e}", file=sys.stderr)
        time.sleep(2)
    page.close()

print(json.dumps(results, ensure_ascii=False, indent=2))
