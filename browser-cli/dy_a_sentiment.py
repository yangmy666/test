"""抖音 A 股情绪 / 主题汇总分析。"""
import json, sys
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

LEX = {
    '看多': ['牛市','看多','看涨','抄底','加仓','上车','利好','长期持有','定投','不卖','能涨','还会涨',
            '继续涨','冲高','突破','新高','反弹','强势','梭哈','稳了','启动','拉升','拐点','底部','跟上'],
    '看空': ['暴跌','崩盘','泡沫','看空','做空','清仓','跑路','套牢','亏麻','亏惨','深套',
            '别买','危险','高位','出货','高估','回调','下跌','跳水','跌停','熊市','砸盘','撤退','割肉',
            '跑','跑了','要跌','大跌'],
    '焦虑': ['担心','紧张','害怕','慌','恐慌','焦虑','绝望','心累','心慌','难受','痛苦','怕',
            '不敢','睡不着','撑不住','无眠','救救','救命'],
    '嘲讽': ['韭菜','割韭菜','镰刀','喊单','骗子','忽悠','骗','垃圾','收割','智商税','装b','吹牛',
            '韭','智商','傻','蠢','小白','喷','骗局','坑','演','大师','导演'],
    '求助': ['怎么办','怎么操作','求建议','求推荐','该不该','应该','不懂','迷茫','问一下','请教',
            '咋办','能不能','请问'],
    '盈利': ['赚了','挣了','回本','翻倍','赚钱','盈利','吃肉','盆满钵满','收益','赚到'],
    '亏损': ['亏了','亏损','亏麻','亏惨','套了','套牢','深套','腰斩','回吐','吃面','负收益','买在山顶'],
}

TICKERS = {
    '上证/沪指':       ['上证','沪指','上证指数','3000点','3500点'],
    '创业板':          ['创业板'],
    '科创板':          ['科创板','科创50'],
    '沪深300':         ['沪深300'],
    '中证500':         ['中证500'],
    'CPU/芯片国产':    ['cpu','芯片','光芯片','算力芯片','国产芯片','英特尔','龙芯','海光'],
    'AI/算力':         ['AI','ai','人工智能','算力','大模型','deepseek','DeepSeek','昇腾','华为'],
    '新能源/光伏':     ['新能源','光伏','锂电','宁德时代','宁德','比亚迪','BYD','储能'],
    '医药':            ['医药','医疗','创新药','中药'],
    '军工/央企':       ['军工','央企','国企','中字头'],
    '银行/红利':       ['银行','红利','低波','分红'],
    '券商':            ['券商','证券'],
    '茅台/白酒':       ['茅台','贵州茅台','白酒','五粮液'],
    '半导体':          ['半导体','光刻机','存储'],
    '题材股/概念':     ['题材','概念股','龙头股','妖股','打板','跟妖','短线'],
    '北向资金':        ['北向','陆股通','外资'],
    '证监会/政策':     ['证监会','政策','减持','回购','立案','停牌','复牌','打击'],
    '关税/中美':       ['关税','特朗普','贸易战','中美','对美翻脸'],
    '国家队/汪汪队':   ['国家队','汪汪队','救市','维稳'],
    '港股':            ['港股','恒生'],
    '美股':            ['美股','纳斯达克','纳指','标普','道指','纳斯达克'],
    '一季报/财报':     ['一季报','财报','业绩','报表','年报'],
    '电力/双低':       ['电力','双低','华辽','华电'],
    'PCB/光模块':      ['PCB','光模块','pcb','光通信','CPO'],
    '无人机':          ['无人机','低空'],
    '商业航天':        ['商业航天','航天','卫星','长征'],
}

def classify(text):
    tl = text.lower()
    hits = {}
    for cat, words in LEX.items():
        c = sum(1 for w in words if w.lower() in tl or w in text)
        if c: hits[cat] = c
    return hits

def find_tickers(text):
    found = []
    for name, kws in TICKERS.items():
        if any((kw in text) or (kw.lower() in text.lower()) for kw in kws):
            found.append(name)
    return found

