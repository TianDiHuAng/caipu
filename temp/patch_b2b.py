# -*- coding: utf-8 -*-
import io
p = r"D:\AI\project\marvis_project\caipu\temp\batch2b.py"
s = io.open(p, encoding="utf-8").read()
n = s.count("羊腿肉")
s = s.replace("羊腿肉", "羊肉")
io.open(p, "w", encoding="utf-8").write(s)
print("replaced", n)
