"""TikTok 匿名状态可行性探测：搜索、结果抓取、视频页、评论。"""
import sys, time, json
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

QUERY = 'us stocks'  # 选英文关键词，避免被本地化语种污染
SEARCH_URL = f'https://www.tiktok.com/search?q={QUERY.replace(" ","+")}'

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    print(f"=== 1. 打开搜索页 {SEARCH_URL} ===")
    try:
        page.goto(SEARCH_URL, wait_until='domcontentloaded', timeout=20000)
    except Exception as e:
        print(f"goto failed: {e}"); sys.exit(1)
    time.sleep(5)
    print(f"final_url: {page.url}")
    print(f"title:     {page.title()}")

    info1 = page.evaluate("""() => {
      const body = document.body?.innerText || '';
      return {
        bodyLen: body.length,
        bodyHead: body.slice(0, 400),
        hasLoginWall: /Log in to|登录后/i.test(body) || /登录$/.test(body.slice(0, 80)),
        hasCaptcha: /captcha|verify you|robot/i.test(body),
        // 各种可能的视频卡 selector
        sels: {
          'data-e2e=search-card-item': document.querySelectorAll('[data-e2e="search-card-item"]').length,
          'data-e2e=search-video-item': document.querySelectorAll('[data-e2e="search-video-item"]').length,
          'data-e2e=search_top-item': document.querySelectorAll('[data-e2e="search_top-item"]').length,
          'data-e2e=search-common-item': document.querySelectorAll('[data-e2e="search-common-item"]').length,
          'a[href*=/video/]': document.querySelectorAll('a[href*="/video/"]').length,
          'all data-e2e count': document.querySelectorAll('[data-e2e]').length,
        }
      };
    }""")
    print("\n=== body sample + selectors ===")
    print(json.dumps(info1, ensure_ascii=False, indent=2)[:2000])

    # 滚一些再看
    for _ in range(5):
        page.evaluate("window.scrollBy(0, 1500)")
        time.sleep(0.8)
    info2 = page.evaluate("""() => {
      const links = Array.from(document.querySelectorAll('a[href*="/video/"]'))
        .map(a => a.href).filter((v,i,arr) => arr.indexOf(v) === i);
      return {videoLinks: links.slice(0, 8), totalLinks: links.length};
    }""")
    print("\n=== 滚动后视频链接 ===")
    print(json.dumps(info2, ensure_ascii=False, indent=2))

    # 拿第一个视频 URL，打开看评论
    if info2['videoLinks']:
        vurl = info2['videoLinks'][0]
        print(f"\n=== 2. 打开第一个视频: {vurl} ===")
        page2 = ctx.new_page()
        try:
            page2.goto(vurl, wait_until='domcontentloaded', timeout=20000)
            time.sleep(5)
            print(f"final_url: {page2.url}")
            print(f"title:     {page2.title()}")

            info3 = page2.evaluate("""() => {
              const body = document.body?.innerText || '';
              return {
                bodyLen: body.length,
                bodySample: body.slice(0, 400),
                hasLoginWall: /Log in to/i.test(body),
                hasCaptcha: /captcha|verify you|robot/i.test(body),
                sels: {
                  'data-e2e=comment-item': document.querySelectorAll('[data-e2e="comment-item"]').length,
                  'data-e2e=comment-level-1': document.querySelectorAll('[data-e2e="comment-level-1"]').length,
                  'data-e2e=comment-list': document.querySelectorAll('[data-e2e="comment-list"]').length,
                  'data-e2e=video-author-uniqueid': document.querySelectorAll('[data-e2e="video-author-uniqueid"]').length,
                  'data-e2e=like-count': document.querySelectorAll('[data-e2e="like-count"]').length,
                  'data-e2e=comment-count': document.querySelectorAll('[data-e2e="comment-count"]').length,
                }
              };
            }""")
            print("\n=== 视频页评论检测 ===")
            print(json.dumps(info3, ensure_ascii=False, indent=2)[:2000])

            # 滚动评论区
            for _ in range(8):
                page2.evaluate("window.scrollBy(0, 1000)")
                time.sleep(0.7)
            info4 = page2.evaluate("""() => ({
              comments: document.querySelectorAll('[data-e2e="comment-level-1"], [data-e2e="comment-item"]').length,
              firstCommentText: (document.querySelector('[data-e2e="comment-level-1"], [data-e2e="comment-item"]')?.innerText || '').slice(0, 200),
            })""")
            print("\n=== 滚动后评论数 ===")
            print(json.dumps(info4, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"video page failed: {e}")
        finally:
            page2.close()

    page.close()
