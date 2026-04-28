# browser-cli

通过 Playwright 直连本机 Chrome（CDP 端口 9222）做爬取的脚本集。所有脚本共用 `connect.py` 的 `attach()` 上下文管理器，自动复用 Chrome 已登录态，绕开大部分平台的反爬。

## 启动 Chrome（必须先做）

关闭所有 Chrome，然后用调试端口启动：

```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="C:\Users\yang\AppData\Local\Google\Chrome\User Data"
```

启动后正常登录 B 站、抖音、X 等。脚本会复用这些登录态。

验证连接通了：

```bash
python connect.py
# 应输出当前打开的 tab 列表
```

## 一个完整任务的标准流程（4 步）

以"近 3 天 X 主题在某平台的股民情绪"为例：

```
1. 搜索       <platform>_<topic>_search.py     → 抓 N 个候选视频
2. 筛选       <platform>_<topic>_top10.py      → 主题相关性 + 播放量过滤
3. 抓评论     <platform>_comments_full.py      → 主楼 + 子回复
4. 情绪分析   <platform>_<topic>_sentiment.py  → 词典分类 + 排序
```

每步产出 JSON，下一步读上一步的 JSON。

## 文件清单（按平台 + 角色）

### 🔧 基础设施

| 文件 | 作用 |
|---|---|
| `connect.py` | Playwright CDP 连接器；所有 scraper 复用 |
| `_archive/` | 探针/调试脚本，开发时用过的一次性产物 |

### 📺 B 站（哔哩哔哩）

**通用工具**：

| 文件 | 输入 → 输出 | 备注 |
|---|---|---|
| `bili_comments_full.py` | top10.json → comments.json | **首选**评论抓取器：DOM shadow piercing + 真鼠标点击展开子回复。可参数化 `python bili_comments_full.py <input> <output>` |
| `bili_comments_dom.py` | top10.json → comments.json | DOM-only 简单版（不展开子回复）。`bili_comments_full.py` 是它的进化版 |

**主题脚本（参照模板，换 KEYWORDS 即复用）**：

| 主题 | 搜索 | 筛选 | 评论 | 情绪 |
|---|---|---|---|---|
| 美股 | `bili_us_stocks_search.py` | `bili_us_stocks_top10.py` | `bili_us_stocks_comments.py`（API版，已被 `bili_comments_full.py` 替代） | `bili_us_stocks_sentiment.py` |
| A 股 | `bili_a_search.py` | `bili_a_top10.py` | `bili_comments_full.py`（通用） | `bili_a_sentiment.py` |

**其他历史脚本**（专题爬取，独立的）：
- `bili_find_videos.py` / `bili_search_games.py` — 视频/游戏搜索
- `bili_video_content.py` / `bili_video_content2.py` — 视频描述+顶部评论
- `bili_official.py` / `bili_linglong.py` / `bili_yihua_deep.py` / `bili_yihua_dynamic.py` — 灵笼/异画专题

### 🎵 抖音

**通用工具**：

| 文件 | 输入 → 输出 | 备注 |
|---|---|---|
| `dy_search_api.py` | 关键词 → results.json | 通过抓包 `/general/search/stream` API 拿元数据。**比卡片抓取信息全**（含 digg_count, comment_count, create_time）|
| `dy_us_stocks.py` | 关键词 → results.json | 卡片版，旧 |
| `dy_comments.py` | input.json → comments.json | 老版，仅主楼 |
| `dy_comments_full.py` | input.json → comments.json | **首选**：主楼+子回复，Playwright 真鼠标点击 `button.comment-reply-expand-btn` |

**主题脚本**：

| 主题 | 搜索 | 筛选 | 情绪 |
|---|---|---|---|
| A 股 | `dy_a_search.py` | `dy_a_top10.py` | `dy_a_sentiment.py` |

### 📺 YouTube

| 文件 | 作用 |
|---|---|
| `yt_us_stocks.py` | 美股视频搜索 |
| `yt_comments.py` | 评论抓取（含子回复） |

### 🐦 X (Twitter)

