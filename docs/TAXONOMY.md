# TAXONOMY — 分类体系（穷举）

> 机器可读源：`data/taxonomy.json`。本文件与 `data/taxonomy.json` 必须一致，脚本 `scripts/gen-progress.mjs` 会校验二者同步。
> 所有 slug 进入 URL，**一经发布不得更改**（改名只能新增别名）。

---

## 1. 三层结构

```
region（cn / intl）
  └─ cuisine（菜系，59 个）
       └─ category（品类，25 个）
```

菜谱的 `cuisine.style` 必须是菜系 slug；`category` 必须是品类枚举中的项，且**至少一项属于该菜系的核心品类**（校验脚本强校验，避免出现「川菜 × 爱尔兰炖菜」这类错误归类）。

---

## 2. 菜系清单（59）

层级用于计算内容目标：A=重点菜系，B=常规菜系，C=小众/特色菜系。

### 2.1 中国（region=cn，21 个）

| slug | 中文 | English | 层级 | 核心品类（category slug） |
| --- | --- | --- | --- | --- |
| sichuan | 川菜 | Sichuan | A | main-meat, main-poultry, main-tofu, appetizer, sauce |
| shandong | 鲁菜 | Shandong | A | main-seafood, main-meat, soup, staple-bread, banquet |
| cantonese | 粤菜 | Cantonese | A | main-seafood, soup, main-poultry, staple-rice, dessert |
| jiangsu | 苏菜 | Jiangsu | A | main-seafood, main-meat, soup, appetizer, snack |
| zhejiang | 浙菜 | Zhejiang | A | main-seafood, main-meat, soup, staple-rice, dessert |
| fujian | 闽菜 | Fujian | A | soup, main-seafood, main-meat, snack, sauce |
| hunan | 湘菜 | Hunan | A | main-meat, main-poultry, main-vegetable, appetizer, fermented |
| anhui | 徽菜 | Anhui | A | main-meat, main-vegetable, soup, fermented, staple-bread |
| beijing | 京菜 | Beijing | B | main-meat, staple-noodle, snack, dessert, banquet |
| shanghai | 沪菜 | Shanghai | B | main-meat, main-seafood, appetizer, snack, dessert |
| dongbei | 东北菜 | Northeastern | B | main-vegetable, main-meat, staple-bread, cold-dish, banquet |
| xibei | 西北菜 | Northwestern | B | staple-noodle, staple-bread, main-meat, soup, snack |
| yunguai | 云贵菜 | Yunnan-Guizhou | B | main-vegetable, soup, main-meat, snack, fermented |
| hakka | 客家菜 | Hakka | B | main-meat, main-tofu, soup, fermented, banquet |
| chaoshan | 潮汕菜 | Chaoshan | B | main-seafood, soup, snack, sauce, staple-congee |
| taiwan | 台湾菜 | Taiwanese | B | snack, main-poultry, main-seafood, staple-rice, dessert |
| hongkong | 港澳菜 | Hong Kong-Macau | B | main-seafood, staple-rice, bakery, dessert, drink |
| xinjiang | 新疆菜 | Xinjiang | B | main-meat, staple-bread, staple-noodle, snack, drink |
| halal-cn | 清真菜 | Chinese Halal | B | main-meat, staple-noodle, soup, snack, banquet |
| tibetan | 藏餐 | Tibetan | C | main-meat, staple-bread, soup, drink, staple-noodle |
| mongolian | 内蒙菜 | Inner Mongolian | C | main-meat, staple-bread, drink, soup, dessert |

### 2.2 外国（region=intl，38 个）

