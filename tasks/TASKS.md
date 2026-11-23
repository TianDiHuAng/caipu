# 任务清单

> 本文件由 `scripts/sync-tasks.mjs` 自动生成，请勿直接编辑。
> 工程任务源：`tasks/engineering.json`；内容任务源：`tasks/progress.json`。
> 生成时间：2026-11-23T08:05:42.318Z

**总览**：工程任务 49/53；菜谱内容 1240/3274（37.9%），共 591 个「菜系 × 品类」格子，59 个菜系。

## 阶段 0 文档与任务清单

- [x] `P0-01` docs/PRD.md 用户、场景、功能、页面清单
- [x] `P0-02` docs/SCHEMA.md + schema/recipe.schema.json
- [x] `P0-03` docs/TAXONOMY.md + data/taxonomy.json 分类体系
- [x] `P0-04` docs/STYLE.md 写作规范与质量门槛
- [x] `P0-05` docs/DECISIONS.md 决策日志
- [x] `P0-06` data/ingredients.json 食材词典（中英名/别名/过敏原）
- [x] `P0-07` scripts/validate 校验脚本（8 项质量门槛 + 一致性规则）
- [x] `P0-08` tasks/progress.json 与 tasks/TASKS.md 生成脚本

## 阶段 1 项目骨架、数据库、导入脚本、API 与测试

- [x] `P1-01` 根工作区：package.json workspaces、tsconfig、.gitignore、.editorconfig
- [x] `P1-02` packages/shared：菜谱类型、份量换算、单位换算、格式化工具
- [x] `P1-03` packages/db：Drizzle ORM schema（SQLite→PostgreSQL 可迁移）
- [x] `P1-04` packages/db：迁移与建库脚本
- [x] `P1-05` scripts/import.mjs：JSON 源数据导入数据库（幂等）
- [x] `P1-06` 导入脚本自动化测试
- [x] `P1-07` apps/api：Fastify 骨架、配置、错误处理、CORS、请求日志
- [x] `P1-08` API：GET /health 与 GET /api/v1/meta 分类树
- [x] `P1-09` API：GET /api/v1/recipes 列表（分页/筛选/排序）
- [x] `P1-10` API：GET /api/v1/recipes/:id 详情
- [x] `P1-11` API：GET /api/v1/search 关键词搜索
- [x] `P1-12` API：GET /api/v1/filters 筛选项聚合
- [x] `P1-13` API：GET /api/v1/recipes/random 随机推荐
- [x] `P1-14` API：GET /api/v1/ingredients 食材反查
- [x] `P1-15` API 自动化测试套件（node:test + inject）
- [x] `P1-16` docs/API.md 接口文档（含 OpenAPI 描述）
- [x] `P1-17` 验收：npm test 26/26 与 scripts/smoke.mjs 17/17 全通过，记录 STAGE_REPORT.md
- [x] `P1-18` 验收：init + import 幂等重建数据库，health 计数正确

## 阶段 2 五十道样板菜谱

- [x] `P2-01` 样板批次 1：川/粤/鲁/苏/浙 12 道
- [x] `P2-02` 样板批次 2：闽/湘/徽/京/沪 13 道
- [x] `P2-03` 样板批次 3：日/韩/泰/意/法 12 道
- [x] `P2-04` 样板批次 4：印/美/墨/中东/烘焙甜点饮品 13 道
- [x] `P2-05` 50 道样板全量 validate 通过并回写 STYLE.md 质量标准

## 阶段 3 网站核心页面、SEO、响应式

- [x] `P3-01` apps/web：Next.js + TypeScript + Tailwind 骨架与布局
- [x] `P3-02` 首页：搜索入口、热门菜系、精选菜谱、分类导航
- [x] `P3-03` 分类树页 /categories 与分类详情 /categories/[slug]
- [x] `P3-04` 菜系列表 /cuisines 与菜系详情 /cuisines/[slug]
- [x] `P3-05` 菜谱详情页 /recipes/[id]（分组配料、步骤、贴士、换算控件）
- [x] `P3-06` 搜索页 /search（关键词 + 多维筛选）
- [x] `P3-07` 食材反查页 /ingredients 与 /ingredients/[slug]
- [x] `P3-08` 份量换算与单位切换组件（客户端计算）
- [x] `P3-09` 打印视图 /recipes/[id]/print
- [x] `P3-10` SEO：metadata、schema.org/Recipe、sitemap.xml、robots.txt、Open Graph
- [x] `P3-11` 响应式与可访问性验收（移动端断点、语义化标签、对比度）

## 阶段 4 内容批量生产（按 progress.json 格子推进，明细见下）

_内容任务见下方「阶段 4」章节，每个格子一行。_

## 阶段 5 搜索优化、多语言、性能、Docker、文档

- [x] `P5-01` 搜索优化：权重排序、同义词、拼音扩展、高亮
- [x] `P5-02` 多语言界面（zh/en）与 locale 路由
- [x] `P5-03` 性能优化：缓存、图片占位、ISR/SSG、索引优化
- [x] `P5-04` Docker 与 docker compose 一键启动
- [x] `P5-05` README（运行、新增菜谱、对接 App/小程序）
- [x] `P5-06` docs/MOBILE_API.md 移动端对接指南
- [x] `P5-07` docs/DEPLOY.md 部署文档

## 阶段 6 全库质量巡检与收尾

- [ ] `P6-01` 全库 validate + 测试全绿，修复所有 [BLOCKED]
- [ ] `P6-02` 每个菜系完成至少一次 5% 随机抽检并修复不合格项
- [ ] `P6-03` tasks/FINAL_CHECK.md 终止条件逐项自检
- [ ] `P6-04` tasks/STAGE_REPORT.md 各阶段验收记录

## 阶段 4 内容批量生产（按 progress.json 格子推进，明细见下）

### 中国菜系（560/1339）

<details><summary><b>川菜 sichuan</b> — A 级，65/107</summary>

