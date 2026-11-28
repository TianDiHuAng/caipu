# -*- coding: utf-8 -*-
import json, os
base = r"E:\ai_project\marvis_project\caipu\data\recipes\intl\french"
d = json.load(open(os.path.join(base, "french-fougasse.json"), encoding="utf-8"))
print("ING_ITEM_KEYS", list(d["ingredients"][2]["items"][0].keys()))
print("SUB", json.dumps(d["substitutions"][0], ensure_ascii=False))
print("TIP", json.dumps(d["tips"][0], ensure_ascii=False))
print("STEP_KEYS", list(d["steps"][0].keys()))
