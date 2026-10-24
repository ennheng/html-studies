#!/usr/bin/env python3
"""新建一件作品：自动占用下一个序号，生成本地 HTML 骨架和元数据文件。

用法：
    python scripts/new_study.py "轨道钟" --slug orbital-clock

生成：
    001-orbital-clock.html   单文件页面骨架
    001-orbital-clock.txt    TITLE / DESCRIPTION / PROMPT 元数据
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<style>
  :root {{ --paper:#f2eee4; --ink:#191713; --accent:#a63a22; }}
  * {{ box-sizing:border-box; }}
  body {{
    margin:0; min-height:100vh; display:grid; place-items:center;
    background:var(--paper); color:var(--ink);
    font-family:"Segoe UI","Microsoft YaHei",system-ui,sans-serif;
  }}
  h1 {{ font-size:clamp(28px,6vw,56px); letter-spacing:-.03em; margin:0 0 12px; }}
  p {{ margin:0; color:#5f594e; }}
</style>
</head>
<body>
<main>
  <h1>{title}</h1>
  <p>把这一段换成你的页面内容。</p>
</main>
</body>
</html>
"""

SIDECAR = """TITLE: {title}

DESCRIPTION:
一句话说清这件作品是什么、视觉上最特别的地方在哪。

PROMPT:
生成这个页面时用的完整提示词。写清：主题、色板、排版、交互、响应式断点、以及"单文件、无外部依赖"的硬性约束。

TECHNIQUES:
- 列出 3~5 个值得一提的实现手法
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("title", help="作品标题，例如 轨道钟")
    parser.add_argument("--slug", default="", help="英文短名，用于文件名；留空则用编号")
    args = parser.parse_args()

    existing = sorted(ROOT.glob("[0-9][0-9][0-9]-*.html"))
    number = f"{(int(existing[-1].name[:3]) + 1 if existing else 1):03d}"
    slug = re.sub(r"[^a-z0-9-]+", "-", args.slug.lower()).strip("-") or "study"
    stem = f"{number}-{slug}"

    description = f"{args.title}——单文件 HTML 作品。"
    (ROOT / f"{stem}.html").write_text(
        TEMPLATE.format(title=args.title, description=description), encoding="utf-8"
    )
    (ROOT / f"{stem}.txt").write_text(SIDECAR.format(title=args.title), encoding="utf-8")
    print(f"已创建 {stem}.html 和 {stem}.txt")
    print("写完页面后执行：python scripts/build_gallery.py")


if __name__ == "__main__":
    main()
