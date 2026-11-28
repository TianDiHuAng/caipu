import json
p = json.load(open('tasks/progress.json', encoding='utf-8'))
regs = p['regions']
k = list(regs.keys())[0]
v = regs[k]
open('temp/reg1.txt', 'w', encoding='utf-8').write(json.dumps({k: v}, ensure_ascii=False)[:1500])
