"""筛选 A 股纯交易内容 Top 10。"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# 去掉非 A 股股市内容（日韩/纯游戏炒作/车展）
EXCLUDE_KW = ['日韩股市','日股','韩股','车展','试驾','试乘','车型','内饰','底盘','试车',
              '纽北','发布会','轿跑','SUV','试坐','开箱','车评','拆车','电驱','智驾','油耗','续航',
              '异环','完美世界','棉花']  # 异环/完美 是游戏触发的股票事件，但讨论以游戏圈为主，剔除
# A 股交易/资本市场关键词
INCLUDE_KW = ['A股','上证','沪指','沪深','创业板','科创板','大盘','涨停','跌停','北向','主力','龙头',
              '板块','复盘','抄底','散户','操盘','题材','炒股','股市','回调','反弹','破净','行情',
              '题材股','概念股','利好','利空','减持','回购','股民','信息差','一季报']

d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/bili_a_search.json', encoding='utf-8'))

def is_a_stock_pure(v):
    title = v['title']
    if any(kw in title for kw in EXCLUDE_KW): return False
    return any(kw in title for kw in INCLUDE_KW)

filtered = [v for v in d['videos'] if is_a_stock_pure(v)]
filtered.sort(key=lambda v: v['play_count'], reverse=True)
top10 = filtered[:10]

print('=== Top 10 A 股纯交易内容（按播放量）===\n')
for i, v in enumerate(top10, 1):
    print(f"{i:2}. {v['play_count']:>7}  [{v.get('date','')}]  {v['title'][:60]}")
    print(f"        ↳ {v['author']}  {v['bv']}  {v['url']}")

with open('C:/Users/yang/desktop/test_project/browser-cli/bili_a_top10.json', 'w', encoding='utf-8') as f:
    json.dump({'top10': top10, 'total_filtered': len(filtered)}, f, ensure_ascii=False, indent=2)
print(f'\n候选 {len(filtered)} 条，保存 top10。')
