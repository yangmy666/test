"""AAAI 论文搜索：找量化交易相关。"""
import sys, time, json, re
from urllib.parse import quote

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

# 量化/金融相关关键词
KEYWORDS = [
    "stock prediction",
    "stock market",
    "trading",
    "portfolio",
    "financial forecast",
    "algorithmic trading",
    "quantitative trading",
    "high frequency trading",
    "limit order book",
    "market microstructure",
    "asset pricing",
    "price prediction",
    "financial time series",
    "alpha factor",
    "volatility prediction",
    "risk management",
    "factor model",
    "market regime",
    "financial sentiment",
    "FinBERT",
    "FinLLM",
    "investment strategy",
    "reinforcement learning trading",
]

EXTRACT_JS = r"""
() => {
  const items = document.querySelectorAll('.obj_article_summary, article.search-result, .result, li.search_results_li');
  const results = [];
  items.forEach(item => {
    const titleEl = item.querySelector('.title a, h3 a, h4 a, a.title');
    const authorEl = item.querySelector('.authors, .meta, .author');
    const title = titleEl?.textContent?.trim() || '';
    const url = titleEl?.href || '';
    const authors = authorEl?.textContent?.trim()?.replace(/\s+/g, ' ').slice(0, 250) || '';
    if (title) results.push({ title, url, authors });
  });
  // 备用选择器
  if (results.length === 0) {
    const allLinks = document.querySelectorAll('a[href*="/article/"]');
    allLinks.forEach(a => {
      const t = a.textContent.trim();
      if (t.length > 15 && t.length < 300 && results.length < 50) {
        const parent = a.closest('div, li, article');
        const authors = parent?.querySelector('.authors, .meta')?.textContent?.trim()?.slice(0, 250) || '';
        results.push({ title: t.slice(0, 250), url: a.href, authors });
      }
    });
  }
  return results;
}
"""

all_papers = {}

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    for kw in KEYWORDS:
        url = f"https://ojs.aaai.org/index.php/AAAI/search/search?query={quote(kw)}"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(2.5)
            page.evaluate("window.scrollBy(0, 1500)")
            time.sleep(1)
            # 翻多页
            for pg in range(3):
                results = page.evaluate(EXTRACT_JS)
                added = 0
                for r in results:
                    u = r["url"]
                    if not u or u in all_papers:
                        continue
                    r["matched_keyword"] = kw
                    all_papers[u] = r
                    added += 1
                # 翻下一页
                next_btn = page.query_selector('a.next:not(.disabled), a[rel="next"]')
                if not next_btn or pg == 2:
                    break
                try:
                    next_btn.click()
                    time.sleep(2)
                except:
                    break
            print(f"  [{kw}] 累计 {len(all_papers)}", file=sys.stderr)
        except Exception as e:
            print(f"  [{kw}] 失败: {str(e)[:100]}", file=sys.stderr)
    page.close()

print(f"\n总抓 {len(all_papers)} 篇唯一论文")

# 标题关键词过滤——只保留真正和量化交易/金融相关的
FINANCIAL_RE = re.compile(
    r"(stock|trading|portfolio|finan|invest|market|asset|price|volatility|risk|alpha|"
    r"option|future|derivative|hedg|arbitr|bond|equit|forex|crypto|bitcoin|economic|"
    r"order book|microstructure|sentiment.*finan|finan.*sentiment|FinBERT|FinLLM|FinGPT|"
    r"high.frequency|HFT|alpha.factor|factor.model|regime.detect|return predict|"
    r"buy.sell|backtest|sharpe|kelly|CAPM|monte carlo|black.scholes|GARCH)",
    re.IGNORECASE,
)

filtered = {}
for u, p in all_papers.items():
    title = p.get("title", "")
    if FINANCIAL_RE.search(title):
        filtered[u] = p

print(f"金融/量化相关: {len(filtered)} 篇")

# 保存
out_path = "C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_raw.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"all": list(all_papers.values()), "filtered": list(filtered.values())}, f, ensure_ascii=False, indent=2)
print(f"保存到 {out_path}")

# 列出过滤后的所有
print("\n=== 金融/量化相关论文 ===")
for p in filtered.values():
    print(f"  · {p['title'][:120]}")
    print(f"    {p['url']}")
    print(f"    [matched: {p['matched_keyword']}]")
