# -*- coding: utf-8 -*-
import json, io, traceback
try:
    p = r"E:\ai_project\marvis_project\caipu\tasks\progress.json"
    d = json.load(io.open(p, encoding="utf-8"))
    lines = ["totals: " + json.dumps(d["totals"], ensure_ascii=False)]
    lines.append("region type: " + str(type(d["regions"]).__name__))
    rows = []
    def walk(node):
        if isinstance(node, dict):
            if "slug" in node and "target" in node and "actual" in node:
                rows.append((node["target"] - node["actual"], node["slug"], node["actual"], node["target"]))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(d["regions"])
    rows.sort(reverse=True)
    lines.append("cuisines: " + str(len(rows)))
    for x in rows[:14]:
        lines.append(str(x))
except Exception:
    lines = [traceback.format_exc()]
io.open(r"E:\ai_project\marvis_project\caipu\temp\stat407.txt", "w", encoding="utf-8").write("\n".join(lines))
