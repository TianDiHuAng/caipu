# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
for x in d["items"]:
    if x["key"] in ("scallion", "welsh-onion"):
        print("before", x["key"], x["zh"], x.get("aliases"))
        x["aliases"] = [a for a in (x.get("aliases") or []) if a not in ("葱段", "葱白")]
        print("after ", x["key"], x.get("aliases"))
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
m = {}
for x in d["items"]:
    for a in [x["zh"], x["en"]] + list(x.get("aliases") or []):
        m.setdefault(a, []).append(x["key"])
print("dup aliases:", {k: v for k, v in m.items() if len(v) > 1})
