# -*- coding: utf-8 -*-
import json, io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
base = r'E:\ai_project\marvis_project\caipu'
ing = json.load(open(base + r'\data\ingredients.json', encoding='utf-8'))['items']
n = {}
for i in ing:
    n[i['zh']] = i['zh']
    for a in i.get('aliases', []):
        n.setdefault(a, i['zh'])
words = '黄油 牛奶 淡奶油 面粉 鸡蛋 奶酪 白葡萄酒 红葡萄酒 白兰地 百里香 迷迭香 月桂叶 欧芹 蘑菇 口蘑 土豆 洋葱 韭葱 培根 火腿 鸡腿肉 鸡胸肉 鸭胸 牛里脊 牛肉 羊肉 猪肉 虾 虾仁 干贝 鳕鱼 三文鱼 青口贝 白豆 番茄 胡萝卜 芹菜 大蒜 盐 白胡椒 黑胡椒 白糖 橄榄油 植物油 醋 芥末 蛋黄酱 香槟 高汤 鸡汤 面包 法棍 酵母 淀粉 玉米淀粉 菠菜 芦笋 花椰菜 西兰花 南瓜 苹果 梨 柠檬 橙子 巧克力 可可粉 香草 肉桂 桂皮 蜂蜜 杏仁 核桃 榛子 葡萄干 朗姆酒 橙皮 糖粉 吉利丁'.split()
for w in words:
    print(w, '=>', n.get(w))
print('---FILES---')
p = base + r'\data\recipes\intl\french'
print(len(os.listdir(p)))
print(' '.join(sorted(x[:-5] for x in os.listdir(p))))
