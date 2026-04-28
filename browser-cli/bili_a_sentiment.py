"""A 股情绪 / 主题汇总分析。"""
import json, sys, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

LEX = {
    '看多': ['牛市','看多','看涨','抄底','加仓','上车','利好','长期持有','定投','不卖','能涨','还会涨',
            '继续涨','冲高','突破','新高','反弹','强势','梭哈','稳了','启动','拉升','拐点','底部'],
    '看空': ['暴跌','崩盘','泡沫','看空','做空','清仓','跑路','套牢','亏麻','亏惨','深套',
            '别买','危险','高位','出货','高估','回调','下跌','跳水','跌停','熊市','砸盘','撤退','割肉'],
    '焦虑': ['担心','紧张','害怕','慌','恐慌','焦虑','绝望','心累','心慌','难受','痛苦','怕',
            '不敢','睡不着','撑不住','无眠'],
    '嘲讽': ['韭菜','割韭菜','镰刀','喊单','骗子','忽悠','骗','垃圾','收割','智商税','装b','吹牛',
            '韭','智商','傻','蠢','小白','喷','骗局','坑','演'],
    '求助': ['怎么办','怎么操作','求建议','求推荐','该不该','应该','不懂','迷茫','问一下','请教',
            '咋办','能不能'],
    '盈利': ['赚了','挣了','回本','翻倍','赚钱','盈利','吃肉','盆满钵满','收益','赚到'],
    '亏损': ['亏了','亏损','亏麻','亏惨','套了','套牢','深套','腰斩','回吐','吃面','负收益','买在山顶'],
}

# A 股板块/概念/个股关键词
TICKERS = {
    '上证/沪指':       ['上证','沪指','上证指数','3000点','3500点'],
    '创业板':          ['创业板'],
    '科创板':          ['科创板','科创50'],
    '沪深300':         ['沪深300'],
    '中证500':         ['中证500'],
    'CPU/芯片国产':    ['cpu','芯片','光芯片','算力芯片','国产芯片','英特尔','龙芯','海光'],
    'AI/算力':         ['AI','ai','人工智能','算力','大模型','deepseek','DeepSeek','昇腾','华为'],
    '新能源/光伏':     ['新能源','光伏','锂电','宁德时代','宁德','比亚迪','BYD','储能'],
    '医药':            ['医药','医疗','创新药','甘李药业','创新','中药'],
    '军工/央企':       ['军工','央企','国企','中字头'],
    '银行/红利':       ['银行','红利','低波','分红'],
    '券商':            ['券商','证券'],
    '茅台/白酒':       ['茅台','贵州茅台','白酒','五粮液','洋河','泸州'],
    '半导体':          ['半导体','光刻机','存储'],
    '题材股/概念':     ['题材','概念股','龙头股','妖股','打板'],
    '北向资金':        ['北向','陆股通','外资'],
    '证监会/政策':     ['证监会','政策','减持','回购','立案','停牌','复牌'],
    '关税/中美':       ['关税','特朗普','贸易战','中美','对美翻脸'],
    '国家队/汪汪队':   ['国家队','汪汪队','救市','维稳'],
    '港股':            ['港股','恒生'],
    '美股':            ['美股','纳斯达克','纳指','标普','道指'],
    '一季报/财报':     ['一季报','财报','业绩','报表','年报'],
    '电力/双低':       ['电力','双低'],
    'PCB/光模块':      ['PCB','光模块','pcb'],
}

def classify(text: str) -> dict:
    tl = text.lower()
    hits = {}
    for cat, words in LEX.items():
        c = sum(1 for w in words if w.lower() in tl or w in text)
        if c: hits[cat] = c
    return hits

def find_tickers(text: str) -> list:
    found = []
    for name, kws in TICKERS.items():
        if any((kw in text) or (kw.lower() in text.lower()) for kw in kws):
            found.append(name)
    return found

