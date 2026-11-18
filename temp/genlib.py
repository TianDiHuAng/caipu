# -*- coding: utf-8 -*-
"""共用生成库：auto allergens + 落盘 + 进度统计"""
import json
from pathlib import Path

ROOT = Path(r"D:\AI\project\marvis_project\caipu")
_T = json.loads((ROOT / "data/taxonomy.json").read_text(encoding="utf-8-sig"))
_ITEMS = json.loads((ROOT / "data/ingredients.json").read_text(encoding="utf-8-sig"))["items"]

IDX = {}
for _it in _ITEMS:
    for _k in [_it["zh"]] + _it.get("aliases", []):
        IDX.setdefault(_k, []).append(_it)

CORE = {}
for c in _T["cuisines"]:
    CORE[c["slug"]] = c.get("core", [])


def allergens_of(names):
    out, unknown = [], []
    for n in names:
        hits = IDX.get(n) or []
        if not hits:
            unknown.append(n)
            continue
        for a in hits[0]["allergens"]:
            if a not in out:
                out.append(a)
    if unknown:
        raise SystemExit("食材未登记词典: " + ", ".join(unknown))
    return sorted(out)


def build(r, check_cat=True):
    groups, names = [], []
    for g in ("main", "aux", "seasoning"):
        rows = r["ingredients"].get(g) or []
        if not rows:
            continue
        items = []
        for row in rows:
            items.append({"name": row[0], "name_en": row[1], "amount": row[2],
                          "unit": row[3], "note": row[4],
                          "optional": row[5] if len(row) > 5 else False})
            names.append(row[0])
        groups.append({"group": g, "items": items})

    if check_cat:
        core = CORE.get(r["cuisine"]["style"], [])
        bad = [c for c in r["category"] if c not in core]
        if bad:
            raise SystemExit(f"{r['id']} 品类不在 {r['cuisine']['style']} core 内: {bad}")

    steps = [{"n": i, "text": s[0], "time_min": s[1], "heat": s[2], "tip": s[3], "visual_cue": s[4]}
             for i, s in enumerate(r["steps"], 1)]

    t = r["time"]
    if abs(t["prep_min"] + t["cook_min"] - t["total_min"]) > 5:
        raise SystemExit(f"{r['id']} time 不一致")

    doc = {
        "schema_version": "1.0", "content_version": 1,
        "id": r["id"], "name": r["name"], "cuisine": r["cuisine"],
        "category": r["category"], "difficulty": r["difficulty"], "time": t,
        "servings": r["servings"], "flavor": r["flavor"], "ingredients": groups,
        "equipment": r["equipment"], "steps": steps, "tips": r["tips"],
        "common_mistakes": r["common_mistakes"],
        "substitutions": [{"original": a, "substitute": b, "ratio": c, "note": d}
                          for a, b, c, d in r["substitutions"]],
        "variations": r["variations"],
        "serving_suggestion": r["serving_suggestion"], "storage": r["storage"],
        "nutrition_estimate": r["nutrition_estimate"],
        "allergens": allergens_of(names), "diet_tags": r.get("diet_tags", []),
        "food_safety_notes": r["food_safety_notes"], "origin_note": r["origin_note"],
        "tags": r["tags"], "related_ids": r["related_ids"],
        "image_url": None, "image_credit": None, "status": "published",
        "created_at": "2026-11-18", "updated_at": "2026-11-18",
    }
    out = ROOT / "data/recipes" / r["cuisine"]["region"] / r["cuisine"]["style"] / f"{r['id']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def write_all(recipes):
    for r in recipes:
        print(build(r))
