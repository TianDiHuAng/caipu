# -*- coding: utf-8 -*-
"""批次 5：沪/东北/西北 共 3 道"""
import sys
sys.path.insert(0, r"D:\AI\project\marvis_project\caipu\temp")
from genlib import IDX, build
R = []

R.append({
 "id": "sikai-kaofu",
 "name": {"zh": "四喜烤麸", "en": "Braised Wheat Gluten with Mushrooms and Daylily", "original": "四喜烤麸"},
 "cuisine": {"region": "cn", "style": "shanghai"},
 "category": ["appetizer"],
 "difficulty": 2,
 "time": {"prep_min": 20, "cook_min": 30, "total_min": 50},
 "servings": 4,
 "flavor": ["sweet", "salty", "umami", "fragrant"],
 "ingredients": {
  "main": [("烤麸", "wheat gluten puff", 400, "g", "选干烤麸，泡发后挤干水分撕成 3 厘米块", False)],
  "aux": [("香菇", "shiitake mushroom", 80, "g", "干香菇温水泡发，泡菇水留用", False),
          ("木耳", "wood ear mushroom", 40, "g", "泡发后撕小朵", False),
          ("黄花菜", "dried daylily", 30, "g", "泡发后掐去硬梗", False),
          ("花生米", "peanut", 50, "g", "生花生提前泡 2 小时", False)],
  "seasoning": [("生抽", "light soy sauce", 35, "ml", "提供咸鲜", False), ("冰糖", "rock sugar", 30, "g", "上海风味偏甜，可按口味减 5 克", False),
                ("香油", "sesame oil", 10, "ml", "出锅前淋入", False), ("菜籽油", "rapeseed oil", 120, "ml", "炸烤麸用，实耗约 40 毫升", False),
                ("盐", "salt", 3, "g", "最后调味", False)],
 },
 "equipment": ["炒锅", "漏勺", "厨房纸", "深碗"],
 "steps": [
  ("干烤麸用温水泡 40 分钟至完全软化，反复挤压换水三次去掉酸味，撕成不规则小块后用力挤干，越干越吸味。", 45, "无火", "烤麸内部蜂窝多，必须挤到捏不出水，否则下锅炸时爆油且不入味。", "烤麸由硬挺转为柔软海绵状、捏后不回弹，挤出的水基本清亮。"),
  ("锅中放 120 毫升菜籽油烧到六成热，下烤麸块中火炸 5 分钟至外壳金黄硬挺，捞出沥油并用厨房纸吸去表面浮油。", 7, "中火", "炸到外壳定型即可，炸过头内部干硬，烧后回不了软。", "烤麸表面金黄起壳、敲之有声，体积略缩小。"),
  ("锅中留 15 毫升底油，下冰糖小火炒化成浅琥珀色，倒入香菇、木耳、黄花菜与花生米翻炒 1 分钟，加 35 毫升生抽与 300 毫升泡菇水烧开。", 6, "小火", "泡菇水沉淀后取上层使用，底部细沙弃去，这是鲜味来源。", "汤汁呈浅酱色、香菇与木耳吸汁变软。"),
  ("放入炸好的烤麸，中小火焖 15 分钟至汤汁收至一半，加 3 克盐调味，转大火收汁 3 分钟，淋 10 毫升香油出锅。", 20, "中小火", "收汁到烤麸表面油亮、盘底只剩薄薄一层汁为准，过干会发柴。", "成品酱红油亮、按压有弹性，盘底无流动汤汁。"),
 ],
 "tips": ["烤麸必须挤干再炸，含水的烤麸炸后会软塌、烧制时吸不进酱汁。", "四喜指香菇、木耳、黄花菜、花生四样配菜，缺一味风味就不完整。"],
 "common_mistakes": ["烤麸泡发后不换水，成品带明显酸味。", "全程大火烧，烤麸外层散开、内部仍硬，口感不一致。"],
 "substitutions": [("烤麸", "油面筋", "1:0.8", "油面筋更吸汁，炸制时间缩短到 2 分钟，成品更软。"), ("冰糖", "白糖", "1:1", "白糖上色快，炒糖时间缩短 20 秒。")],
 "variations": ["家庭简化版：烤麸不炸，改为平底锅少油煎至表面结壳，用油量减少 60 毫升。", "本帮甜口版：冰糖增至 45 克并加 10 毫升老抽，颜色更深、甜味更重。"],
 "serving_suggestion": "4 人份冷热皆宜，作冷盘时冷藏 2 小时后风味更融合；配粥或米饭均可。",
 "storage": "冷藏密封 4 天，风味随时间加深；不建议冷冻，解冻后烤麸易碎。",
 "nutrition_estimate": {"basis": "每份（约 150 克成品）", "calories_kcal": 328, "protein_g": 14.2, "fat_g": 18.6, "carbs_g": 28.4, "sodium_mg": 760, "is_estimate": True,
   "disclaimer": "按配料用量与常见食材成分表推算，烤麸吸油量与挤水程度相关，热量可能浮动 20%。"},
 "diet_tags": ["vegetarian", "vegan", "dairy-free"],
 "food_safety_notes": ["烤麸为小麦面筋制品，含麸质，乳糜泻患者禁食。", "干香菇与木耳需用冷水或温水泡发，泡发超过 4 小时应冷藏，出现黏液即丢弃。", "炸制用油温度控制在 170 摄氏度左右，油色发暗后不再复用。"],
 "origin_note": "四喜烤麸是上海本帮菜中的经典冷盘，以烤麸配香菇、木耳、黄花菜、花生四样，取「四喜」的吉意。其做法在上海、江浙一带的家常菜中广泛流传，具体源流不作确切考证。",
 "tags": ["沪菜", "本帮菜", "素菜", "冷盘", "甜咸口"],
 "related_ids": ["yandu-xian", "dongpo-rou"],
})

