# -*- coding: utf-8 -*-
import io
p = r"D:\AI\project\marvis_project\caipu\temp\batch2b.py"
s = io.open(p, encoding="utf-8").read()
n = s.count("猪肋排")
s = s.replace("猪肋排", "猪排骨")
io.open(p, "w", encoding="utf-8").write(s)
print("replaced 猪肋排 ->猪排骨:", n)
