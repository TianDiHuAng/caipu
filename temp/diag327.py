# -*- coding: utf-8 -*-
import json, io, os, re
os.chdir(r"E:\ai_project\marvis_project\caipu")
ing=json.load(io.open("data/ingredients.json",encoding="utf-8"))
for it in ing["items"]:
    if it["zh"] in ("小白菜","大米","带鱼","鸡腿肉","虾仁","米饭"):
        print(it["zh"], "aliases:", it.get("aliases"))
def texts(j):
    res=[]
    for s in j["steps"]:
        for k in ("text","tip","visual_cue"):
            if k in s and isinstance(s[k],str): res.append((k,s[k]))
    for k in ("tips","common_mistakes","food_safety_notes"):
        for x in j.get(k) or []:
            if isinstance(x,str): res.append((k,x))
    for k in ("serving_suggestion","storage","origin_note"):
        if isinstance(j.get(k),str): res.append((k,j[k]))
    for x in j.get("substitutions") or []:
        for k,v in x.items():
            if isinstance(v,str): res.append(("sub."+k,v))
    for x in j.get("variations") or []:
        if isinstance(x,str): res.append(("var",x))
    return res
targets={"chaoshan-haozi-zhou":["小白菜","青菜","菜末"],"chaoshan-lushui-doufu":["大米","米饭","饭"],
"chaoshan-shacha-chao-hetiao":["小白菜"],"chaoshan-puning-doujiang-yu":["带","鱼"],"chaoshan-nanjiang-ji":["鸡腿","虾"]}
for sid,keys in targets.items():
    p="data/recipes/cn/chaoshan/%s.json"%sid
    j=json.load(io.open(p,encoding="utf-8"))
    print("=====",sid)
    for f,t in texts(j):
        if any(k in t for k in keys):
            print("  [",f,"]",t[:90])
