import json, os, sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT = json.load(open(os.path.join(ROOT, 'data', 'ingredients.json'), encoding='utf-8'))
TAX = json.load(open(os.path.join(ROOT, 'data', 'taxonomy.json'), encoding='utf-8'))
BY_NAME = {}
for it in DICT['items']:
    BY_NAME.setdefault(it['zh'], it)
    for a in it.get('aliases') or []:
        BY_NAME.setdefault(a, it)
CUISINE = {c['slug']: c for c in TAX['cuisines']}
GROUP = {'main': 'main', 'aux': 'aux', 'season': 'seasoning'}

MEAT = ['五花肉','猪里脊','猪肩肉','猪蹄','猪排骨','猪肝','猪大肠','猪肉末','牛里脊','牛腩','牛腱','肥牛','牛肉末',
        '羊肉','羊排','鸡胸肉','鸡腿肉','整鸡','鸡翅','鸡爪','鸭','鸭胸','培根','火腿','腊肉','腊肠','牛肉','咸肉','牛肚']
SEA = ['鲈鱼','草鱼','鲫鱼','带鱼','三文鱼','鳕鱼','金枪鱼','虾','虾仁','虾米','蟹','蛤蜊','牡蛎','扇贝','鱿鱼','章鱼',
       '青口','咸鱼','干贝','紫菜','海带','鲤鱼','黄鳝','海参','鳜鱼','河虾仁','海藻']
DAIRY = ['牛奶','淡奶油','黄油','酸奶','奶酪','帕玛森芝士','马苏里拉','炼乳','酥油']
EGG = ['鸡蛋','蛋黄','蛋清','鸭蛋','咸蛋黄','皮蛋']
FISHBASE = ['鱼露','虾酱','蚝油','高汤']
NUT = ['花生','核桃','腰果','杏仁','松子','芝麻酱','花生酱']

def checks(d):
    p = []
    if d['cuisine'] not in CUISINE:
        p.append('%s: 菜系不存在' % d['id'])
    if len(d['steps']) < 4:
        p.append('%s: 步骤不足 4 步' % d['id'])
    for i, s in enumerate(d['steps'], 1):
        if len(s[0]) < 12: p.append('%s: 步骤 %d 文本过短' % (d['id'], i))
        if len(s[4]) < 8: p.append('%s: 步骤 %d cue 过短' % (d['id'], i))
        if len(s[3]) < 6: p.append('%s: 步骤 %d tip 过短' % (d['id'], i))
        if '适量' in s[0]: p.append('%s: 步骤 %d 含适量' % (d['id'], i))
    if len(d.get('tips', [])) < 2: p.append('%s: tips 不足' % d['id'])
    if len(d.get('mistakes', [])) < 1: p.append('%s: mistakes 不足' % d['id'])
    return p

def build(d):
    problems = checks(d)
    names, allergens, groups = set(), set(), []
    for gkey, items in d['ing']:
        rows = []
        for item in items:
            nm, amount, unit, note = item[0], item[1], item[2], item[3]
            entry = BY_NAME.get(nm)
            if not entry:
                problems.append('%s: 食材未登记 → %s' % (d['id'], nm))
                continue
            names.add(entry['zh'])
            for a in entry.get('allergens') or []:
                allergens.add(a)
            row = {'name': entry['zh'], 'name_en': entry['en'], 'amount': amount, 'unit': unit,
                   'note': note, 'optional': False}
            if len(item) > 4 and item[4]:
                row['substitute'] = item[4]
            rows.append(row)
        groups.append({'group': GROUP[gkey], 'items': rows})
    if problems:
        return None, problems

    def has(lst):
        return any(n in lst for n in names)

    has_meat = has(MEAT)
    has_sea = has(SEA)
    animal = has_meat or has_sea or has(FISHBASE) or has(EGG) or has(DAIRY)
    diet = []
    if not animal:
        diet.append('vegetarian')
        if not has(EGG) and not has(DAIRY) and '蜂蜜' not in names:
            diet.append('vegan')
    elif has_sea and not has_meat and not has(EGG) and not has(DAIRY):
        diet.append('pescatarian')
    if not has(DAIRY):
        diet.append('dairy-free')
    if 'gluten' not in allergens:
        diet.append('gluten-free')

    region = CUISINE[d['cuisine']]['region']
    basis, kcal, prot, fat, carbs, sodium, disc = d['nutrition']
    name = {'zh': d['zh'], 'en': d['en']}
    if d.get('original'):
        name['original'] = d['original']
    recipe = {
        'schema_version': '1.0', 'content_version': 1, 'id': d['id'],
        'name': name,
        'cuisine': {'region': region, 'style': d['cuisine']},
        'category': d['category'], 'difficulty': d['difficulty'],
        'time': {'prep_min': d['prep'], 'cook_min': d['cook'], 'total_min': d['prep'] + d['cook']},
        'servings': d['servings'], 'flavor': d['flavor'], 'ingredients': groups,
        'equipment': d['equip'],
        'steps': [{'n': i + 1, 'text': s[0], 'time_min': s[1], 'heat': s[2], 'tip': s[3], 'visual_cue': s[4]}
                  for i, s in enumerate(d['steps'])],
        'tips': d['tips'], 'common_mistakes': d['mistakes'],
        'substitutions': [{'original': s[0], 'substitute': s[1], 'ratio': s[2], 'note': s[3]} for s in d['subs']],
        'variations': d['variations'], 'serving_suggestion': d['serving'], 'storage': d['storage'],
        'nutrition_estimate': {'basis': basis, 'calories_kcal': kcal, 'protein_g': prot, 'fat_g': fat,
                               'carbs_g': carbs, 'sodium_mg': sodium, 'is_estimate': True, 'disclaimer': disc},
        'allergens': sorted(allergens), 'diet_tags': diet,
        'food_safety_notes': d['safety'], 'origin_note': d['origin'], 'tags': d['tags'],
        'related_ids': d['related'], 'image_url': None, 'image_credit': None,
        'status': 'published', 'created_at': str(date.today()), 'updated_at': str(date.today())
    }
    rel = os.path.join('data', 'recipes', region, d['cuisine'], d['id'] + '.json')
    return rel, recipe

def main():
    drafts = json.load(open(sys.argv[1], encoding='utf-8'))
    dry = '--dry' in sys.argv
    written, problems = [], []
    for d in drafts:
        rel, res = build(d)
        if rel is None:
            problems += res
            continue
        abs_path = os.path.join(ROOT, rel)
        if os.path.exists(abs_path) and not d.get('overwrite'):
            problems.append('%s: 已存在' % d['id'])
            continue
        if not dry:
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(res, ensure_ascii=False, indent=2) + '\n')
        written.append(rel.replace('\\', '/'))
    print(json.dumps({'drafts': len(drafts), 'written': len(written), 'files': written, 'problems': problems},
                     ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
