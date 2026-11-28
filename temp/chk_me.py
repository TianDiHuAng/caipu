# -*- coding: utf-8 -*-
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
base = r'E:\ai_project\marvis_project\caipu'
ing = json.load(open(base + r'\data\ingredients.json', encoding='utf-8'))['items']
n = {}
for i in ing:
    n[i['zh']] = i['zh']
    for a in i.get('aliases', []):
        n.setdefault(a, i['zh'])
words = '鹰嘴豆 扁豆 红扁豆 小麦粉 全麦面粉 面粉 酵母 芝麻酱 芝麻 欧芹 薄荷 黄瓜 番茄 洋葱 柠檬 石榴糖蜜 茄子 西葫芦 彩椒 羊肉 牛肉 鸡肉 鸡蛋 酸奶 黄油 橄榄油 孜然 肉桂 豆蔻 藏红花 松子 核桃 大米 碾碎小麦 布格麦 皮塔饼 鹰嘴豆泥 南瓜 胡萝卜 土豆 大蒜 香菜 生菜 酸奶酪 白芸豆 青豆 菠菜 花椰菜 甜椒粉 辣椒粉 蜂蜜 椰枣 开心果 杏仁 牛奶 淡奶油 白糖 盐'.split()
for w in words:
    print(w, '=>', n.get(w))
