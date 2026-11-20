# 会话交接状态（SESSION_STATE）

> 任何新会话接手时，先读 CLAUDE.md、tasks/TASKS.md、tasks/progress.json、docs/DECISIONS.md，再读本文件。

## 一、当前事实

| 项 | 状态 |
| --- | --- |
| 阶段 0（文档 / 任务清单 / 校验脚本） | 已完成 |
| 阶段 1（monorepo、DB、导入脚本、API、测试） | 已完成（测试通过） |
| 阶段 2（50 道样板菜谱） | 已完成 |
| 阶段 3（网站核心页面 / SEO / 响应式） | 已完成 |
| 阶段 4（按格子批量生产菜谱） | **进行中**：597 道已发布，目标 3274 |
| 阶段 5（性能 / 多语言 / Docker / 移动端指南） | 已完成主体 |
| 阶段 6（全库巡检） | 未开始（依赖阶段 4 数量） |

进度基准：`tasks/progress.json` → totals.target = 3274，totals.actual = 597（口径为「菜谱 × 品类」格子计数，一道菜多品类会重复计）。

## 二、单批生产关系（固定套路，勿改）

1. 用 python 生成草稿 `temp/drafts/batch-NN.json`，草稿用短键以省 token：
   `n`(名称) `a`(数量) `u`(单位) `note`；菜谱级键 `id/zh/en/original/cuisine/category/difficulty/prep/cook/servings/flavor/ingredients/equipment/steps/tips/mistakes/subs/variations/serving/storage/nutrition/safety/origin/tags/related`。
2. `node scripts/author.mjs temp/drafts/batch-NN.json` → 自动展开为正式字段、查食材词典、写 `data/recipes/{region}/{cuisine}/{id}.json`。
   - 已存在文件默认跳过；确需覆盖在草稿中加 `"overwrite": true`。
   - 报「食材未登记 → X」时：把 X 加入 `data/ingredients.json`（字段 key/zh/en/aliases/allergens/category），**不要**为了绕过校验改动菜名。
3. `node scripts/validate.mjs` → 修到 0 错误。
4. 导入：宿主 Node 是 22，better-sqlite3 编译于 24，必须
   `cmd /c "set PATH=D:\Node;%PATH% && npx tsx scripts/import.ts"`。
5. `npm run progress` → 更新 progress.json 与 TASKS.md 勾选。
6. `git add -A && git commit`，提交信息写清本批菜系与菜名。

## 三、写内容时的硬性红线（踩过的坑）

- 步骤文本 ≥ 20 字；`tips[i]` / `food_safety_notes[i]` ≥ 15 字；极简饮品 ≥ 3 步，其余 ≥ 4 步。
- 每份盐 ≤ 6g（盐焗类铺锅粗盐写进 note 且不要把总盐量堆到主料里）。
- 配料表里的食材必须在步骤或 tips 里出现；步骤里提到的食材必须在配料表里。
- **食材名不要用泛称**：`瘦肉`、`鸡`、`辣椒`、`蒜` 等词条一旦进词典，会让大量既有菜谱写「瘦肉」的步骤突然报错；统一用 `猪里脊`、`鸡腿肉`、`大蒜`、`小米辣`。
- `related_ids` 只能写真实存在的 id，不能含自身；跨菜系引用前先确认 id 存在。
- 含鸡蛋/豆角/菌菇/贝类等高风险食材时，`food_safety` 必须出现「安全/彻底加热/中心温度/熟透/不要生食/冷藏」之一。
- `time.total_min` 要 ≥ 步骤时长合计（含熬汤等并行工序时下调单步时长，并在 tip 里写「可提前熬制」）。
- 每份主料总量 ≤ 700g（汤、高汤放 seasoning 分组，不要放 main）。
- 油炸类总油量上限 270ml（非油炸 360ml）；「复炸」步骤必须写明 `植物油`，否则判未使用。
- `common_mistakes` 每条 ≥ 15 字，`origin_note` ≥ 40 字。
- 步骤里的比喻别用食材名（如「黄豆粒大小」会判为未登记的黄豆），改用「小指盖大小」。
- author.mjs 会把食材名规范化（「牛腱肉」→「牛腱」、「河虾仁」→「虾仁」），步骤文本须按落库名书写。
- 单字食材名（如「虾」）无法被 coveredByDeclared 豁免，含虾菜品慎用「虾仁」写法，或改用干贝、干鱿鱼丝等词条。
- 手写 recipe JSON 时字段必须是 `name{zh,en,original}` / `time{prep_min,cook_min,total_min}` / `steps[].{n,text,time_min,heat,tip,visual_cue}`。

