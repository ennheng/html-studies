#!/usr/bin/env python3
"""给每个作品拍一张 1440×900 的预览图，输出到 thumbs/。

用法：
    python scripts/capture_screenshots.py            # 全部重拍
    python scripts/capture_screenshots.py 003 007    # 只拍指定编号

优先用 Playwright（能等动画、能并行）；没装就用本机 Chrome 无头模式兜底。
Playwright 的安装方式：
    pip install playwright
    python -m playwright install chromium
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THUMBS = ROOT / "thumbs"
VIEWPORT = (1440, 900)
WAIT_MS = 1800

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome() -> str | None:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    for name in ("chrome", "chromium", "google-chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    return None


def capture_with_playwright(files: list[Path]) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(args=["--no-sandbox", "--hide-scrollbars"])
        try:
            for file in files:
                page = browser.new_page(viewport={"width": VIEWPORT[0], "height": VIEWPORT[1]}, device_scale_factor=1)
                try:
                    page.goto(file.as_uri(), wait_until="load")
                    page.wait_for_timeout(WAIT_MS)
                    page.screenshot(
                        path=str(THUMBS / (file.stem + ".jpg")),
                        type="jpeg",
                        quality=82,
                        full_page=False,
                    )
                    print(f"已截图 {file.name} · playwright", flush=True)
                finally:
                    page.close()
        finally:
            browser.close()


def capture_with_chrome(files: list[Path], chrome: str) -> None:
    with tempfile.TemporaryDirectory() as profile:
        for file in files:
            target = THUMBS / (file.stem + ".png")
            command = [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--no-first-run",
                "--no-default-browser-check",
                f"--user-data-dir={profile}",
                f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}",
                "--force-device-scale-factor=1",
                f"--virtual-time-budget={WAIT_MS + 1200}",
                f"--screenshot={target}",
                file.as_uri(),
            ]
            try:
                subprocess.run(command, check=True, capture_output=True, timeout=90)
                print(f"已截图 {file.name} · chrome", flush=True)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
                print(f"截图失败 {file.name}: {error}", file=sys.stderr)


def compress_to_jpeg(files: list[Path]) -> None:
    """Chrome 只能输出 PNG；装了 Pillow 就压成 JPEG，20 张能省 4MB 左右。"""
    try:
        from PIL import Image
    except ImportError:
        return
    for file in files:
        png = THUMBS / (file.stem + ".png")
        if not png.exists():
            continue
        with Image.open(png) as image:
            image.convert("RGB").save(
                THUMBS / (file.stem + ".jpg"), "JPEG", quality=82, optimize=True, progressive=True
            )
        png.unlink()


def main() -> None:
    THUMBS.mkdir(exist_ok=True)
    files = sorted(
        {path for pattern in ("[0-9][0-9]-*.html", "[0-9][0-9][0-9]-*.html") for path in ROOT.glob(pattern)},
        key=lambda path: (int(path.name.split("-")[0]), path.name),
    )
    if not files:
        raise SystemExit("没有找到作品文件")

    wanted = {arg.zfill(3) for arg in sys.argv[1:] if arg.isdigit()}
    if wanted:
        files = [file for file in files if file.name[:3] in wanted]

    try:
        import playwright  # noqa: F401
    except ImportError:
        chrome = find_chrome()
        if not chrome:
            raise SystemExit("既没有 Playwright，也没有找到本机 Chrome/Edge。先执行 pip install playwright。")
        print(f"未安装 Playwright，改用 {chrome}")
        capture_with_chrome(files, chrome)
        compress_to_jpeg(files)
        return

    capture_with_playwright(files)

    missing = [file.name for file in files if not any((THUMBS / (file.stem + ext)).exists() for ext in (".jpg", ".png"))]
    if missing:
        raise SystemExit("以下作品没有生成截图：" + ", ".join(missing))
    print(f"完成：{len(files)} 张预览图，位于 thumbs/")


if __name__ == "__main__":
    main()
