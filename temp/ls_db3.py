# -*- coding: utf-8 -*-
import json, glob, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
out=[]
fs=sorted(glob.glob("data/recipes/cn/dongbei/*.json"))
out.append("count=%d"%len(fs))
for f in fs:
    o=json.load(io.open(f,encoding="utf-8"))
    out.append("%s | %s | %s"%(o["id"],o.get("title") or o.get("name"),",".join(o.get("category",[]))))
io.open("temp/ls_db.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
