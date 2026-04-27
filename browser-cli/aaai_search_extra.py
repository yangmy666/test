"""补充搜索：LLM agent、自动交易、多模态、新型金融 AI 等。"""
import sys, time, json, re
from urllib.parse import quote

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

with open("C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_full.json", encoding="utf-8") as f:
    existing = json.load(f)
existing_urls = {p["url"] for p in existing}
print(f"已有 {len(existing_urls)} 篇")

EXTRA_KEYWORDS = [
    "LLM agent finance",
    "FinGPT",
    "earnings call",
    "deep learning stock",
    "neural network trading",
    "graph stock",
    "financial graph",
    "transformer stock",
    "finance LLM",
    "stock movement",
    "diffusion finance",
    "alpha mining",
    "financial reasoning",
    "FinAgent",
    "market simulation",
    "financial GPT",
    "financial multi-agent",
    "credit risk",
]

EXTRACT_LIST_JS = r"""
() => {
  const items = document.querySelectorAll('.obj_article_summary, article.search-result, .result, li.search_results_li');
  const results = [];
  items.forEach(item => {
    const titleEl = item.querySelector('.title a, h3 a, h4 a, a.title');
    const title = titleEl?.textContent?.trim() || '';
    const url = titleEl?.href || '';
    if (title && url) results.push({ title, url });
  });
  if (results.length === 0) {
    const allLinks = document.querySelectorAll('a[href*="/article/"]');
    allLinks.forEach(a => {
      const t = a.textContent.trim();
      if (t.length > 15 && t.length < 300 && results.length < 50) {
        results.push({ title: t.slice(0, 250), url: a.href });
      }
    });
  }
  return results;
}
"""

EXTRACT_PAPER_JS = r"""
() => {
  const title = document.querySelector('.page_title, h1.title, h1')?.textContent?.trim() || '';
  const absEl = document.querySelector('.abstract, section.abstract, [class*="abstract"]');
  const abstract = absEl?.textContent?.trim()?.replace(/^Abstract\s*/i, '') || '';
  const authors = document.querySelector('.authors, ul.authors')?.textContent?.trim()?.replace(/\s+/g, ' ').slice(0, 400) || '';
  const issueLink = document.querySelector('a[href*="/issue/view/"]');
  const issueText = issueLink?.textContent?.trim() || '';
  return { title: title.slice(0, 250), abstract: abstract.slice(0, 3000), authors, issueText };
}
"""

FINANCIAL_RE = re.compile(
    r"(stock|trading|portfolio|finan|invest|market|asset|price|volatility|risk|alpha|"
    r"option|future|derivative|hedg|arbitr|bond|equit|forex|crypto|economic|"
    r"earnings|fundamental|FinBERT|FinGPT|FinLLM|backtest|sharpe|return predict)",
    re.IGNORECASE,
)

new_papers = {}
with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    for kw in EXTRA_KEYWORDS:
        try:
            url = f"https://ojs.aaai.org/index.php/AAAI/search/search?query={quote(kw)}"
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(2)
            page.evaluate("window.scrollBy(0, 1500)")
            time.sleep(1)
            results = page.evaluate(EXTRACT_LIST_JS)
            added = 0
            for r in results:
                u = r["url"]
                if u in existing_urls or u in new_papers:
                    continue
                if not FINANCIAL_RE.search(r["title"]):
                    continue
                new_papers[u] = {**r, "matched_keyword": kw}
                added += 1
            print(f"  [{kw}] 新增 {added} (总新 {len(new_papers)})", file=sys.stderr)
        except Exception as e:
            print(f"  [{kw}] 失败 {str(e)[:80]}", file=sys.stderr)

    print(f"\n抓 {len(new_papers)} 篇补充论文，开始抓摘要...", file=sys.stderr)
    for i, (u, p) in enumerate(new_papers.items(), 1):
        try:
            page.goto(u, wait_until="domcontentloaded", timeout=15000)
            time.sleep(0.7)
            data = page.evaluate(EXTRACT_PAPER_JS)
            new_papers[u].update(data)
        except Exception as e:
            print(f"  [{i}] 失败: {str(e)[:60]}", file=sys.stderr)

    page.close()

# 合并到原数据
all_papers = list(existing) + list(new_papers.values())
out_path = "C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_full.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_papers, f, ensure_ascii=False, indent=2)

print(f"\n总计 {len(all_papers)} 篇 (新增 {len(new_papers)})", file=sys.stderr)

# 列出新增的
print("\n=== 新增论文 ===")
for p in new_papers.values():
    print(f"  · {p.get('title','')[:120]}")
    print(f"    {p['url']}")
