import json
from pathlib import Path

p = Path(r"D:\AI\project\marvis_project\caipu\data\ingredients.json")
d = json.loads(p.read_text(encoding="utf-8-sig"))
items = d["items"]

# (key, zh, en, aliases, allergens, category)
NEW = [
    ("carp", "鲤鱼", "carp", ["鲤"], ["fish"], "fish"),
    ("crucian-carp", "鲫鱼", "crucian carp", ["鲫"], ["fish"], "fish"),
    ("grass-carp", "草鱼", "grass carp", ["鲩鱼"], ["fish"], "fish"),
    ("eel", "黄鳝", "swamp eel", ["鳝鱼", "鳝丝", "鳝段"], ["fish"], "fish"),
    ("sea-cucumber", "海参", "sea cucumber", ["水发海参"], ["shellfish"], "seafood"),
    ("squid", "鱿鱼", "squid", ["鱿鱼须", "鲜鱿"], ["shellfish"], "seafood"),
    ("clam", "蛤蜊", "clam", ["花蛤", "文蛤"], ["shellfish"], "seafood"),
    ("scallop", "扇贝", "scallop", ["带子", "扇贝肉"], ["shellfish"], "seafood"),
    ("oyster", "生蚝", "oyster", ["牡蛎", "蚝"], ["shellfish"], "seafood"),
    ("beef", "牛肉", "beef", ["黄牛肉"], [], "meat"),
    ("chicken-breast", "鸡胸肉", "chicken breast", ["鸡胸", "鸡脯肉"], [], "poultry"),
    ("chicken-wing", "鸡翅", "chicken wings", ["翅中", "鸡中翅", "翅根"], [], "poultry"),
    ("duck", "鸭肉", "duck", ["老鸭", "仔鸭"], [], "poultry"),
    ("pork-loin", "猪里脊", "pork tenderloin", ["里脊肉", "猪柳"], [], "meat"),
    ("pork-mince", "猪肉末", "ground pork", ["肉末", "猪肉馅", "肉馅"], [], "meat"),
    ("beef-mince", "牛肉末", "ground beef", ["牛肉馅"], [], "meat"),
    ("tofu-skin", "豆腐皮", "tofu skin", ["千张", "油豆皮", "百叶"], ["soy"], "soy"),
    ("dried-tofu", "豆干", "dried firm tofu", ["香干", "白干", "豆腐干"], ["soy"], "soy"),
    ("rice-cake", "年糕", "rice cake", ["韩式年糕", "水磨年糕"], [], "grain"),
    ("glutinous-rice", "糯米", "glutinous rice", ["江米"], [], "grain"),
    ("rice", "大米", "white rice", ["香米", "粳米"], [], "grain"),
    ("wheat-flour", "中筋面粉", "all-purpose flour", ["面粉", "普通面粉"], ["gluten"], "grain"),
    ("bread-flour", "高筋面粉", "bread flour", ["高粉", "面包粉"], ["gluten"], "grain"),
    ("noodle", "鲜面条", "fresh wheat noodles", ["面条", "手擀面", "挂面"], ["gluten"], "grain"),
    ("rice-noodle", "米粉", "rice noodles", ["米线", "河粉"], [], "grain"),
    ("dried-shrimp", "虾米", "dried shrimp", ["海米", "开洋"], ["shellfish"], "seafood"),
    ("nori", "紫菜", "nori", ["海苔", "烤紫菜"], [], "vegetable"),
    ("sake", "清酒", "sake", ["日本清酒"], [], "seasoning"),
    ("mirin", "味淋", "mirin", ["味醂"], [], "seasoning"),
    ("miso", "味噌", "miso", ["白味噌", "赤味噌", "日式大酱"], ["soy"], "seasoning"),
    ("gochujang", "韩式辣酱", "gochujang", ["苦椒酱"], ["soy", "gluten"], "seasoning"),
    ("kimchi", "韩式泡菜", "kimchi", ["辣白菜"], ["fish", "shellfish"], "fermented"),
    ("fish-sauce", "鱼露", "fish sauce", ["鱼酱油"], ["fish"], "seasoning"),
    ("coconut-milk", "椰浆", "coconut milk", ["椰奶", "浓椰浆"], [], "seasoning"),
    ("lemongrass", "香茅", "lemongrass", ["柠檬草", "香茅草"], [], "vegetable"),
    ("galangal", "南姜", "galangal", ["高良姜"], [], "vegetable"),
    ("lime", "青柠", "lime", ["青柠檬"], [], "fruit"),
    ("curry-powder", "咖喱粉", "curry powder", ["黄咖喱粉"], [], "seasoning"),
    ("garam-masala", "印度综合香料", "garam masala", ["葛拉姆马萨拉"], [], "seasoning"),
    ("turmeric", "姜黄", "turmeric", ["姜黄粉"], [], "seasoning"),
    ("cumin", "孜然", "cumin", ["孜然粉", "孜然粒"], [], "seasoning"),
    ("olive-oil", "橄榄油", "olive oil", ["初榨橄榄油", "特级初榨橄榄油"], [], "oil"),
    ("butter", "黄油", "butter", ["无盐黄油", "发酵黄油"], ["milk"], "dairy"),
    ("parmesan", "帕玛森奶酪", "Parmesan", ["帕尔玛干酪", "巴马干酪"], ["milk"], "dairy"),
    ("mozzarella", "马苏里拉奶酪", "mozzarella", ["披萨芝士", "水牛芝士"], ["milk"], "dairy"),
    ("milk", "牛奶", "milk", ["全脂牛奶", "鲜奶"], ["milk"], "dairy"),
    ("cream", "淡奶油", "heavy cream", ["鲜奶油", "动物性淡奶油"], ["milk"], "dairy"),
    ("yeast", "干酵母", "instant yeast", ["酵母", "酵母粉"], [], "baking"),
    ("tomato-paste", "番茄膏", "tomato paste", ["番茄浓缩酱"], [], "vegetable"),
    ("canned-tomato", "罐装番茄", "canned tomatoes", ["去皮番茄罐头", "番茄罐头"], [], "vegetable"),
    ("chickpea", "鹰嘴豆", "chickpeas", ["鸡心豆"], [], "legume"),
    ("lentil", "小扁豆", "lentils", ["兵豆", "红扁豆"], [], "legume"),
    ("cornmeal", "玉米面", "cornmeal", ["玉米粉", "棒子面"], [], "grain"),
    ("tortilla", "玉米饼", "corn tortilla", ["墨西哥玉米饼", "玉米薄饼"], [], "grain"),
    ("avocado", "牛油果", "avocado", ["鳄梨"], [], "fruit"),
    ("basil", "罗勒", "basil", ["九层塔", "甜罗勒"], [], "herb"),
    ("parsley", "欧芹", "parsley", ["法香", "洋香菜"], [], "herb"),
    ("thyme", "百里香", "thyme", ["百里香叶"], [], "herb"),
    ("bay-leaf", "香叶", "bay leaf", ["月桂叶"], [], "herb"),
    ("paprika", "红椒粉", "paprika", ["甜椒粉"], [], "seasoning"),
    ("chili-flakes", "辣椒碎", "chili flakes", ["辣椒面", "干辣椒碎"], [], "seasoning"),
    ("honey", "蜂蜜", "honey", ["洋槐蜜"], [], "seasoning"),
    ("cocoa", "可可粉", "cocoa powder", ["无糖可可粉"], [], "baking"),
    ("dark-chocolate", "黑巧克力", "dark chocolate", ["苦甜巧克力", "黑巧"], ["milk"], "baking"),
    ("gelatin", "吉利丁", "gelatin", ["明胶片", "吉利丁片"], [], "baking"),
    ("bacon", "培根", "bacon", ["烟肉", "培根片"], [], "meat"),
    ("sausage", "香肠", "sausage", ["腊肠", "香肠片"], [], "meat"),
    ("ham", "火腿", "ham", ["火腿片", "金华火腿"], [], "meat"),
]