- [ ] `P4-sichuan/main-meat` 主菜·肉（Meat Main）目标 15，已完成 11
- [ ] `P4-sichuan/main-poultry` 主菜·禽（Poultry Main）目标 15，已完成 5
- [ ] `P4-sichuan/main-tofu` 主菜·豆制品（Tofu Main）目标 15，已完成 5
- [ ] `P4-sichuan/appetizer` 前菜（Appetizer）目标 15，已完成 5
- [ ] `P4-sichuan/sauce` 酱汁与基础调味（Sauce）目标 15，已完成 4
- [ ] `P4-sichuan/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 6
- [ ] `P4-sichuan/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-sichuan/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 3
- [ ] `P4-sichuan/staple-rice` 主食·饭（Rice Dish）目标 8，已完成 1
- [x] `P4-sichuan/soup` 汤羹（Soup）目标 0，已完成 10
- [x] `P4-sichuan/cold-dish` 凉菜（Cold Dish）目标 0，已完成 5
- [x] `P4-sichuan/snack` 小吃（Street Food）目标 0，已完成 3
- [x] `P4-sichuan/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 3
- [x] `P4-sichuan/banquet` 宴客菜（Banquet）目标 0，已完成 2
- [x] `P4-sichuan/hotpot-bbq` 火锅与烧烤（Hotpot & BBQ）目标 0，已完成 1

</details>

<details><summary><b>鲁菜 shandong</b> — A 级，47/107</summary>

- [ ] `P4-shandong/main-seafood` 主菜·海鲜（Seafood Main）目标 15，已完成 9
- [ ] `P4-shandong/main-meat` 主菜·肉（Meat Main）目标 15，已完成 11
- [ ] `P4-shandong/soup` 汤羹（Soup）目标 15，已完成 5
- [ ] `P4-shandong/staple-bread` 主食·饼（Bread Staple）目标 15，已完成 5
- [ ] `P4-shandong/banquet` 宴客菜（Banquet）目标 15，已完成 5
- [ ] `P4-shandong/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 2
- [ ] `P4-shandong/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-shandong/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 0
- [ ] `P4-shandong/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 1
- [x] `P4-shandong/snack` 小吃（Street Food）目标 0，已完成 3
- [x] `P4-shandong/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 2
- [x] `P4-shandong/appetizer` 前菜（Appetizer）目标 0，已完成 2
- [x] `P4-shandong/breakfast` 早餐（Breakfast）目标 0，已完成 1

</details>

<details><summary><b>粤菜 cantonese</b> — A 级，63/122</summary>

- [x] `P4-cantonese/main-seafood` 主菜·海鲜（Seafood Main）目标 15，已完成 18
- [ ] `P4-cantonese/main-meat` 主菜·肉（Meat Main）目标 15，已完成 8
- [ ] `P4-cantonese/soup` 汤羹（Soup）目标 15，已完成 7
- [ ] `P4-cantonese/main-poultry` 主菜·禽（Poultry Main）目标 15，已完成 5
- [ ] `P4-cantonese/staple-rice` 主食·饭（Rice Dish）目标 15，已完成 6
- [ ] `P4-cantonese/dessert` 甜点（Dessert）目标 15，已完成 5
- [ ] `P4-cantonese/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 6
- [ ] `P4-cantonese/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 2
- [ ] `P4-cantonese/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 1
- [ ] `P4-cantonese/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 1
- [x] `P4-cantonese/appetizer` 前菜（Appetizer）目标 0，已完成 2
- [x] `P4-cantonese/snack` 小吃（Street Food）目标 0，已完成 2

</details>

<details><summary><b>苏菜 jiangsu</b> — A 级，42/107</summary>

- [ ] `P4-jiangsu/main-seafood` 主菜·海鲜（Seafood Main）目标 15，已完成 8
- [ ] `P4-jiangsu/main-meat` 主菜·肉（Meat Main）目标 15，已完成 5
- [ ] `P4-jiangsu/soup` 汤羹（Soup）目标 15，已完成 6
- [ ] `P4-jiangsu/appetizer` 前菜（Appetizer）目标 15，已完成 4
- [ ] `P4-jiangsu/snack` 小吃（Street Food）目标 15，已完成 5
- [ ] `P4-jiangsu/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 2
- [ ] `P4-jiangsu/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 2
- [ ] `P4-jiangsu/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 2
- [ ] `P4-jiangsu/staple-rice` 主食·饭（Rice Dish）目标 8，已完成 1
- [x] `P4-jiangsu/cold-dish` 凉菜（Cold Dish）目标 0，已完成 3
- [x] `P4-jiangsu/dessert` 甜点（Dessert）目标 0，已完成 2
- [x] `P4-jiangsu/breakfast` 早餐（Breakfast）目标 0，已完成 1
- [x] `P4-jiangsu/banquet` 宴客菜（Banquet）目标 0，已完成 1

</details>

<details><summary><b>浙菜 zhejiang</b> — A 级，41/107</summary>

- [ ] `P4-zhejiang/main-seafood` 主菜·海鲜（Seafood Main）目标 15，已完成 6
- [ ] `P4-zhejiang/main-meat` 主菜·肉（Meat Main）目标 15，已完成 5
- [ ] `P4-zhejiang/soup` 汤羹（Soup）目标 15，已完成 7
- [ ] `P4-zhejiang/staple-rice` 主食·饭（Rice Dish）目标 15，已完成 5
- [ ] `P4-zhejiang/dessert` 甜点（Dessert）目标 15，已完成 6
- [ ] `P4-zhejiang/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 2
- [ ] `P4-zhejiang/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-zhejiang/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 1
- [ ] `P4-zhejiang/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 1
- [x] `P4-zhejiang/snack` 小吃（Street Food）目标 0，已完成 2
- [x] `P4-zhejiang/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 2
- [x] `P4-zhejiang/breakfast` 早餐（Breakfast）目标 0，已完成 1
- [x] `P4-zhejiang/appetizer` 前菜（Appetizer）目标 0，已完成 1
- [x] `P4-zhejiang/banquet` 宴客菜（Banquet）目标 0，已完成 1

</details>

<details><summary><b>闽菜 fujian</b> — A 级，40/107</summary>

- [ ] `P4-fujian/soup` 汤羹（Soup）目标 15，已完成 6
- [ ] `P4-fujian/main-seafood` 主菜·海鲜（Seafood Main）目标 15，已完成 6
- [ ] `P4-fujian/main-meat` 主菜·肉（Meat Main）目标 15，已完成 8
- [ ] `P4-fujian/snack` 小吃（Street Food）目标 15，已完成 6
- [ ] `P4-fujian/sauce` 酱汁与基础调味（Sauce）目标 15，已完成 4
- [ ] `P4-fujian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 2
- [ ] `P4-fujian/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-fujian/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 1
- [ ] `P4-fujian/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 2
- [x] `P4-fujian/dessert` 甜点（Dessert）目标 0，已完成 2
- [x] `P4-fujian/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 1
- [x] `P4-fujian/staple-rice` 主食·饭（Rice Dish）目标 0，已完成 1

</details>

<details><summary><b>湘菜 hunan</b> — A 级，39/107</summary>

- [ ] `P4-hunan/main-meat` 主菜·肉（Meat Main）目标 15，已完成 7
- [ ] `P4-hunan/main-poultry` 主菜·禽（Poultry Main）目标 15，已完成 5
- [ ] `P4-hunan/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 15，已完成 8
- [ ] `P4-hunan/appetizer` 前菜（Appetizer）目标 15，已完成 4
- [ ] `P4-hunan/fermented` 腌制发酵（Pickle & Ferment）目标 15，已完成 5
- [ ] `P4-hunan/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-hunan/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 1
- [ ] `P4-hunan/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 1
- [ ] `P4-hunan/staple-rice` 主食·饭（Rice Dish）目标 8，已完成 1
- [x] `P4-hunan/cold-dish` 凉菜（Cold Dish）目标 0，已完成 2
- [x] `P4-hunan/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 1
- [x] `P4-hunan/hotpot-bbq` 火锅与烧烤（Hotpot & BBQ）目标 0，已完成 1
- [x] `P4-hunan/snack` 小吃（Street Food）目标 0，已完成 1
- [x] `P4-hunan/soup` 汤羹（Soup）目标 0，已完成 1

</details>

<details><summary><b>徽菜 anhui</b> — A 级，37/107</summary>