R.append({
 "id": "dongbei-dalapi",
 "name": {"zh": "东北大拉皮", "en": "Northeastern Sheet Jelly Salad", "original": "东北大拉皮"},
 "cuisine": {"region": "cn", "style": "dongbei"},
 "category": ["cold-dish"],
 "difficulty": 2,
 "time": {"prep_min": 15, "cook_min": 10, "total_min": 25},
 "servings": 4,
 "flavor": ["sour", "salty", "fragrant", "spicy"],
 "ingredients": {
  "main": [("粉皮", "mung bean sheet jelly", 300, "g", "选现成湿粉皮，切 1.5 厘米宽条；干粉皮需提前泡软", False)],
  "aux": [("黄瓜", "cucumber", 150, "g", "切细丝", False), ("胡萝卜", "carrot", 60, "g", "切细丝", False),
          ("绿豆芽", "mung bean sprout", 100, "g", "焯 20 秒过凉沥干", False), ("香菜", "coriander", 15, "g", "切段", False),
          ("蒜", "garlic", 15, "g", "切末，调汁用", False)],
  "seasoning": [("生抽", "light soy sauce", 30, "ml", "底味", False), ("香醋", "black vinegar", 30, "ml", "酸度按口味增减", False),
                ("白糖", "sugar", 8, "g", "和味", False), ("辣椒油", "chili oil", 25, "ml", "自炼红油更香", False),
                ("香油", "sesame oil", 8, "ml", "增香", False), ("白芝麻", "toasted sesame", 8, "g", "干锅小火焙香后撒面", False),
                ("盐", "salt", 3, "g", "调节咸度", False)],
 },
 "equipment": ["大拌菜盆", "漏勺", "擦丝器"],
 "steps": [
  ("粉皮放入沸水焯 30 秒至透明柔软，立即捞出过冷水，沥干后切 1.5 厘米宽条，拌 3 毫升香油防止粘连。", 4, "大火", "粉皮焯到刚透明就捞出，久煮会化成一团没有筋性。", "粉皮由乳白转为半透明、边缘柔韧，筷子夹起不断。"),
  ("黄瓜与胡萝卜切细丝，豆芽焯 20 秒过凉水沥干，香菜切段，依次码放在大盆中。", 6, "大火", "蔬菜丝要沥干水分，带水下盆会让料汁变稀、成品出水。", "菜丝干爽挺立、盆底无水。"),
  ("取小碗放蒜末、30 毫升生抽、30 毫升香醋、8 克白糖、3 克盐、25 毫升辣椒油与 8 毫升香油，搅到糖盐完全溶解。", 3, "无火", "料汁先调好再拌，边拌边尝，酸甜咸三者要平衡。", "料汁呈红亮油润状、蒜香冲鼻，碗底无未溶颗粒。"),
  ("粉皮铺在菜丝上，淋入料汁，从盆底向上翻拌 10 下，撒熟白芝麻与香菜段即可装盘。", 2, "无火", "翻拌而不是抓拌，淀粉类的粉皮容易被抓断。", "粉皮均匀挂汁、蔬菜丝颜色分明，盆底留有少量汤汁。"),
 ],
 "tips": ["粉皮焯后立刻过冷水能保持筋道，泡在热水里会继续软化。", "料汁中的醋建议用陈醋或香醋，米醋酸度不足，拌出来寡淡。"],
 "common_mistakes": ["粉皮焯完不沥干直接拌，料汁被稀释，成品口味发淡。", "蔬菜丝切得太粗，与粉皮口感不协调，且不易挂汁。"],
 "substitutions": [("粉皮", "绿豆凉粉", "1:1", "凉粉更滑，切条后不需焯水，直接拌制。"), ("辣椒油", "花椒油", "1:1", "香气转向麻香，辣度大幅降低。")],
 "variations": ["家庭简化版：省去焯粉皮，用即食凉皮直接拌，口感略硬但省时。", "加肉版：加 100 克熟鸡丝或酱牛肉丝，蛋白质更足，可作主菜。"],
 "serving_suggestion": "4 人份凉菜，现拌现吃，配烤肉或炖菜解腻；夏天可冷藏 20 分钟后再上桌。",
 "storage": "拌好后冷藏不超过 12 小时，粉皮会持续吸汁变硬；配料可分开冷藏保存 2 天。",
 "nutrition_estimate": {"basis": "每份（约 180 克成品）", "calories_kcal": 186, "protein_g": 4.2, "fat_g": 8.4, "carbs_g": 24.6, "sodium_mg": 780, "is_estimate": True,
   "disclaimer": "按配料用量与常见食材成分表推算，粉皮含水量差异大，碳水数值可能浮动 20%。"},
 "diet_tags": ["vegetarian", "vegan", "dairy-free"],
 "food_safety_notes": ["凉拌菜不加热，蔬菜与粉皮处理后须在 2 小时内食用，室温放置不超过 2 小时。", "豆芽焯水要彻底，生豆芽可能携带致病菌。", "粉皮含绿豆淀粉，对豆类过敏者需留意。"],
 "origin_note": "东北大拉皮是东北家庭的常见凉菜，以绿豆或土豆淀粉制成的拉皮配黄瓜丝、豆芽，浇蒜香酸辣汁。各地配菜略有差异，此处按家常做法整理。",
 "tags": ["东北菜", "凉菜", "爽口", "快手菜", "素菜"],
 "related_ids": ["guobao-rou", "lajiao-chaorou"],
})

