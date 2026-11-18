# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
for x in d["items"]:
    if x["key"] in ("pork-ribs", "onion", "pork-belly", "beef-tenderloin"):
        print(x)
