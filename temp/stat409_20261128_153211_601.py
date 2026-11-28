# -*- coding: utf-8 -*-
import json, io, collections
T = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(T + r"\tasks\progress.json", encoding="utf-8"))
print(p["totals"])
gap = collections.Counter()
det = collections.defaultdict(list)
def walk(node, path):
    if isinstance(node, dict):
        if "target" in node and "actual" in node:
            slug = node.get("slug") or path[-1]
            t, a = node["target"], node["actual"]
            gap[slug] += t - a
            if t - a > 0:
                det[slug].append((path[-1], t, a))
            return
        for k, v in node.items():
            walk(v, path + [k])
    elif isinstance(node, list):
        for v in node:
            walk(v, path)
walk(p["regions"], [])
for slug, g in gap.most_common(12):
    print(slug, g, det[slug][:8])
