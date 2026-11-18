import json
from pathlib import Path
ROOT = Path(r"D:\AI\project\marvis_project\caipu")
edits = {
    "data/recipes/cn/cantonese/baiqie-ji.json": [("从鸡腿最厚处插入到底", "从腿根最厚处插入到底")],
    "data/recipes/cn/zhejiang/dongpo-rou.json": [("表层蛋白质瞬间凝固", "表层肌纤维瞬间凝固")],
}
for rel, pairs in edits.items():
    p = ROOT / rel
    raw = p.read_text(encoding="utf-8")
    doc = json.loads(raw.lstrip("\ufeff"))
    n = 0
    for s in doc["steps"]:
        for k in ("text", "tip", "visual_cue"):
            for a, b in pairs:
                if a in s[k]:
                    s[k] = s[k].replace(a, b)
                    n += 1
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(rel, "替换", n, "处")
