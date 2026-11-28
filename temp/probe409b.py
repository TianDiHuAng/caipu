# -*- coding: utf-8 -*-
import json, io
T = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(T + r"\tasks\progress.json", encoding="utf-8"))
tax = json.load(io.open(T + r"\data\taxonomy.json", encoding="utf-8"))
cu = [c for c in tax["cuisines"] if c["slug"] == "yunguai"][0]
print("core", cu.get("core"), "keys", list(cu.keys()))
def walk(node, path):
    if isinstance(node, dict):
        if "target" in node and "actual" in node:
            return [(path[-1], node["target"], node["actual"])] if path[-1] == "yunguai" or "yunguai" in path else []
        out = []
        for k, v in node.items():
            out += walk(v, path + [k])
        return out
    if isinstance(node, list):
        out = []
        for v in node:
            out += walk(v, path)
        return out
    return []

def find(node, path, want):
    if isinstance(node, dict):
        if "target" in node and "actual" in node:
            if path and path[-1] == want:
                yield node
            else:
                pass
            for k, v in node.items():
                if isinstance(v, dict) and "target" in v and "actual" in v:
                    pass
        for k, v in node.items():
            yield from find(v, path + [k], want)
    elif isinstance(node, list):
        for v in node:
            yield from find(v, path, want)

# 尝试常见结构：regions.cn.cuisines[].cells
txt = json.dumps(p, ensure_ascii=False)
i = txt.find("yunguai")
print(txt[max(0, i - 200):i + 900])