alias_owner = {}
for it in items:
    for a in [it["zh"]] + it.get("aliases", []):
        alias_owner[a] = it["key"]

existing_keys = {it["key"] for it in items}
added, skipped = 0, []
for key, zh, en, aliases, allergens, cat in NEW:
    if key in existing_keys:
        skipped.append(f"{key}(exists)")
        continue
    if zh in alias_owner:
        skipped.append(f"{zh}(name taken by {alias_owner[zh]})")
        continue
    keep = []
    for a in aliases:
        if a in alias_owner:
            skipped.append(f"{key}:{a}(taken by {alias_owner[a]})")
            continue
        keep.append(a)
    items.append({"key": key, "zh": zh, "en": en, "aliases": keep, "allergens": allergens, "category": cat})
    alias_owner[zh] = key
    for a in keep:
        alias_owner[a] = key
    existing_keys.add(key)
    added += 1

# 剁椒 作为 泡椒 的别名（川湘通用叫法）
for it in items:
    if it["key"] == "pickled-chili" and "剁椒" not in it["aliases"]:
        if "剁椒" not in alias_owner:
            it["aliases"].append("剁椒")
            alias_owner["剁椒"] = "pickled-chili"

d["note"] = d.get("note", "") 
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("added:", added, "total:", len(items))
print("skipped:", skipped)