## 四、下批推荐格子（热门优先）

| 菜系 | 品类 | 已完成/目标 |
| --- | --- | --- |
| sichuan | main-meat / soup / staple-noodle | 9 / 15（主力） |
| cantonese | main-seafood / soup | 7 / 15 |
| hunan | main-meat | 6 / 15 |
| shandong | main-seafood / main-meat | 5 / 15 |
| jiangsu / zhejiang | main-meat / main-seafood | 3-4 / 15 |
| japanese / thai / korean / vietnamese | main-* | 1-3 / 15 |
| 其余 40 余个菜系 | core 品类 | 0 / 5-15 |

## 五、新会话第一步

```
cd E:\ai_project\marvis_project\caipu
node scripts/validate.mjs
npm run progress
```
确认无错误后，按「二、单批生产关系」继续领格子生产，每批 6 道，批次号接续 `temp/drafts/` 中最大编号。

## 较早更新（batch-66~75 阶段）

- 工作区已迁移至 `E:\ai_project\marvis_project\caipu`，本文件内旧路径已全部替换。
- 菜谱库：485 道，validate 全绿（485 文件 / 0 错误）；内容进度 597/3274（18.2%）。
- 第 66 批（6 道，commit 38a2bf2）：徽州刀板香｜徽州包袱饺｜徽州腊八豆腐｜无锡油面筋塞肉｜宁波蟹炒年糕｜雪菜大汤黄鱼。
- 第 67 批（6 道，commit 65011f6）：厦门沙茶面｜闽南姜母鸭｜闽南炸醋肉｜客家三杯鸡｜南昌拌粉｜南昌瓦罐汤。
- 第 68 批（6 道，commit f4c91d5）：蒜蓉粉丝蒸扇贝｜莲藕排骨汤｜干煎带鱼｜醋溜土豆丝｜干菜焖肉｜油爆虾。
- 第 69 批（6 道，commit b3332f6）：连锅汤｜小米辣炒蛋｜豉油煎豆腐｜木须肉｜照烧鸡腿｜大酱汤。
- 第 70 批（6 道，commit 0ba7792）：清蒸鲈鱼｜客家梅菜扣肉｜台式三杯中卷｜香煎鳕鱼｜越式牛肉粉｜莼菜干贝羹。
- 第 71 批（6 道，commit 439d13f）：豉椒炒蛏子｜干煎大明虾｜椒盐龙利鱼柳｜清蒸石斑鱼（粤）｜酥肉冬瓜汤｜豌豆尖肉丸汤（川）。
- 第 72 批（6 道，commit 8f598cb）：花雕蒸花蟹（粤）｜冰糖肘子｜博山炸肉（鲁）｜日式生姜烧猪肉｜泰式烤猪颈肉｜泰式鱼饼。
- 第 73 批（6 道，commit e544422）：豉汁蒸鳝片｜香煎黄鱼（粤）｜京酱肉丝（鲁）｜番茄煎蛋汤（川）｜日式汉堡排｜泰式黄咖喱鸡。
- 第 74 批（实际入库 4 道，commit 1a951fa）：红烧鲍鱼（粤）｜四喜丸子（鲁）｜紫菜蛋花汤（川）｜日式炸猪排；原计划的山东糖醋鲤鱼与泰式椰奶鸡汤与既有文件重名（id 冲突），已删除草稿与残缺数据文件，改由下批替代。
- 第 75 批（6 道，commit 00be2c4）：香酥虾｜黄焖猪蹄（鲁）｜清蒸白鲳鱼（粤）｜白菜豆腐汤（川）｜日式猪肉涮涮锅｜泰式红咖喱猪肉；本批同时清除了上一批遗留的 2 个重复文件。
- 第 70 批 audit（满 10 批节点）：平均 97 分，抽样 49 道全部 A 级，C/D 级 0 道，无需重写。
- 待办：阶段 4 继续按批推进（下批从 batch-76 起）；建议 cantonese/main-seafood、sichuan/soup、shandong/main-meat、japanese/main-meat、thai 的汤/咖喱格。
- 已知遗留重复（同菜异 id，共 8 组）：蒜蓉粉丝蒸扇贝、豉油鸡、豉汁蒸排骨、南京盐水鸭、蒜泥白肉、宋嫂鱼羹、西湖牛肉羹、照烧鸡腿各 2 份，需在阶段 6 全库巡检时统一去重。
- 每 10 批后执行 npm run audit，C/D 级按报告明细重写。

## 最近一次更新（本轮结束）

