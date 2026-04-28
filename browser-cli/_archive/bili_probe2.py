"""Probe B 站搜索结果卡片当前结构，找播放量在哪。"""
import sys, time
from urllib.parse import quote
sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
from connect import attach

PROBE_JS = r"""
() => {
  const c = document.querySelector('div.bili-video-card');
  if (!c) return {error: 'no cards'};
  const out = {};
  // try several selectors for play count
  const queries = {
    'stats-text': '.bili-video-card__stats--text',
    'stats-item': '.bili-video-card__stats--item',
    'stats-any': '[class*="stats"]',
    'stats-span': '.bili-video-card__stats span',
  };
  for (const [k, sel] of Object.entries(queries)) {
    out[k] = Array.from(c.querySelectorAll(sel)).slice(0,5).map(el => ({
      cls: (el.className && typeof el.className === 'string') ? el.className.slice(0,80) : (el.getAttribute('class') || '').slice(0,80),
      tag: el.tagName,
      txt: (el.innerText || el.textContent || '').slice(0,40),
    }));
  }
  // also: find empty-class spans with numeric text and show their parent path
  const emptySpans = [];
  c.querySelectorAll('span').forEach(s => {
    const cls = (s.className && typeof s.className === 'string') ? s.className : '';
    if (cls === '' && /\d/.test(s.innerText || '')) {
      const parents = [];
      let p = s.parentElement;
      for (let i = 0; i < 4 && p; i++) {
        parents.push(`${p.tagName}.${(typeof p.className === 'string' ? p.className : '').slice(0,40)}`);
        p = p.parentElement;
      }
      emptySpans.push({txt: s.innerText, parents});
    }
  });
  out.emptySpans = emptySpans.slice(0, 5);
  return out;
}
"""

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    import time as _t
    now = int(_t.time())
    page.goto(f"https://search.bilibili.com/video?keyword={quote('美股')}&order=click&pubtime_begin_s={now-3*86400}&pubtime_end_s={now}", timeout=25000)
    time.sleep(3)
    info = page.evaluate(PROBE_JS)
    page.close()
    import json
    print(json.dumps(info, ensure_ascii=False, indent=2)[:8000])
