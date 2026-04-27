"""B 站搜索：找类七日杀 A17 的近期生存类游戏。

策略：
- 多关键词搜索（生存、僵尸、建造、类七日杀、末日、塔防生存）
- 排序按最新或最多播放
- 提取标题，统计被频繁提及的游戏名
"""
import sys
import time
import json
import re
from collections import Counter
from urllib.parse import quote

sys.path.insert(0, "C:/Users/yang/desktop/test_project/browser-cli")
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
from connect import attach

KEYWORDS = [
    "类七日杀",
    "七日杀替代",
    "像七日杀",
    "生存建造游戏 2026",
    "生存建造游戏 2025",
    "末日生存游戏推荐",
    "僵尸生存游戏 新",
    "塔防生存游戏",
    "硬核生存游戏",
    "开放世界生存 新",
    "新生存类游戏",
    "好玩的生存游戏",
]

# 已知游戏关键词字典 — 用于在视频标题里抓游戏名
KNOWN_GAMES = {
    "七日杀": ["七日杀", "7 days to die", "7days"],
    "Once Human": ["七日世界", "once human", "OnceHuman"],
    "Sons of the Forest": ["森林之子", "sons of the forest"],
    "The Forest": ["森林", "the forest"],
    "Project Zomboid": ["僵尸毁灭工程", "project zomboid", "PZ", "僵毁"],
    "Enshrouded": ["层层世界", "enshrouded"],
    "ICARUS": ["伊卡洛斯", "icarus"],
    "Soulmask": ["灵魂面甲", "soulmask"],
    "V Rising": ["夜族崛起", "v rising", "vrising"],
    "Valheim": ["英灵神殿", "valheim"],
    "Pacific Drive": ["太平洋之旅", "pacific drive"],
    "Nightingale": ["夜莺传说", "nightingale"],
    "Pax Dei": ["pax dei"],
    "Manor Lords": ["庄园领主", "manor lords"],
    "Mist Survival": ["迷雾求生", "mist survival"],
    "DayZ": ["dayz"],
    "Rust": ["腐蚀", "rust"],
    "ARK": ["方舟", "ark"],
    "Conan Exiles": ["流放者柯南", "conan exiles"],
    "Dread Hunger": ["恐惧饥饿", "dread hunger"],
    "Don't Starve": ["饥荒", "dont starve", "don't starve"],
    "Subnautica": ["深海迷航", "subnautica"],
    "Green Hell": ["绿色地狱", "green hell"],
    "The Long Dark": ["漫漫长夜", "long dark"],
    "Raft": ["木筏求生", "raft"],
    "Frostpunk 2": ["冰汽时代2", "frostpunk 2"],
    "State of Decay": ["腐烂国度", "state of decay"],
    "Dying Light": ["消逝的光芒", "dying light"],
    "Mist Legacy": ["mist legacy"],
    "Necesse": ["necesse"],
    "Core Keeper": ["core keeper"],
    "Vintage Story": ["vintage story"],
    "Lights Out": ["lights out", "灯火熄灭"],
    "GTFO": ["gtfo"],
    "Outlast Trials": ["逃生试炼", "outlast trials"],
    "Abiotic Factor": ["abiotic factor"],
    "Pacific Drive": ["太平洋之旅"],
    "ASKA": ["aska"],
    "Tribe": ["部落"],
    "Bellwright": ["钟楼大师", "bellwright"],
    "Ressurectum": ["ressurectum"],
    "Smalland": ["smalland"],
    "Frostfall": ["frostfall"],
    "RuneScape Survival": [],
    "Last Train Home": ["last train home"],
    "Returning to forest": [],
    "Ravenswatch": ["ravenswatch"],
    "Diluvian Winds": ["diluvian"],
    "Land of the Vikings": ["land of vikings"],
    "DESYNC": [],
    "Forever Skies": ["forever skies"],
    "Stranded: Alien Dawn": ["stranded alien dawn", "外星黎明"],
    "Last Oasis": ["最后绿洲", "last oasis"],
    "Rust Legacy": [],
    "WildFrost": ["wildfrost"],
    "Frostbite": [],
    "终末地": ["终末地", "明日方舟终末地"],
    "Pioneer": ["pioneer"],
    "Frozen Flame": ["寒霜之炎", "frozen flame"],
    "永劫无间": ["永劫无间"],  # 不是生存但常被提及
}

