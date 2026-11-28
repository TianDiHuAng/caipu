# -*- coding: utf-8 -*-
import json
ing = json.load(open('data/ingredients.json', encoding='utf-8'))['items']
names = set()
for it in ing:
    names.add(it['zh'])
    for a in it.get('aliases', []):
        names.add(a)
want = ['黄油','奶油','淡奶油','面粉','中筋面粉','牛奶','奶酪','帕玛森','白葡萄酒','菠菜','蘑菇','口蘑','百里香','欧芹','洋葱','大蒜','鸡蛋','豆腐','嫩豆腐','面条','通心粉','意大利面','米饭','高汤','白胡椒','黑胡椒','盐','橄榄油','植物油','白糖','柠檬','番茄','土豆','胡萝卜','西兰花','青豆','蘑菇','培根','牛肉','鸡腿肉','鱼','虾仁','蛤蜊','鼠尾草','月桂叶','迷迭香','蒜末','小葱','面包','吐司','酵母','蜂蜜','芥末','醋','白醋','红葡萄酒','藏红花','肉桂','香草','杏仁','核桃','葡萄干','栗子','南瓜','西葫芦','茄子','韭葱','芹菜','小葱']
miss = [w for w in dict.fromkeys(want) if w not in names]
open('temp/chk2.txt','w',encoding='utf-8').write('MISSING:\n' + '\n'.join(miss))