| slug | 中文 | English | 层级 | 核心品类 |
| --- | --- | --- | --- | --- |
| japanese | 日本料理 | Japanese | A | main-seafood, staple-rice, soup, appetizer, dessert |
| korean | 韩国料理 | Korean | A | main-meat, soup, staple-rice, fermented, snack |
| thai | 泰国菜 | Thai | A | main-poultry, soup, salad, main-seafood, dessert |
| italian | 意大利菜 | Italian | A | staple-bread, main-poultry, dessert, appetizer, sauce |
| french | 法国菜 | French | A | main-meat, dessert, sauce, soup, bakery |
| spanish | 西班牙菜 | Spanish | A | main-seafood, appetizer, staple-rice, dessert, sauce |
| vietnamese | 越南菜 | Vietnamese | B | soup, staple-noodle, salad, main-meat, drink |
| indonesian | 印尼菜 | Indonesian | B | staple-rice, main-poultry, soup, snack, dessert |
| malaysian | 马来菜 | Malaysian | B | staple-noodle, main-seafood, soup, snack, dessert |
| singaporean | 新加坡菜 | Singaporean | B | staple-rice, main-seafood, soup, snack, drink |
| filipino | 菲律宾菜 | Filipino | B | main-meat, soup, staple-rice, dessert, snack |
| indian | 印度菜 | Indian | A | main-vegetable, main-poultry, staple-bread, soup, dessert |
| south-asian | 南亚菜 | South Asian | B | staple-rice, main-vegetable, soup, snack, dessert |
| middle-eastern | 中东风味 | Middle Eastern | B | appetizer, main-meat, staple-bread, salad, dessert |
| turkish | 土耳其菜 | Turkish | B | main-meat, staple-bread, appetizer, dessert, soup |
| mediterranean | 地中海菜 | Mediterranean | B | salad, main-seafood, appetizer, main-vegetable, sauce |
| greek | 希腊菜 | Greek | B | appetizer, main-meat, salad, dessert, bakery |
| portuguese | 葡萄牙菜 | Portuguese | B | main-seafood, dessert, main-meat, soup, bakery |
| german | 德国菜 | German | B | main-meat, bakery, fermented, salad, dessert |
| british | 英国菜 | British | B | main-meat, bakery, dessert, breakfast, soup |
| irish | 爱尔兰菜 | Irish | C | main-meat, staple-bread, soup, breakfast, drink |
| nordic | 北欧菜 | Nordic | B | main-seafood, bakery, fermented, dessert, breakfast |
| eastern-european | 东欧菜 | Eastern European | B | soup, main-meat, staple-bread, fermented, dessert |
| russian | 俄式菜 | Russian | B | soup, main-meat, salad, bakery, drink |
| american | 美式菜 | American | A | main-meat, bakery, dessert, breakfast, salad |
| american-south | 美国南方菜 | Southern US | B | main-poultry, main-vegetable, bakery, dessert, breakfast |
| tex-mex | 德州墨西哥菜 | Tex-Mex | B | main-meat, snack, sauce, breakfast, main-vegetable |
| cajun | 卡真菜 | Cajun | C | main-seafood, staple-rice, soup, main-poultry, sauce |
| mexican | 墨西哥菜 | Mexican | A | snack, main-meat, sauce, soup, drink |
| peruvian | 秘鲁菜 | Peruvian | C | main-seafood, main-poultry, appetizer, staple-rice, drink |
| brazilian | 巴西菜 | Brazilian | C | main-meat, staple-rice, snack, dessert, drink |
| argentinian | 阿根廷菜 | Argentinian | C | main-meat, sauce, bakery, dessert, drink |
| caribbean | 加勒比菜 | Caribbean | C | main-poultry, main-seafood, staple-rice, drink, dessert |
| north-african | 北非菜 | North African | B | soup, main-vegetable, staple-bread, salad, dessert |
| west-african | 西非菜 | West African | C | staple-rice, soup, main-meat, snack, sauce |
| east-african | 东非菜 | East African | C | main-meat, staple-bread, soup, main-vegetable, drink |
| south-african | 南非菜 | South African | C | main-meat, staple-bread, dessert, snack, salad |
| australian | 澳新菜 | Australian-NZ | C | main-seafood, bakery, breakfast, dessert, salad |

> 说明：`hongkong` 归入中国区域（港澳地方菜系），与「中国之外的国家料理」区分；这是内容分类决策，见 DECISIONS D-006。

---

## 3. 品类清单（25）

