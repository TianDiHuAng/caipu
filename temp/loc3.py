# -*- coding: utf-8 -*-
import json, os
base = r"D:\AI\project\marvis_project\caipu\data\recipes"

def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + "[" + str(i) + "]")
    else:
        yield path, o

for rel, words in [(r"cn\jiangsu\shizitou.json", ["肉末"]),
                   (r"cn\sichuan\shuizhu-niurou.json", ["牛肉"])]:
    r = json.loads(open(os.path.join(base, rel), encoding="utf-8-sig").read())
    print("==", r["id"])
    for path, v in walk(r):
        if isinstance(v, str):
            for w in words:
                if w in v:
                    print("  ", path, "::", v[:120])
