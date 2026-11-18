import json
from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\tasks\engineering.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))

done_ids = [f"P1-{i:02d}" for i in range(1, 17)]
seen = set()
for ph in d["phases"]:
    for it in ph["items"]:
        if it["id"] in done_ids:
            it["done"] = True
            seen.add(it["id"])

# 阶段 1 追加两项验收任务
p1 = next(ph for ph in d["phases"] if ph["id"] == "P1")
if not any(it["id"] == "P1-17" for it in p1["items"]):
    p1["items"].append({"id": "P1-17", "title": "验收：npm test 26/26 与 scripts/smoke.mjs 17/17 全通过，记录 STAGE_REPORT.md", "done": True})
    p1["items"].append({"id": "P1-18", "title": "验收：init + import 幂等重建数据库，health 计数正确", "done": True})

p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
print("marked:", sorted(seen))
