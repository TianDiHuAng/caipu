# -*- coding: utf-8 -*-
import json
b = r"E:\ai_project\marvis_project\caipu\data\recipes\cn\zhejiang" + "\\"
def L(i): return json.load(open(b + i + ".json", encoding="utf-8"))
def W(i, d): json.dump(d, open(b + i + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

d = L("zhejiang-dongsun-doufu-tang")
d["variations"][1] = "放一小把洗净的青菜心，汤里多一抹绿色，看着更有食欲。"
d["variations"][2] = "换成鸡汤打底，鲜味更厚实，冬天喝起来也更暖身。"
d["common_mistakes"][3] = "一开始就放盐，豆腐被盐逼出水，煮完又老又硬。"
W("zhejiang-dongsun-doufu-tang", d)

d = L("zhejiang-hongshao-paigu")
d["common_mistakes"][2] = "烧的时间不够，肉咬不动还挂牙，白费一锅好料。"
# 步骤合计 84 > 78，调整 prep/cook
d["prep_min"] = 21; d["cook_min"] = 63
d["time"]["total_min"] = 84
W("zhejiang-hongshao-paigu", d)

d = L("zhejiang-hongshao-yukuai")
d["variations"][2] = "改用鲫鱼整条烧，不去头尾，摆盘更有面子也更像宴客菜。"
d["related_ids"] = ["xihu-cuyu", "zhejiang-qingzheng-luyu", "congyou-yu"]
W("zhejiang-hongshao-yukuai", d)

d = L("zhejiang-nangua-bing")
d["variations"][1] = "表面裹一层面包糠再煎，外壳更酥，咬下去有咔哧的响声。"
d["common_mistakes"][1] = "饼压得太薄，豆沙一煎就漏出来，锅里全是黑糊的糖色。"
d["common_mistakes"][2] = "大火煎，外面已经焦黑，里面还是带着生粉味的硬芯。"
W("zhejiang-nangua-bing", d)

d = L("zhejiang-paigu-fan")
d["variations"][1] = "放两片腊肠一起焖，油脂渗进米饭，咸香比单放排骨更浓。"
d["steps"][1]["text"] = "大米淘洗三遍至水变清，沥干后静置十分钟让米粒吸足表面水分。"
d["prep_min"] = 34; d["cook_min"] = 40
d["time"]["total_min"] = 74
W("zhejiang-paigu-fan", d)

d = L("zhejiang-sanxian-zhengdan")
d["variations"][1] = "表面撒几粒泡软的枸杞，颜色更喜气，待客时也好看。"
d["common_mistakes"][1] = "蛋液不过筛直接蒸，表面全是小气泡，口感粗得像海绵。"
d["common_mistakes"][3] = "蒸的时间太长，蛋羹老了出水，盘底积一层清汤。"
d["steps"][3]["text"] = "蛋液沿盘边缓缓倒入，盖上保鲜膜并在四角扎几个小孔透气。"
W("zhejiang-sanxian-zhengdan", d)

d = L("zhejiang-xiangjian-doufu")
d["variations"][1] = "焖的时候加几片泡软的香菇，鲜味更足，汤汁也更浓。"
d["common_mistakes"][2] = "焖的时间太短，汤汁只在表面，里面还是白味。"
d["steps"][2]["text"] = "翻面继续煎三分钟至两面金黄，盛出放在漏勺上沥掉多余油分。"
d["steps"][3]["text"] = "锅里留一层底油，下姜末与蒜末小火慢慢炒出香味。"
W("zhejiang-xiangjian-doufu", d)

d = L("zhejiang-yumi-chaoding")
d["flavor"] = ["sweet", "light", "savory"]
d["variations"][2] = "用黄油代替植物油来炒，奶香更浓，孩子特别喜欢。"
d["common_mistakes"][2] = "芡汁调得太稠，整盘菜糊成一坨，完全看不出颗粒。"
d["steps"][0]["text"] = "玉米粒放沸水里焯两分钟，捞出后彻底沥干水分备用。"
W("zhejiang-yumi-chaoding", d)
print("ok")
