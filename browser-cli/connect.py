"""连接到已运行的 Chrome（端口 9222）的复用工具。

用法：
    from connect import attach
    with attach() as (pw, browser, ctx):
        page = ctx.pages[0]
        ...
"""
import os
import sys
from contextlib import contextmanager

os.environ.setdefault("NODE_NO_WARNINGS", "1")
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

CDP_URL = "http://127.0.0.1:9222"


@contextmanager
def attach(cdp_url: str = CDP_URL, timeout_ms: int = 600000):
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(cdp_url, timeout=timeout_ms)
        ctx = browser.contexts[0]
        try:
            yield pw, browser, ctx
        finally:
            browser.close()


def list_pages():
    with attach() as (_, _, ctx):
        return [{"url": p.url, "title": p.title()} for p in ctx.pages]


if __name__ == "__main__":
    import json
    print(json.dumps(list_pages(), ensure_ascii=False, indent=2))
