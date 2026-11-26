# -*- coding: utf-8 -*-
import json, glob, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
for f in sorted(glob.glob("data/recipes/cn/dongbei/*.json")):
    o=json.load(io.open(f,encoding="utf-8"))
    print(o["id"], o["zh"], ",".join(o.get("category",[])))
