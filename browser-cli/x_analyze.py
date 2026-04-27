import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

def parse_count(s):
    if not s: return 0
    s = str(s).strip().replace(',', '').replace('，', '')
    m = re.match(r'^([\d.]+)\s*([KMBkmb万千])?', s)
    if not m: return 0
    n = float(m.group(1))
    u = (m.group(2) or '').upper()
    mult = {'K':1000,'M':1000000,'B':1e9,'万':10000,'千':1000}.get(u, 1)
    return int(n * mult)


with open('C:/Users/yang/desktop/test_project/browser-cli/x_replies.json', encoding='utf-8') as f:
    data = json.load(f)

print('=' * 80)
print('每个推文按点赞排序前 12 条回复')
print('=' * 80)

for url, info in data.items():
    cs = info.get('comments', [])
    if not cs: continue
    for c in cs:
        c['like_n'] = parse_count(c.get('like', ''))
        c['views_n'] = parse_count(c.get('views', ''))
    cs.sort(key=lambda x: x['like_n'], reverse=True)
    print(f"\n### {info['label']}")
    print(f"### {len(cs)} 条回复")
    for c in cs[:12]:
        text = (c.get('text') or '').replace('\n', ' ')[:200]
        print(f"  [{c['like_n']:>5}❤ / {c.get('views',''):>6} views] {text}")

# 全局关键词词频
print()
print('=' * 80)
print('全局关键词')
print('=' * 80)
all_text = ''
all_count = 0
for info in data.values():
    for c in info.get('comments', []):
        all_text += ' ' + (c.get('text') or '').lower()
        all_count += 1
print(f'总评论: {all_count} 条')

cats = {
    'bullish': ['bull','long','buy','rally','pump','bullish','moon','breakout','突破','买入','看多','加仓','抄底','满仓'],
    'bearish': ['bear','short','sell','crash','dump','bearish','collapse','crash','暴跌','做空','看空','清仓','割肉','跑路','利空'],
    'recession/economy': ['recession','depression','inflation','unemployment','衰退','通胀','失业','经济'],
    'fed/powell': ['fed','powell','rate','fomc','美联储','鲍威尔','降息','加息','利率','pce'],
    'trump/政治': ['trump','tariff','biden','republican','democrat','tax','川普','特朗普','关税'],
    'mag7/companies': ['tesla','tsla','apple','aapl','google','googl','goog','amazon','amzn','microsoft','msft','meta','nvidia','nvda','mag 7','magnificent 7','七巨头'],
    'options/derivative': ['option','options','put','call','0dte','straddle','iv','期权','双买'],
    'china/cn': ['china','chinese','yuan','rmb','中国','人民币','大陆'],
    'manipulation/conspiracy': ['rigged','manipulation','scam','pump and dump','操纵','骗','陷阱','拉高出货'],
    'cash/sidelines': ['cash','sideline','wait','观望','持现','空仓'],
}
for k, words in cats.items():
    count = sum(all_text.count(w) for w in words)
    print(f'  {k}: {count}')
