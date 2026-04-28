import sys, time, json
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

JS = """
() => {
  const tweet = document.querySelector('article[data-testid="tweet"]');
  if (!tweet) return null;
  const userName = tweet.querySelector('[data-testid="User-Name"]')?.textContent;
  const text = tweet.querySelector('[data-testid="tweetText"]')?.textContent;
  const stats = {};
  ['reply','retweet','like','bookmark'].forEach(k => {
    const el = tweet.querySelector('[data-testid="' + k + '"]');
    stats[k] = {
      ariaLabel: el?.getAttribute('aria-label'),
      text: el?.textContent.trim(),
    };
  });
  // 找浏览量：通常在分析链接里
  const allLinks = Array.from(tweet.querySelectorAll('a'));
  const viewLinks = allLinks
    .map(a => ({
      href: a.href,
      label: a.getAttribute('aria-label')?.slice(0, 100),
      text: a.textContent.slice(0, 40)
    }))
    .filter(a => a.href.includes('analytics') || /view|浏览/i.test((a.label||'') + ' ' + (a.text||'')));
  const timeEl = tweet.querySelector('time');
  const statusLink = tweet.querySelector('a[href*="/status/"]');
  return {
    userName: userName?.slice(0, 100),
    text: text?.slice(0, 250),
    stats,
    viewLinks,
    time: timeEl?.getAttribute('datetime'),
    timeText: timeEl?.textContent,
    statusUrl: statusLink?.href,
  };
}
"""

with attach() as (pw, browser, ctx):
    page = next(p for p in ctx.pages if 'x.com/search' in p.url)
    info = page.evaluate(JS)
    print(json.dumps(info, ensure_ascii=False, indent=2))
