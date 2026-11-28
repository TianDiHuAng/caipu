# -*- coding: utf-8 -*-
import json, os
root = r"E:\ai_project\marvis_project\caipu"
p = os.path.join(root, "temp", "drafts", "batch-409.json")
# 先由 gen409 只输出草稿（问题版），再统一打补丁
import subprocess

CUE = {
 ("guizhou-lawei-chao-zhusun", 5): "笋片油亮发亮，边缘微微巻起",
 ("guizhou-ganjiao-tudoupian", 1): "水色清透不浑，薯片干爽不粘连",
 ("guizhou-ganjiao-tudoupian", 2): "辣椒段长短整齐，籽已抖净",
 ("guizhou-ganjiao-tudoupian", 3): "辣椒转深红发亮，油面浮起香味",
 ("guizhou-ganjiao-tudoupian", 5): "薯片均匀染上一层浅浅的酱色",
 ("guizhou-ganjiao-tudoupian", 6): "薯片脆亮泛光，葱段翠绿挺直",
 ("yunnan-suancai-chao-yumi", 1): "玉米粒干爽松散，颗颗分明不粘连",
 ("yunnan-suancai-chao-yumi", 2): "酸菜碎干爽不滴水，酸香明显冲鼻",
 ("yunnan-zhusun-paigu-tang", 0): "排骨发白，泡出的水呈淡红色",
 ("yunnan-zhusun-paigu-tang", 2): "笋块由白转浅黄，涩味散尽",
 ("yunnan-zhusun-paigu-tang", 3): "汤面大火翻滚，只浮少量细沫",
 ("yunnan-zhusun-paigu-tang", 5): "笋块在汤中浮沉，汤带清甜笋香",
 ("yunnan-zhusun-paigu-tang", 6): "枸杞吸汤饱满，汤色微黄发亮",
 ("guizhou-suancai-doufu-tang", 0): "豆腐块完整不破，边缘齐整",
 ("guizhou-suancai-doufu-tang", 1): "酸菜碎干爽不滴水，酸香明显",
 ("guizhou-suancai-doufu-tang", 2): "姜丝边缘微焦，猪油香气扑鼻",
 ("guizhou-suancai-doufu-tang", 3): "酸菜碎炒软出香，香气直冲鼻子",
 ("guizhou-suancai-doufu-tang", 4): "汤色微黄清亮，酸香扑鼻而来",
 ("guizhou-suancai-doufu-tang", 7): "葱花翠绿浮面，汤面漂一层薄油",
 ("yunnan-xiangmao-ji-tang", 0): "鸡块冲至发白，水基本清澈",
 ("yunnan-xiangmao-ji-tang", 1): "浮沫灰白成团，鸡块表面干净",
 ("yunnan-xiangmao-ji-tang", 3): "柠檬皮薄而黄，汁水清亮无渣",
 ("yunnan-xiangmao-ji-tang", 4): "汤面翻滚冒泡，香茅段浮起打转",
 ("guizhou-huiguo-rou", 2): "肉片薄透见光，肥膘半透明",
 ("guizhou-huiguo-rou", 3): "蒜白段厚实饱满，蒜叶青绿鲜亮",
 ("guizhou-huiguo-rou", 5): "豆豉散开化油，辣椒转成深红色",
 ("yunnan-xiaomila-chao-niurou", 0): "肉片薄透见光，白色纹理被横断",
 ("yunnan-xiaomila-chao-niurou", 2): "肉片挂上一层薄浆，片片分开",
 ("yunnan-xiaomila-chao-niurou", 3): "椒圈切得整齐，辣气直冲鼻腔",
 ("yunnan-xiaomila-chao-niurou", 6): "椒圈转深红出香，油色红亮",
}

TIP = {
 ("yunnan-suancai-chao-yumi", 7): "葱花只负责提香，翻两下就出锅，炒软了发黄还失香。",
 ("yunnan-zhusun-paigu-tang", 2): "鲜笋不焯会涩口，焯透之后汤才清甜，笋也不扎嘴。",
 ("yunnan-zhusun-paigu-tang", 3): "水要一次加足，中途添水汤味立刻变淡，鲜味也散了。",
 ("guizhou-suancai-doufu-tang", 0): "淡盐水泡一下能让豆腐定形，下锅煮才不容易散成渣。",
 ("guizhou-suancai-doufu-tang", 4): "先煮酸菜再下豆腐，汤的酸度才均匀，豆腐也不会发硬。",
 ("yunnan-xiangmao-ji-tang", 0): "冲掉表面血水，汤才清亮，炖出来也不带一点腥气。",
}

TEXT = {
 ("yunnan-zhusun-paigu-tang", 6): "加盐和白胡椒调味，撒入泡软的枸杞，再小火炖两分钟让味道融开。",
 ("guizhou-suancai-doufu-tang", 7): "关火撒上葱花，淋几滴猪油增香，趁热盛进碗里端上桌。",
}
