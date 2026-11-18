import json
from pathlib import Path

ROOT = Path(r"D:\AI\project\marvis_project\caipu")
ITEMS = json.loads((ROOT / "data/ingredients.json").read_text(encoding="utf-8-sig"))["items"]
VOCAB = {}
for it in ITEMS:
    for k in [it["zh"]] + it.get("aliases", []):
        VOCAB.setdefault(k, it["zh"])

targets = ["cn/cantonese/baiqie-ji", "cn/sichuan/huiguo-rou", "cn/zhejiang/dongpo-rou"]
for t in targets:
    doc = json.loads((ROOT / "data/recipes" / (t + ".json")).read_text(encoding="utf-8-sig"))
    names = set()
    for g in doc["ingredients"]:
        for it in g["items"]:
            names.add(it["name"])
    print("==", t, "配料:", names)
    for s in doc["steps"]:
        blob = s["text"] + "｜" + s["tip"] + "｜" + s["visual_cue"]
        for w, zh in VOCAB.items():
            if w in blob and zh not in names and w not in names:
                i = blob.find(w)
                print(f"  步{s['n']} 命中「{w}」(标准名 {zh}) 上下文: ...{blob[max(0,i-12):i+12]}...")