def main():
    d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/bili_a_comments.json', encoding='utf-8'))
    videos = d['videos']

    cat_counts_all = Counter()
    cat_likes_all = Counter()
    ticker_counts = Counter()
    ticker_likes = Counter()
    total = 0; total_main = 0; total_sub = 0
    total_likes = 0
    per_video = []
    top_liked, bullish, bearish, anxious, mocking = [], [], [], [], []

    for v in videos:
        v_cat = Counter(); v_likes = Counter()
        for c in v['comments']:
            text = (c.get('content') or '').strip()
            if not text: continue
            total += 1
            if c.get('is_sub'): total_sub += 1
            else: total_main += 1
            likes = c.get('like') or 0
            total_likes += likes
            emo = classify(text)
            for cat, n in emo.items():
                cat_counts_all[cat] += 1
                cat_likes_all[cat] += likes
                v_cat[cat] += 1; v_likes[cat] += likes
            for t in find_tickers(text):
                ticker_counts[t] += 1
                ticker_likes[t] += likes
            top_liked.append((likes, v['title'][:30], c.get('uname'), text, c.get('is_sub')))
            if '看多' in emo: bullish.append((likes, c.get('uname'), text))
            if '看空' in emo: bearish.append((likes, c.get('uname'), text))
            if '焦虑' in emo: anxious.append((likes, c.get('uname'), text))
            if '嘲讽' in emo: mocking.append((likes, c.get('uname'), text))

        per_video.append({
            'rank': v['rank'], 'title': v['title'], 'author': v['author'], 'play': v['play_count'],
            'main': v.get('main_count', 0), 'sub': v.get('sub_count', 0),
            'cat_counts': dict(v_cat), 'cat_likes': dict(v_likes),
        })

    for lst in (top_liked, bullish, bearish, anxious, mocking): lst.sort(reverse=True)

    print('=' * 70)
    print(f'分析样本：{len(videos)} 视频 / 主楼 {total_main} + 子回复 {total_sub} = {total} 条 / 总赞 {total_likes:,}')
    print('=' * 70)

    print('\n## 情绪分布（条数 / 总点赞）')
    for cat in ['看多','看空','焦虑','嘲讽','求助','盈利','亏损']:
        n = cat_counts_all[cat]; l = cat_likes_all[cat]
        pct = n / total * 100 if total else 0
        print(f'  {cat:>4}: {n:>4} 条 ({pct:5.1f}%)  | 点赞 {l:>6,}')

    bull_l = cat_likes_all['看多']; bear_l = cat_likes_all['看空']
    print(f'\n## 看多/看空点赞 = {bull_l}:{bear_l} → 看多 {bull_l/(bull_l+bear_l)*100:.1f}%' if bull_l+bear_l else '\n## 多空均衡')

    print('\n## 提及最多的板块/主题')
    for tk, n in ticker_counts.most_common(20):
        print(f'  {tk:>16}: {n:>3} 条, 赞 {ticker_likes[tk]:>5,}')

    print('\n## 各视频情绪')
    for pv in per_video:
        b = pv['cat_counts']; bull = b.get('看多',0); bear = b.get('看空',0); anx = b.get('焦虑',0); mock = b.get('嘲讽',0)
        print(f"  #{pv['rank']:>2} [{pv['play']:>6} 播放, 主{pv['main']:>3}+子{pv['sub']:>3}] 多{bull:>2} 空{bear:>2} 焦{anx:>2} 讽{mock:>2}  | {pv['title'][:48]}")

    def show_top(label, lst, n=10):
        print(f'\n## Top {label} 评论（按点赞）')
        for item in lst[:n]:
            if len(item) == 5:
                likes, title, uname, text, is_sub = item
                tag = '[子]' if is_sub else '[主]'
                print(f'  [{likes:>4} 赞] {tag} @{uname}: {text[:200].replace(chr(10),chr(32))}')
            else:
                likes, uname, text = item
                print(f'  [{likes:>4} 赞] @{uname}: {text[:200].replace(chr(10),chr(32))}')

    show_top('点赞', top_liked, 15)
    show_top('看多', bullish)
    show_top('看空', bearish)
    show_top('焦虑', anxious)
    show_top('嘲讽', mocking)

    out = {
        'total_videos': len(videos), 'total_main': total_main, 'total_sub': total_sub, 'total': total,
        'total_likes': total_likes,
        'cat_counts': dict(cat_counts_all), 'cat_likes': dict(cat_likes_all),
        'ticker_counts': dict(ticker_counts.most_common()),
        'ticker_likes': dict(ticker_likes),
        'per_video': per_video,
        'top_liked': [{'likes': l, 'title': t, 'uname': u, 'text': c, 'is_sub': s} for l,t,u,c,s in top_liked[:40]],
        'bullish_top': [{'likes': l, 'uname': u, 'text': t} for l,u,t in bullish[:25]],
        'bearish_top': [{'likes': l, 'uname': u, 'text': t} for l,u,t in bearish[:25]],
        'anxious_top': [{'likes': l, 'uname': u, 'text': t} for l,u,t in anxious[:25]],
        'mocking_top': [{'likes': l, 'uname': u, 'text': t} for l,u,t in mocking[:25]],
    }
    with open('C:/Users/yang/desktop/test_project/browser-cli/bili_a_sentiment.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
