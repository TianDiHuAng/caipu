# -*- coding: utf-8 -*-
import json, io, sys, traceback
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
try:
    p = json.load(open(r'E:\ai_project\marvis_project\caipu\tasks\progress.json', encoding='utf-8'))
    regs = p['regions']
    print('type regions', type(regs))
    print(json.dumps(regs, ensure_ascii=False)[:600])
    rows = []
    def walk(c):
        if isinstance(c, dict):
            t = c.get('actual', 0); g = c.get('target', 0)
            if isinstance(g, int) and isinstance(t, int) and g and t < g:
                rows.append((g - t, c.get('slug') or c.get('name'), t, g))
            for v in c.values():
                walk(v)
        elif isinstance(c, list):
            for v in c:
                walk(v)
    walk(regs)
    rows.sort(reverse=True)
    print('GAPS')
    for x in rows[:16]:
        print(x)
except Exception:
    traceback.print_exc()
