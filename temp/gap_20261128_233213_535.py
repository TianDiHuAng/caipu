import json, io
p = json.load(open('tasks/progress.json', encoding='utf-8'))
lines = []
regs = p['regions']
lines.append('regions type: %s' % type(regs).__name__)
items = regs.items() if isinstance(regs, dict) else [(str(i), r) for i, r in enumerate(regs)]
rows = []
for rid, reg in items:
    if not isinstance(reg, dict):
        continue
    cs = reg.get('cuisines') or reg.get('items') or []
    if isinstance(cs, dict):
        cs = list(cs.values())
    for c in cs:
        a = c.get('actual', 0)
        t = c.get('target', 0)
        if a < t:
            rows.append((c.get('slug', '?'), a, t))
rows.sort(key=lambda x: x[1] - x[2])
lines.append('gap=%d n=%d' % (sum(t - a for _, a, t in rows), len(rows)))
for s, a, t in rows[:12]:
    lines.append('%s / %d / %d' % (s, a, t))
open('temp/gap.txt', 'w', encoding='utf-8').write('\n'.join(lines))
