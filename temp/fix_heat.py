# -*- coding: utf-8 -*-
import json, os
BASE = r"D:\AI\project\marvis_project\caipu\data\recipes"
MAP = {"jiuzhuan-dachang": {"无火，手工处理": "无火", "大火烧开转中火": "中火", "大火烧开转小火": "小火", "大火收汁": "大火"},
       "fuqi-feipian": {"大火烧开转中火": "中火", "小火，水面只冒小泡": "小火", "无火，冷藏定型": "无火", "小火焙香": "小火"}}
for rel_id, m in MAP.items():
    for root, _, files in os.walk(BASE):
        if rel_id + ".json" in files:
            p = os.path.join(root, rel_id + ".json")
            r = json.loads(open(p, encoding="utf-8-sig").read())
            for s in r["steps"]:
                if s["heat"] in m:
                    s["heat"] = m[s["heat"]]
            json.dump(r, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print("fixed", p)
