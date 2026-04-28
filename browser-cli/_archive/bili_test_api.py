"""单点测试 B站 reply API 当前响应。"""
import sys, time
sys.path.insert(0, 'C:/Users/yang/desktop/test_project/browser-cli')
sys.stdout.reconfigure(encoding='utf-8')
from connect import attach

TEST = """
async () => {
  const aid = 116471342633364;
  const out = {};
  // mode=3 之前能用
  const r3 = await fetch(`https://api.bilibili.com/x/v2/reply/main?type=1&oid=${aid}&mode=3&next=0&ps=20`, {credentials:'include'});
  out.mode3_status = r3.status;
  out.mode3_sample = (await r3.text()).slice(0, 200);
  // mode=2
  const r2 = await fetch(`https://api.bilibili.com/x/v2/reply/main?type=1&oid=${aid}&mode=2&next=0&ps=20`, {credentials:'include'});
  out.mode2_status = r2.status;
  out.mode2_sample = (await r2.text()).slice(0, 200);
  return out;
}
"""

with attach() as (pw, browser, ctx):
    page = ctx.new_page()
    page.goto('https://www.bilibili.com/', wait_until='domcontentloaded', timeout=20000)
    time.sleep(2)
    info = page.evaluate(TEST)
    page.close()
    import json
    print(json.dumps(info, ensure_ascii=False, indent=2))