- [ ] `P4-anhui/main-meat` 主菜·肉（Meat Main）目标 15，已完成 6
- [ ] `P4-anhui/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 15，已完成 6
- [ ] `P4-anhui/soup` 汤羹（Soup）目标 15，已完成 5
- [ ] `P4-anhui/fermented` 腌制发酵（Pickle & Ferment）目标 15，已完成 4
- [ ] `P4-anhui/staple-bread` 主食·饼（Bread Staple）目标 15，已完成 4
- [ ] `P4-anhui/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-anhui/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 2
- [ ] `P4-anhui/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 1
- [ ] `P4-anhui/staple-rice` 主食·饭（Rice Dish）目标 8，已完成 0
- [x] `P4-anhui/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 2
- [x] `P4-anhui/snack` 小吃（Street Food）目标 0，已完成 2
- [x] `P4-anhui/appetizer` 前菜（Appetizer）目标 0，已完成 2
- [x] `P4-anhui/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-anhui/breakfast` 早餐（Breakfast）目标 0，已完成 1

</details>

<details><summary><b>京菜 beijing</b> — B 级，12/38</summary>

- [ ] `P4-beijing/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-beijing/staple-noodle` 主食·面（Noodle Dish）目标 6，已完成 2
- [ ] `P4-beijing/snack` 小吃（Street Food）目标 6，已完成 3
- [ ] `P4-beijing/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-beijing/banquet` 宴客菜（Banquet）目标 6，已完成 0
- [ ] `P4-beijing/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 1
- [ ] `P4-beijing/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 1
- [x] `P4-beijing/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 1

</details>

<details><summary><b>沪菜 shanghai</b> — B 级，14/38</summary>

- [ ] `P4-shanghai/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-shanghai/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 1
- [ ] `P4-shanghai/appetizer` 前菜（Appetizer）目标 6，已完成 2
- [ ] `P4-shanghai/snack` 小吃（Street Food）目标 6，已完成 3
- [ ] `P4-shanghai/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-shanghai/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-shanghai/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 1
- [x] `P4-shanghai/staple-noodle` 主食·面（Noodle Dish）目标 0，已完成 1
- [x] `P4-shanghai/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-shanghai/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1

</details>

<details><summary><b>东北菜 dongbei</b> — B 级，14/38</summary>

- [ ] `P4-dongbei/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 6，已完成 2
- [ ] `P4-dongbei/main-meat` 主菜·肉（Meat Main）目标 6，已完成 4
- [ ] `P4-dongbei/staple-bread` 主食·饼（Bread Staple）目标 6，已完成 1
- [ ] `P4-dongbei/cold-dish` 凉菜（Cold Dish）目标 6，已完成 2
- [ ] `P4-dongbei/banquet` 宴客菜（Banquet）目标 6，已完成 0
- [ ] `P4-dongbei/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 1
- [ ] `P4-dongbei/main-tofu` 主菜·豆制品（Tofu Main）目标 4，已完成 0
- [x] `P4-dongbei/soup` 汤羹（Soup）目标 0，已完成 2
- [x] `P4-dongbei/appetizer` 前菜（Appetizer）目标 0，已完成 1
- [x] `P4-dongbei/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1

</details>

<details><summary><b>西北菜 xibei</b> — B 级，12/38</summary>

- [ ] `P4-xibei/staple-noodle` 主食·面（Noodle Dish）目标 6，已完成 2
- [ ] `P4-xibei/staple-bread` 主食·饼（Bread Staple）目标 6，已完成 3
- [ ] `P4-xibei/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-xibei/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-xibei/snack` 小吃（Street Food）目标 6，已完成 1
- [ ] `P4-xibei/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-xibei/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 1
- [x] `P4-xibei/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1

</details>

<details><summary><b>云贵菜 yunguai</b> — B 级，14/38</summary>

- [ ] `P4-yunguai/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 6，已完成 1
- [ ] `P4-yunguai/soup` 汤羹（Soup）目标 6，已完成 3
- [ ] `P4-yunguai/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-yunguai/snack` 小吃（Street Food）目标 6，已完成 2
- [ ] `P4-yunguai/fermented` 腌制发酵（Pickle & Ferment）目标 6，已完成 1
- [ ] `P4-yunguai/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [ ] `P4-yunguai/main-tofu` 主菜·豆制品（Tofu Main）目标 4，已完成 0
- [x] `P4-yunguai/staple-noodle` 主食·面（Noodle Dish）目标 0，已完成 3
- [x] `P4-yunguai/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-yunguai/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 1

</details>

<details><summary><b>客家菜 hakka</b> — B 级，14/38</summary>

- [x] `P4-hakka/main-meat` 主菜·肉（Meat Main）目标 6，已完成 6
- [ ] `P4-hakka/main-tofu` 主菜·豆制品（Tofu Main）目标 6，已完成 1
- [ ] `P4-hakka/soup` 汤羹（Soup）目标 6，已完成 1
- [ ] `P4-hakka/fermented` 腌制发酵（Pickle & Ferment）目标 6，已完成 1
- [ ] `P4-hakka/banquet` 宴客菜（Banquet）目标 6，已完成 2
- [ ] `P4-hakka/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 1
- [ ] `P4-hakka/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-hakka/staple-noodle` 主食·面（Noodle Dish）目标 0，已完成 1
- [x] `P4-hakka/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1

</details>

<details><summary><b>潮汕菜 chaoshan</b> — B 级，13/38</summary>

- [ ] `P4-chaoshan/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 3
- [ ] `P4-chaoshan/soup` 汤羹（Soup）目标 6，已完成 1
- [ ] `P4-chaoshan/snack` 小吃（Street Food）目标 6，已完成 3
- [ ] `P4-chaoshan/sauce` 酱汁与基础调味（Sauce）目标 6，已完成 2
- [ ] `P4-chaoshan/staple-congee` 主食·粥（Congee）目标 6，已完成 1
- [ ] `P4-chaoshan/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-chaoshan/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 1
- [x] `P4-chaoshan/main-meat` 主菜·肉（Meat Main）目标 0，已完成 2

</details>

<details><summary><b>台湾菜 taiwan</b> — B 级，17/38</summary>

- [ ] `P4-taiwan/snack` 小吃（Street Food）目标 6，已完成 3
- [ ] `P4-taiwan/main-poultry` 主菜·禽（Poultry Main）目标 6，已完成 3
- [ ] `P4-taiwan/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 3
- [ ] `P4-taiwan/staple-rice` 主食·饭（Rice Dish）目标 6，已完成 1
- [ ] `P4-taiwan/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-taiwan/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-taiwan/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 1
- [x] `P4-taiwan/main-meat` 主菜·肉（Meat Main）目标 0，已完成 2
- [x] `P4-taiwan/staple-noodle` 主食·面（Noodle Dish）目标 0，已完成 2

</details>

<details><summary><b>港澳菜 hongkong</b> — B 级，15/38</summary>

- [ ] `P4-hongkong/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 4
- [ ] `P4-hongkong/staple-rice` 主食·饭（Rice Dish）目标 6，已完成 1
- [ ] `P4-hongkong/bakery` 烘焙面包（Bakery）目标 6，已完成 3
- [ ] `P4-hongkong/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-hongkong/drink` 饮品（Drink）目标 6，已完成 1
- [ ] `P4-hongkong/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-hongkong/main-tofu` 主菜·豆制品（Tofu Main）目标 4，已完成 1
- [x] `P4-hongkong/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1
- [x] `P4-hongkong/main-meat` 主菜·肉（Meat Main）目标 0，已完成 1
- [x] `P4-hongkong/staple-noodle` 主食·面（Noodle Dish）目标 0，已完成 1