EXTRACT_JS = r"""
() => {
  const cards = document.querySelectorAll('div.bili-video-card');
  return Array.from(cards).map(c => {
    const titleEl = c.querySelector('.bili-video-card__info--tit, h3.bili-video-card__info--tit');
    const title = titleEl?.title || titleEl?.textContent?.trim() || c.querySelector('a')?.title;
    const link = c.querySelector('a[href*="/video/"]');
    const stats = c.querySelectorAll('.bili-video-card__stats--text');
    const owner = c.querySelector('.bili-video-card__info--owner, .bili-video-card__info--author')?.textContent?.trim();
    const dateEl = c.querySelector('.bili-video-card__info--date');
    const duration = c.querySelector('.bili-video-card__stats__duration')?.textContent?.trim();
    return {
      title: title?.slice(0, 200),
      url: link?.href,
      author: owner?.slice(0, 50),
      stats: Array.from(stats).map(s => s.textContent.trim()).slice(0, 3),
      date: dateEl?.textContent?.trim(),
      duration,
    };
  }).filter(c => c.title);
}
"""


def main():
    t0 = time.time()
    all_videos = []
    seen_urls = set()

    with attach() as (pw, browser, ctx):
        page = ctx.new_page()
        for kw in KEYWORDS:
            kw_t0 = time.time()
            url = f"https://search.bilibili.com/video?keyword={quote(kw)}&order=pubdate"
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(2.5)
                for _ in range(3):
                    page.evaluate("window.scrollBy(0, 1500)")
                    time.sleep(0.5)
                videos = page.evaluate(EXTRACT_JS)
            except Exception as e:
                print(f"  [{kw}] 失败: {str(e)[:80]}", file=sys.stderr)
                continue

            added = 0
            for v in videos:
                u = v.get("url")
                if not u or u in seen_urls:
                    continue
                seen_urls.add(u)
                v["matched_keyword"] = kw
                all_videos.append(v)
                added += 1
            print(f"  [{kw}] +{added} (总 {len(all_videos)}, {time.time()-kw_t0:.1f}s)", file=sys.stderr)

        page.close()

    # 在所有视频标题里搜游戏名
    game_mentions = Counter()
    game_videos = {}
    for v in all_videos:
        title = (v.get("title") or "").lower()
        for game, aliases in KNOWN_GAMES.items():
            for alias in aliases:
                if alias.lower() in title:
                    game_mentions[game] += 1
                    game_videos.setdefault(game, []).append(v)
                    break

    print(f"\n抓 {len(all_videos)} 条 / 总耗时 {time.time()-t0:.1f}s", file=sys.stderr)

    # 输出游戏排名
    print("\n=== 被提及次数最多的游戏 ===")
    for game, n in game_mentions.most_common(25):
        print(f"  {n:>3}× {game}")

    # 输出每个 top 游戏的代表视频
    print("\n=== 各游戏代表视频（每游戏最多 3 个）===")
    for game, n in game_mentions.most_common(15):
        print(f"\n## {game}（{n} 次提及）")
        for v in game_videos[game][:3]:
            print(f"  - {v['title'][:90]}")
            print(f"    {v.get('author','')} | {v.get('date','')} | {v.get('stats','')}")
            print(f"    {v['url']}")

    out_path = "C:/Users/yang/desktop/test_project/browser-cli/bili_games.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"videos": all_videos, "game_mentions": dict(game_mentions)}, f, ensure_ascii=False, indent=2)
    print(f"\n已存到 {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
