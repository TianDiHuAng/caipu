# -*- coding: utf-8 -*-
import json, os, re, sys
from datetime import date

repo = r"E:\ai_project\marvis_project\caipu"
draft = sys.argv[1] if len(sys.argv) > 1 else os.path.join(repo, "temp", "drafts", "batch-390.json")
if not os.path.isabs(draft):
    draft = os.path.join(repo, draft)

tax = json.load(open(os.path.join(repo, "data", "taxonomy.json"), encoding="utf-8-sig"))
cuis = {c["slug"]: c for c in tax["cuisines"]}
dic = json.load(open(os.path.join(repo, "data", "ingredients.json"), encoding="utf-8-sig"))
idx = {}
for it in dic["items"]:
    idx.setdefault(it["zh"], it)
    for a in it.get("aliases") or []:
        idx.setdefault(a, it)

DISCLAIMER = "按配料表用量与常见食材成分表推算，实际数值随品牌与烹饪损耗浮动。"
today = str(date.today())

def fmt_amount(v):
    if isinstance(v, float) and v == int(v):
        v = int(v)
    return v

def fmt_ratio(s):
    m = re.match(r"^\s*([\d.]+)\s*(\S*?)\s*:\s*([\d.]+)\s*(\S*)\s*$", s)
    if not m:
        return s
    a, ua, b, ub = m.groups()
    return f"{a} {ua}:{b} {ub}"

def build(r):
    cuisine = cuis.get(r["cuisine"])
    if not cuisine:
        raise SystemExit("菜系不存在: " + r["cuisine"])
    region = cuisine["region"]
    groups, allergens = [], set()
    for g in r["ingredients"]:
        items = []
        for it in g["items"]:
            e = idx.get(it["n"])
            if not e:
                raise SystemExit(f'{r["id"]}: 食材未登记 {it["n"]}')
            for al in e.get("allergens") or []:
                allergens.add(al)
            items.append({"name": e["zh"], "name_en": e["en"],
                          "amount": fmt_amount(it["a"]), "unit": it["u"],
                          "note": it["note"], "optional": False})
        groups.append({"group": g["group"], "items": items})

    name = {"zh": r["zh"], "en": r["en"]}
    if r.get("original"):
        name["original"] = r["original"]

    rec = {
        "schema_version": "1.0", "content_version": 1, "id": r["id"], "name": name,
        "cuisine": {"region": region, "style": r["cuisine"]},
        "category": r["category"], "difficulty": r["difficulty"],
        "time": {"prep_min": r["prep"], "cook_min": r["cook"], "total_min": r["prep"] + r["cook"]},
        "servings": r["servings"], "flavor": r["flavor"], "ingredients": groups,
        "equipment": r["equipment"],
        "steps": [{"n": i + 1, "text": s["t"], "time_min": s["time"], "heat": s["heat"],
                   "tip": s["tip"], "visual_cue": s["cue"]} for i, s in enumerate(r["steps"])],
        "tips": r["tips"], "common_mistakes": r["mistakes"],
        "substitutions": [{"original": s["orig"], "substitute": s["sub"], "ratio": fmt_ratio(s["ratio"]),
                           "note": s["note"]} for s in r["subs"]],
        "variations": r["variations"], "serving_suggestion": r["serving"], "storage": r["storage"],
        "nutrition_estimate": {"basis": r["nutrition"]["basis"], "calories_kcal": r["nutrition"]["kcal"],
                               "protein_g": r["nutrition"]["protein"], "fat_g": r["nutrition"]["fat"],
                               "carbs_g": r["nutrition"]["carbs"], "sodium_mg": r["nutrition"]["sodium"],
                               "is_estimate": True, "disclaimer": DISCLAIMER},
        "allergens": sorted(allergens), "diet_tags": r["diet"],
        "food_safety_notes": r["safety"], "origin_note": r["origin"], "tags": r["tags"],
        "related_ids": r["related"], "image_url": None, "image_credit": None,
        "status": "published", "created_at": today, "updated_at": today,
    }
    return os.path.join("data", "recipes", region, r["cuisine"], r["id"] + ".json"), rec

drafts = json.load(open(draft, encoding="utf-8"))
written = []
for r in drafts:
    rel, rec = build(r)
    abs_p = os.path.join(repo, rel)
    if os.path.exists(abs_p) and not r.get("overwrite"):
        print("SKIP exists:", r["id"])
        continue
    os.makedirs(os.path.dirname(abs_p), exist_ok=True)
    with open(abs_p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False, indent=2) + "\n")
    written.append(rel.replace("\\", "/"))
print(json.dumps({"drafts": len(drafts), "written": len(written)}, ensure_ascii=False))
