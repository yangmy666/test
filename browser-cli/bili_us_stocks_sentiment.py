"""对 Top 10 美股视频评论做情绪 / 主题汇总分析。"""
import json, sys, re
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')

# 情绪词典（中文 + 部分英文）
LEX = {
    '看多':   ['牛市', '看多', '看涨', '抄底', '加仓', '上车', '利好', '长期持有', '定投', '不卖', '能涨', '还会涨',
              '继续涨', '冲高', '突破', '新高', '反弹', '强势', '坚定持有', '梭哈', '定海神针', '稳了', '香'],
    '看空':   ['暴跌', '崩盘', '泡沫', '看空', '做空', '清仓', '跑路', '套牢', '亏麻', '亏惨', '深套',
              '别买', '危险', '高位', '出货', '高估', '回调', '下跌', '跳水', '跌停', '熊市', '砸盘', '撤'],
    '焦虑':   ['担心', '紧张', '害怕', '慌', '恐慌', '恐惧', '焦虑', '绝望', '心累', '心慌', '难受', '痛苦',
              '怕', '不敢', '睡不着', '撑不住'],
    '嘲讽':   ['韭菜', '割韭菜', '镰刀', '喊单', '骗子', '忽悠', '骗', '垃圾', '收割', '智商税', '装b', '吹',
              '吹牛', '韭', '智商', '傻', '蠢', '小白'],
    '求助':   ['怎么办', '怎么操作', '求建议', '求推荐', '该不该', '应该', '不懂', '迷茫', '问一下', '请教',
              '咋办', '能不能'],
    '盈利':   ['赚了', '挣了', '回本', '翻倍', '赚钱', '盈利', '吃肉', '盆满钵满', '收益', '赚到'],
    '亏损':   ['亏了', '亏损', '亏麻', '亏惨', '套了', '套牢', '深套', '腰斩', '回吐', '吃面', '亏', '负收益'],
}

# 美股个股 / ETF / 主题词
TICKERS = {
    '特斯拉/TSLA':   ['特斯拉', 'tsla', 'TSLA', 'Tesla'],
    '英伟达/NVDA':   ['英伟达', 'nvda', 'NVDA', '老黄'],
    '苹果/AAPL':    ['苹果', 'AAPL', 'aapl'],
    '微软/MSFT':    ['微软', 'MSFT', 'msft'],
    '谷歌/GOOG':    ['谷歌', 'GOOG', 'goog', 'Google'],
    '亚马逊/AMZN':  ['亚马逊', 'AMZN', 'amzn'],
    'Meta/META':    ['Meta', 'meta', 'METAA', '脸书', 'Facebook'],
    'QQQ':          ['QQQ', 'qqq', '纳指ETF', '纳斯达克ETF'],
    '纳斯达克':      ['纳斯达克', '纳指'],
    '标普500':      ['标普', 'SP500', 'spy', 'SPY', '标普500'],
    '巴菲特':       ['巴菲特', '伯克希尔', 'Buffett'],
    '美联储':       ['美联储', '鲍威尔', '加息', '降息', 'Fed'],
    '关税':         ['关税', '特朗普', '贸易战'],
    '财报':         ['财报', '业绩'],
    '黄金':         ['黄金', 'XAU', '金价'],
    'AI':           ['AI', 'ai', '人工智能', 'agi', 'AGI'],
}

def classify_emotion(text: str) -> dict:
    text_low = text.lower()
    hits = {}
    for cat, words in LEX.items():
        c = sum(1 for w in words if w.lower() in text_low or w in text)
        if c: hits[cat] = c
    return hits

def find_tickers(text: str) -> list:
    found = []
    for name, kws in TICKERS.items():
        if any((kw in text) or (kw.lower() in text.lower()) for kw in kws):
            found.append(name)
    return found