</details>

<details><summary><b>新疆菜 xinjiang</b> — B 级，13/38</summary>

- [ ] `P4-xinjiang/main-meat` 主菜·肉（Meat Main）目标 6，已完成 3
- [ ] `P4-xinjiang/staple-bread` 主食·饼（Bread Staple）目标 6，已完成 1
- [ ] `P4-xinjiang/staple-noodle` 主食·面（Noodle Dish）目标 6，已完成 3
- [ ] `P4-xinjiang/snack` 小吃（Street Food）目标 6，已完成 2
- [ ] `P4-xinjiang/drink` 饮品（Drink）目标 6，已完成 1
- [ ] `P4-xinjiang/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 1
- [ ] `P4-xinjiang/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-xinjiang/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-xinjiang/staple-rice` 主食·饭（Rice Dish）目标 0，已完成 1

</details>

<details><summary><b>清真菜 halal-cn</b> — B 级，17/38</summary>

- [x] `P4-halal-cn/main-meat` 主菜·肉（Meat Main）目标 6，已完成 7
- [ ] `P4-halal-cn/staple-noodle` 主食·面（Noodle Dish）目标 6，已完成 2
- [ ] `P4-halal-cn/soup` 汤羹（Soup）目标 6，已完成 3
- [ ] `P4-halal-cn/snack` 小吃（Street Food）目标 6，已完成 3
- [ ] `P4-halal-cn/banquet` 宴客菜（Banquet）目标 6，已完成 1
- [ ] `P4-halal-cn/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-halal-cn/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-halal-cn/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1

</details>

<details><summary><b>藏餐 tibetan</b> — C 级，15/25</summary>

- [ ] `P4-tibetan/main-meat` 主菜·肉（Meat Main）目标 5，已完成 4
- [ ] `P4-tibetan/staple-bread` 主食·饼（Bread Staple）目标 5，已完成 4
- [ ] `P4-tibetan/soup` 汤羹（Soup）目标 5，已完成 2
- [ ] `P4-tibetan/drink` 饮品（Drink）目标 5，已完成 1
- [ ] `P4-tibetan/staple-noodle` 主食·面（Noodle Dish）目标 5，已完成 3
- [x] `P4-tibetan/staple-rice` 主食·饭（Rice Dish）目标 0，已完成 1

</details>

<details><summary><b>内蒙菜 mongolian</b> — C 级，16/25</summary>

- [x] `P4-mongolian/main-meat` 主菜·肉（Meat Main）目标 5，已完成 8
- [ ] `P4-mongolian/staple-bread` 主食·饼（Bread Staple）目标 5，已完成 2
- [ ] `P4-mongolian/drink` 饮品（Drink）目标 5，已完成 1
- [ ] `P4-mongolian/soup` 汤羹（Soup）目标 5，已完成 2
- [ ] `P4-mongolian/dessert` 甜点（Dessert）目标 5，已完成 2
- [x] `P4-mongolian/staple-noodle` 主食·面（Noodle Dish）目标 0，已完成 1

</details>

### 外国菜系（680/1935）

<details><summary><b>日本料理 japanese</b> — A 级，39/107</summary>

- [ ] `P4-japanese/main-seafood` 主菜·海鲜（Seafood Main）目标 15，已完成 4
- [ ] `P4-japanese/staple-rice` 主食·饭（Rice Dish）目标 15，已完成 5
- [ ] `P4-japanese/soup` 汤羹（Soup）目标 15，已完成 5
- [ ] `P4-japanese/appetizer` 前菜（Appetizer）目标 15，已完成 5
- [ ] `P4-japanese/dessert` 甜点（Dessert）目标 15，已完成 4
- [ ] `P4-japanese/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 1
- [ ] `P4-japanese/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 2
- [ ] `P4-japanese/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 0
- [ ] `P4-japanese/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 1
- [x] `P4-japanese/main-meat` 主菜·肉（Meat Main）目标 0，已完成 5
- [x] `P4-japanese/snack` 小吃（Street Food）目标 0，已完成 3
- [x] `P4-japanese/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 2
- [x] `P4-japanese/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1
- [x] `P4-japanese/breakfast` 早餐（Breakfast）目标 0，已完成 1

</details>

<details><summary><b>韩国料理 korean</b> — A 级，36/107</summary>

- [ ] `P4-korean/main-meat` 主菜·肉（Meat Main）目标 15，已完成 5
- [ ] `P4-korean/soup` 汤羹（Soup）目标 15，已完成 5
- [ ] `P4-korean/staple-rice` 主食·饭（Rice Dish）目标 15，已完成 6
- [ ] `P4-korean/fermented` 腌制发酵（Pickle & Ferment）目标 15，已完成 5
- [ ] `P4-korean/snack` 小吃（Street Food）目标 15，已完成 5
- [ ] `P4-korean/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 1
- [ ] `P4-korean/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 0
- [ ] `P4-korean/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 1
- [ ] `P4-korean/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 2
- [x] `P4-korean/hotpot-bbq` 火锅与烧烤（Hotpot & BBQ）目标 0，已完成 2
- [x] `P4-korean/sauce` 酱汁与基础调味（Sauce）目标 0，已完成 1
- [x] `P4-korean/appetizer` 前菜（Appetizer）目标 0，已完成 1
- [x] `P4-korean/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 1
- [x] `P4-korean/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1

</details>

<details><summary><b>泰国菜 thai</b> — A 级，33/107</summary>

- [ ] `P4-thai/main-poultry` 主菜·禽（Poultry Main）目标 15，已完成 4
- [ ] `P4-thai/soup` 汤羹（Soup）目标 15，已完成 5
- [ ] `P4-thai/salad` 沙拉（Salad）目标 15，已完成 5
- [ ] `P4-thai/main-seafood` 主菜·海鲜（Seafood Main）目标 15，已完成 5
- [ ] `P4-thai/dessert` 甜点（Dessert）目标 15，已完成 4
- [ ] `P4-thai/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 1
- [ ] `P4-thai/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-thai/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 0
- [ ] `P4-thai/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 3
- [x] `P4-thai/main-meat` 主菜·肉（Meat Main）目标 0，已完成 3
- [x] `P4-thai/staple-rice` 主食·饭（Rice Dish）目标 0，已完成 1
- [x] `P4-thai/appetizer` 前菜（Appetizer）目标 0，已完成 1

</details>

<details><summary><b>意大利菜 italian</b> — A 级，34/107</summary>

- [ ] `P4-italian/staple-bread` 主食·饼（Bread Staple）目标 15，已完成 4
- [ ] `P4-italian/main-poultry` 主菜·禽（Poultry Main）目标 15，已完成 4
- [ ] `P4-italian/dessert` 甜点（Dessert）目标 15，已完成 5
- [ ] `P4-italian/appetizer` 前菜（Appetizer）目标 15，已完成 4
- [ ] `P4-italian/sauce` 酱汁与基础调味（Sauce）目标 15，已完成 4
- [ ] `P4-italian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 1
- [ ] `P4-italian/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 0
- [ ] `P4-italian/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 0
- [ ] `P4-italian/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 4
- [x] `P4-italian/cold-dish` 凉菜（Cold Dish）目标 0，已完成 2
- [x] `P4-italian/main-meat` 主菜·肉（Meat Main）目标 0，已完成 2
- [x] `P4-italian/staple-rice` 主食·饭（Rice Dish）目标 0，已完成 2
- [x] `P4-italian/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 1
- [x] `P4-italian/soup` 汤羹（Soup）目标 0，已完成 1

