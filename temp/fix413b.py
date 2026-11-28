# -*- coding: utf-8 -*-
import json, traceback

ids = ['french-nouilles-creme-champignons','french-tagliatelle-provencale','french-tofu-champignons',
       'french-sauce-beurre-blanc','french-tofu-basquaise','french-sauce-provencale',
       'french-omelette-fromage','french-soupe-carottes']

def fix(s):
    if not isinstance(s, str):
        return s
    return (s.replace('生粉味', '生面腥味')
             .replace('面条', '意大利面')
             .replace('面汤里的淀粉', '面汤里的糊化物质'))

for i in ids:
    p = f'data/recipes/intl/french/{i}.json'
    try:
        d = json.load(open(p, encoding='utf-8'))
        for g in d.get('ingredients', []):
            for it in g.get('items', []):
                if it.get('name') == '面粉':
                    it['name'] = '中筋面粉'
        for s in d.get('steps', []):
            for k in ('text', 'tip', 'visual_cue'):
                if k in s:
                    s[k] = fix(s[k])
        for k in ('tips', 'common_mistakes', 'food_safety_notes', 'variations'):
            if isinstance(d.get(k), list):
                d[k] = [fix(t) for t in d[k]]
        for k in ('serving_suggestion', 'storage', 'origin_note'):
            if isinstance(d.get(k), str):
                d[k] = fix(d[k])
        for sub in d.get('substitutions', []) or []:
            if isinstance(sub, dict):
                for kk in list(sub.keys()):
                    sub[kk] = fix(sub[kk])
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print('done', i)
    except Exception as e:
        print('ERR', i, repr(e))
