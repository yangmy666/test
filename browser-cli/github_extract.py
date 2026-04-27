"""提取所有论文摘要中的 GitHub/项目链接，方便用户去找开源实现。"""
import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open("C:/Users/yang/desktop/test_project/browser-cli/aaai_papers_full.json", encoding='utf-8') as f:
    aaai = json.load(f)
with open("C:/Users/yang/desktop/test_project/browser-cli/arxiv_papers.json", encoding='utf-8') as f:
    arxiv = json.load(f)
try:
    with open("C:/Users/yang/desktop/test_project/browser-cli/openreview_papers.json", encoding='utf-8') as f:
        openreview = json.load(f)
except FileNotFoundError:
    openreview = []

papers = []
for p in aaai:
    issue = p.get("issueText", "")
    m = re.search(r"Vol\.\s*(\d+)", issue)
    year = {40:2026,39:2025,38:2024}.get(int(m.group(1))) if m else None
    if year and year >= 2024:
        papers.append({"src":"AAAI","title":p.get("title",""),"abstract":p.get("abstract","") or "",
                       "url":p.get("url",""),"year":year})
for p in arxiv:
    pub = p.get("published","")
    year = int(pub[:4]) if pub else None
    if year and year >= 2024:
        papers.append({"src":"arXiv","title":p.get("title",""),"abstract":p.get("summary","") or "",
                       "url":p.get("id",""),"year":year})
for p in openreview:
    if p.get("year") and p["year"] >= 2024:
        papers.append({"src":"OpenReview","title":p.get("title",""),"abstract":p.get("abstract","") or "",
                       "url":p.get("id",""),"year":p["year"]})

print(f"扫描 {len(papers)} 篇")

# GitHub 链接 + 项目页 + Code 关键词
GITHUB_RE = re.compile(r"(https?://(?:www\.)?github\.com/[\w\-\.]+/[\w\-\.]+)", re.IGNORECASE)
HUGGINGFACE_RE = re.compile(r"(https?://huggingface\.co/[\w\-\./]+)", re.IGNORECASE)
PROJECT_RE = re.compile(r"(https?://[\w\-\.]+\.(?:github\.io|netlify\.app|vercel\.app)/[\w\-\.]+)", re.IGNORECASE)
CODE_AVAILABLE_RE = re.compile(r"(code (?:is )?(?:available|released|open[-\s]?sourced?))|"
                                r"(code (?:can be )?(?:found|accessed))|"
                                r"(open[-\s]?source(?:d)?)|"
                                r"(publicly available)|"
                                r"(release.*code)|"
                                r"(implementation.*available)", re.IGNORECASE)

results = {"github": [], "huggingface": [], "project": [], "code_claim": []}

for p in papers:
    text = p["abstract"]
    # GitHub 链接
    for m in GITHUB_RE.finditer(text):
        results["github"].append({"link": m.group(1), "paper": p["title"][:120], "year": p["year"], "url": p["url"]})
    # HF
    for m in HUGGINGFACE_RE.finditer(text):
        results["huggingface"].append({"link": m.group(1), "paper": p["title"][:120], "year": p["year"], "url": p["url"]})
    # 项目页
    for m in PROJECT_RE.finditer(text):
        results["project"].append({"link": m.group(1), "paper": p["title"][:120], "year": p["year"], "url": p["url"]})
    # 代码声明
    if CODE_AVAILABLE_RE.search(text) and "github.com" not in text.lower():
        results["code_claim"].append({"paper": p["title"][:120], "year": p["year"], "url": p["url"]})

print(f"\nGitHub 直链: {len(results['github'])}")
print(f"HuggingFace: {len(results['huggingface'])}")
print(f"项目页: {len(results['project'])}")
print(f"声称代码可用但未给链接: {len(results['code_claim'])}")

# 写报告
md = []
md.append("# 量化 AI 论文 · 开源代码索引\n\n")
md.append(f"_扫描 {len(papers)} 篇 2024+ 论文，提取摘要里的 GitHub/项目链接_\n\n")

md.append("## 🔗 直接的 GitHub 链接\n\n")
md.append("**这些是论文摘要里直接给出的开源仓库地址。**\n\n")
md.append("| 仓库 | 论文 | 年份 |\n|---|---|---:|\n")
seen = set()
for r in results["github"]:
    key = r["link"]
    if key in seen: continue
    seen.add(key)
    md.append(f"| {r['link']} | {r['paper']} | {r['year']} |\n")

md.append("\n## 🤗 HuggingFace 链接\n\n")
if results["huggingface"]:
    md.append("| 链接 | 论文 |\n|---|---|\n")
    seen = set()
    for r in results["huggingface"]:
        if r["link"] in seen: continue
        seen.add(r["link"])
        md.append(f"| {r['link']} | {r['paper']} |\n")
else:
    md.append("（暂无）\n")

md.append("\n## 📦 项目主页\n\n")
if results["project"]:
    md.append("| 链接 | 论文 |\n|---|---|\n")
    seen = set()
    for r in results["project"]:
        if r["link"] in seen: continue
        seen.add(r["link"])
        md.append(f"| {r['link']} | {r['paper']} |\n")
else:
    md.append("（暂无）\n")

md.append(f"\n## 📝 声称'代码可用'但摘要没给链接的论文（共 {len(results['code_claim'])} 篇）\n\n")
md.append("**这些论文有可能在论文 PDF 里附了 GitHub 链接，但摘要没有。建议优先去 PDF 找。**\n\n")
md.append("（仅列前 30 篇）\n\n")
for r in results["code_claim"][:30]:
    md.append(f"- [{r['year']}] {r['paper']} → {r['url']}\n")

md.append("\n---\n\n## 💡 找代码的实用建议\n\n")
md.append("1. **先 Google：** 论文标题 + \"github\" 通常能找到\n")
md.append("2. **去 PaperWithCode**：https://paperswithcode.com 把论文和代码绑定\n")
md.append("3. **arXiv 论文页**：左侧 'Code & Data' 链接通常有\n")
md.append("4. **第一作者 GitHub**：很多研究者把代码放自己 profile 而不是 institution\n")
md.append("5. **Issues 区**：作者经常在 issue 里回应 \"code coming soon\"，能等到时间表\n\n")

out_path = "C:/Users/yang/desktop/test_project/量化AI论文_开源代码索引.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write("".join(md))

print(f"\n✅ 开源索引已写入 {out_path}")
print(f"   长度: {sum(len(s) for s in md):,} 字符")
