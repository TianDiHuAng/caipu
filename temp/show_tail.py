# -*- coding: utf-8 -*-
import json, io, os
os.chdir(r"E:\ai_project\marvis_project\caipu")
o=json.load(io.open("temp/drafts/batch-325.json",encoding="utf-8"))[0]
tail={k:o[k] for k in o if k not in ("steps","ingredients")}
print(json.dumps(tail,ensure_ascii=False,indent=1))