def main():
    d = json.load(open('C:/Users/yang/desktop/test_project/browser-cli/bili_us_stocks_comments.json', encoding='utf-8'))
    videos = d['videos']

    # 全局 + 按视频
    cat_counts_all = Counter()           # 命中条数（按情绪类）
    cat_likes_all = Counter()            # 命中加权（按 like）
    ticker_counts = Counter()
    ticker_likes = Counter()
    total_comments = 0
    total_likes = 0
    per_video = []
    top_liked = []           # 全局 top liked comments
    bullish_top = []
    bearish_top = []
    anxious_top = []
    mocking_top = []

    for v in videos:
        v_cat = Counter()
        v_likes = Counter()
        # 按 (uname, content[:100]) 去重 — DOM 走访 shadow DOM 出现 3 倍重复
        seen_keys = set()
        deduped = []
        for c in v['comments']:
            text = (c.get('content') or '').strip()
            if not text: continue
            key = (c.get('uname',''), text[:100])
            if key in seen_keys: continue
            seen_keys.add(key)
            deduped.append(c)
        v['comments'] = deduped
        for c in v['comments']:
            text = (c.get('content') or '').strip()
            if not text: continue
            total_comments += 1
            likes = c.get('like') or 0
            # 兼容字段：DOM 版没有 uname 必带，content 里有时含混
            c.setdefault('uname', c.get('uname',''))
            total_likes += likes
            emo = classify_emotion(text)
            for cat, n in emo.items():
                cat_counts_all[cat] += 1
                cat_likes_all[cat] += likes
                v_cat[cat] += 1
                v_likes[cat] += likes
            tks = find_tickers(text)
            for t in tks:
                ticker_counts[t] += 1
                ticker_likes[t] += likes
            top_liked.append((likes, v['title'][:30], c.get('uname'), text))
            if '看多' in emo: bullish_top.append((likes, c.get('uname'), text))
            if '看空' in emo: bearish_top.append((likes, c.get('uname'), text))
            if '焦虑' in emo: anxious_top.append((likes, c.get('uname'), text))
            if '嘲讽' in emo: mocking_top.append((likes, c.get('uname'), text))

        per_video.append({
            'rank': v['rank'],
            'title': v['title'],
            'author': v['author'],
            'play': v['play_count'],
            'count': len(v['comments']),
            'cat_counts': dict(v_cat),
            'cat_likes': dict(v_likes),
        })

    top_liked.sort(reverse=True)
    bullish_top.sort(reverse=True)
    bearish_top.sort(reverse=True)
    anxious_top.sort(reverse=True)
    mocking_top.sort(reverse=True)

    # 情绪分布（条数 + 点赞加权）
    print("=" * 70)
    print(f"分析样本：{len(videos)} 个视频，{total_comments} 条评论，总点赞 {total_likes:,}")
    print("=" * 70)

    print("\n## 情绪分布（条数 / 总点赞数）")
    for cat in ['看多', '看空', '焦虑', '嘲讽', '求助', '盈利', '亏损']:
        n = cat_counts_all[cat]
        l = cat_likes_all[cat]
        pct = n / total_comments * 100 if total_comments else 0
        print(f"  {cat:>4}: {n:>4} 条 ({pct:5.1f}%)  | 点赞总和 {l:>6,}")

    print("\n## 看多 vs 看空 (按点赞加权)")
    bull_l = cat_likes_all['看多']
    bear_l = cat_likes_all['看空']
    if bull_l + bear_l > 0:
        ratio = bull_l / (bull_l + bear_l) * 100
        print(f"  看多/看空点赞比 = {bull_l}:{bear_l}  →  看多占 {ratio:.1f}%")

    print("\n## 提及最多的标的 / 主题（条数, 点赞总和）")
    for tk, n in ticker_counts.most_common(15):
        print(f"  {tk:>14}: {n:>3} 条, 点赞 {ticker_likes[tk]:>5,}")

    print("\n## 各视频情绪小结")
    for pv in per_video:
        bull = pv['cat_counts'].get('看多', 0)
        bear = pv['cat_counts'].get('看空', 0)
        anx = pv['cat_counts'].get('焦虑', 0)
        mock = pv['cat_counts'].get('嘲讽', 0)
        print(f"  #{pv['rank']:>2} [{pv['play']:>6}播放, {pv['count']:>3}评] 多{bull:>2} 空{bear:>2} 焦{anx:>2} 讽{mock:>2}  | {pv['title'][:50]}")

    def show_top(label, lst, n=8):
        print(f"\n## Top {label} 评论（按点赞）")
        for likes, uname, text in lst[:n]:
            print(f"  [{likes:>4} 赞] @{uname}: {text[:200].replace(chr(10),' ')}")

    show_top('点赞', [(l, u, t) for l, _, u, t in top_liked], n=12)
    show_top('看多', bullish_top)
    show_top('看空', bearish_top)
    show_top('焦虑', anxious_top)
    show_top('嘲讽', mocking_top)

    # 也保存到 json
    out = {
        'total_videos': len(videos),
        'total_comments': total_comments,
        'total_likes': total_likes,
        'cat_counts': dict(cat_counts_all),
        'cat_likes': dict(cat_likes_all),
        'ticker_counts': dict(ticker_counts.most_common()),
        'ticker_likes': dict(ticker_likes),
        'per_video': per_video,
        'top_liked': [{'likes': l, 'title': t, 'uname': u, 'text': c} for l, t, u, c in top_liked[:30]],
        'bullish_top':  [{'likes': l, 'uname': u, 'text': t} for l, u, t in bullish_top[:20]],
        'bearish_top':  [{'likes': l, 'uname': u, 'text': t} for l, u, t in bearish_top[:20]],
        'anxious_top':  [{'likes': l, 'uname': u, 'text': t} for l, u, t in anxious_top[:20]],
        'mocking_top':  [{'likes': l, 'uname': u, 'text': t} for l, u, t in mocking_top[:20]],
    }
    with open('C:/Users/yang/desktop/test_project/browser-cli/bili_us_stocks_sentiment.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
