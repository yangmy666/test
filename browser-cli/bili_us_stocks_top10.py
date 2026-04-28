"""从 search 结果里筛 Top 10 (US-stock 相关) 并保存。"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

EXCLUDE_TITLE_KEYWORDS = ['炫彩勇敢者', '副本', '王者', '荣耀', '日股', '红利低波', '大a的']
EXCLUDE_AUTHORS = ['依然范家发丶', '网友小卷毛imb']
# US-stock 相关核心关键词（任一命中标题即视为相关）
US_STOCK_KEYWORDS = ['美股', '纳斯达克', '纳指', '标普', '道琼斯', '道指', '美联储',
                     '特斯拉', '英伟达', '苹果', '微软', '谷歌', '亚马逊', 'Meta',
                     'TSLA', 'NVDA', 'AAPL', 'QQQ', 'SPY', '巴菲特', '华尔街', '美债',
                     '科技巨头', '大空头', '马斯克', '美元', '美国股']

d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/bili_us_stocks_search.json', encoding='utf-8'))

def is_us_stock(v):
    title = v['title']
    if any(kw in title for kw in EXCLUDE_TITLE_KEYWORDS): return False
    if v.get('author') in EXCLUDE_AUTHORS: return False
    return any(kw in title for kw in US_STOCK_KEYWORDS)

filtered = [v for v in d['videos'] if is_us_stock(v)]
filtered.sort(key=lambda v: v['play_count'], reverse=True)
top10 = filtered[:10]

print("=== Top 10 美股相关（按播放量）===\n")
for i, v in enumerate(top10, 1):
    print(f"{i:2}. {v['play_count']:>7}  [{v.get('date','')}]  {v['title'][:65]}")
    print(f"        ↳ {v['author']}  {v['bv']}  {v['url']}")

with open('C:/Users/yang/desktop/test_project/browser-cli/bili_us_stocks_top10.json', 'w', encoding='utf-8') as f:
    json.dump({'top10': top10, 'total_filtered': len(filtered)}, f, ensure_ascii=False, indent=2)
print(f"\n候选 {len(filtered)} 条，保存 top10 到 bili_us_stocks_top10.json")
