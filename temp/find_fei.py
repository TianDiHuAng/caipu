# -*- coding: utf-8 -*-
import json, os
BASE = r"D:\AI\project\marvis_project\caipu\data\recipes"
p = None
for root, _, files in os.walk(BASE):
    if "fuqi-feipian.json" in files:
        p = os.path.join(root, "fuqi-feipian.json")
t = open(p, encoding="utf-8-sig").read()
i = t.find("肥牛")
print("idx", i)
if i >= 0:
    print(repr(t[max(0, i-120):i+80]))
