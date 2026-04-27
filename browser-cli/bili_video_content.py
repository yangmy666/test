"""读取 B 站视频的描述 + 顶部评论，了解视频实际内容（不只是标题）。"""
import sys, time, json
sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

VIDEOS = [
    # 标题说"全是谣言"的
    ("辟谣派 sharp动漫 04-17", "https://www.bilibili.com/video/BV1qQdzBjEnv/", "《灵笼3》6月13日上线？3.25亿经费？官方实锤：全是谣言！"),
    ("辟谣派 老何不姓何 04-19", "https://www.bilibili.com/video/BV1vzd9BDECw/", "灵笼第三季回归，6月播，鹅厂播？？谣言！！！"),
    ("中性 苏夜漫剪 04-12", "https://www.bilibili.com/video/BV1nNDQBBE8B/", "网传《灵笼第三季》6月腾讯独播，是实锤还是溜粉？"),
    # 标题说"定档"的
    ("定档派 拿真心换伤心 04-17", "https://www.bilibili.com/video/BV1m3d6BYETx/", "灵笼第三季定档六月。新的故事开始"),
    ("定档派 -小刘漫剪- 04-15", "https://www.bilibili.com/video/BV1QqQ3B7Ei8/", "灵笼第三季正式定档于6月播出，播出平台竟然从小破站换到了鹅厂"),
    ("定档派 老何不姓何之外 04-08", "https://www.bilibili.com/video/BV1AJDrBEEB5/", "灵笼第三季终于要在6月杀回来了！鹅厂直接狂砸3.25亿"),
    # 官方相关
    ("电影官宣 04-21", "https://www.bilibili.com/video/BV1vedSBBEz4/", "《灵笼》院线电影官宣"),
]

EXTRACT_JS = r"""
() => {
  // 视频描述
  const descEl = document.querySelector('.basic-desc-info, [class*="desc-info"], [class*="-desc-text"], #v_desc');
  const desc = descEl?.textContent?.trim() || '';
  // 标题
  const title = document.querySelector('h1, .video-title')?.textContent?.trim() || '';
  // 简介按钮可能要展开
  // 顶部评论（通常按热度排序）
  const comments = Array.from(document.querySelectorAll('.reply-item, .comment-item, [class*="comment-item"], [class*="reply-list"] [class*="content"]'))
    .slice(0, 15)
    .map(c => c.textContent.trim().slice(0, 300))
    .filter(t => t.length > 5);
  return { title, desc: desc.slice(0, 800), commentCount: comments.length, comments };
}
"""

results = []
with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    for label, url, expected in VIDEOS:
        print(f"\n=== {label} ===", file=sys.stderr)
        print(f"标题: {expected}", file=sys.stderr)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(4)
            # 滚到评论区
            page.evaluate("window.scrollBy(0, 1500)")
            time.sleep(2)
            # 试图点开"展开更多"以获取完整简介
            try:
                page.evaluate("""() => {
                  const btn = Array.from(document.querySelectorAll('span, button, div'))
                    .find(e => /展开|更多|查看更多/.test(e.textContent || '') && e.children.length === 0);
                  if (btn) btn.click();
                }""")
                time.sleep(0.8)
            except: pass
            data = page.evaluate(EXTRACT_JS)
            results.append({"label": label, "url": url, "data": data})
            print(f"简介: {data['desc'][:300]}", file=sys.stderr)
            print(f"评论 {data['commentCount']} 条 (top 5):", file=sys.stderr)
            for c in data['comments'][:5]:
                print(f"  · {c[:120]}", file=sys.stderr)
        except Exception as e:
            print(f"  失败: {e}", file=sys.stderr)
        time.sleep(2)
    page.close()

print(json.dumps(results, ensure_ascii=False, indent=2))