| slug | 中文 | English | 说明 |
| --- | --- | --- | --- |
| appetizer | 前菜 | Appetizer | 开胃菜、冷盘、小份头盘 |
| salad | 沙拉 | Salad | 以生鲜蔬果为主体的拌菜（含中式凉拌的「凉菜」另设 cold-dish） |
| cold-dish | 凉菜 | Cold Dish | 中式凉拌/卤味冷盘 |
| soup | 汤羹 | Soup & Broth | 汤、羹、炖汤 |
| main-meat | 主菜·肉 | Meat Main | 猪牛羊等畜肉主菜 |
| main-poultry | 主菜·禽 | Poultry Main | 鸡鸭鹅等禽类主菜 |
| main-seafood | 主菜·海鲜 | Seafood Main | 鱼虾蟹贝类主菜 |
| main-egg | 主菜·蛋 | Egg Main | 以蛋为主体的主菜 |
| main-tofu | 主菜·豆制品 | Tofu & Soy Main | 豆腐、豆干、腐竹等 |
| main-vegetable | 主菜·蔬菜 | Vegetable Main | 以蔬菜为主体的热菜 |
| staple-rice | 主食·饭 | Rice Dish | 米饭、炒饭、烩饭、饭团 |
| staple-noodle | 主食·面 | Noodle Dish | 面条、米粉、意面 |
| staple-bread | 主食·饼 | Bread & Flatbread Staple | 饼、馍、馕、面食主食（非烘焙甜面包） |
| staple-congee | 主食·粥 | Congee & Porridge | 粥、糊、燕麦粥 |
| snack | 小吃街头食物 | Street Food & Snack | 街头小吃、点心、便携小食 |
| bakery | 烘焙面包 | Bakery | 面包、酥皮、烘焙点心（含西式早餐面包） |
| dessert | 甜点 | Dessert | 甜品、糕点、糖水、冰品 |
| drink | 饮品 | Drink | 茶、咖啡、果汁、鸡尾酒、无酒精饮 |
| sauce | 酱汁与基础调味 | Sauce & Base | 酱、蘸料、底汤、复合调味 |
| fermented | 腌制发酵 | Pickle & Ferment | 泡菜、腌菜、酱腌、发酵调味 |
| breakfast | 早餐 | Breakfast | 成套早餐组合 |
| kids | 儿童餐 | Kids-Friendly | 少辣少盐、适口性好 |
| banquet | 宴客菜 | Banquet | 摆盘与工序适合请客的大菜 |
| low-cal | 低卡健身餐 | Low-Cal & Fitness | 高蛋白/低热量，标注热量 |
| special-diet | 特殊饮食 | Special Diet | 素食、纯素、无麸质、清真等专项 |
| hotpot-bbq | 火锅与烧烤 | Hotpot & BBQ | 火锅、涮锅、烧烤、铁板 |

> 共 26 项（含 `cold-dish`）。品类枚举以 `data/taxonomy.json` 中的 `categories` 数组为准。

---

## 4. 标签枚举

### 4.1 flavor（口味）

`salty` 咸鲜、`spicy` 辣、`numbing` 麻、`sour` 酸、`sweet` 甜、`bitter` 苦、`umami` 鲜、`smoky` 熏烤、`fragrant` 香、`light` 清淡、`rich` 浓郁、`tangy` 酸香、`savory` 咸香、`herbal` 草本

### 4.2 diet_tag（饮食标签）

`vegetarian` 素食（可含蛋奶）、`vegan` 纯素、`gluten-free` 无麸质、`dairy-free` 无乳、`halal` 清真、`kosher` 犹太洁食、`low-carb` 低碳水、`high-protein` 高蛋白、`pescatarian` 鱼素

> 标签必须**由食材推导**，不允许随意声明：`vegetarian` 要求全部食材不含肉/禽/海鲜；`gluten-free` 要求不含小麦、大麦、黑麦及其制品（注意酱油含小麦）。

### 4.3 allergen（过敏原）

`gluten` 麸质、`crustacean` 甲壳类、`mollusk` 软体类、`fish` 鱼、`egg` 蛋、`peanut` 花生、`tree-nut` 树坚果、`soy` 大豆、`milk` 乳、`sesame` 芝麻、`celery` 芹菜、`mustard` 芥末、`sulfite` 亚硫酸盐、`lupin` 羽扇豆

### 4.4 高风险食材（必须写 food_safety_notes）

生食海鲜与生肉、河豚、野生菌、豆角/四季豆（未熟含皂苷）、木薯、发芽土豆、鲜黄花菜、自制发酵品（豆豉/纳豆/酸汤）、溏心蛋、生豆奶、苦杏仁。

---

## 5. 目标数量规则

| 菜系层级 | 核心品类目标 | 非核心品类目标 | 单菜系合计 |
| --- | --- | --- | --- |
| A（重点） | 15 | 3 | ≈ 135 |
| B（常规） | 6 | 1 | ≈ 40 |
| C（小众） | 5 | 1 | ≈ 33 |

- A 级 15 个菜系共约 **2025** 道
- B 级 24 个菜系共约 **960** 道
- C 级 20 个菜系共约 **660** 道
- **总目标 ≈ 3645**，满足「≥3000」要求。

格子总数 = 59 菜系 × 26 品类中**实际存在的组合**（非核心品类目标为 1 的格子仍需至少 1 道）。凡 `data/taxonomy.json` 中标注 `unsupported` 的组合（例如「藏餐 × 沙拉」不成立）目标为 0，不计入。

`tasks/progress.json` 由 `scripts/gen-progress.mjs` 依据本规则生成，不得手改。
