#!/usr/bin/env python3
import json, os, sys, urllib.parse, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV = ROOT / ".env.local"
OUT = ROOT / "private_exports"

def load_env():
    data = {}
    if ENV.exists():
        for raw in ENV.read_text(encoding="utf-8-sig").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line: continue
            k,v=line.split("=",1); data[k.strip()]=v.strip()
    return data

def api(base, token, path, params=None):
    url=base.rstrip("/") + path
    if params: url += "?" + urllib.parse.urlencode(params)
    req=urllib.request.Request(url, headers={"Authorization":"Bearer "+token})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))

def safe_name(s):
    bad='<>:"/\\|?*'
    s="".join("_" if c in bad else c for c in (s or "wechat"))
    return s.strip(" .")[:80] or "wechat"

def main():
    env=load_env()
    base=env.get("WEFLOW_BASE_URL","http://127.0.0.1:5031")
    token=env.get("WEFLOW_TOKEN","").strip()
    if not token:
        print("未配置 WEFLOW_TOKEN。请先双击 setup.bat。")
        return 2
    try:
        api(base, token, "/api/v1/health")
    except Exception as e:
        print("无法连接 WeFlow API：", e)
        print("请确认 WeFlow -> 设置 -> API 服务 已启动，Token 正确。")
        return 3

    try:
        sessions=api(base, token, "/api/v1/sessions")
    except Exception as e:
        print("读取会话失败：",e); return 4

    items=sessions.get("sessions", sessions if isinstance(sessions,list) else [])
    if not items:
        print("没有读取到会话。"); return 5

    print("\n最近会话：")
    for i,s in enumerate(items[:100],1):
        name=s.get("name") or s.get("displayName") or s.get("nickname") or s.get("talker") or s.get("id") or "未知"
        sid=s.get("id") or s.get("talker") or s.get("sessionId") or ""
        print(f"{i:3}. {name}  [{sid}]")
    raw=input("\n输入序号：").strip()
    try: chosen=items[int(raw)-1]
    except Exception:
        print("序号无效。"); return 6

    sid=chosen.get("id") or chosen.get("talker") or chosen.get("sessionId")
    name=chosen.get("name") or chosen.get("displayName") or chosen.get("nickname") or sid
    if not sid:
        print("无法取得会话 ID。"); return 7

    all_messages=[]; offset=0; page=5000
    print(f"\n正在读取：{name}")
    while True:
        data=api(base, token, "/api/v1/messages", {
            "talker":sid, "limit":page, "offset":offset, "format":"chatlab"
        })
        msgs=data.get("messages", [])
        all_messages.extend(msgs)
        print(f"已读取 {len(all_messages)} 条")
        if not data.get("hasMore") or not msgs: break
        offset += len(msgs)

    OUT.mkdir(parents=True, exist_ok=True)
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    stem=f"{safe_name(name)}_{stamp}"
    payload={"source":"WeFlow","session":{"id":sid,"name":name},"messageCount":len(all_messages),"messages":all_messages}
    jpath=OUT/(stem+"_chatgpt.json")
    mpath=OUT/(stem+"_chatgpt.md")
    jpath.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")

    lines=[f"# 微信聊天：{name}","",f"- 消息数：{len(all_messages)}",f"- 会话 ID：{sid}","","## 聊天记录",""]
    for m in all_messages:
        ts=m.get("timestamp") or m.get("createTime")
        try: when=datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S") if ts else ""
        except: when=str(ts or "")
        who=m.get("accountName") or m.get("groupNickname") or m.get("sender") or ("我" if m.get("isSend") else "对方")
        content=m.get("content") or m.get("parsedContent") or m.get("rawContent") or ""
        lines.append(f"[{when}] {who}: {content}")
    mpath.write_text("\n".join(lines),encoding="utf-8")
    print("\n完成：")
    print(mpath)
    print(jpath)
    try: os.startfile(str(OUT))
    except Exception: pass
    print("\n把 *_chatgpt.md 直接拖进 ChatGPT，然后告诉它你想分析什么。")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
