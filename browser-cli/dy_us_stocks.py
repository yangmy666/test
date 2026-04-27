"""抖音美股视频聚合搜索（按点赞数排序）。

抖音搜索卡片只显示点赞数不显示播放量，用点赞作为热度代理指标。
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


def parse_likes(s):
    if not s:
        return 0
    s = s.strip().replace(",", "")
    m = re.match(r"^([\d.]+)\s*([万千wW])?$", s)
    if not m:
        return 0
    n = float(m.group(1))
    unit = (m.group(2) or "").lower()
    if unit in ("万", "w"):
        n *= 10000
    elif unit == "千":
        n *= 1000
    return int(n)


def parse_age_hours(s):
    if not s:
        return None
    s = s.strip()
    m = re.search(r"(\d+)\s*分钟", s)
    if m:
        return float(m.group(1)) / 60
    m = re.search(r"(\d+)\s*小时", s)
    if m:
        return float(m.group(1))
    m = re.search(r"(\d+)\s*天", s)
    if m:
        return float(m.group(1)) * 24
    if "昨天" in s:
        return 30
    if "前天" in s:
        return 54
    if "刚刚" in s or "刚才" in s:
        return 0.1
    m = re.search(r"(\d{4})[.\-](\d{1,2})[.\-](\d{1,2})", s)
    if m:
        try:
            d = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            return (TODAY - d).total_seconds() / 3600
        except ValueError:
            pass
    m = re.match(r"^(\d{1,2})[.\-](\d{1,2})$", s)
    if m:
        try:
            d = datetime(2026, int(m.group(1)), int(m.group(2)))
            return (TODAY - d).total_seconds() / 3600
        except ValueError:
            pass
    return None


EXTRACT_JS = r"""
() => {
  const cards = document.querySelectorAll('div.search-result-card');
  return Array.from(cards).map(card => {
    // 1) 找所有纯数字/数字+万千w 叶节点
    const numericLeaves = [];
    const walker = el => {
      if (el.children.length === 0) {
        const t = el.textContent.trim();
        if (/^[\d.]+[万千wW]?$/.test(t) || /^\d{1,2}:\d{2}$/.test(t)) {
          numericLeaves.push(t);
        }
      } else {
        for (const c of el.children) walker(c);
      }
    };
    walker(card);
    // 时长是 mm:ss，点赞数是除时长外的纯数字
    const duration = numericLeaves.find(t => /^\d{1,2}:\d{2}$/.test(t)) || null;
    const likes_str = numericLeaves.find(t => !/^\d{1,2}:\d{2}$/.test(t)) || null;

    // 2) 解析全文本：[图文 N | mm:ss N] Title @Author · TimeAgo
    const text = card.textContent;
    const isImage = text.startsWith('图文');
    const type_label = duration ? '视频' : (isImage ? '图文' : '其他');

    // 3) 标题：去掉前缀和后缀
    let title = text;
    if (isImage && likes_str) {
      title = title.replace(new RegExp('^图文' + likes_str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')), '');
    } else if (duration && likes_str) {
      title = title.replace(new RegExp('^' + duration.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + likes_str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')), '');
    }
    const atIdx = title.indexOf('@');
    if (atIdx > 0) title = title.slice(0, atIdx).trim();

    // 4) 作者 + 时间
    const tail = atIdx > 0 ? text.slice(text.indexOf('@', atIdx > 0 ? card.textContent.indexOf('@') : 0)) : '';
    const tailMatch = tail.match(/@([^·]+)·\s*(.+?)\s*$/);
    const author = tailMatch ? tailMatch[1].trim() : null;
    const time_ago = tailMatch ? tailMatch[2].trim() : null;

    return { type_label, duration, likes_str, title, author, time_ago };
  });
}
"""


t0 = time.time()
all_cards = []

with attach() as (pw, browser, ctx):
    page = next((p for p in ctx.pages if "douyin.com/search" in p.url), None)
    if page is None:
        page = ctx.new_page()
    url = "https://www.douyin.com/search/%E7%BE%8E%E8%82%A1?publish_time=7&sort_type=2"
    page.goto(url, wait_until="domcontentloaded", timeout=20000)
    time.sleep(3)

    prev_count, stable = 0, 0
    for i in range(40):
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(0.7)
        cur = page.evaluate("document.querySelectorAll('div.search-result-card').length")
        if cur == prev_count:
            stable += 1
            if stable >= 4:
                break
        else:
            stable = 0
        prev_count = cur
    print(f"  最终 {prev_count} 张卡片", file=sys.stderr)

    raw = page.evaluate(EXTRACT_JS)

# 过滤 + 排序
filtered = []
for c in raw:
    age = parse_age_hours(c.get("time_ago"))
    likes = parse_likes(c.get("likes_str"))
    if age is None or age > 72:
        continue
    if not c.get("title"):
        continue
    c["likes_n"] = likes
    c["age_h"] = age
    filtered.append(c)

filtered.sort(key=lambda x: x["likes_n"], reverse=True)

print(f"3 天内: {len(filtered)} 张, 总耗时 {time.time()-t0:.1f}s", file=sys.stderr)

with open("C:/Users/yang/desktop/test_project/browser-cli/dy_results.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, ensure_ascii=False, indent=2)

print(json.dumps(filtered[:10], ensure_ascii=False, indent=2))
