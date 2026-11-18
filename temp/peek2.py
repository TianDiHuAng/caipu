from pathlib import Path
import re

root = Path(r"D:\AI\project\marvis_project\caipu")
for f in ["scripts/validate.mjs", "scripts/lib/rules.mjs"]:
    s = (root / f).read_text(encoding="utf-8")
    print("=====", f)
    for m in re.finditer(r"matchIngredients\([^)]*\)", s):
        print("  ", m.group(0))
    for m in re.finditer(r"^import .*$", s, re.M):
        print("  IMP", m.group(0))