</details>

<details><summary><b>法国菜 french</b> — A 级，33/107</summary>

- [ ] `P4-french/main-meat` 主菜·肉（Meat Main）目标 15，已完成 5
- [ ] `P4-french/dessert` 甜点（Dessert）目标 15，已完成 4
- [ ] `P4-french/sauce` 酱汁与基础调味（Sauce）目标 15，已完成 4
- [ ] `P4-french/soup` 汤羹（Soup）目标 15，已完成 4
- [ ] `P4-french/bakery` 烘焙面包（Bakery）目标 15，已完成 5
- [ ] `P4-french/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 2
- [ ] `P4-french/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-french/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 0
- [ ] `P4-french/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 0
- [x] `P4-french/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 2
- [x] `P4-french/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 2
- [x] `P4-french/snack` 小吃（Street Food）目标 0，已完成 1
- [x] `P4-french/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-french/breakfast` 早餐（Breakfast）目标 0，已完成 1
- [x] `P4-french/appetizer` 前菜（Appetizer）目标 0，已完成 1

</details>

<details><summary><b>西班牙菜 spanish</b> — A 级，33/107</summary>

- [ ] `P4-spanish/main-seafood` 主菜·海鲜（Seafood Main）目标 15，已完成 6
- [ ] `P4-spanish/appetizer` 前菜（Appetizer）目标 15，已完成 6
- [ ] `P4-spanish/staple-rice` 主食·饭（Rice Dish）目标 15，已完成 5
- [ ] `P4-spanish/dessert` 甜点（Dessert）目标 15，已完成 4
- [ ] `P4-spanish/sauce` 酱汁与基础调味（Sauce）目标 15，已完成 5
- [ ] `P4-spanish/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 1
- [ ] `P4-spanish/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-spanish/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 0
- [ ] `P4-spanish/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 0
- [x] `P4-spanish/soup` 汤羹（Soup）目标 0，已完成 3
- [x] `P4-spanish/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1
- [x] `P4-spanish/breakfast` 早餐（Breakfast）目标 0，已完成 1

</details>

<details><summary><b>越南菜 vietnamese</b> — B 级，16/38</summary>

- [ ] `P4-vietnamese/soup` 汤羹（Soup）目标 6，已完成 3
- [ ] `P4-vietnamese/staple-noodle` 主食·面（Noodle Dish）目标 6，已完成 3
- [ ] `P4-vietnamese/salad` 沙拉（Salad）目标 6，已完成 1
- [ ] `P4-vietnamese/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-vietnamese/drink` 饮品（Drink）目标 6，已完成 0
- [ ] `P4-vietnamese/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-vietnamese/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-vietnamese/snack` 小吃（Street Food）目标 0，已完成 3
- [x] `P4-vietnamese/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 1
- [x] `P4-vietnamese/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 1
- [x] `P4-vietnamese/appetizer` 前菜（Appetizer）目标 0，已完成 1
- [x] `P4-vietnamese/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1

</details>

<details><summary><b>印尼菜 indonesian</b> — B 级，12/38</summary>

- [ ] `P4-indonesian/staple-rice` 主食·饭（Rice Dish）目标 6，已完成 1
- [ ] `P4-indonesian/main-poultry` 主菜·禽（Poultry Main）目标 6，已完成 3
- [ ] `P4-indonesian/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-indonesian/snack` 小吃（Street Food）目标 6，已完成 2
- [ ] `P4-indonesian/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-indonesian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-indonesian/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-indonesian/main-meat` 主菜·肉（Meat Main）目标 0，已完成 1
- [x] `P4-indonesian/hotpot-bbq` 火锅与烧烤（Hotpot & BBQ）目标 0，已完成 1

</details>

<details><summary><b>马来菜 malaysian</b> — B 级，13/38</summary>

- [ ] `P4-malaysian/staple-noodle` 主食·面（Noodle Dish）目标 6，已完成 2
- [ ] `P4-malaysian/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 2
- [ ] `P4-malaysian/soup` 汤羹（Soup）目标 6，已完成 1
- [ ] `P4-malaysian/snack` 小吃（Street Food）目标 6，已完成 4
- [ ] `P4-malaysian/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-malaysian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-malaysian/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-malaysian/staple-rice` 主食·饭（Rice Dish）目标 0，已完成 1
- [x] `P4-malaysian/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1

</details>

<details><summary><b>新加坡菜 singaporean</b> — B 级，15/38</summary>

- [ ] `P4-singaporean/staple-rice` 主食·饭（Rice Dish）目标 6，已完成 1
- [ ] `P4-singaporean/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 2
- [ ] `P4-singaporean/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-singaporean/snack` 小吃（Street Food）目标 6，已完成 3
- [ ] `P4-singaporean/drink` 饮品（Drink）目标 6，已完成 1
- [ ] `P4-singaporean/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-singaporean/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-singaporean/staple-noodle` 主食·面（Noodle Dish）目标 0，已完成 3
- [x] `P4-singaporean/main-meat` 主菜·肉（Meat Main）目标 0，已完成 1
- [x] `P4-singaporean/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-singaporean/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 1

</details>

<details><summary><b>菲律宾菜 filipino</b> — B 级，13/38</summary>

- [ ] `P4-filipino/main-meat` 主菜·肉（Meat Main）目标 6，已完成 4
- [ ] `P4-filipino/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-filipino/staple-rice` 主食·饭（Rice Dish）目标 6，已完成 1
- [ ] `P4-filipino/dessert` 甜点（Dessert）目标 6，已完成 1
- [ ] `P4-filipino/snack` 小吃（Street Food）目标 6，已完成 1
- [ ] `P4-filipino/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-filipino/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-filipino/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 3
- [x] `P4-filipino/staple-noodle` 主食·面（Noodle Dish）目标 0，已完成 1

</details>

<details><summary><b>印度菜 indian</b> — A 级，29/107</summary>

- [ ] `P4-indian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 15，已完成 5
- [ ] `P4-indian/main-poultry` 主菜·禽（Poultry Main）目标 15，已完成 6
- [ ] `P4-indian/staple-bread` 主食·饼（Bread Staple）目标 15，已完成 4
- [ ] `P4-indian/soup` 汤羹（Soup）目标 15，已完成 4
- [ ] `P4-indian/dessert` 甜点（Dessert）目标 15，已完成 4
- [ ] `P4-indian/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 0
- [ ] `P4-indian/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 1
- [ ] `P4-indian/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 0
- [ ] `P4-indian/staple-rice` 主食·饭（Rice Dish）目标 8，已完成 1
- [x] `P4-indian/sauce` 酱汁与基础调味（Sauce）目标 0，已完成 1
- [x] `P4-indian/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1
- [x] `P4-indian/snack` 小吃（Street Food）目标 0，已完成 1
- [x] `P4-indian/appetizer` 前菜（Appetizer）目标 0，已完成 1

