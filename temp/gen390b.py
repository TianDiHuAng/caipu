# -*- coding: utf-8 -*-
import json, os, glob

repo = r"E:\ai_project\marvis_project\caipu"
draft_path = os.path.join(repo, "temp", "drafts", "batch-390.json")
exist = {os.path.splitext(os.path.basename(f))[0]
         for f in glob.glob(os.path.join(repo, "data", "recipes", "*", "*", "*.json"))}

def I(n, a, u, note):
    return {"n": n, "a": a, "u": u, "note": note}

def S(t, time, heat, tip, cue):
    return {"t": t, "time": time, "heat": heat, "tip": tip, "cue": cue}

new = []

new.append(dict(
    id="american-succotash", zh="奶油玉米毛豆", en="Creamed Succotash",
    original="Succotash", cuisine="american", category=["main-vegetable"],
    difficulty=1, servings=4, flavor=["savory", "sweet", "rich"],
    equipment=["炒锅", "木铲", "刀", "砧板", "漏勺"],
    related=["american-glazed-carrots", "american-corn-pudding", "american-cornbread"],
    ingredients=[
        {"group": "main", "items": [I("玉米粒", 300, "g", "新鲜或冷冻均可"),
                                    I("毛豆", 200, "g", "剥出豆粒")]},
        {"group": "aux", "items": [I("洋葱", 100, "g", "切小丁"),
                                   I("红椒", 80, "g", "切小丁")]},
        {"group": "seasoning", "items": [I("黄油", 20, "g", "起锅增香"),
                                          I("淡奶油", 60, "ml", "收汁用"),
                                          I("盐", 4, "g", "调味"),
                                          I("黑胡椒", 2, "g", "现磨"),
                                          I("植物油", 15, "ml", "煸炒底油")]},
    ],
    steps=[
        S("毛豆剥出豆粒后冲洗两遍，玉米粒若是整根甜玉米先削下来，两样分开装碗备用。", 8, "无火",
          "毛豆外层的薄皮遇热容易发硬，剥的时候顺手搓掉口感更嫩。", "豆粒饱满发亮，碗底没有积水"),
        S("炒锅烧热倒植物油，下洋葱丁用中火煸炒到边缘透亮、香气散出。", 4, "中火",
          "洋葱要炒到透明才出甜味，急着放别的料会带生辛气。", "洋葱变半透明，锅里有甜香"),
        S("放红椒丁同炒一分钟，再把玉米粒与毛豆一起下锅翻炒均匀。", 3, "中火",
          "毛豆比玉米难熟，下锅后先铺平让它贴住锅底受热。", "玉米粒边缘微微起泡，颜色转深"),
        S("沿锅边淋入少量清水，加盖焖三分钟，让毛豆彻底断生熟透。", 3, "小火",
          "豆类别省这道焖，生的毛豆带豆腥还会闹肚子。", "豆粒一压就碎，锅里水汽将干"),
        S("开盖加黄油与淡奶油，转大火快速翻炒到汤汁变浓、裹住每一粒豆。", 3, "大火",
          "奶油下锅后要不停翻，火大了容易糊底发苦。", "汤汁挂在豆粒上不再流动"),
        S("撒盐与现磨黑胡椒翻匀，尝一颗豆子调好咸淡即可盛盘。", 2, "小火",
          "盐最后放，早放会让毛豆表皮收紧、口感发韧。", "咸淡合适，盘面油亮不积水"),
    ],
    tips=["冷冻毛豆不用解冻，直接下锅多焖一分钟就行。",
          "想更浓稠可以多加二十毫升淡奶油，收汁时火要更小。",
          "加两片培根先煸出油再炒洋葱，风味更接近南方做法。",
          "剩下的冷吃也好吃，拌一点柠檬汁当沙拉。"],
    mistakes=["毛豆没焖透就出锅，咬起来咯吱响还带豆腥味。",
              "奶油下锅后大火猛烧，锅底结出一层焦褐的奶皮。",
              "盐和洋葱一起早放，毛豆表皮变硬嚼不烂。",
              "玉米用的是罐头甜玉米却没沥干，整盘变成稀汤。"],
    subs=[{"orig": "淡奶油", "sub": "牛奶", "ratio": "60毫升:60毫升",
           "note": "浓度低一些，收汁时间要延长两分钟。"},
          {"orig": "毛豆", "sub": "青豆", "ratio": "200克:200克",
           "note": "口感更软，焖的时间可以缩短到两分钟。"}],
    variations=["把淡奶油换成椰浆，做成带椰香的素食版本。",
                "最后拌入一把撕碎的罗勒叶，香气会清爽很多。"],
    serving="盛进浅口盘里，黄绿两色分明，配烤鸡腿或煎猪排都合适，汤汁别倒掉，拌饭正好。",
    storage="冷藏密封可存两天，复热时加一勺清水用小火翻热，不要用大火久煮否则奶油会分离。",
    nutrition={"basis": "按四人份估算", "kcal": 214, "protein": 7, "fat": 12, "carbs": 20, "sodium": 420},
    diet=["vegetarian", "gluten-free"],
    tags=["美式", "玉米", "毛豆", "家常"],
    safety=["毛豆必须彻底焖熟断生，生豆类含凝集素易引起肠胃不适。",
            "含奶制品，乳糖不耐者请改用无乳替代品；剩菜须冷藏并在两天内吃完。"],
    origin="Succotash 是新英格兰与南方都认的家常菜，源自原住民把玉米和豆子一起煮的做法，名字来自纳拉甘西特语。早期用熊油和咸肉提味，后来改用黄油与奶油收汁，就成了如今甜咸交错的配菜。",
    prep=10, cook=15))

