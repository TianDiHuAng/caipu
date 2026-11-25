# -*- coding: utf-8 -*-
import json, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
pg = json.load(open("tasks/progress.json", encoding="utf-8"))
rows = []
for region in ("cn", "intl"):
    for c in pg["regions"][region]:
        slug = c.get("slug") or c.get("id")
        name = c.get("name") or c.get("zh")
        cells = c.get("cells") or []
        tot = sum(x.get("target", 0) for x in cells)
        act = sum(x.get("actual", 0) for x in cells)
        zero = [x.get("slug") or x.get("category") for x in cells if x.get("actual", 0) == 0]
        low = sorted([(x.get("actual", 0), x.get("slug") or x.get("category")) for x in cells])[:3]
        rows.append((act - tot, act, tot, slug, name, region, len(zero), zero[:6], low))
rows.sort()
print("deficit actual target slug  zeroCells low3")
for r in rows[:30]:
    print("%6d %5d %5d %-22s %-10s %s zero=%d %s low=%s" % (r[0], r[1], r[2], r[3], r[4] or "", r[5], r[6], r[7], r[8]))
print("---- 总量 ----")
print(pg["totals"])