| 文件 | 作用 |
|---|---|
| `x_search.py` | X 搜索 |
| `x_replies.py` | 帖子回复抓取 |
| `x_analyze.py` | 已抓取数据分析 |
| `elon_today.py` | Elon Musk 当日推文 |

### 📚 学术爬取

| 文件 | 作用 |
|---|---|
| `arxiv_search.py` / `arxiv_specialized.py` | arXiv 论文搜索 |
| `aaai_search.py` / `aaai_search_extra.py` / `aaai_abstracts.py` / `aaai_make_doc.py` | AAAI 论文搜索 + 摘要 + 文档生成 |
| `openreview_search.py` | OpenReview 搜索 |
| `github_extract.py` | GitHub repo 信息抽取 |

### 📊 通用分析

| 文件 | 作用 |
|---|---|
| `analyze_comments.py` | 通用评论分析 |
| `methods_analysis.py` | 方法论分析 |
| `trend_analysis.py` | 趋势分析 |
| `exec_summary.py` / `final_doc.py` | 文档生成 |
| `very_recent.py` | 时间过滤工具 |

## 可复用度说明

| 等级 | 内容 | 下次任务我会怎么做 |
|---|---|---|
| ✅ 开箱即用 | `connect.py`, `*_comments_full.py`, `yt_comments.py` | 直接调用，不改一行 |
| 🟡 改 1-2 处常量 | `*_search.py`, `*_top10.py` | 编辑 `KEYWORDS` / `INCLUDE_KW` / `EXCLUDE_KW` |
| 🟠 改字典 | `*_sentiment.py` | 替换 `TICKERS = {...}`（A 股/美股/加密各一份）|

## 关键技术经验（写脚本时少踩的坑）

1. **B 站搜索 URL**：`search.bilibili.com/video?keyword=X&order=click&pubtime_begin_s=<ts>&pubtime_end_s=<ts2>`，`order=click` 是按播放量
2. **B 站搜索结果卡片**：播放量在 `.bili-video-card__stats--item` 的无 class span 里，第 1 个是播放量第 2 个是弹幕数
3. **B 站评论 API 412 限流**：`/x/v2/reply/main` 和 `/x/v2/reply` 需 WBI 签名，**直接 fetch 会被反爬挡掉**。改用 DOM 深度穿透 shadow DOM 抓取
4. **B 站 shadow DOM 结构**：`bili-comment-thread-renderer`（主楼）+ `bili-comment-reply-renderer`（子回复，需点击展开）。展开按钮是 `bili-text-button` 含文本"点击查看"
5. **B 站新 tab 反爬**：`ctx.new_page()` 开的标签页 B 站不给加载评论（缺少 WBI session 状态），**必须用 `ctx.pages[0]` 现有标签页**
6. **抖音搜索 URL**：`douyin.com/search/<keyword>?publish_time=7&sort_type=2`（`publish_time=7` 是近一周，`sort_type=2` 是按热度）
7. **抖音评论结构**：主楼+子回复都用 `[data-e2e="comment-item"]`，子回复套在 `.replyContainer` 容器里，**用 ancestor 检查区分**
8. **抖音展开子回复**：button 是 `button.comment-reply-expand-btn`，**JS click() 不触发 React 处理器**，必须用 `Playwright locator.click()` 真鼠标事件
9. **B 站缓存数据 vs 实时**：去重时按 `(uname, content[:100])` 而不是 rpid——同一条评论会因 shadow DOM 多次访问出现 3 倍重复
10. **DOM 深度文本提取要跳 STYLE/SCRIPT/SVG/BILI-AVATAR**，否则会把 CSS `:host {...}` 当文本

## TODO

- [ ] 把 `*_search.py` / `*_top10.py` / `*_sentiment.py` 重构成参数化 CLI，下次换主题不用编辑代码
- [ ] 抽出 `tickers/` 子目录存各主题的标的字典（a_stocks.json、us_stocks.json、crypto.json）
- [ ] 抽出 `lexicons/` 子目录存通用情绪词典
