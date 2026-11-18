# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\ingredients.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
for x in d["items"]:
    if x["category"] != "other":
        for a in [x["zh"]] + list(x.get("aliases") or []):
            if a in ("猪肉", "牛肉", "鸡肉", "羊肉", "猪肉末", "牛肉末"):
                print(x["key"], "|", x["zh"], "|", a)
