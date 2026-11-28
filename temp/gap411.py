# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(os.path.join(root, "tasks", "progress.json"), encoding="utf-8"))
rows = []
for c in p.get("cuisines", []):
    name = c.get("name") or c.get("zh") or c.get("slug")
    slug = c.get("slug")
    done = c.get("done", 0)
    target = c.get("target", 0)
    gap = target - done
    rows.append((gap, slug, name, done, target))
rows.sort(reverse=True)
for r in rows[:12]:
    print(r)
print("---- total", p.get("summary"))