new.append(dict(
    id="american-almond-green-beans", zh="杏仁黄油四季豆", en="Almond Green Beans",
    original="Green beans almondine", cuisine="american", category=["main-vegetable"],
    difficulty=1, servings=4, flavor=["savory", "nutty", "fresh"],
    equipment=["炒锅", "汤锅", "漏勺", "刀", "砧板"],
    related=["american-glazed-carrots", "american-green-bean-casserole", "american-broccoli-casserole"],
    ingredients=[
        {"group": "main", "items": [I("四季豆", 500, "g", "掐头去尾")]},
        {"group": "aux", "items": [I("杏仁", 50, "g", "切薄片"),
                                   I("大蒜", 15, "g", "切薄片")]},
        {"group": "seasoning", "items": [I("黄油", 25, "g", "收尾增香"),
                                          I("盐", 4, "g", "焯水与调味"),
                                          I("黑胡椒", 2, "g", "现磨"),
                                          I("植物油", 15, "ml", "煸蒜")]},
    ],
    steps=[
        S("四季豆掐掉两头顺便撕去两侧的老筋，洗净后掰成五厘米左右的段。", 8, "无火",
          "两侧的筋不撕掉，吃的时候会拖出一根粗纤维。", "豆段两头断面平整无筋丝"),
        S("汤锅烧开大半锅水，加一小撮盐，把四季豆下锅焯三分钟。", 5, "大火",
          "水里先加盐能让豆子保住翠绿，不加会发黄发灰。", "豆身转成深绿，浮在水面打转"),
        S("捞出的四季豆立刻放进凉水里过一遍，彻底降温后沥干水分。", 4, "无火",
          "过凉能锁住脆度，捞起就放着会继续变软变黄。", "豆段摸起来冰凉硬挺"),
        S("炒锅小火烧热植物油，下杏仁片慢慢煸到边缘泛金，盛出备用。", 4, "小火",
          "杏仁片薄，火一大几秒就发黑发苦，务必全程小火。", "杏仁片卷边，锅里有坚果香"),
        S("锅里放黄油与蒜片炒出香味，倒入沥干的四季豆大火快速翻炒。", 3, "大火",
          "豆子下锅前要沥干，带水下锅只会溅油不挂香。", "蒜片微黄，豆段表面裹上油光"),
        S("撒盐与黑胡椒翻匀，关火后把杏仁片撒回锅里拌匀即可上桌。", 2, "小火",
          "杏仁片最后放才保持脆口，早放会吸潮变软。", "咸淡合适，豆身翠绿不塌"),
    ],
    tips=["四季豆选细一点的，粗的豆荚纤维多，焯水时间要加一分钟。",
          "焯完的凉水可以加几块冰，豆子会更脆更绿。",
          "黄油换成橄榄油就是更清爽的素食版本。",
          "多煸一点杏仁片备着，撒在别的蔬菜上同样好吃。"],
    mistakes=["四季豆只炒不焯，外面焦了里面还是生的，嚼起来发硬。",
              "杏仁片用中火爆香，一转身就全糊成黑色。",
              "豆子焯完不过凉水，上桌时已经软塌塌发黄。",
              "黄油烧到冒烟才下蒜，蒜片瞬间焦掉带苦味。"],
    subs=[{"orig": "杏仁", "sub": "核桃仁", "ratio": "50克:50克",
           "note": "掰成小块，煸的时间缩短一分钟。"},
          {"orig": "黄油", "sub": "橄榄油", "ratio": "25克:20毫升",
           "note": "香气更清淡，适合配油腻的主菜。"}],
    variations=["最后撒一层帕玛森芝士碎，味道会更厚重。",
                "加一小勺柠檬皮屑同炒，豆香里带一点清亮的酸气。"],
    serving="装进长方形浅盘，把杏仁片均匀撒在表面，配牛排或烤鸡都合适，冷的也好吃。",
    storage="冷藏可存两天，复热用平底锅小火干炒两分钟，别用微波炉，豆子会出水变软。",
    nutrition={"basis": "按四人份估算", "kcal": 168, "protein": 5, "fat": 12, "carbs": 11, "sodium": 400},
    diet=["vegetarian", "gluten-free"],
    tags=["美式", "四季豆", "杏仁", "配菜"],
    safety=["四季豆须焯透并彻底炒熟，半生的豆角含皂苷与凝集素，食用后易恶心呕吐。",
            "含坚果与乳制品，过敏体质者请更换配料；剩菜须冷藏并两天内复热食用。"],
    origin="杏仁黄油四季豆是美式牛排馆的标配配菜，名字来自法语的 amandine，指用杏仁装饰的作法。煮到脆嫩再过冰水，最后用黄油和烤香的杏仁片拌匀，讲究的就是豆子翠绿、杏仁酥脆这一口对比。",
    prep=12, cook=13))