</details>

<details><summary><b>南亚菜 south-asian</b> — B 级，12/38</summary>

- [ ] `P4-south-asian/staple-rice` 主食·饭（Rice Dish）目标 6，已完成 1
- [ ] `P4-south-asian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 6，已完成 5
- [ ] `P4-south-asian/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-south-asian/snack` 小吃（Street Food）目标 6，已完成 2
- [ ] `P4-south-asian/dessert` 甜点（Dessert）目标 6，已完成 1
- [ ] `P4-south-asian/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [ ] `P4-south-asian/main-tofu` 主菜·豆制品（Tofu Main）目标 4，已完成 0
- [x] `P4-south-asian/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 1

</details>

<details><summary><b>中东风味 middle-eastern</b> — B 级，13/38</summary>

- [ ] `P4-middle-eastern/appetizer` 前菜（Appetizer）目标 6，已完成 3
- [ ] `P4-middle-eastern/main-meat` 主菜·肉（Meat Main）目标 6，已完成 3
- [ ] `P4-middle-eastern/staple-bread` 主食·饼（Bread Staple）目标 6，已完成 1
- [ ] `P4-middle-eastern/salad` 沙拉（Salad）目标 6，已完成 1
- [ ] `P4-middle-eastern/dessert` 甜点（Dessert）目标 6，已完成 1
- [ ] `P4-middle-eastern/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 1
- [ ] `P4-middle-eastern/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-middle-eastern/sauce` 酱汁与基础调味（Sauce）目标 0，已完成 1
- [x] `P4-middle-eastern/snack` 小吃（Street Food）目标 0，已完成 1
- [x] `P4-middle-eastern/staple-rice` 主食·饭（Rice Dish）目标 0，已完成 1

</details>

<details><summary><b>土耳其菜 turkish</b> — B 级，13/38</summary>

- [ ] `P4-turkish/main-meat` 主菜·肉（Meat Main）目标 6，已完成 1
- [ ] `P4-turkish/staple-bread` 主食·饼（Bread Staple）目标 6，已完成 1
- [ ] `P4-turkish/appetizer` 前菜（Appetizer）目标 6，已完成 2
- [ ] `P4-turkish/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-turkish/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-turkish/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 1
- [ ] `P4-turkish/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 1
- [x] `P4-turkish/snack` 小吃（Street Food）目标 0，已完成 2
- [x] `P4-turkish/breakfast` 早餐（Breakfast）目标 0，已完成 1

</details>

<details><summary><b>地中海菜 mediterranean</b> — B 级，15/38</summary>

- [ ] `P4-mediterranean/salad` 沙拉（Salad）目标 6，已完成 2
- [ ] `P4-mediterranean/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 1
- [ ] `P4-mediterranean/appetizer` 前菜（Appetizer）目标 6，已完成 3
- [ ] `P4-mediterranean/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 6，已完成 2
- [ ] `P4-mediterranean/sauce` 酱汁与基础调味（Sauce）目标 6，已完成 3
- [ ] `P4-mediterranean/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 1
- [ ] `P4-mediterranean/main-tofu` 主菜·豆制品（Tofu Main）目标 4，已完成 0
- [x] `P4-mediterranean/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1
- [x] `P4-mediterranean/hotpot-bbq` 火锅与烧烤（Hotpot & BBQ）目标 0，已完成 1
- [x] `P4-mediterranean/breakfast` 早餐（Breakfast）目标 0，已完成 1

</details>

<details><summary><b>希腊菜 greek</b> — B 级，16/38</summary>

- [ ] `P4-greek/appetizer` 前菜（Appetizer）目标 6，已完成 2
- [ ] `P4-greek/main-meat` 主菜·肉（Meat Main）目标 6，已完成 3
- [ ] `P4-greek/salad` 沙拉（Salad）目标 6，已完成 1
- [ ] `P4-greek/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-greek/bakery` 烘焙面包（Bakery）目标 6，已完成 3
- [ ] `P4-greek/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 1
- [ ] `P4-greek/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-greek/soup` 汤羹（Soup）目标 0，已完成 1
- [x] `P4-greek/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-greek/snack` 小吃（Street Food）目标 0，已完成 1
- [x] `P4-greek/sauce` 酱汁与基础调味（Sauce）目标 0，已完成 1

</details>

<details><summary><b>葡萄牙菜 portuguese</b> — B 级，14/38</summary>

- [ ] `P4-portuguese/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 3
- [ ] `P4-portuguese/dessert` 甜点（Dessert）目标 6，已完成 3
- [ ] `P4-portuguese/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-portuguese/soup` 汤羹（Soup）目标 6，已完成 1
- [ ] `P4-portuguese/bakery` 烘焙面包（Bakery）目标 6，已完成 2
- [ ] `P4-portuguese/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-portuguese/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-portuguese/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 2
- [x] `P4-portuguese/staple-rice` 主食·饭（Rice Dish）目标 0，已完成 1

</details>

<details><summary><b>德国菜 german</b> — B 级，13/38</summary>

- [ ] `P4-german/main-meat` 主菜·肉（Meat Main）目标 6，已完成 5
- [ ] `P4-german/bakery` 烘焙面包（Bakery）目标 6，已完成 2
- [ ] `P4-german/fermented` 腌制发酵（Pickle & Ferment）目标 6，已完成 1
- [ ] `P4-german/salad` 沙拉（Salad）目标 6，已完成 2
- [ ] `P4-german/dessert` 甜点（Dessert）目标 6，已完成 1
- [ ] `P4-german/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-german/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-german/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-german/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1

</details>

<details><summary><b>英国菜 british</b> — B 级，14/38</summary>

- [ ] `P4-british/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-british/bakery` 烘焙面包（Bakery）目标 6，已完成 3
- [ ] `P4-british/dessert` 甜点（Dessert）目标 6，已完成 4
- [ ] `P4-british/breakfast` 早餐（Breakfast）目标 6，已完成 2
- [ ] `P4-british/soup` 汤羹（Soup）目标 6，已完成 1
- [ ] `P4-british/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 1
- [ ] `P4-british/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-british/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 1

</details>

<details><summary><b>爱尔兰菜 irish</b> — C 级，13/25</summary>

- [ ] `P4-irish/main-meat` 主菜·肉（Meat Main）目标 5，已完成 2
- [ ] `P4-irish/staple-bread` 主食·饼（Bread Staple）目标 5，已完成 2
- [ ] `P4-irish/soup` 汤羹（Soup）目标 5，已完成 3
- [ ] `P4-irish/breakfast` 早餐（Breakfast）目标 5，已完成 3
- [ ] `P4-irish/drink` 饮品（Drink）目标 5，已完成 0
- [x] `P4-irish/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 0，已完成 1
- [x] `P4-irish/special-diet` 特殊饮食（Special Diet）目标 0，已完成 1
- [x] `P4-irish/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 1

</details>

<details><summary><b>北欧菜 nordic</b> — B 级，13/38</summary>

