#!/usr/bin/env python3
"""扫描 NNN-*.html 和同名 .txt，生成画廊 index.html。

用法：
    python scripts/build_gallery.py

约定：
    - 作品文件名 001-slug.html，序号三位，按序号排序
    - 同目录 001-slug.txt 写元数据（TITLE / DESCRIPTION / PROMPT / TECHNIQUES）
    - thumbs/001-slug.jpg 存在就用截图，否则画廊自动降级成实时 iframe 预览
"""
from __future__ import annotations

import json
import re
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "index.html"
THUMBS = ROOT / "thumbs"
STUDY_GLOBS = ("[0-9][0-9]-*.html", "[0-9][0-9][0-9]-*.html")

COLLECTION = "HTML 单文件作品集"
EYEBROW = "COLLECTION · SINGLE-FILE HTML"
LEDE = (
    "每个页面都是一个独立的 HTML 文件：样式、脚本、字体、图形全部内联，"
    "不依赖 CDN，也没有构建步骤。双击就能离线打开，也可以直接丢进任意静态托管。"
)
TARGET = 20
REPO_URL = ""  # 例如 "https://github.com/ennheng/html-studies"，留空则不显示

ALIASES = {
    "title": ("TITLE", "标题"),
    "prompt": ("PROMPT", "提示词", "原始提示词"),
    "description": ("DESCRIPTION", "描述", "简介"),
    "techniques": ("TECHNIQUES", "技术要点", "技术"),
}
LABEL_TO_KEY = {alias.casefold(): key for key, aliases in ALIASES.items() for alias in aliases}


def parse_sidecar(path: Path) -> dict[str, str]:
    """解析 key: value 形式的元数据文件，值可以跨多行。"""
    if not path.exists():
        return {}
    data: dict[str, list[str]] = {}
    key: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        label, sep, rest = line.partition(":")
        if not sep:
            label, sep, rest = line.partition("：")
        found = LABEL_TO_KEY.get(label.strip().casefold()) if sep else None
        if found:
            key = found
            data.setdefault(key, [])
            if rest.strip():
                data[key].append(rest.strip())
        elif key:
            data[key].append(line)
    return {k: "\n".join(v).strip() for k, v in data.items()}


def fallback_title(path: Path) -> str:
    match = re.search(r"<title[^>]*>(.*?)</title>", path.read_text(encoding="utf-8", errors="ignore"), re.S | re.I)
    return unescape(match.group(1)).strip() if match else path.stem


def fallback_description(path: Path) -> str:
    match = re.search(
        r"<meta[^>]+name=[\"']description[\"'][^>]+content=[\"'](.*?)[\"']",
        path.read_text(encoding="utf-8", errors="ignore"),
        re.S | re.I,
    )
    return unescape(match.group(1)).strip() if match else ""


def thumb_for(path: Path) -> str | None:
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        candidate = THUMBS / (path.stem + ext)
        if candidate.exists():
            return candidate.name
    return None


def render_card(entry: dict) -> str:
    num, title, href = entry["num"], escape(entry["title"]), entry["href"]

    if entry["thumb"]:
        preview = (
            f'<img src="thumbs/{entry["thumb"]}" width="1440" height="900" '
            f'alt="{title} 预览图" loading="lazy" decoding="async">'
        )
    else:
        preview = (
            f'<iframe class="live" data-src="{href}" title="{title} 实时预览" '
            f'loading="lazy" sandbox="allow-scripts" tabindex="-1" aria-hidden="true"></iframe>'
        )

    prompt_button = ""
    prompt_panel = ""
    if entry["prompt"]:
        prompt_button = (
            f'<button class="btn btn-prompt" type="button" aria-expanded="false" '
            f'aria-controls="prompt-{num}">提示词</button>'
        )
        techniques = ""
        if entry["techniques"]:
            techniques = f'<p class="tech">{escape(entry["techniques"])}</p>'
        prompt_panel = (
            f'<div class="prompt" id="prompt-{num}" hidden>'
            f'<p class="label">原始提示词</p>'
            f'<p class="prompt-text">{escape(entry["prompt"])}</p>'
            f"{techniques}"
            f'<p class="src"><a href="{entry["source"]}">{entry["source"]}</a></p>'
            f"</div>"
        )

    return f"""<article class="card" id="study-{num}">
  <a class="thumb" href="{href}" target="_blank" rel="noopener" aria-label="打开 {title}">{preview}</a>
  <div class="row">
    <span class="num">{num}</span>
    <div>
      <h2 class="title"><a href="{href}" target="_blank" rel="noopener">{title}</a></h2>
      <p class="desc">{escape(entry["description"])}</p>
    </div>
    <div class="actions"><a class="btn btn-open" href="{href}" target="_blank" rel="noopener">打开 ↗</a>{prompt_button}</div>
  </div>
  {prompt_panel}
</article>"""


