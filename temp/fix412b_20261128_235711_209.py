# -*- coding: utf-8 -*-
import json, os
B = r"E:\ai_project\marvis_project\caipu\data\recipes\intl\thai"
def load(i): return json.load(open(os.path.join(B, i + ".json"), encoding="utf-8"))
def save(i, d): json.dump(d, open(os.path.join(B, i + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

d = load("thai-pad-pak-ruam")
d["diet_tags"] = [t for t in d["diet_tags"] if t != "gluten-free"]
save("thai-pad-pak-ruam", d)

d = load("thai-tao-hu-neung")
for s in d["steps"]:
    s["text"] = s["text"].replace("姜末", "南姜末").replace("姜香", "南姜香")
save("thai-tao-hu-neung", d)

d = load("thai-tom-kha-goong")
d["steps"][7]["visual_cue"] = "汤面浮着辣椒圈与翠绿香菜"
save("thai-tom-kha-goong", d)
print("ok")