new.append(dict(
    id="american-denver-omelette", zh="丹佛煎蛋卷", en="Denver Omelette",
    original="Denver omelette", cuisine="american", category=["main-egg"],
    difficulty=1, servings=2, flavor=["savory", "rich", "umami"],
    equipment=["不粘平底锅", "硅胶铲", "打蛋器", "刀", "砧板"],
    related=["american-cheese-omelette", "american-veggie-frittata", "american-scrambled-eggs"],
    ingredients=[
        {"group": "main", "items": [I("鸡蛋", 200, "g", "约四个")]},
        {"group": "aux", "items": [I("火腿", 80, "g", "切小丁"),
                                   I("洋葱", 60, "g", "切细丁"),
                                   I("甜椒", 60, "g", "切细丁"),
                                   I("切达奶酪", 40, "g", "刨丝")]},
        {"group": "seasoning", "items": [I("黄油", 20, "g", "煎蛋用"),
                                          I("盐", 3, "g", "调味"),
                                          I("黑胡椒", 2, "g", "现磨"),
                                          I("植物油", 10, "ml", "炒馅料")]},
    ],
    steps=[
        S("火腿切成半厘米小丁，洋葱与甜椒同样切细，三样分开放好备用。", 8, "无火",
          "馅料切得越细越好卷，块太大蛋皮一定会裂开。", "三种丁大小均匀，颗粒分明"),
        S("平底锅倒植物油中火烧热，下洋葱与甜椒炒两分钟到出水变软。", 3, "中火",
          "蔬菜要先炒掉水分，带水的馅会把蛋皮泡破。", "蔬菜丁变软透亮，锅底没有水"),
        S("放火腿丁同炒一分钟，撒一半盐与黑胡椒调味后盛出摊凉。", 2, "中火",
          "馅料必须放凉再卷，滚烫的馅会当场把蛋皮烫穿。", "火腿边缘微卷，馅料不烫手"),
        S("鸡蛋打散加剩下的盐与黑胡椒，用打蛋器搅到蛋清蛋黄完全融合。", 2, "无火",
          "搅到看不见蛋清的丝状物，蛋皮才会平整不起泡。", "蛋液颜色均匀，表面有细泡"),
        S("锅里放黄油化开，倒入蛋液转中小火，用铲子把边缘推向中间让蛋液流动。", 3, "中小火",
          "边缘往中间推，未熟的部分才会流到锅底受热。", "蛋皮半凝，表面还略带湿润"),
        S("把馅料与奶酪丝铺在蛋皮一侧，对折盖住，再小火焖一分钟定型出锅。", 3, "小火",
          "焖一分钟让奶酪化开，蛋皮也不会因为急翻而断。", "奶酪渗出边缘，折口粘合"),
    ],
    tips=["鸡蛋从冰箱拿出来先回温十分钟，蛋液更容易摊匀。",
          "锅子用不粘锅最稳，铸铁锅容易让蛋皮粘底。",
          "馅料别贪多，铺满一半就够，多了卷不起来。",
          "想要更嫩可以在蛋液里加一小勺牛奶。"],
    mistakes=["大火煎蛋皮，底下焦了上面还是流动的蛋液。",
              "蔬菜没炒干就卷，吃的时候盘底渗出一滩水。",
              "馅料刚出锅就铺上去，蛋皮被烫出几个破洞。",
              "蛋液没打匀，蛋白结成白块贴在蛋皮上。"],
    subs=[{"orig": "火腿", "sub": "培根", "ratio": "80克:80克",
           "note": "先煎脆再切丁，咸度更高可少放盐。"},
          {"orig": "切达奶酪", "sub": "马苏里拉", "ratio": "40克:40克",
           "note": "拉丝更明显，奶味稍淡一些。"}],
    variations=["把火腿换成烟熏三文鱼，就是更精致的版本。",
                "最后淋一勺番茄莎莎酱，酸甜能解掉奶酪的腻。"],
    serving="出锅后对角切成两半，配一片烤吐司和一小把芝麻菜，趁热吃蛋皮最嫩。",
    storage="最好现做现吃；冷藏可存一天，复热用平底锅小火两面各热三十秒，微波会让蛋皮发硬。",
    nutrition={"basis": "按两人份估算", "kcal": 386, "protein": 26, "fat": 28, "carbs": 7, "sodium": 780},
    diet=["gluten-free", "low-carb", "high-protein"],
    tags=["美式", "鸡蛋", "早餐", "煎"],
    safety=["鸡蛋须煎至蛋液完全凝固，避免沙门氏菌风险；老人与孕妇请勿食用半熟蛋皮。",
            "含蛋、乳制品与猪肉制品，相关过敏或不耐受者请更换配料。"],
    origin="丹佛煎蛋卷在西部被称为西部煎蛋卷，火腿、洋葱与青椒这三样是标志。传说它起源于十九世纪西部铁路与矿区餐馆的早餐，用料扎实、一折即走，后来成了全美早餐店的固定选项。",
    prep=8, cook=13))

