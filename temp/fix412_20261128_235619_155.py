# -*- coding: utf-8 -*-
import json, os
B = r"E:\ai_project\marvis_project\caipu\data\recipes\intl\thai"
def load(i): return json.load(open(os.path.join(B, i + ".json"), encoding="utf-8"))
def save(i, d): json.dump(d, open(os.path.join(B, i + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

d = load("thai-ba-mee-nam")
d["tips"][0] = "肉片切薄一点，在滚汤里烫熟才够嫩滑。"
d["tips"][3] = "面条煮到刚断生就捞起，久煮会发坨粘连。"
d["variations"][0] = "加一颗溏心蛋，汤面更有饱足感也更好看。"
d["variations"][1] = "加一勺炸蒜油，香气立刻冲上一个层次。"
save("thai-ba-mee-nam", d)

d = load("thai-goong-pad-khai-dao")
d["common_mistakes"][3] = "虾仁和蛋液一起久炒，虾肉发老蛋块发干。"
d["variations"][1] = "淋一点椰浆，蛋花更滑顺还带奶香。"
save("thai-goong-pad-khai-dao", d)

d = load("thai-khai-pad-hed")
d["tips"][1] = "香菇用湿布擦净表面，别长时间泡在水里。"
d["variations"][0] = "加一把绿豆芽同炒，口感更脆爽也解腻。"
d["variations"][1] = "撒一点朝天椒碎，做成微辣版本更下饭。"
save("thai-khai-pad-hed", d)

d = load("thai-pad-pak-ruam")
d["variations"][2] = "加几只虾仁同炒，鲜味更足也更像一道主菜。"
save("thai-pad-pak-ruam", d)

d = load("thai-tao-hu-neung")
s = d["steps"]
s[1]["text"] = "香菇去蒂切成细丝，南姜和大蒜分别切成细末备用。"
s[4]["text"] = "蒸锅水大火烧开后放入浅盘，大火蒸八分钟至豆腐定型。"
s[5]["visual_cue"] = "盘底清亮无水，豆腐表面微鼓"
s[6]["text"] = "把调好的调味汁均匀淋在豆腐上，再淋一层芝麻油。"
s[7]["text"] = "撒上葱花、朝天椒圈和香菜段，趁热连盘上桌即可。"
d["tips"][1] = "姜末切得越细越好，蒸过之后才不会呛口。"
d["variations"][1] = "铺几只虾仁一起蒸，鲜味更足也更像宴客菜。"
d["variations"][2] = "淋一点辣椒油，做成微辣版本更开胃下饭。"
save("thai-tao-hu-neung", d)

d = load("thai-tom-kha-goong")
d["steps"][2]["text"] = "草菇对半切开，用清水快速冲一遍后沥干水分备用。"
d["tips"][0] = "香茅下锅前先用力拍扁，香气才出得来。"
d["common_mistakes"][2] = "虾仁在汤里煮足五分钟，口感硬得像橡皮。"
save("thai-tom-kha-goong", d)

d = load("thai-yam-phak-kat-hom")
d["steps"][5]["text"] = "水煮蛋切成六瓣，切的时候刀蘸一下水更利落。"
d["tips"][2] = "辣酱用杵臼捣出来，比刀切更出味更辣。"
d["tips"][3] = "花生碎最后撒在表面，早拌会吸汁变软。"
d["variations"][0] = "加一把炸猪皮，脆感更有层次也更香。"
save("thai-yam-phak-kat-hom", d)
print("patched")
