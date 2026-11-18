import re

p = r"D:\AI\project\marvis_project\caipu\scripts\lib\rules.mjs"
s = open(p, encoding="utf-8").read()
i = s.index("R4 ")
j = s.index("R5 ", i)
print(s[max(0, i - 60):j + 20])
print("---- total len:", len(s))
