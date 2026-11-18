# -*- coding: utf-8 -*-
import json, os
ROOT = r"D:\AI\project\marvis_project\caipu"
ip = ROOT + r"\data\ingredients.json"
d = json.loads(open(ip, encoding="utf-8-sig").read())
for x in d["items"]:
    if x["zh"] == "肥牛":
        print("before", x["aliases"])
        x["aliases"] = [a for a in x["aliases"] if a not in ("牛肉片", "牛肉")]
        print("after", x["aliases"])
json.dump(d, open(ip, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

flour = [x for x in d["items"] if x["zh"] == "面粉"]
print("flour entry:", [f["key"] for f in flour])

def patch(rel, repl, add_aux):
    p = ROOT + "\\data\\recipes\\" + rel
    r = json.loads(open(p, encoding="utf-8-sig").read())
    for s in r["steps"]:
        for f in ("text", "tip", "visual_cue"):
            v = s.get(f) or ""
            for a, b in repl:
                v = v.replace(a, b)
            s[f] = v
    if add_aux:
        for g in r["ingredients"]:
            if g["group"] == "aux":
                g["items"].append(add_aux)
    json.dump(r, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("patched", p)

patch(r"cn\sichuan\fuqi-feipian.json", [("牛肉片", "牛腱片"), ("一把面粉", "20 克面粉")],
      {"name": "面粉", "name_en": "plain flour", "amount": 20, "unit": "g",
       "note": "仅用于搓洗牛肚表面黏液，冲洗后不留在成品中", "optional": False})
patch(r"cn\shandong\jiuzhuan-dachang.json", [("一把面粉", "20 克面粉")],
      {"name": "面粉", "name_en": "plain flour", "amount": 20, "unit": "g",
       "note": "仅用于搓洗肠壁黏液，冲洗后不留在成品中", "optional": False})
