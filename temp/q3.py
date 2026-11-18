# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\taxonomy.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
for c in d["cuisines"]:
    if c["slug"] in ("northeast", "xinjiang", "beijing", "shanghai", "anhui", "fujian", "hunan", "jiangsu", "shandong", "zhejiang", "sichuan", "cantonese", "japanese"):
        print(c["slug"], c["zh"], "| core:", c.get("core"), "| unsupported:", c.get("unsupported"))
print("---all slugs---")
print(", ".join(c["slug"] for c in d["cuisines"]))
