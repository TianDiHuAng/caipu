import fs from 'node:fs';
const d = JSON.parse(fs.readFileSync('data/ingredients.json', 'utf8'));
const arr = Array.isArray(d) ? d : d.ingredients;
const names = new Set();
for (const x of arr) {
  if (x.zh) names.add(x.zh);
  for (const a of x.aliases || []) names.add(a);
}
const cand = `咸肉 冬笋 排骨 年糕 梭子蟹 黄鱼 雪菜 草鱼 豆腐皮 五花肉 猪肉 豆腐 辣椒粉 糯米粉 粘米粉 澄粉 面粉 酵母 黄豆酱 蒲菜 花生 汤圆 芝麻 椰浆 三文鱼 味淋 木鱼花 昆布 白萝卜 魔芋 鱼饼 年糕条 韩式辣椒酱 虾 鱿鱼 香茅 鱼露 青柠 米纸 米粉 生菜 薄荷 帕玛森奶酪 蜜瓜 生火腿 高筋面粉 番茄 马苏里拉奶酪 罗勒 鸡蛋 牛奶 低筋面粉 黄油 淡奶油 培根 土豆 韭葱 面包糠 火腿 鸡腿肉 酸奶 孜然 烟熏辣椒粉 姜黄粉 玉米粉 玉米面 泡打粉 牛肉 彩椒 洋葱 可可粉 肉桂 玉米淀粉 生抽 老抽 蚝油 料酒 白糖 盐 葱 生姜 大蒜 小米辣 干辣椒 花椒 八角 桂皮 香醋 米醋 芝麻油 辣椒油 豆豉 虾皮 紫菜 米饭 面条 白胡椒 黑胡椒 鸡精 香菜 青葱 蒜苗 白菜 油菜 香菇 木耳 金针菇 胡萝卜 黄瓜 芹菜 青椒 豆芽 韭菜 玉米 山药 莲藕 南瓜 红薯 芋头 板栗 莲子 红枣 枸杞 当归 黄芪 花雕酒 黄酒 冰糖 蜂蜜 炼乳 可可 巧克力 奶油奶酪 吉利丁 香草精 泡菜 豆腐乳 红曲米 豆瓣酱 甜面酱 沙茶酱 咖喱块 咖喱粉 椰浆 柠檬 罗勒叶 百里香 迷迭香 月桂叶 红酒 白葡萄酒 啤酒 高汤 鸡汤 猪骨 牛骨 鸡胸肉 鸭 鹅 羊肉 猪蹄 猪五花 猪里脊 培根 香肠 腊肠 火腿片 鱼 鲈鱼 鲫鱼 带鱼 鳕鱼 虾仁 蛤蜊 扇贝 生蚝 墨鱼 贝 螃蟹 蟹 龙虾 三文鱼 金枪鱼 章鱼 海带 紫苏 芝麻 花生米 腰果 核桃 杏仁 糯米 大米 小米 燕麦 荞麦 意大利面 通心粉 馄饨皮 饺子皮 春卷皮 吐司 淡奶油 车打奶酪 奶油 奶酪`.split(/\s+/).filter(Boolean);
const miss = cand.filter(c => !names.has(c));
console.log('missing:', miss.join(' '));
console.log('dict size', arr.length);
