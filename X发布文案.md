# 发到 X

## 主贴（英文，和 Mia 那条同一路数）

> 20 HTML files. One model: Kimi 3.1 Pro.
>
> Every page is a single self-contained file — all CSS, JS and SVG inline. No libraries, no CDN, no web fonts, no build step. Open it offline and it runs.
>
> The gallery: https://ennheng.github.io/html-studies/
>
> A few of them in the thread ↓

配图：01-chromatic-orbit、06-brutalist-radio、09-alpine-air、20-the-last-signal

## 主贴（中文）

> 20 个 HTML 文件，全部来自同一个模型：Kimi 3.1 Pro。
>
> 每一页都是单文件：CSS、JS、SVG 全内联，没有库、没有 CDN、没有网络字体、没有构建步骤，离线打开就能跑。
>
> 画廊：https://ennheng.github.io/html-studies/
>
> 挑几件放在评论区 ↓

---

## 回复串（每条 4 张图）

**1/5 生成艺术**

> 01 Chromatic Orbit — 144 个天体在引力场里聚散，移动指针能弯曲空间
> 05 Tide & Time — 4 秒吸、4 秒停、6 秒呼，波纹跟着走
> 16 Sound Sculptor — 振荡器驱动 128 个顶点的实时几何
> 07 Celestial Archive — 四个星座，四只档案抽屉

图：thumbs/01-chromatic-orbit.jpg、05-tide-and-time.jpg、16-sound-sculptor.jpg、07-celestial-archive.jpg

**2/5 编辑式排版**

> 02 After Hours — 凌晨两点的蓝调聆听室
> 06 OFF/AIR — 用巨型字幕堆出来的独立电台
> 17 Mono Museum — 只有黑和白的数字展览
> 15 Atlas of Elsewhere — 四座只存在于记忆里的城市

图：thumbs/02-after-hours.jpg、06-brutalist-radio.jpg、17-mono-museum.jpg、15-invisible-cities.jpg

**3/5 能点的小工具**

> 11 Type in Motion — 输入你的短语，四种运动模式
> 12 Golden Hour Kitchen — 拖动太阳，光照和阴影跟着变
> 18 Fieldwork — 拖时间轴看未来 24 小时的天气
> 10 Cloud Kettle — 可以点单的云上茶室，猫替你留了座位

图：thumbs/11-type-in-motion.jpg、12-solar-cooking.jpg、18-pocket-weather.jpg、10-pixel-teahouse.jpg

**4/5 游戏与交互**

> 14 Pair Up! — 8 对牌的记忆街机，最高分存在本地
> 04 Neon Velocity — 按住 ↑ 的夜间赛道，转速和圈速实时联动
> 08 Little Riot — 12 格分镜，每秒 6 帧逐格播放
> 19 Mooncrumb — 四款糕点绕着轨道转

图：thumbs/14-memory-arcade.jpg、04-neon-velocity.jpg、08-paper-cinema.jpg、19-cosmic-bakery.jpg

**5/5 收尾**

> 13 Moonstem — 用 SVG 现场画出来的午夜花束
> 03 Wild Atlas — 三份植物标本的田野档案
> 09 ALTITUDE — 三天行程分三幕的编辑式长页
> 20 The Last Signal — 一段深空信号的解码过程
>
> 全部 20 件：https://ennheng.github.io/html-studies/

图：thumbs/13-midnight-florist.jpg、03-wild-atlas.jpg、09-alpine-air.jpg、20-the-last-signal.jpg

---

## 提示词补上后，再加这两句

主贴末尾追加：

> Every page is published next to the prompt that produced it.

中文版：

> 每一页的原始提示词，都公开在画廊里。

加之前要先把 20 个 txt 的 **PROMPT** 段填满，重新 build 并 push —— 那时卡片上才会出现「提示词」按钮。

## 操作要点

- 一条推最多 **4 张图**，直接拖 `thumbs/` 里的文件。
- 主贴带图时链接 **不会出大卡片**，只显示一行蓝字，这是 X 的正常行为。
- 想让人看到 1200×630 的分享卡（og.jpg），就单独发一条纯链接的推，或者把链接放在第一条回复。
- 每条图都写 **Alt text**，X 支持，对无障碍和检索都有用。
- 发完置顶主贴，再把 5 条回复按顺序接上。
- 改过 og.jpg 之后重发同一个链接，X 可能还显示旧图（缓存），链接后加 `?v=2` 可以强制重抓。
- 图会被 X 轻微裁切：thumbs 是 16:10，X 按 16:9 显示，上下各掉一点，关键信息都在中间。
- 别在一条推文里塞 20 个链接，容易被判定为链接堆砌。
