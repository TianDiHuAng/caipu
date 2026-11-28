# -*- coding: utf-8 -*-
import json, io, os
root = r"E:\ai_project\marvis_project\caipu"
p = json.load(io.open(os.path.join(root, "tasks", "progress.json"), encoding="utf-8"))
print(type(p), list(p.keys())[:10])
for k, v in p.items():
    if isinstance(v, list):
        print(k, len(v), json.dumps(v[0], ensure_ascii=False)[:400])
    elif isinstance(v, dict):
        print(k, "dict", json.dumps(v, ensure_ascii=False)[:400])
    else:
        print(k, v)
