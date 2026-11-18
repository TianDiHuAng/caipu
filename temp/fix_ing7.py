# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
for x in d["items"]:
    if x["key"] == "river-shrimp":
        x["aliases"] = ["河虾", "鲜虾仁"]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
m = {}
for x in d["items"]:
    for a in [x["zh"], x["en"]] + list(x.get("aliases") or []):
        m.setdefault(a, []).append(x["key"])
print("dup:", {k: v for k, v in m.items() if len(v) > 1})
print("total", len(d["items"]))
