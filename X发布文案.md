# 发到 X：和 Mia 那组推文的差别在哪

## 结论

**X 不会在推文里运行 HTML。** Mia 那条推文里你能看到的是「图片 + 一个链接」，真正的页面跑在她自己的 GitHub Pages 上，X 只负责把人导过去。

所以「像她一样发」= 四件事：

1. 一个公网地址（已完成：https://ennheng.github.io/html-studies/）
2. 一张 1200×630 的分享卡，链接粘贴进推文时自动变成大图（已完成：og.jpg + og 元标签）
3. 一组 16:9 的作品截图（已完成：thumbs/ 里 20 张 1440×900）
4. 推文结构：主推文抛结论，回复串里每楼放 4 张

## 两种发法，选一个

**A. 纯链接**——推文里只放 URL，X 会渲染 og 大卡片。点击率最高，适合「作品集」这种整体发布。

**B. 4 图 + 链接**——Mia 用的这种。X 优先展示图片，链接退化成一行蓝字，但首屏视觉冲击强得多。20 件作品建议用 B，主推文选 4 张反差最大的。

## 主推文（英文）

> 20 self-contained HTML pages, each written in a single shot.
>
> No CDN, no web fonts, no images, no build step — every page is one file that opens offline.
>
> Searchable gallery: https://ennheng.github.io/html-studies/
>
> Favourites in the thread ↓

配图选：01-chromatic-orbit、06-brutalist-radio、09-alpine-air、20-the-last-signal（一暗一亮、一密一空，缩略图墙里最能拉开对比）。

## 回复串（每条 4 张，图在 thumbs/ 下）

**1/5 生成艺术**
- 01-chromatic-orbit：144 个天体在引力场里聚散
- 05-tide-and-time：4-4-6 的呼吸节奏驱动波纹
- 16-sound-sculptor：振荡器驱动 128 个顶点的几何
- 07-celestial-archive：星座档案抽屉

**2/5 编辑式排版**
- 02-after-hours：凌晨两点的蓝调聆听室
- 06-brutalist-radio：用巨型字幕堆出来的独立电台
- 17-mono-museum：只有黑白的数字展览
- 15-invisible-cities：四座虚构城市的横向图集

**3/5 小工具，真的能用**
- 11-type-in-motion：输入短语，四种运动模式
- 12-solar-cooking：拖动太阳改变光照
- 18-pocket-weather：拖时间轴看未来 24 小时
- 10-pixel-teahouse：可以点单的云上茶室

**4/5 游戏与交互**
- 14-memory-arcade：8 对牌的记忆街机
- 04-neon-velocity：按住 ↑ 的夜间赛道
- 08-paper-cinema：12 格分镜逐帧播放
- 19-cosmic-bakery：糕点绕着轨道转

**5/5 收尾**
- 13-midnight-florist：SVG 现场画出来的花束
- 03-wild-atlas：植物标本档案
- 09-alpine-air：三天行程的编辑式长页
- 20-the-last-signal：深空信号的解码过程

最后一条回复写：

> All 20 pages, with the brief behind each one: https://ennheng.github.io/html-studies/
>
> Built as single files so they survive: no dependency rot, no broken CDN, just open and it works.

## 操作清单

1. 每张图都写 **Alt text**（X 支持，且对无障碍和搜索都有用）。
2. 主推文发出后立刻置顶，然后把 5 条回复按顺序接上。
3. 图片会被 X 轻微裁切：thumbs 是 16:10，X 按 16:9 显示，上下各掉一点，作品的关键信息都在中间，不影响。
4. 单张上限 5MB，我们的图 60–120KB，完全够。
5. 别在一条推文里塞 20 个链接——X 会判定为链接堆砌，降权。

## 发之前要知道的两个坑

**og 缓存。** X 抓到分享卡后会缓存。以后改了 og.jpg 或标题，重新发同一个 URL 仍可能显示旧图。解决办法是等缓存过期，或在链接后加一个无意义的查询参数（`?v=2`）逼它重新抓。

**纯文本链接不会出卡。** 如果推文里同时有 4 张图和 URL，X 就不渲染大卡片了——这是预期行为，不是配置错了。想要大卡片就用发法 A。

## 发完看什么

- X Analytics：看 link clicks，不看 impressions
- GitHub → Insights → Traffic：看 referrers 里 x.com 的占比，这才是真实导流