- 菜谱库：546 道，validate 全绿（546 文件 / 0 错误）；`npm test` 29/29 通过；progress 内容进度 633/3274（19.3%）。
- 数据对齐核查（本轮）：`data/db/caipu.sqlite` recipes 表 534 条 = 菜谱文件 534 个，id 一一对应，无残留旧记录或重复（db-only 0 / file-only 0）；progress 的 619 为「菜谱×品类」格子累加值（449 道 1 格、85 道 2 格），与文件数口径不同，属正常，无需清理重导。
- 阶段 6 去重已完成（commit c015502）：8 组同菜异 id 重复各保留质量更优一份，`related_ids` 全量重映射，删除冗余文件 8 个：
  - cantonese-suanrong-fensi-zheng-shanbei.json（保留 suanrong-fensi-shanbei）
  - cantonese-siyou-ji.json（保留 chiyou-ji）
  - cantonese-chizhi-paigu.json（保留 chizhi-zheng-paigu）
  - jiangsu-yanshui-ya.json（保留 nanjing-yanshui-ya）
  - sichuan-suanni-bairou.json（保留 suan-ni-bai-rou）
  - zhejiang-songsao-yugen.json（保留 songsao-yugeng）
  - zhejiang-xihu-niurougeng.json（保留 xihu-niurou-geng）
  - japanese-teriyaki-chicken.json（保留 japanese-zhaoshao-jitui）
- 同批修复 `basil` / `thai-basil` 别名指向冲突（同一别名不得指向两个食材），去重后无悬挂引用。
- 第 76 批（6 道，commit 1ad6ccd）：美式考伯沙拉｜法式樱桃克拉芙缇｜印度坦都里烤鸡｜意式炸饭团｜墨西哥香普拉多｜泰式猪骨清汤。
- 第 77 批（6 道，commit db707d4）：美式薯饼｜美式焖烤牛肉｜法式巧克力面包｜印度玫瑰蜜炸球｜韩式酱土豆烧鸡｜西班牙杏仁酥饼。
- 第 78 批（6 道，commit a3bc78a）：意式蔬菜汤｜意式番茄面包沙拉｜日式玉子烧｜墨西哥酸柑烤猪｜墨西哥炒豆泥｜泰式炒河粉。
- 第 79 批（6 道，commit 623aabd）：美式白脱牛奶饼干｜韩式泡菜煎饼｜墨西哥红莎莎酱｜西班牙白酒煮蛤蜊｜西班牙鸡肉饭｜泰式酸辣粉丝沙拉。
- 第 80 批（6 道，commit ca61fc4）：日式筑前煮｜日式可乐饼｜意式茄子面（诺尔玛）｜印度菠菜鸡肉咖喱｜美式芝士通心粉｜墨西哥青柠烤鸡腿。
- 第 80 批 audit（满 10 批节点）：平均 97 分，抽样 55 道，需重写 0 道。
- 遗留观察：库内仍有 6 组「跨菜系同名」菜（京酱肉丝 京/鲁、清蒸鲈鱼 粤/苏、香煎鳕鱼 粤/港、紫菜蛋花汤 粤/川、三杯鸡 客家/浙、油爆虾 苏/沪），属不同菜系独立版本，暂不合并，待阶段 6 全库巡检统一决策。
- 第 81 批（6 道，commit ffcb35c）：北京豌豆黄｜北京炒肝｜北京驴打滚｜上海蟹壳黄｜上海条头糕｜北京烧二冬。
- 第 82 批（6 道，commit 4f58efb）：云南小米辣炒苦瓜｜云南洋芋粑｜贵州糟辣椒｜客家咸菜猪肚汤｜客家酸萝卜｜潮汕蚝烙。
- 第 83 批（6 道，commit 1c3afa6）：日式油豆腐乌冬｜泰式香草煎蛋｜越南鸡肉凉拌菜｜越南椰汁焖猪肉｜法式香草蛋卷｜意式焗茄子千层。
- 第 83 批新增食材登记：`udon`（乌冬面，grain，allergens: gluten），词典 428 项。
- 第 84 批（6 道，commit 待填）：日式咖喱饭｜韩式泡菜炒饭｜意式番茄罗勒酱｜法式土豆大葱浓汤｜印度酸辣胡椒汤｜墨西哥洛神花茶饮。
- 第 84 批新增食材登记：`hibiscus`（洛神花，dried-fruit），词典 429 项。
- 当前库：558 道，validate 全绿（558 文件 / 0 错误）；progress 内容进度 645/3274（19.7%）。
- 待办：阶段 4 继续（下批从 batch-85 起），优先补 intl 菜系 core 品类与 cn 中低覆盖格子。