- [ ] `P4-nordic/main-seafood` 主菜·海鲜（Seafood Main）目标 6，已完成 2
- [ ] `P4-nordic/bakery` 烘焙面包（Bakery）目标 6，已完成 3
- [ ] `P4-nordic/fermented` 腌制发酵（Pickle & Ferment）目标 6，已完成 1
- [ ] `P4-nordic/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-nordic/breakfast` 早餐（Breakfast）目标 6，已完成 2
- [ ] `P4-nordic/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-nordic/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-nordic/main-meat` 主菜·肉（Meat Main）目标 0，已完成 2
- [x] `P4-nordic/soup` 汤羹（Soup）目标 0，已完成 1

</details>

<details><summary><b>东欧菜 eastern-european</b> — B 级，11/38</summary>

- [ ] `P4-eastern-european/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-eastern-european/main-meat` 主菜·肉（Meat Main）目标 6，已完成 3
- [ ] `P4-eastern-european/staple-bread` 主食·饼（Bread Staple）目标 6，已完成 1
- [ ] `P4-eastern-european/fermented` 腌制发酵（Pickle & Ferment）目标 6，已完成 1
- [ ] `P4-eastern-european/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-eastern-european/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 1
- [ ] `P4-eastern-european/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-eastern-european/snack` 小吃（Street Food）目标 0，已完成 1

</details>

<details><summary><b>俄式菜 russian</b> — B 级，13/38</summary>

- [ ] `P4-russian/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-russian/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-russian/salad` 沙拉（Salad）目标 6，已完成 2
- [ ] `P4-russian/bakery` 烘焙面包（Bakery）目标 6，已完成 2
- [ ] `P4-russian/drink` 饮品（Drink）目标 6，已完成 1
- [ ] `P4-russian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 4，已完成 0
- [ ] `P4-russian/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [x] `P4-russian/dessert` 甜点（Dessert）目标 0，已完成 2
- [x] `P4-russian/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 1
- [x] `P4-russian/breakfast` 早餐（Breakfast）目标 0，已完成 1

</details>

<details><summary><b>美式菜 american</b> — A 级，26/107</summary>

- [ ] `P4-american/main-meat` 主菜·肉（Meat Main）目标 15，已完成 4
- [ ] `P4-american/bakery` 烘焙面包（Bakery）目标 15，已完成 4
- [ ] `P4-american/dessert` 甜点（Dessert）目标 15，已完成 4
- [ ] `P4-american/breakfast` 早餐（Breakfast）目标 15，已完成 4
- [ ] `P4-american/salad` 沙拉（Salad）目标 15，已完成 4
- [ ] `P4-american/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 0
- [ ] `P4-american/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 0
- [ ] `P4-american/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 0
- [ ] `P4-american/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 1
- [x] `P4-american/snack` 小吃（Street Food）目标 0，已完成 2
- [x] `P4-american/soup` 汤羹（Soup）目标 0，已完成 1
- [x] `P4-american/appetizer` 前菜（Appetizer）目标 0，已完成 1
- [x] `P4-american/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1

</details>

<details><summary><b>美国南方菜 american-south</b> — B 级，12/38</summary>

- [ ] `P4-american-south/main-poultry` 主菜·禽（Poultry Main）目标 6，已完成 2
- [ ] `P4-american-south/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 6，已完成 2
- [ ] `P4-american-south/bakery` 烘焙面包（Bakery）目标 6，已完成 1
- [ ] `P4-american-south/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-american-south/breakfast` 早餐（Breakfast）目标 6，已完成 3
- [ ] `P4-american-south/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [ ] `P4-american-south/main-tofu` 主菜·豆制品（Tofu Main）目标 4，已完成 0
- [x] `P4-american-south/main-meat` 主菜·肉（Meat Main）目标 0，已完成 1
- [x] `P4-american-south/hotpot-bbq` 火锅与烧烤（Hotpot & BBQ）目标 0，已完成 1

</details>

<details><summary><b>德州墨西哥菜 tex-mex</b> — B 级，12/38</summary>

- [ ] `P4-tex-mex/main-meat` 主菜·肉（Meat Main）目标 6，已完成 2
- [ ] `P4-tex-mex/snack` 小吃（Street Food）目标 6，已完成 3
- [ ] `P4-tex-mex/sauce` 酱汁与基础调味（Sauce）目标 6，已完成 2
- [ ] `P4-tex-mex/breakfast` 早餐（Breakfast）目标 6，已完成 1
- [ ] `P4-tex-mex/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 6，已完成 2
- [ ] `P4-tex-mex/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [ ] `P4-tex-mex/main-tofu` 主菜·豆制品（Tofu Main）目标 4，已完成 0
- [x] `P4-tex-mex/salad` 沙拉（Salad）目标 0，已完成 1
- [x] `P4-tex-mex/soup` 汤羹（Soup）目标 0，已完成 1

</details>

<details><summary><b>卡真菜 cajun</b> — C 级，15/25</summary>

- [ ] `P4-cajun/main-seafood` 主菜·海鲜（Seafood Main）目标 5，已完成 3
- [ ] `P4-cajun/staple-rice` 主食·饭（Rice Dish）目标 5，已完成 4
- [ ] `P4-cajun/soup` 汤羹（Soup）目标 5，已完成 3
- [ ] `P4-cajun/main-poultry` 主菜·禽（Poultry Main）目标 5，已完成 1
- [ ] `P4-cajun/sauce` 酱汁与基础调味（Sauce）目标 5，已完成 2
- [x] `P4-cajun/main-meat` 主菜·肉（Meat Main）目标 0，已完成 1
- [x] `P4-cajun/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 0，已完成 1

</details>

<details><summary><b>墨西哥菜 mexican</b> — A 级，31/107</summary>

- [ ] `P4-mexican/snack` 小吃（Street Food）目标 15，已完成 5
- [ ] `P4-mexican/main-meat` 主菜·肉（Meat Main）目标 15，已完成 5
- [ ] `P4-mexican/sauce` 酱汁与基础调味（Sauce）目标 15，已完成 4
- [ ] `P4-mexican/soup` 汤羹（Soup）目标 15，已完成 5
- [ ] `P4-mexican/drink` 饮品（Drink）目标 15，已完成 4
- [ ] `P4-mexican/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 8，已完成 2
- [ ] `P4-mexican/main-egg` 主菜·蛋（Egg Main）目标 8，已完成 1
- [ ] `P4-mexican/main-tofu` 主菜·豆制品（Tofu Main）目标 8，已完成 0
- [ ] `P4-mexican/staple-noodle` 主食·面（Noodle Dish）目标 8，已完成 0
- [x] `P4-mexican/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 2
- [x] `P4-mexican/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 2
- [x] `P4-mexican/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1

</details>

<details><summary><b>秘鲁菜 peruvian</b> — C 级，15/25</summary>

