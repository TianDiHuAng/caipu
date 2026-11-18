import json
from pathlib import Path

root = Path(r"D:\AI\project\marvis_project\caipu")

# 1) 撤销给大葱加的与「小葱」冲突的别名（葱白/葱段属于 scallion）
p = root / "data" / "ingredients.json"
d = json.loads(p.read_text(encoding="utf-8-sig"))
for it in d["items"]:
    if it["key"] == "welsh-onion":
        it["aliases"] = [a for a in it["aliases"] if a not in ("葱白", "葱段")]
        if "葱丝" not in it["aliases"]:
            it["aliases"].append("葱丝")
        print("welsh-onion aliases:", it["aliases"])
p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def rename_in_steps(recipe, mapping):
    """只在 steps 的 text/tip/visual_cue 中做有序替换，避免重复替换"""
    for s in recipe.get("steps", []):
        for f in ("text", "tip", "visual_cue"):
            t = s.get(f)
            if not isinstance(t, str):
                continue
            for k, v in mapping:
                t = t.replace(k, v)
            s[f] = t


# 2) 麻婆豆腐：豆腐 → 嫩豆腐，肉末 → 牛肉末（保证词典唯一命中）
mp = root / "data" / "recipes" / "cn" / "sichuan" / "mapo-doufu.json"
r = json.loads(mp.read_text(encoding="utf-8-sig"))
rename_in_steps(r, [("嫩豆腐", "\u0001"), ("豆腐", "嫩豆腐"), ("\u0001", "嫩豆腐"),
                    ("牛肉末", "\u0002"), ("肉末", "牛肉末"), ("\u0002", "牛肉末")])
mp.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")

# 3) 宫保鸡丁 / 鱼香肉丝：葱白丁、葱白丝 → 大葱丁、大葱丝
for name in ("gongbao-jiding", "yuxiang-rousi"):
    fp = root / "data" / "recipes" / "cn" / "sichuan" / f"{name}.json"
    rr = json.loads(fp.read_text(encoding="utf-8-sig"))
    rename_in_steps(rr, [("葱白", "大葱")])
    fp.write_text(json.dumps(rr, ensure_ascii=False, indent=2), encoding="utf-8")

print("done")