CSS = """
:root{
  --paper:#f2eee4;--card:#fbf9f3;--ink:#191713;--muted:#5f594e;--faint:#8b8374;
  --line:#d9d1bf;--line-2:#c1b7a2;--accent:#a63a22;
  --mono:"JetBrains Mono","Cascadia Mono",Consolas,ui-monospace,monospace;
  --sans:"Segoe UI","Microsoft YaHei",-apple-system,system-ui,sans-serif;
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;background-color:var(--paper);color:var(--ink);
  font-family:var(--sans);font-size:15px;line-height:1.6;
  background-image:radial-gradient(rgba(25,23,19,.05) 1px,transparent 0);
  background-size:24px 24px;
}
.wrap{max-width:860px;margin:0 auto;padding:54px 20px 40px}
.eyebrow{margin:0 0 14px;font-family:var(--mono);font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent)}
h1{margin:0;font-size:clamp(29px,4.6vw,44px);line-height:1.1;letter-spacing:-.025em;font-weight:700}
.lede{margin:16px 0 0;max-width:60ch;color:var(--muted)}
.stats{display:flex;flex-wrap:wrap;gap:24px;margin-top:24px;font-family:var(--mono);font-size:11px;letter-spacing:.04em;color:var(--faint)}
.stats b{color:var(--ink);font-weight:600}
.toolbar{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:18px;margin:26px -20px 16px;padding:14px 20px;background:var(--paper);border-bottom:1px solid var(--line)}
.search{position:relative;flex:1}
.search svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:15px;height:15px;color:var(--faint);pointer-events:none}
.search input{width:100%;padding:11px 14px 11px 34px;border:1px solid var(--line-2);border-radius:2px;background:var(--card);color:var(--ink);font:inherit;font-size:14px}
.search input::placeholder{color:var(--faint)}
.search input:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.count{font-family:var(--mono);font-size:11px;letter-spacing:.12em;color:var(--faint);white-space:nowrap}
.count b{color:var(--accent);font-weight:600}
.list{display:flex;flex-direction:column;gap:18px;margin-top:6px}
.card{background:var(--card);border:1px solid var(--line);border-radius:3px;overflow:hidden;transition:border-color .18s}
.card:hover{border-color:var(--line-2)}
.thumb{display:block;position:relative;aspect-ratio:16/10;overflow:hidden;background:#e7e0d1;border-bottom:1px solid var(--line)}
.thumb img{display:block;width:100%;height:100%;object-fit:cover;object-position:top center}
.live{position:absolute;top:0;left:0;width:1440px;height:900px;border:0;background:#fff;transform-origin:top left;pointer-events:none}
.row{display:grid;grid-template-columns:46px 1fr auto;gap:14px;align-items:start;padding:16px 18px 18px}
.num{padding-top:3px;font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--accent)}
.title{margin:0 0 5px;font-size:17px;font-weight:650;letter-spacing:-.01em}
.title a{color:inherit;text-decoration:none;border-bottom:1px solid transparent}
.title a:hover{border-color:var(--ink)}
.desc{margin:0;font-size:13.5px;line-height:1.65;color:var(--muted);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.actions{display:flex;align-items:center;gap:16px;padding-top:2px}
.btn{padding:0 0 2px;border:0;border-bottom:1px solid var(--line-2);background:none;color:var(--muted);font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;cursor:pointer;white-space:nowrap}
.btn:hover{color:var(--accent);border-color:var(--accent)}
.btn-open{color:var(--ink)}
.btn-prompt[aria-expanded=true]{color:var(--accent);border-color:var(--accent)}
.prompt{padding:16px 18px 18px;border-top:1px solid var(--line);background:#efe9db}
.label{margin:0 0 10px;font-family:var(--mono);font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint)}
.prompt-text{margin:0;font-size:13px;line-height:1.78;color:#3d372c;white-space:pre-wrap;overflow-wrap:anywhere}
.tech{margin:12px 0 0;padding-top:12px;border-top:1px solid #e0d8c6;font-size:12.5px;line-height:1.7;color:#5a5244;white-space:pre-wrap}
.src{margin:12px 0 0;font-family:var(--mono);font-size:11px;color:var(--faint)}
.src a{color:inherit}
.empty{padding:56px 20px;border:1px dashed var(--line-2);border-radius:3px;text-align:center;color:var(--muted)}
footer{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;margin-top:52px;padding-top:18px;border-top:1px solid var(--line);font-family:var(--mono);font-size:11px;letter-spacing:.08em;color:var(--faint)}
footer a{color:var(--accent);text-decoration:none}
footer a:hover{text-decoration:underline}
[hidden]{display:none!important}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media(max-width:620px){
  .wrap{padding-top:36px}
  .row{grid-template-columns:1fr;gap:10px}
  .num{padding:0}
  .actions{gap:20px}
  .toolbar{margin:22px -20px 14px}
}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
}
"""

