"""TikTok 美股 Top 10 (按点赞)，过滤 false positives。"""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# 误命中关键词（西语 bolsa=包/招聘 等非股市意思）
FALSE_POS = [
    r'bolsa\s+de\s+empleo', r'bolsas?\s+(más|mais|de moda)',
    r'bolso', r'bolsa\s+rifa',  # 抽奖、时尚
    r'mercanc[ií]a', r'reventa',
    r'#fashion', r'manchesterunited', r'#football',
]
def is_false_positive(title):
    if not title: return False
    tl = title.lower()
    return any(re.search(p, tl) for p in FALSE_POS)

d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/tt_us_search.json', encoding='utf-8'))
videos_3d = d['videos_3d']
filtered = [v for v in videos_3d if not is_false_positive(v.get('title',''))]
filtered.sort(key=lambda v: v.get('digg_count', 0), reverse=True)
top10 = filtered[:10]

print(f'总 3 天: {len(videos_3d)}, 过滤误命中后: {len(filtered)}, 取 Top 10\n')
print('=== TikTok Top 10 美股（3 天内, 按点赞）===')
for i, v in enumerate(top10, 1):
    ts = v.get('create_time_str','?')[:16]
    print(f"{i:2}. 赞{v['digg_count']:>5} 评{v['comment_count']:>4} 分享{v['share_count']:>4} 播放{v.get('play_count',0):>7}  [{ts}]")
    print(f"     {v['title'][:90]}")
    print(f"     ↳ @{v['author']} ({v.get('matched_keyword','')}) {v['url']}")

with open('C:/Users/yang/desktop/test_project/browser-cli/tt_us_top10.json', 'w', encoding='utf-8') as f:
    json.dump({'top10': top10}, f, ensure_ascii=False, indent=2)
labels = [{'label': f"#{i} @{v['author']} - {v['title'][:30]}", 'url': v['url']}
          for i, v in enumerate(top10, 1)]
with open('C:/Users/yang/desktop/test_project/browser-cli/tt_us_top10_input.json', 'w', encoding='utf-8') as f:
    json.dump(labels, f, ensure_ascii=False, indent=2)
print(f'\nSaved tt_us_top10.json + tt_us_top10_input.json')