new.append(dict(
    id="american-crispy-tofu-nuggets", zh="香脆豆腐块", en="Crispy Tofu Nuggets",
    original="Tofu nuggets", cuisine="american", category=["main-tofu"],
    difficulty=2, servings=4, flavor=["savory", "umami", "spicy"],
    equipment=["平底锅", "厨房纸", "重物", "三个浅盘", "夹子"],
    related=["american-tofu-burger", "american-bbq-tofu", "american-buffalo-tofu"],
    ingredients=[
        {"group": "main", "items": [I("北豆腐", 500, "g", "压去水分")]},
        {"group": "aux", "items": [I("玉米淀粉", 40, "g", "裹粉用"),
                                   I("面包糠", 50, "g", "外层脆壳"),
                                   I("鸡蛋", 50, "g", "沾粉黏合")]},
        {"group": "seasoning", "items": [I("盐", 4, "g", "调味"),
                                          I("黑胡椒", 2, "g", "现磨"),
                                          I("辣椒粉", 3, "g", "提香"),
                                          I("植物油", 40, "ml", "半煎半炸")]},
    ],
    steps=[
        S("北豆腐用厨房纸包好，压上重物静置二十分钟，把里面的水分挤出来。", 20, "无火",
          "水分挤不干，下锅只会软塌塌粘成一团，脆壳根本挂不住。", "豆腐厚度变薄，纸吸满水"),
        S("压好的豆腐切成三厘米见方的块，表面再拍一层干玉米淀粉。", 5, "无火",
          "淀粉要拍匀拍薄，厚的粉层炸完会脱壳。", "块面泛白，摸起来滑而不粘手"),
        S("鸡蛋打散成蛋液，把豆腐块先蘸蛋液再滚一层面包糠，轻压让糠粘牢。", 6, "无火",
          "蘸完蛋液要沥一下，太湿会把面包糠泡成糊。", "每块裹满糠粒，边角也盖住"),
        S("平底锅倒植物油中火烧到筷子插入冒小泡，把豆腐块排进去不要挤。", 2, "中火",
          "块之间留空隙才不会粘成饼，油温不够会吸油发软。", "豆腐边缘立刻冒密集小泡"),
        S("每面煎两到三分钟，翻面时用夹子托住底部，煎到通体金黄捞出。", 6, "中火",
          "翻面太早壳会破，看到边缘定型变色再翻最稳。", "六面金黄，敲起来有脆响"),
        S("出锅后趁热撒盐、黑胡椒与辣椒粉，抖匀后放在厨房纸上吸去浮油。", 2, "无火",
          "调味要在刚出锅时撒，凉了表面出油就挂不住。", "表面干爽，调味均匀不结块"),
    ],
    tips=["老豆腐比嫩豆腐好操作，压水后不容易碎。",
          "没有面包糠可以用压碎的玉米片代替，更脆。",
          "想少油可以改成烤箱二百度烤二十分钟，中途翻一次面。",
          "一次多做点冷冻起来，吃前直接回锅复烤就行。"],
    mistakes=["豆腐没压水就下锅，煎出来软趴趴还粘满锅底。",
              "油温太低就下锅，面包糠吸饱油变得又腻又软。",
              "锅里塞得太满，块和块粘在一起翻不动。",
              "调味撒得太早，盐把脆壳泡软变成一层糊。"],
    subs=[{"orig": "面包糠", "sub": "玉米片", "ratio": "50克:50克",
           "note": "压碎成粗粒，脆度更明显。"},
          {"orig": "鸡蛋", "sub": "玉米淀粉糊", "ratio": "50克:60克",
           "note": "纯素版本，黏合稍弱要轻拿轻放。"}],
    variations=["裹好糠后刷一层辣酱再烤，做成水牛城风味。",
                "把辣椒粉换成孜然粉与蒜粉，香气更接近炸鸡。"],
    serving="趁热装盘，配一小碟番茄酱或蜂蜜芥末酱，旁边放几根芹菜条解腻，当正餐或下酒都合适。",
    storage="冷藏可存两天，复热用平底锅小火两面各煎一分钟，或烤箱一百八十度烤六分钟恢复脆度。",
    nutrition={"basis": "按四人份估算", "kcal": 302, "protein": 16, "fat": 18, "carbs": 19, "sodium": 520},
    diet=["vegetarian"],
    tags=["美式", "豆腐", "煎", "素食"],
    safety=["豆腐含水量高，煎制时油易飞溅，下锅前务必沥干并控好油温。",
            "含大豆、蛋与麸质，相关过敏者请改用无麸质面包糠并去掉鸡蛋。"],
    origin="豆腐块是美式炸鸡块的素食改写版，最早出现在加州的素食餐馆，用压水的北豆腐替代鸡肉，裹粉后半煎半炸，外壳咬起来有响，里面仍是嫩的。蘸酱和配菜沿用炸鸡那一套，吃起来毫不违和。",
    prep=31, cook=10))

