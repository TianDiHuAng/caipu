# -*- coding: utf-8 -*-
import json, io, collections
T = r"E:\ai_project\marvis_project\caipu"
prog = json.load(io.open(T + r"\tasks\progress.json", encoding="utf-8"))
rows = prog.get("cuisines") or prog.get("rows") or []
print(type(prog), list(prog.keys())[:8])
gap = collections.Counter()
detail = collections.defaultdict(list)
def walk(o):
    if isinstance(o, dict):
        if "target" in o and "actual" in o:
            name = o.get("slug") or o.get("cuisine") or o.get("id") or o.get("name")
            vals = o
        for v in o.values(): walk(v)
walk(prog)
