# -*- coding: utf-8 -*-
import json, glob, io, os, sys, traceback
os.chdir(r"E:\ai_project\marvis_project\caipu")
out=[]
try:
    fs=sorted(glob.glob("data/recipes/cn/dongbei/*.json"))
    out.append("count=%d"%len(fs))
    for f in fs:
        o=json.load(io.open(f,encoding="utf-8"))
        out.append("%s | %s | %s"%(o["id"],o["zh"],",".join(o.get("category",[]))))
except Exception:
    out.append(traceback.format_exc())
io.open("temp/ls_db.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
