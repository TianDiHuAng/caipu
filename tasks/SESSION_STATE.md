# 会话交接状态（SESSION_STATE）

> 任何新会话接手时，先读 CLAUDE.md、tasks/TASKS.md、tasks/progress.json、docs/DECISIONS.md，再读本文件。

## 一、当前事实

| 项 | 状态 |
| --- | --- |
| 阶段 0（文档 / 任务清单 / 校验脚本） | 已完成 |
| 阶段 1（monorepo、DB、导入脚本、API、测试） | 已完成（测试通过） |
| 阶段 2（50 道样板菜谱） | 已完成 |
| 阶段 3（网站核心页面 / SEO / 响应式） | 已完成 |
| 阶段 4（按格子批量生产菜谱） | **进行中**：65 道已发布，目标 3274 |
| 阶段 5（性能 / 多语言 / Docker / 移动端指南） | 已完成主体 |
| 阶段 6（全库巡检） | 未开始（依赖阶段 4 数量） |

进度基准：`tasks/progress.json` → totals.target = 3274，totals.actual = 103（口径为「菜谱 × 品类」格子计数，一道菜多品类会重复计）。

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
cd D:\AI\project\marvis_project\caipu
node scripts/validate.mjs
npm run progress
```
确认无错误后，按「二、单批生产关系」继续领格子生产，每批 6 道，批次号接续 `temp/drafts/` 中最大编号。


## 最近一次更新（本轮结束）

- 菜谱库：139 道，validate 全绿；测试 29/29（Node 24）；内容进度 168/3274（5.1%）。
- 第 21 批（6 道）：山东醋椒鱼汤｜嘉兴鲜肉粽｜福州七星鱼丸｜湖南剁辣椒｜韩式猪肉汤饭｜泰式绿咖喱鸡。
- 抽检：`npm run audit` 覆盖 32 菜系，均分 95，无 C/D 级。
- 食材词典补 5 项（粽叶/红辣椒/绿咖喱酱/白酒/小鱼干/辣椒酱，共 325 条）。
- 待办：阶段 4 继续按批推进；下批建议 cantonese/soup、sichuan/staple-noodle、jiangsu/main-seafood。
- 历史批次（第 13-14 批，共 12 道）：
  - cantonese：蚝油生菜、虾仁滑蛋
  - hunan：酸辣藕丁｜anhui：火腿烧笋｜yunguai：汽锅鸡｜sichuan：凉拌腐竹
  - jiangsu：阳春面｜chaoshan：潮汕牛肉丸｜xinjiang：新疆炒米粉｜dongbei：拍黄瓜
  - 第 13 批另含：蒜蓉炒菜心（cantonese）、剁椒蒸芋头（hunan）
- 已确认菜系 slug：潮汕为 `chaoshan`（不是 chaozhou）。
- 待办：阶段 4 内容生产（119/3274，3.6%）。下批建议 sichuan/soup、cantonese/soup、hunan/main-meat、shandong/main-seafood，再接 beijing、taiwan、hongkong 薄弱菜系。
- 每 10 批后执行 `npm run audit`，C/D 级按报告明细重写。