new.append(dict(
    id="american-chicken-alfredo", zh="奶油鸡肉意面", en="Chicken Alfredo",
    original="Chicken Alfredo", cuisine="american", category=["staple-noodle"],
    difficulty=2, servings=4, flavor=["rich", "savory", "umami"],
    equipment=["深锅", "平底锅", "夹子", "刨丝器", "漏勺"],
    related=["american-mac-and-cheese", "american-beef-noodle-skillet", "american-chicken-pot-pie"],
    ingredients=[
        {"group": "main", "items": [I("意大利面", 400, "g", "宽面"),
                                    I("鸡胸肉", 400, "g", "切厚片")]},
        {"group": "aux", "items": [I("淡奶油", 200, "ml", "酱汁主体"),
                                   I("帕玛森芝士", 60, "g", "刨丝"),
                                   I("黄油", 30, "g", "炒香"),
                                   I("大蒜", 15, "g", "切末"),
                                   I("洋葱", 80, "g", "切细丁")]},
        {"group": "seasoning", "items": [I("盐", 6, "g", "煮面与调味"),
                                          I("黑胡椒", 3, "g", "现磨"),
                                          I("橄榄油", 20, "ml", "煎鸡"),
                                          I("欧芹", 5, "g", "切碎点缀")]},
    ],
    steps=[
        S("深锅烧开大半锅水，加一勺盐，把意大利面下锅按包装时间煮到略硬。", 11, "大火",
          "面要煮到咬开中心还有一点白芯，后面拌酱还会继续变软。", "面条能弯不易断，中心留白点"),
        S("煮面同时把鸡胸肉横刀片成两片，两面撒盐与黑胡椒腌十分钟。", 10, "无火",
          "片薄再煎受热均匀，整块厚肉外面老了里面还没熟。", "肉片厚薄一致，表面挂满调料"),
        S("平底锅倒橄榄油中火烧热，放鸡胸肉每面煎四分钟，煎好夹出静置。", 9, "中火",
          "下锅后别急着翻，等边缘变白定型再翻才不粘锅。", "两面金黄，按压有弹性"),
        S("原锅放黄油，下洋葱丁与蒜末小火炒到洋葱透亮、蒜香散出。", 3, "小火",
          "蒜末容易焦，火一定要小，闻到香就下奶油。", "洋葱透明，锅底泛出奶白"),
        S("倒入淡奶油小火加热，边搅边煮到微微冒泡，再放帕玛森芝士搅到融化。", 4, "小火",
          "奶油不能大滚，滚过头会油水分离变成颗粒状。", "酱汁顺滑挂勺，表面光亮"),
        S("把沥干的面条与切条鸡肉倒进酱汁，翻拌到每根面都裹上酱，撒欧芹出锅。", 2, "小火",
          "留半碗煮面水，酱太稠时加两勺就能重新顺滑。", "面条被酱裹住，盘底不积油"),
    ],
    tips=["煮面水别全倒掉，含淀粉的水是调稀酱汁的最好材料。",
          "帕玛森现刨比预刨粉香得多，用量也可适当减少。",
          "鸡肉煎完静置三分钟再切，汁水不会全流在板上。",
          "想更浓可以加一个蛋黄同拌，但温度不能太高否则会结块。"],
    mistakes=["奶油大火烧滚，酱汁当场分成油和白色颗粒。",
              "面条煮到全软才捞，拌酱时一搅就烂成糊。",
              "蒜末和洋葱一起大火爆，蒜焦黑带苦味毁了整锅。",
              "鸡肉煎完直接切，一盘汁水全渗在盘底。"],
    subs=[{"orig": "淡奶油", "sub": "牛奶加黄油", "ratio": "200毫升:180毫升加20克",
           "note": "更清爽，收汁时间要延长三分钟。"},
          {"orig": "鸡胸肉", "sub": "鸡腿肉", "ratio": "400克:400克",
           "note": "口感更嫩，煎的时间每面多一分钟。"}],
    variations=["加一把白蘑菇同炒，做成蘑菇奶油意面。",
                "最后撒一点红椒碎与帕玛森同烤两分钟，表面多一层焦壳。"],
    serving="装进预热的深盘，鸡肉条摆在面上，再刨一层芝士与黑胡椒，配一份蒜香面包把酱汁蘸干净。",
    storage="冷藏可存两天，复热时加两勺牛奶用小火翻拌，别用大火，酱汁容易分离。",
    nutrition={"basis": "按四人份估算", "kcal": 742, "protein": 42, "fat": 32, "carbs": 68, "sodium": 820},
    diet=["high-protein"],
    tags=["美式", "意面", "奶油", "鸡肉"],
    safety=["鸡胸肉中心须完全熟透，切开不见粉红色汁水；生熟案板与夹子要分开使用。",
            "含麸质与乳制品，相关过敏或不耐受者请替换面条与奶油；剩菜须冷藏并两天内复热。"],
    origin="Alfredo 原本是罗马一家餐馆在二十世纪初为妻子做的黄油芝士拌面，传到美国后被加进淡奶油与鸡肉，成了连锁餐厅的招牌菜。美式版本奶香更厚重、酱汁更多，配宽面和煎鸡胸是标准搭配。",
    prep=20, cook=14))

