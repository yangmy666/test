"""TikTok 美股情绪分析（多语言：英/中/西/葡/日/韩，含 emoji 信号）。

用法：python tt_us_sentiment.py [<comments.json>] [<output.json>]
默认从 tt_us_comments.json 读，输出到 tt_us_sentiment.json
"""
import json, sys, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

INPUT = sys.argv[1] if len(sys.argv) > 1 else 'C:/Users/yang/desktop/test_project/browser-cli/tt_us_comments.json'
OUTPUT = sys.argv[2] if len(sys.argv) > 2 else 'C:/Users/yang/desktop/test_project/browser-cli/tt_us_sentiment.json'

# 多语言情绪词典 + emoji 信号
LEX = {
    '看多': [
        # 中文
        '牛市','看多','看涨','抄底','加仓','上车','利好','长期','定投','突破','新高','反弹','梭哈','启动','拉升','买入',
        # 英文
        'bullish','buy the dip','buying','dip','long','hold','holding','HODL','long term','to the moon','moon',
        'all in','add to position','accumulating','undervalued','breakout','rally','recovery','reversal',
        'opportunity','opportunities','great buy','solid pick','pump','rocket',
        # 西/葡
        'compra','comprar','alcista','subir',
        # emoji
        '🚀','🌙','📈','💎','🤲','🐂','💸','💰','💪','✅','💯','🔥',
    ],
    '看空': [
        '暴跌','崩盘','泡沫','看空','做空','清仓','跑路','套牢','亏麻','深套','危险','回调','下跌','跳水','熊市','割肉',
        'bearish','crash','dump','dumping','sell','sold','short','shorting','overvalued','bubble','top',
        'overbought','correction','dip','red','blood','bear','dead cat','tank','tanking','tanked','plummet',
        'baja','bajista','vender','crashing',
        '📉','🐻','🩸','💀','😱','😭','⚠️','🔻','😬',
    ],
    '焦虑': [
        '担心','害怕','慌','恐慌','焦虑','救救','无眠','撑不住','风险',
        'worried','scared','afraid','fear','panic','nervous','uncertainty','risky','help','lost',
        'preocupado','miedo',
        '😨','😰','😢','😭','🤔','😟','😖',
    ],
    '嘲讽': [
        '韭菜','割韭菜','骗子','忽悠','骗局','垃圾','收割','智商税','收割机','导演','演',
        'scam','rugpull','rug','clown','joke','crap','garbage','BS','copium','stupid','dumb','idiot','sheep',
        'estafa','tonto',
        '🤡','💩','🙄','🤣','😂','🤦',
    ],
    '求助': [
        '怎么办','怎么操作','建议','应该','不懂','迷茫','请教','咋办',
        'should i','what should','what do you','recommend','suggestion','advice','noob','beginner','help me',
        'cómo','consejo','recomendar',
    ],
    '盈利': [
        '赚了','回本','翻倍','盈利','吃肉','收益',
        'profit','profits','gains','gainz','green','up','make money','beat the market','outperform',
        'won','winning','tendies',
        'ganancia','ganando',
        '💸','💰','✅','📈',
    ],
    '亏损': [
        '亏了','亏损','亏麻','套了','腰斩','吃面','负收益','买在山顶',
        'loss','losses','losing','lost money','underwater','bag holder','baghold','rekt','wrecked',
        'bagholder','red','down','drawdown',
        'pérdida','perdiendo',
        '💀','📉','😭','😢','💔',
    ],
}

# 美股 ticker / 主题字典（多语言）
TICKERS = {
    'NVDA / 英伟达': ['NVDA','$NVDA','nvidia','英伟达','엔비디아'],
    'TSLA / 特斯拉': ['TSLA','$TSLA','tesla','特斯拉','테슬라','elon','musk'],
    'AAPL / 苹果':   ['AAPL','$AAPL','apple','苹果','애플'],
    'MSFT / 微软':   ['MSFT','$MSFT','microsoft','微软'],
    'GOOG/GOOGL':    ['GOOG','GOOGL','google','alphabet','谷歌'],
    'META':          ['META','$META','facebook','meta','脸书'],
    'AMZN':          ['AMZN','$AMZN','amazon','亚马逊'],
    'AMD':           ['AMD','$AMD'],
    'NFLX':          ['NFLX','$NFLX','netflix','奈飞'],
    'PLTR':          ['PLTR','$PLTR','palantir'],
    'SPY/S&P 500':   ['SPY','$SPY','S&P','SP500','标普','标普500'],
    'QQQ/纳斯达克':  ['QQQ','$QQQ','NASDAQ','纳斯达克','纳指','나스닥','ナスダック'],
    'DIA/道琼斯':    ['DIA','$DIA','dow jones','道琼斯','道指'],
    '比特币/BTC':    ['BTC','$BTC','bitcoin','比特币','크립토'],
    '美联储/Fed':    ['fed','federal reserve','美联储','rate cut','rate hike','fomc','powell','鲍威尔'],
    '财报/Earnings': ['earnings','quarterly','q1','q2','q3','q4','财报','quarterly results','eps','revenue'],
    'AI/人工智能':   ['AI','人工智能','artificial intelligence','OpenAI','ChatGPT'],
    '关税/tariff':   ['tariff','tariffs','关税','贸易战','trade war','trump'],
    '黄金/gold':     ['gold','黄金','金价','XAU'],
    '期权/options':  ['option','options','call','put','strike','iv','期权'],
    '股息/dividend': ['dividend','dividends','股息','divvy'],
    '指数基金':      ['index fund','etf','S&P','VOO','VTI','VOO','SCHD','SCHG','sector','sectores'],
    '利率/interest': ['interest rate','利率','yield','treasuries','treasury','bonds','债券'],
}

