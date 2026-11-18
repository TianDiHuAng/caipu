# -*- coding: utf-8 -*-
import json, os
base = r"D:\AI\project\marvis_project\caipu\data\recipes"
for rel, words in [(r"cn\jiangsu\shizitou.json", ["猪肉末"]),
                   (r"cn\sichuan\shuizhu-niurou.json", ["牛肉"])]:
    r = json.loads(open(os.path.join(base, rel), encoding="utf-8-sig").read())
    t = "\n".join([f'{s["text"]} {s.get("tip","")} {s.get("visual_cue","")}' for s in r["steps"]])
    print("==", r["id"], "name:", r["name"]["zh"])
    for w in words:
        i = 0
        while True:
            j = t.find(w, i)
            if j < 0:
                break
            print("  ...", t[max(0, j - 25):j + 25].replace("\n", " / "))
            i = j + 1
