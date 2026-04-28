"""抓取 elonmusk 主页的近期推文，过滤出今天 (UTC) 的内容。"""
import sys, time, json
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach
from datetime import datetime, timezone, timedelta

PROFILE = "https://x.com/elonmusk"

SCRAPE_JS = """
() => {
  const out = [];
  const seen = new Set();
  document.querySelectorAll('article[data-testid="tweet"]').forEach(art => {
    const timeEl = art.querySelector('time');
    const statusA = art.querySelector('a[href*="/status/"]');
    const url = statusA?.href || '';
    if (!url || seen.has(url)) return;
    seen.add(url);
    const userName = art.querySelector('[data-testid="User-Name"]')?.innerText?.split('\\n').slice(0,2).join(' | ');
    const text = art.querySelector('[data-testid="tweetText"]')?.innerText || '';
    const socialContext = art.querySelector('[data-testid="socialContext"]')?.innerText || '';
    const stats = {};
    ['reply','retweet','like'].forEach(k => {
      const el = art.querySelector('[data-testid="' + k + '"]');
      stats[k] = el?.getAttribute('aria-label') || el?.innerText?.trim() || null;
    });
    out.push({
      url,
      datetime: timeEl?.getAttribute('datetime'),
      timeText: timeEl?.innerText,
      userName: userName?.slice(0, 120),
      socialContext: socialContext.slice(0, 80),
      text: text.slice(0, 800),
      stats,
    });
  });
  return out;
}
"""

with attach() as (pw, browser, ctx):
    page = ctx.pages[0]
    print(f"[nav] {PROFILE}", flush=True)
    page.goto(PROFILE, wait_until='domcontentloaded', timeout=45000)
    page.wait_for_selector('article[data-testid="tweet"]', timeout=30000)

    bj = timezone(timedelta(hours=8))
    today_bj = datetime.now(bj).date()

    all_tweets = {}
    stop_after = 0
    for i in range(25):
        time.sleep(1.6)
        batch = page.evaluate(SCRAPE_JS)
        for t in batch:
            all_tweets[t['url']] = t
        # stop if we've scrolled into yesterday (BJT) for several iterations
        oldest_bjt = None
        for t in all_tweets.values():
            dt = t.get('datetime')
            if not dt: continue
            bj_dt = datetime.fromisoformat(dt.replace('Z','+00:00')).astimezone(bj)
            if oldest_bjt is None or bj_dt < oldest_bjt:
                oldest_bjt = bj_dt
        print(f"[scroll {i+1}] {len(all_tweets)} unique, oldest BJT={oldest_bjt}", flush=True)
        if oldest_bjt and oldest_bjt.date() < today_bj:
            stop_after += 1
            if stop_after >= 2:
                break
        page.evaluate("window.scrollBy(0, window.innerHeight * 1.8)")

    tweets = list(all_tweets.values())
    for t in tweets:
        dt = datetime.fromisoformat(t['datetime'].replace('Z','+00:00'))
        t['bjt'] = dt.astimezone(bj).isoformat()
    tweets.sort(key=lambda t: t.get('datetime') or '', reverse=True)

    today_tweets = [t for t in tweets if datetime.fromisoformat(t['datetime'].replace('Z','+00:00')).astimezone(bj).date() == today_bj]

    out = {
        'fetched_at': datetime.now(timezone.utc).isoformat(),
        'today_bjt': today_bj.isoformat(),
        'total_collected': len(tweets),
        'today_count': len(today_tweets),
        'today_tweets': today_tweets,
        'all_collected': tweets,
    }
    with open('C:/Users/yang/desktop/test_project/browser-cli/elon_today.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[done] today={len(today_tweets)} total={len(tweets)}")