def main():
    d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/dy_a_comments.json', encoding='utf-8'))
    # d is keyed by url -> {label, main_count, sub_count, comments: [...]}

    cat_counts = Counter()
    cat_likes = Counter()
    ticker_counts = Counter()
    ticker_likes = Counter()
    total = 0; total_main = 0; total_sub = 0; total_likes = 0
    per_video = []
    top_liked, bullish, bearish, anxious, mocking = [], [], [], [], []

    for url, vd in d.items():
        if not vd.get('comments'): continue
        v_cat = Counter(); v_likes = Counter()
        for c in vd['comments']:
            text = (c.get('text') or '').strip()
            if not text or len(text) < 2: continue
            total += 1
            if c.get('is_sub'): total_sub += 1
            else: total_main += 1
            likes = c.get('likes') or 0
            total_likes += likes
            emo = classify(text)
            for cat, n in emo.items():
                cat_counts[cat] += 1
                cat_likes[cat] += likes
                v_cat[cat] += 1; v_likes[cat] += likes
            for t in find_tickers(text):
                ticker_counts[t] += 1
                ticker_likes[t] += likes
            author = c.get('author') or ''
            top_liked.append((likes, vd.get('label','')[:30], author, text, bool(c.get('is_sub'))))
            if '看多' in emo: bullish.append((likes, author, text))
            if '看空' in emo: bearish.append((likes, author, text))
            if '焦虑' in emo: anxious.append((likes, author, text))
            if '嘲讽' in emo: mocking.append((likes, author, text))

        per_video.append({
            'label': vd.get('label',''),
            'main': vd.get('main_count', 0),
            'sub': vd.get('sub_count', 0),
            'cat_counts': dict(v_cat),
        })

    for lst in (top_liked, bullish, bearish, anxious, mocking): lst.sort(reverse=True)

    print('='*70)
    print(f'分析样本：{len(per_video)} 视频 / 主 {total_main} + 子 {total_sub} = {total} / 总赞 {total_likes:,}')
    print('='*70)

    print('\n## 情绪分布（条数 / 总赞）')
    for cat in ['看多','看空','焦虑','嘲讽','求助','盈利','亏损']:
        n = cat_counts[cat]; l = cat_likes[cat]
        pct = n / total * 100 if total else 0
        print(f'  {cat:>4}: {n:>4} 条 ({pct:5.1f}%) | 赞 {l:>6,}')

    bull_l, bear_l = cat_likes['看多'], cat_likes['看空']
    if bull_l + bear_l:
        print(f'\n## 看多/看空 点赞 = {bull_l}:{bear_l} → 看多 {bull_l/(bull_l+bear_l)*100:.1f}%')

    print('\n## 提及最多的板块/主题')
    for tk, n in ticker_counts.most_common(20):
        print(f'  {tk:>16}: {n:>3} 条, 赞 {ticker_likes[tk]:>5,}')

    print('\n## 各视频情绪')
    for pv in per_video:
        b = pv['cat_counts']
        bull, bear, anx, mock = b.get('看多',0), b.get('看空',0), b.get('焦虑',0), b.get('嘲讽',0)
        print(f"  [主{pv['main']:>3}+子{pv['sub']:>3}] 多{bull:>2} 空{bear:>2} 焦{anx:>2} 讽{mock:>2}  | {pv['label'][:55]}")

    def show(label, lst, n=12):
        print(f'\n## Top {label}（按赞）')
        for item in lst[:n]:
            if len(item) == 5:
                l, t, u, txt, is_sub = item
                tag = '[子]' if is_sub else '[主]'
                print(f'  [{l:>4}] {tag} @{u}: {txt[:200]}')
            else:
                l, u, txt = item
                print(f'  [{l:>4}] @{u}: {txt[:200]}')

    show('点赞', top_liked, 15)
    show('看多', bullish)
    show('看空', bearish)
    show('焦虑', anxious)
    show('嘲讽', mocking)

    out = {
        'total_videos': len(per_video), 'total_main': total_main, 'total_sub': total_sub, 'total': total,
        'total_likes': total_likes,
        'cat_counts': dict(cat_counts), 'cat_likes': dict(cat_likes),
        'ticker_counts': dict(ticker_counts.most_common()),
        'ticker_likes': dict(ticker_likes),
        'per_video': per_video,
        'top_liked':   [{'likes':l,'label':t,'author':u,'text':c,'is_sub':s} for l,t,u,c,s in top_liked[:50]],
        'bullish_top': [{'likes':l,'author':u,'text':t} for l,u,t in bullish[:30]],
        'bearish_top': [{'likes':l,'author':u,'text':t} for l,u,t in bearish[:30]],
        'anxious_top': [{'likes':l,'author':u,'text':t} for l,u,t in anxious[:30]],
        'mocking_top': [{'likes':l,'author':u,'text':t} for l,u,t in mocking[:30]],
    }
    with open('C:/Users/yang/desktop/test_project/browser-cli/dy_a_sentiment.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
