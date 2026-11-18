# -*- coding: utf-8 -*-
import json, os
base = r"D:\AI\project\marvis_project\caipu\data\recipes"
for rel, words in [(r"cn\jiangsu\shizitou.json", ["猪肉末", "肉末"]),
                   (r"cn\sichuan\shuizhu-niurou.json", ["牛肉"])]:
    r = json.loads(open(os.path.join(base, rel), encoding="utf-8-sig").read())
    print("==", r["id"])
    for s in r["steps"]:
        for w in words:
            if w in s["text"]:
                print("  step", s["n"], "::", s["text"][:160])
