# -*- coding: utf-8 -*-
import json
p = r"D:\AI\project\marvis_project\caipu\data\taxonomy.json"
d = json.loads(open(p, encoding="utf-8-sig").read())
changed = []
for c in d["cuisines"]:
    if c["slug"] == "cantonese":
        uns = c.get("unsupported") or []
        if "main-meat" in uns:
            uns.remove("main-meat")
            c["unsupported"] = uns
            changed.append("removed main-meat from cantonese unsupported")
        if "main-meat" not in c["core"]:
            c["core"].insert(1, "main-meat")
            changed.append("added main-meat to cantonese core")
        print("cantonese core:", c["core"])
        print("cantonese unsupported:", c["unsupported"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("changed:", changed)