def find_hits(text, words):
    """返回命中的单词数（不区分大小写，含 emoji 直接匹配）。"""
    if not text: return 0
    tl = text.lower()
    n = 0
    for w in words:
        wl = w.lower()
        # 短词用 word boundary（防止 "buy" 命中 "buyer"）；长词或 emoji 直接 substring
        if len(w) <= 3 and not any(ord(c) > 127 for c in w):
            if re.search(r'\b' + re.escape(wl) + r'\b', tl): n += 1
        else:
            if wl in tl or w in text: n += 1
    return n

def classify(text):
    hits = {}
    for cat, words in LEX.items():
        n = find_hits(text, words)
        if n: hits[cat] = n
    return hits

def find_tickers(text):
    found = []
    for name, kws in TICKERS.items():
        if find_hits(text, kws):
            found.append(name)
    return found

def main():
    d = json.load(open(INPUT, encoding='utf-8'))

    cat_counts = Counter()
    cat_likes = Counter()
    ticker_counts = Counter()
    ticker_likes = Counter()
    total = 0; total_main = 0; total_sub = 0; total_likes = 0
    per_video = []
    top_liked, bullish, bearish, anxious, mocking = [], [], [], [], []

    for url, vd in d.items():
        if not vd.get('comments'): continue
        v_cat = Counter()
        for c in vd['comments']:
            text = (c.get('text') or '').strip()
            if not text or len(text) < 2: continue
            total += 1
            if c.get('level') == 2 or c.get('is_sub'): total_sub += 1
            else: total_main += 1
            likes = c.get('likes') or 0
            total_likes += likes
            emo = classify(text)
            for cat, n in emo.items():
                cat_counts[cat] += 1
                cat_likes[cat] += likes
                v_cat[cat] += 1
            for t in find_tickers(text):
                ticker_counts[t] += 1
                ticker_likes[t] += likes
            author = c.get('author') or ''
            top_liked.append((likes, vd.get('label','')[:30], author, text, c.get('level')==2))
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
        print(f'  {cat:>4}: {n:>4} 条 ({pct:5.1f}%) | 赞 {l:>5,}')

    bull_l, bear_l = cat_likes['看多'], cat_likes['看空']
    if bull_l + bear_l:
        print(f'\n## 看多/看空 点赞 = {bull_l}:{bear_l} → 看多 {bull_l/(bull_l+bear_l)*100:.1f}%')

    print('\n## 提及最多的标的/主题')
    for tk, n in ticker_counts.most_common(20):
        print(f'  {tk:>20}: {n:>3} 条, 赞 {ticker_likes[tk]:>4,}')

    print('\n## 各视频情绪')
    for pv in per_video:
        b = pv['cat_counts']
        bull, bear, anx, mock = b.get('看多',0), b.get('看空',0), b.get('焦虑',0), b.get('嘲讽',0)
        print(f"  [主{pv['main']:>2}+子{pv['sub']:>2}] 多{bull:>2} 空{bear:>2} 焦{anx:>2} 讽{mock:>2}  | {pv['label'][:55]}")

    def show(title, lst, n=10):
        print(f'\n## Top {title}（按赞）')
        for item in lst[:n]:
            if len(item) == 5:
                l, _, u, t, is_sub = item
                tag = '[子]' if is_sub else '[主]'
                print(f'  [{l:>4}] {tag} @{u}: {t[:200]}')
            else:
                l, u, t = item
                print(f'  [{l:>4}] @{u}: {t[:200]}')

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
        'bullish_top': [{'likes':l,'author':u,'text':t} for l,u,t in bullish[:25]],
        'bearish_top': [{'likes':l,'author':u,'text':t} for l,u,t in bearish[:25]],
        'anxious_top': [{'likes':l,'author':u,'text':t} for l,u,t in anxious[:25]],
        'mocking_top': [{'likes':l,'author':u,'text':t} for l,u,t in mocking[:25]],
    }
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