JS = """
const cards = [...document.querySelectorAll('.card')];
const haystack = cards.map(card => card.textContent.toLowerCase());
const query = document.getElementById('q');
const count = document.getElementById('count');
const empty = document.getElementById('empty');
const total = cards.length;

function filter() {
  const words = query.value.toLowerCase().trim().split(/\\s+/).filter(Boolean);
  let shown = 0;
  cards.forEach((card, i) => {
    const hit = words.every(word => haystack[i].includes(word));
    card.hidden = !hit;
    if (hit) shown += 1;
  });
  count.innerHTML = '<b>' + shown + '</b> / ' + total;
  empty.hidden = shown !== 0;
}
query.addEventListener('input', filter);

document.getElementById('list').addEventListener('click', event => {
  const button = event.target.closest('.btn-prompt');
  if (!button) return;
  const open = button.getAttribute('aria-expanded') !== 'true';
  button.setAttribute('aria-expanded', String(open));
  document.getElementById(button.getAttribute('aria-controls')).hidden = !open;
});

function fitFrames() {
  document.querySelectorAll('.live').forEach(frame => {
    frame.style.transform = 'scale(' + frame.parentElement.clientWidth / 1440 + ')';
  });
}
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const frame = entry.target;
    if (!entry.isIntersecting || !frame.dataset.src) return;
    frame.src = frame.dataset.src;
    delete frame.dataset.src;
    observer.unobserve(frame);
  });
}, {rootMargin: '600px 0px'});
document.querySelectorAll('.live').forEach(frame => observer.observe(frame));
addEventListener('resize', fitFrames);
addEventListener('load', fitFrames);
fitFrames();
"""


def main() -> None:
    files = sorted(
        {path for pattern in STUDY_GLOBS for path in ROOT.glob(pattern)},
        key=lambda path: (int(path.name.split("-")[0]), path.name),
    )
    if not files:
        raise SystemExit(f"没有找到作品文件：{' / '.join(STUDY_GLOBS)}")

    entries = []
    for path in files:
        meta = parse_sidecar(path.with_suffix(".txt"))
        entries.append(
            {
                "num": path.name.split("-")[0],
                "file": path.name,
                "href": escape(path.name, quote=True),
                "source": escape(path.with_suffix(".txt").name, quote=True),
                "title": meta.get("title") or fallback_title(path),
                "description": meta.get("description") or fallback_description(path),
                "prompt": meta.get("prompt", ""),
                "techniques": meta.get("techniques", ""),
                "thumb": thumb_for(path),
            }
        )

    with_thumbs = sum(1 for entry in entries if entry["thumb"])
    count = len(entries)
    target_line = f"<span>目标{TARGET}件</span>" if TARGET else ""

    head = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(COLLECTION)} · {count} 件</title>
<meta name="description" content="{escape(LEDE)}">
<meta name="generator" content="scripts/build_gallery.py">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<style>{CSS}</style>
</head>
<body>
<main class="wrap">
<header>
  <p class="eyebrow">{escape(EYEBROW)}</p>
  <h1>{escape(COLLECTION)}</h1>
  <p class="lede">{escape(LEDE)}</p>
  <p class="stats"><span><b>{count}</b>件作品</span>{target_line}<span>无依赖 · 可离线</span></p>
</header>
<div class="toolbar">
  <div class="search">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>
    <input type="search" id="q" placeholder="搜索标题、编号、描述或提示词…" aria-label="搜索作品" autocomplete="off" spellcheck="false">
  </div>
  <div class="count" id="count" role="status" aria-live="polite"><b>{count}</b> / {count}</div>
</div>
<div class="list" id="list">
"""

    tail = f"""</div>
<p class="empty" id="empty" hidden>没有匹配的作品，换个关键词试试。</p>
<noscript><p class="src">全部作品与预览已列在上方；启用 JavaScript 后可以使用搜索和提示词面板。</p></noscript>
<footer><span>{escape(COLLECTION)} · {count}件 · 单文件 HTML</span>{f'<a href="{REPO_URL}">GitHub ↗</a>' if REPO_URL else '<span>由 build_gallery.py 生成</span>'}</footer>
</main>
<script>{JS}</script>
</body>
</html>
"""

    OUT.write_text(head + "\n".join(render_card(entry) for entry in entries) + "\n" + tail, encoding="utf-8")

    manifest = [
        {key: entry[key] for key in ("num", "file", "title", "description", "techniques", "prompt", "thumb")}
        for entry in entries
    ]
    (ROOT / "studies.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"已生成 index.html：{count} 件作品（截图 {with_thumbs}，实时预览 {count - with_thumbs}）")
    if TARGET and count != TARGET:
        print(f"提示：当前 {count} 件，目标 {TARGET} 件，还差 {TARGET - count} 件。")


if __name__ == "__main__":
    main()