- [ ] `P4-peruvian/main-seafood` 主菜·海鲜（Seafood Main）目标 5，已完成 1
- [ ] `P4-peruvian/main-poultry` 主菜·禽（Poultry Main）目标 5，已完成 3
- [ ] `P4-peruvian/appetizer` 前菜（Appetizer）目标 5，已完成 4
- [ ] `P4-peruvian/staple-rice` 主食·饭（Rice Dish）目标 5，已完成 2
- [ ] `P4-peruvian/drink` 饮品（Drink）目标 5，已完成 1
- [x] `P4-peruvian/cold-dish` 凉菜（Cold Dish）目标 0，已完成 2
- [x] `P4-peruvian/main-meat` 主菜·肉（Meat Main）目标 0，已完成 1
- [x] `P4-peruvian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 0，已完成 1

</details>

<details><summary><b>巴西菜 brazilian</b> — C 级，9/25</summary>

- [ ] `P4-brazilian/main-meat` 主菜·肉（Meat Main）目标 5，已完成 2
- [ ] `P4-brazilian/staple-rice` 主食·饭（Rice Dish）目标 5，已完成 1
- [ ] `P4-brazilian/snack` 小吃（Street Food）目标 5，已完成 1
- [ ] `P4-brazilian/dessert` 甜点（Dessert）目标 5，已完成 2
- [ ] `P4-brazilian/drink` 饮品（Drink）目标 5，已完成 1
- [x] `P4-brazilian/main-seafood` 主菜·海鲜（Seafood Main）目标 0，已完成 2

</details>

<details><summary><b>阿根廷菜 argentinian</b> — C 级，13/25</summary>

- [ ] `P4-argentinian/main-meat` 主菜·肉（Meat Main）目标 5，已完成 3
- [ ] `P4-argentinian/sauce` 酱汁与基础调味（Sauce）目标 5，已完成 2
- [ ] `P4-argentinian/bakery` 烘焙面包（Bakery）目标 5，已完成 2
- [ ] `P4-argentinian/dessert` 甜点（Dessert）目标 5，已完成 2
- [ ] `P4-argentinian/drink` 饮品（Drink）目标 5，已完成 0
- [x] `P4-argentinian/snack` 小吃（Street Food）目标 0，已完成 2
- [x] `P4-argentinian/staple-bread` 主食·饼（Bread Staple）目标 0，已完成 1
- [x] `P4-argentinian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 0，已完成 1

</details>

<details><summary><b>加勒比菜 caribbean</b> — C 级，11/25</summary>

- [ ] `P4-caribbean/main-poultry` 主菜·禽（Poultry Main）目标 5，已完成 3
- [ ] `P4-caribbean/main-seafood` 主菜·海鲜（Seafood Main）目标 5，已完成 2
- [ ] `P4-caribbean/staple-rice` 主食·饭（Rice Dish）目标 5，已完成 2
- [ ] `P4-caribbean/drink` 饮品（Drink）目标 5，已完成 1
- [ ] `P4-caribbean/dessert` 甜点（Dessert）目标 5，已完成 2
- [x] `P4-caribbean/hotpot-bbq` 火锅与烧烤（Hotpot & BBQ）目标 0，已完成 1

</details>

<details><summary><b>北非菜 north-african</b> — B 级，13/38</summary>

- [ ] `P4-north-african/soup` 汤羹（Soup）目标 6，已完成 2
- [ ] `P4-north-african/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 6，已完成 2
- [ ] `P4-north-african/staple-bread` 主食·饼（Bread Staple）目标 6，已完成 2
- [ ] `P4-north-african/salad` 沙拉（Salad）目标 6，已完成 2
- [ ] `P4-north-african/dessert` 甜点（Dessert）目标 6，已完成 2
- [ ] `P4-north-african/main-egg` 主菜·蛋（Egg Main）目标 4，已完成 0
- [ ] `P4-north-african/main-tofu` 主菜·豆制品（Tofu Main）目标 4，已完成 0
- [x] `P4-north-african/special-diet` 特殊饮食（Special Diet）目标 0，已完成 1
- [x] `P4-north-african/main-meat` 主菜·肉（Meat Main）目标 0，已完成 1
- [x] `P4-north-african/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1

</details>

<details><summary><b>西非菜 west-african</b> — C 级，14/25</summary>

- [ ] `P4-west-african/staple-rice` 主食·饭（Rice Dish）目标 5，已完成 2
- [ ] `P4-west-african/soup` 汤羹（Soup）目标 5，已完成 2
- [ ] `P4-west-african/main-meat` 主菜·肉（Meat Main）目标 5，已完成 2
- [ ] `P4-west-african/snack` 小吃（Street Food）目标 5，已完成 3
- [ ] `P4-west-african/sauce` 酱汁与基础调味（Sauce）目标 5，已完成 3
- [x] `P4-west-african/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-west-african/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 0，已完成 1

</details>

<details><summary><b>东非菜 east-african</b> — C 级，15/25</summary>

- [ ] `P4-east-african/main-meat` 主菜·肉（Meat Main）目标 5，已完成 2
- [ ] `P4-east-african/staple-bread` 主食·饼（Bread Staple）目标 5，已完成 2
- [ ] `P4-east-african/soup` 汤羹（Soup）目标 5，已完成 1
- [ ] `P4-east-african/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 5，已完成 3
- [ ] `P4-east-african/drink` 饮品（Drink）目标 5，已完成 1
- [x] `P4-east-african/breakfast` 早餐（Breakfast）目标 0，已完成 2
- [x] `P4-east-african/cold-dish` 凉菜（Cold Dish）目标 0，已完成 1
- [x] `P4-east-african/appetizer` 前菜（Appetizer）目标 0，已完成 1
- [x] `P4-east-african/hotpot-bbq` 火锅与烧烤（Hotpot & BBQ）目标 0，已完成 1
- [x] `P4-east-african/staple-congee` 主食·粥（Congee）目标 0，已完成 1

</details>

<details><summary><b>南非菜 south-african</b> — C 级，14/25</summary>

- [ ] `P4-south-african/main-meat` 主菜·肉（Meat Main）目标 5，已完成 2
- [ ] `P4-south-african/staple-bread` 主食·饼（Bread Staple）目标 5，已完成 3
- [ ] `P4-south-african/dessert` 甜点（Dessert）目标 5，已完成 2
- [ ] `P4-south-african/snack` 小吃（Street Food）目标 5，已完成 3
- [ ] `P4-south-african/salad` 沙拉（Salad）目标 5，已完成 2
- [x] `P4-south-african/bakery` 烘焙面包（Bakery）目标 0，已完成 1
- [x] `P4-south-african/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1

</details>

<details><summary><b>澳新菜 australian</b> — C 级，14/25</summary>

- [ ] `P4-australian/main-seafood` 主菜·海鲜（Seafood Main）目标 5，已完成 2
- [ ] `P4-australian/bakery` 烘焙面包（Bakery）目标 5，已完成 4
- [ ] `P4-australian/breakfast` 早餐（Breakfast）目标 5，已完成 3
- [ ] `P4-australian/dessert` 甜点（Dessert）目标 5，已完成 2
- [ ] `P4-australian/salad` 沙拉（Salad）目标 5，已完成 0
- [x] `P4-australian/main-poultry` 主菜·禽（Poultry Main）目标 0，已完成 1
- [x] `P4-australian/snack` 小吃（Street Food）目标 0，已完成 1
- [x] `P4-australian/main-vegetable` 主菜·蔬菜（Vegetable Main）目标 0，已完成 1

</details>

---

### 抽检任务规则

每完成约 10 个内容批次，自动新增一个「抽检任务」：随机抽取 5% 已写菜谱，以审稿人视角重读并打分（准确性、完整性、可操作性、安全性），不合格的重写。抽检记录写入 `tasks/REVIEW.md`。