# 合并
cur = json.load(open(draft_path, encoding="utf-8"))
ids = {r["id"] for r in cur}
for r in new:
    assert r["id"] not in exist, "已入库:" + r["id"]
    assert r["id"] not in ids, "批内重复:" + r["id"]
    cur.append(r)

batch_ids = {r["id"] for r in cur}
for r in cur:
    for x in r.get("related", []):
        assert x in exist or x in batch_ids, f'{r["id"]}: related 缺失 {x}'

probs = []
for r in cur:
    ss = sum(s["time"] for s in r["steps"])
    if ss > r["prep"] + r["cook"]:
        probs.append((r["id"], "steps over", ss, r["prep"] + r["cook"]))
    for s in r["steps"]:
        if len(s["t"]) < 21: probs.append((r["id"], "step", len(s["t"]), s["t"]))
        if len(s["tip"]) < 17: probs.append((r["id"], "tip", len(s["tip"]), s["tip"]))
        if len(s["cue"]) < 10: probs.append((r["id"], "cue", len(s["cue"]), s["cue"]))
    for k, lim in (("tips", 15), ("mistakes", 17), ("variations", 17)):
        for t in r[k]:
            if len(t) < lim: probs.append((r["id"], k, len(t), t))
    for k, lim in (("serving", 20), ("storage", 20), ("origin", 46)):
        if len(r[k]) < lim: probs.append((r["id"], k, len(r[k]), r[k]))
    for g in r["ingredients"]:
        for it in g["items"]:
            if len(it["note"]) < 2: probs.append((r["id"], "note", it["n"]))
    mg = sum(i["a"] for g in r["ingredients"] if g["group"] == "main" for i in g["items"] if i["u"] == "g")
    if mg / r["servings"] < 60:
        probs.append((r["id"], "主料每份<60g", round(mg / r["servings"], 1)))
    oil = sum(i["a"] for g in r["ingredients"] for i in g["items"] if "油" in i["n"] and i["u"] == "ml")
    if oil > 45 * r["servings"]:
        probs.append((r["id"], "油超限", oil, 45 * r["servings"]))

print("problems:", probs if probs else "none")
json.dump(cur, open(draft_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("count", len(cur), [r["id"] for r in cur])
