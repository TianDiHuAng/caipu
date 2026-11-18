# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
d["items"] = [x for x in d["items"] if x["key"] != "lamb-leg"]
for x in d["items"]:
    if x["key"] == "lamb":
        print("lamb:", x)
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("total", len(d["items"]))
