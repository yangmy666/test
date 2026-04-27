"""遍历每篇论文页面抓 abstract + 年份/卷期。"""
import sys, time, json, re
sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

with open("C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_raw.json", encoding="utf-8") as f:
    raw = json.load(f)

papers = raw["filtered"]
print(f"开始抓 {len(papers)} 篇摘要...", file=sys.stderr)

EXTRACT_JS = r"""
() => {
  // 标题
  const title = document.querySelector('.page_title, h1.title, h1')?.textContent?.trim() || '';
  // 摘要
  const absEl = document.querySelector('.abstract, section.abstract, [class*="abstract"]');
  let abstract = '';
  if (absEl) {
    abstract = absEl.textContent.trim().replace(/^Abstract\s*/i, '');
  }
  // 作者
  const authors = document.querySelector('.authors, ul.authors, .author-list')?.textContent?.trim()?.replace(/\s+/g, ' ').slice(0, 400) || '';
  // 卷/期 — 通常在 breadcrumbs 或 issue 链接里
  const issueLink = document.querySelector('a[href*="/issue/view/"]');
  const issueText = issueLink?.textContent?.trim() || '';
  // DOI
  const doiEl = document.querySelector('.doi, a[href*="doi.org"]');
  const doi = doiEl?.textContent?.trim() || doiEl?.href || '';
  // 关键词
  const kwEl = document.querySelector('.keywords, [class*="keyword"]');
  const keywords = kwEl?.textContent?.trim()?.replace(/^Keywords?:?\s*/i, '').slice(0, 300) || '';
  // 发布日期
  const pubEl = document.querySelector('.published, [class*="publish"]');
  const published = pubEl?.textContent?.trim()?.slice(0, 60) || '';
  return { title: title.slice(0, 250), abstract: abstract.slice(0, 3000), authors, issueText, doi, keywords, published };
}
"""

results = []
with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    for i, p in enumerate(papers, 1):
        try:
            page.goto(p["url"], wait_until="domcontentloaded", timeout=15000)
            time.sleep(0.8)
            data = page.evaluate(EXTRACT_JS)
            results.append({**p, **data})
            if i % 10 == 0:
                print(f"  {i}/{len(papers)} 完成", file=sys.stderr)
        except Exception as e:
            print(f"  [{i}] 失败 {p['url']}: {str(e)[:80]}", file=sys.stderr)
            results.append({**p, "abstract": "", "issueText": "", "error": str(e)[:200]})
    page.close()

out_path = "C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_full.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n完成 {len(results)} 篇，保存到 {out_path}", file=sys.stderr)

# 简单按 issue/卷期分类
from collections import Counter
issues = Counter(p.get("issueText", "Unknown") for p in results)
print("\n=== 按卷期分布 ===")
for issue, n in issues.most_common():
    print(f"  {n}× {issue[:80]}")
