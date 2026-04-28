"""抖音 A 股 Top 10 输出（按点赞数）。"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/dy_a_search.json', encoding='utf-8'))
videos = d['videos']

# 简单 A 股相关性过滤（标题或 hashtag）
INCLUDE = ['A股','a股','大A','大a','上证','沪指','沪深','创业板','科创','涨停','跌停','大盘','板块','股市',
           '股票','行情','复盘','题材','板块','股民','韭菜','炒股','指数','北向','新高','开盘','收盘',
           '盘面','盘中','利好','利空','减持','回购','板块','破位','调整','周期']
EXCLUDE = ['车展','试驾','内饰','车机','试乘']

def is_relevant(v):
    title = v['title']
    if any(kw in title for kw in EXCLUDE): return False
    return any(kw in title for kw in INCLUDE)

filtered = [v for v in videos if is_relevant(v)]
filtered.sort(key=lambda v: v['digg_count'], reverse=True)
top10 = filtered[:10]

print(f'候选 {len(filtered)} / 总 {len(videos)}')
print('=== 抖音 Top 10 A 股（按点赞）===\n')
for i, v in enumerate(top10, 1):
    print(f"{i:2}. 赞{v['digg_count']:>5} 评{v['comment_count']:>4}  [{v['create_time_str'][5:16]}]  {v['title'][:55]}")
    print(f"        ↳ {v['author']}  {v['url']}")

# 输出 dy_comments.py 兼容格式
out_top10 = {'top10': top10}
with open('C:/Users/yang/desktop/test_project/browser-cli/dy_a_top10.json', 'w', encoding='utf-8') as f:
    json.dump(out_top10, f, ensure_ascii=False, indent=2)

# label+url 格式给 dy_comments.py
labels = [{'label': f"#{i} {v['author']} - {v['title'][:30]}", 'url': v['url']}
          for i, v in enumerate(top10, 1)]
with open('C:/Users/yang/desktop/test_project/browser-cli/dy_a_top10_input.json', 'w', encoding='utf-8') as f:
    json.dump(labels, f, ensure_ascii=False, indent=2)
print(f'\nSaved dy_a_top10.json + dy_a_top10_input.json')
