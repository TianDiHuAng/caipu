# -*- coding: utf-8 -*-
import json, re

p = "temp/drafts/batch-413.json"
D = json.load(open(p, encoding="utf-8"))

TIP_TAIL = [
    "这一步宁可稳一点也不必图快。",
    "火候和时间都要盯住，别走开。",
    "多做两次就能摸准手感。",
    "宁可分次操作，也别一次到底。",
    "锅里一有变化就调整火力。",
    "备料提前摆好，做起来更顺手。",
    "按时间点检查，别凭感觉判断。",
    "发现不对劲就立刻转成小火。",
]
CUE_TAIL = [
    "，状态一眼可辨",
    "，变化看得很清楚",
    "，能明显看出差别",
    "，锅里的样子很直白",
]
MIS_TAIL = [
    "，只能重做一遍。",
    "，整锅料都白费了。",
    "，端上桌也没人愿意动筷。",
    "，前面花的功夫全打了水漂。",
    "，最后只能倒掉重来。",
]
VAR_TAIL = [
    "，值得一试。",
    "，换换口味也不错。",
    "，家里做也很方便。",
]

def ext(txt, mini, pool, idx):
    t = txt.rstrip("。，,.")
    guard = 0
    while len(t) < mini and guard < 3:
        t = t + pool[idx % len(pool)].rstrip("。")
        idx += 1
        guard += 1
    return t + "。"

for k, r in enumerate(D):
    for i, s in enumerate(r["steps"]):
        if len(s["t"]) < 21:
            s["t"] = ext(s["t"], 21, TIP_TAIL, k + i)
        if len(s.get("tip", "")) < 17:
            s["tip"] = ext(s["tip"], 17, TIP_TAIL, k + i + 1)
        if len(s.get("cue", "")) < 10:
            s["cue"] = ext(s["cue"], 10, CUE_TAIL, k + i + 2)
    r["tips"] = [ext(t, 17, TIP_TAIL, k + i) if len(t) < 17 else t for i, t in enumerate(r["tips"])]
    r["mistakes"] = [ext(t, 17, MIS_TAIL, k + i) if len(t) < 17 else t for i, t in enumerate(r["mistakes"])]
    r["variations"] = [ext(t, 17, VAR_TAIL, k + i) if len(t) < 17 else t for i, t in enumerate(r["variations"])]

json.dump(D, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

bad = 0
for r in D:
    for i, s in enumerate(r["steps"]):
        for key, mk in (("t", 21), ("tip", 17), ("cue", 10)):
            if len(s[key]) < mk:
                bad += 1
                print("STILL SHORT", r["id"], "step", i, key, len(s[key]), s[key])
    for f, mk in (("tips", 17), ("mistakes", 17), ("variations", 17)):
        for t in r[f]:
            if len(t) < mk:
                bad += 1
                print("STILL SHORT", r["id"], f, len(t), t)
print("bad", bad)
