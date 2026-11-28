# -*- coding: utf-8 -*-
import json
base = r"E:\ai_project\marvis_project\caipu\data\recipes\intl\japanese"
def L(i): return json.load(open(base + "\\" + i + ".json", encoding="utf-8"))
def W(i, d): json.dump(d, open(base + "\\" + i + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

d = L("japanese-ganmodoki")
d["variations"][0] = "拌料里加一把煮熟切碎的毛豆，颜色更鲜绿，口感也更扎实。"
W("japanese-ganmodoki", d)

d = L("japanese-chakin-shibori")
d["diet_tags"] = []
W("japanese-chakin-shibori", d)

d = L("japanese-nabeyaki-udon")
d["steps"][1]["text"] = "高汤加酱油、味淋、清酒与盐煮开，放入鸡腿肉小火煮六分钟。"
d["steps"][0]["visual_cue"] = "乌冬面分明不粘连，手感滑爽"
d["steps"][3]["visual_cue"] = "乌冬面在汤中舒展，砂锅边缘冒小泡"
d["steps"][3]["text"] = "把煮好的乌冬面放进砂锅，倒入汤汁与配料，中火加热到微沸。"
W("japanese-nabeyaki-udon", d)

d = L("japanese-manju")
d["related_ids"] = ["dorayaki", "japanese-ohagi", "japanese-castella"]
W("japanese-manju", d)
print("ok")
