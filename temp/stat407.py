# -*- coding: utf-8 -*-
import json, io
p = r"E:\ai_project\marvis_project\caipu\tasks\progress.json"
d = json.load(io.open(p, encoding="utf-8"))
print(json.dumps(d["totals"], ensure_ascii=False))
r0 = d["regions"][0]
print(json.dumps({k: v for k, v in r0.items() if k != "cuisines"}, ensure_ascii=False))
print(json.dumps(r0["cuisines"][0], ensure_ascii=False)[:600])
rows = []
for r in d["regions"]:
    for c in r.get("cuisines", []):
        rows.append((c["target"] - c["actual"], c["slug"], c["actual"], c["target"]))
rows.sort(reverse=True)
for x in rows[:14]:
    print(x)
