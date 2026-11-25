# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
p="temp/drafts/batch-325.json"
d=json.load(io.open(p,encoding="utf-8")); m={r["id"]:r for r in d}
m["xibei-yangrou-fentang"]["tips"][1]="白胡椒别省，它是羊汤去膻的关键，起锅前再补撒一次，辛香更冲。"
json.dump(d, io.open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok")
