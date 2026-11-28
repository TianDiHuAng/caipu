import json
p = json.load(open('tasks/progress.json', encoding='utf-8'))
print('keys', list(p['regions'][0].keys()))
g = p['regions'][0]
print(json.dumps(g, ensure_ascii=False)[:500])
