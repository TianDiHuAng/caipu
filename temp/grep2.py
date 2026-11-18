from pathlib import Path
import re

root = Path(r"D:\AI\project\marvis_project\caipu") / "apps" / "api" / "src"
for f in sorted(root.rglob("*.ts")):
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if "getDb(" in line or "sqlite" in line or "buildApp" in line or "db:" in line:
            print(f"{f.relative_to(root)}:{i}: {line.strip()[:150]}")