R.append({
 "id": "youpo-mian",
 "name": {"zh": "油泼面", "en": "Oil-Splashed Noodles", "original": "油泼面"},
 "cuisine": {"region": "cn", "style": "xibei"},
 "category": ["staple-noodle"],
 "difficulty": 3,
 "time": {"prep_min": 20, "cook_min": 10, "total_min": 30},
 "servings": 2,
 "flavor": ["spicy", "salty", "fragrant", "rich"],
 "ingredients": {
  "main": [("面条", "wheat noodles", 300, "g", "选 2 厘米宽的手擀宽面，或现扯的裤带面", False)],
  "aux": [("青菜", "bok choy", 120, "g", "上海青或小油菜，最后与面同煮 30 秒", False),
          ("大葱", "welsh onion", 20, "g", "切葱花", False), ("蒜", "garlic", 15, "g", "切末，泼油前铺在面上", False)],
  "seasoning": [("辣椒面", "chili flakes", 20, "g", "选粗颗粒秦椒面，香而不燥", False),
                ("生抽", "light soy sauce", 25, "ml", "碗底调味", False), ("香醋", "black vinegar", 15, "ml", "吃前淋入", False),
                ("盐", "salt", 3, "g", "面汤与碗底各半", False), ("菜籽油", "rapeseed oil", 80, "ml", "泼油用，须烧到冒烟", False)],
 },
 "equipment": ["深汤锅", "小奶锅", "大碗", "漏勺"],
 "steps": [
  ("大碗中放 25 毫升生抽、1.5 克盐与 10 毫升清水调成碗底汁；蒜切末、大葱切葱花备用。", 3, "无火", "碗底先放液体调料，泼油后味道能顺面条渗下去。", "碗底汁呈浅酱色、无未溶盐粒。"),
  ("汤锅加 2 升水与 1.5 克盐烧开，下宽面大火煮 3 分钟，用筷子轻推防止粘连，起锅前 30 秒下青菜同煮。", 4, "大火", "宽面下锅后水会降温，须保持大火让水快速回到沸腾。", "面条浮起、边缘略透，掐断中心留一点白芯。"),
  ("面条与青菜捞入碗中，铺上 20 克辣椒面、蒜末与葱花，堆在面条中央。", 1, "无火", "辣椒面要集中堆放，泼油时才能一次激透。", "调料堆成小山状、覆盖住面条中心。"),
  ("小奶锅倒 80 毫升菜籽油烧到冒青烟，分两次泼在辣椒面上，听到滋滋声后淋 15 毫升香醋，立即从碗底向上拌匀。", 3, "大火", "油温必须够高，油不冒烟泼下去只有生油味；分两次泼能避免辣椒面焦糊。", "辣椒面由鲜红转为暗红油亮、空气中弥漫焦香与蒜香。"),
 ],
 "tips": ["泼油时油温是关键，烧到油面微微冒烟、插入筷子冒密集小泡即可。", "香醋在泼油后立刻淋，热油激出的醋酸香比直接拌更立体。"],
 "common_mistakes": ["辣椒面受潮结块，泼油后一半焦一半生，香气不均。", "面条煮好后不沥干就装碗，碗底积水使料汁变淡。"],
 "substitutions": [("辣椒面", "辣椒油", "20 克辣椒面对应 40 毫升辣椒油", "用辣椒油则不需泼油，直接拌匀即可，香气略逊。"), ("青菜", "菠菜", "1:1", "菠菜需焯水去草酸，煮 20 秒即可。")],
 "variations": ["家庭简化版：用挂面替代宽面，煮 4 分钟，成品少了筋道但省去和面时间。", "西安街头版：加 50 克臊子肉末与 20 克豆芽，成为臊子油泼面。"],
 "serving_suggestion": "2 人份，趁热拌开食用，配一瓣生蒜与面汤；不宜久放，面条会吸干油汁。",
 "storage": "现做现吃；油泼辣子可单独多做，冷藏保存 2 周。",
 "nutrition_estimate": {"basis": "每份（约 280 克成品）", "calories_kcal": 746, "protein_g": 18.4, "fat_g": 38.6, "carbs_g": 82.4, "sodium_mg": 1160, "is_estimate": True,
   "disclaimer": "按配料用量与常见食材成分表推算，油泼面用油量高，热量随实际吸油量浮动约 15%。"},
 "diet_tags": ["vegetarian", "dairy-free"],
 "food_safety_notes": ["泼油温度接近 200 摄氏度，操作时远离水滴，碗须耐热陶瓷或搪瓷。", "面条含小麦与麸质，麸质过敏者禁食。", "油泼辣子冷藏保存，取用时用干勺，避免进水变质。"],
 "origin_note": "油泼面是陕西关中一带的传统面食，以宽面配辣椒面、热油泼香为特征，讲究面宽、辣香、油亮。具体起源年代难以确证，此处仅作地域饮食背景说明。",
 "tags": ["西北菜", "陕西", "面食", "辣", "快手菜"],
 "related_ids": ["zhajiangmian", "ziran-yangrouchuan"],
})

print("检查食材")
names = set()
for r in R:
    for g in ("main", "aux", "seasoning"):
        for row in r["ingredients"].get(g) or []:
            names.add(row[0])
missing = sorted(n for n in names if n not in IDX)
if missing:
    print("MISSING:", missing); raise SystemExit(0)
for r in R:
    print(build(r))
