# DECISIONS — 决策日志

> 规则：任何不确定处，按最佳实践自行决策，并把「决策 + 理由」追加到本文件。只增不改，被推翻的决策标记 `SUPERSEDED`。

格式：`D-序号 | 日期 | 决策主题 | 决策内容 | 理由 | 影响面`

---

### D-001 | 2026-11-18 | 项目根目录
**决策**：项目根为 `D:\AI\project\marvis_project\caipu`（项目资源中登记的本地目录），而非会话临时 workspace。
**理由**：该目录是项目已登记的引用资源，用户可直接访问；临时 workspace 随会话结束不可靠。
**影响面**：全部工程与数据文件。

### D-002 | 2026-11-18 | 后端框架
**决策**：选用 **Fastify**（而非 NestJS）。
**理由**：项目核心是数据读取型 API，无复杂依赖注入与模块治理需求；Fastify 启动快、内置 JSON Schema 校验、插件生态足够，测试面小。NestJS 的抽象层在本项目属于过度设计。
**影响面**：`apps/api`。

### D-003 | 2026-11-18 | ORM 与迁移
**决策**：选用 **Drizzle ORM** + `drizzle-kit`。
**理由**：SQLite→PostgreSQL 迁移只需替换 driver 与方言配置；schema 用 TS 定义，类型可跨 web/api 复用；相比 Prisma 无 Rust 引擎与生成产物依赖，容器镜像更小。
**影响面**：`packages/db`。

### D-004 | 2026-11-18 | 仓库形态
**决策**：npm workspaces（不自建 pnpm/turbo）。
**理由**：环境已装 npm 10，无需额外安装包管理器；workspace 数量少（web/api/db/schema），npm workspaces 足以胜任，减少工具链风险。
**影响面**：根 `package.json`。

### D-005 | 2026-11-18 | 内容生产规模与目标矩阵
**决策**：总目标 **≈3645 道**，按「菜系层级 × 品类」分配：A 级核心品类 15 道、非核心 3 道；B 级核心 6、非核心 1；C 级核心 5、非核心 1。
**理由**：若严格按"每个菜系 × 每个品类 15-40 道"计算，59 菜系 × 26 品类 × 15 ≈ 23000 道，超出单人可交付范围且大量组合在真实烹饪体系中不成立（如「藏餐 × 沙拉」）。采用分层目标，保证热门菜系核心品类达到 15 道（符合"每格 15-40"的要求区间），总量仍远超 3000 的下限。
**影响面**：`docs/TAXONOMY.md`、`tasks/progress.json`。

### D-006 | 2026-11-18 | 港澳与台湾的分类归属
**决策**：`hongkong`、`taiwan` 归入 `region: cn`。
**理由**：它们是中文饮食圈的地方风味分支，与"外国料理"在食材体系、调味逻辑上同源；独立成菜系而非按国家划分，能更准确地组织内容。`region` 只承担"中国菜 / 外国菜"的一级导航职责。
**影响面**：`data/taxonomy.json`、分类树 API。

### D-007 | 2026-11-18 | 图片策略
**决策**：本期 `image_url` 与 `image_credit` 固定为 `null`，前端渲染确定性占位图（CSS 渐变 + 菜名首字）。
**理由**：不爬取、不盗用是硬约束；采购图库授权在无预算前提下不可行。占位图方案保证版式稳定且不产生版权风险。
**影响面**：前端组件 `RecipeImage`。

### D-008 | 2026-11-18 | 食材反查的实现
**决策**：在数据库中建立 `recipe_ingredient` 关联表（recipe_id, ingredient_key, group），反查用 SQL 聚合 + `HAVING count >= n`。
**理由**：纯文本 LIKE 在大库上不可用且易误命中（"花生"命中"花生油"却非主料）；关联表可按主料/辅料区分权重，并可区分 `match_mode = all | any`。
**影响面**：`packages/db` schema、`/api/v1/ingredients/recipes`。

### D-009 | 2026-11-18 | 份量换算与单位切换的位置
**决策**：换算在**客户端**完成，API 只返回基准用量（`servings` + 原始 amount/unit）。
**理由**：换算率是纯函数，无需往返请求；服务端换算会导致缓存碎片化（每个份量一套响应）。同时 API 返回 `servings` 基准，保证 App/小程序可用同一套逻辑复用（换算函数发布为 `packages/shared`）。
**影响面**：`packages/shared/scaling.ts`、详情页。

### D-010 | 2026-11-18 | 校验脚本形态
**决策**：`scripts/validate` 用 Node.js (ESM) 实现，零第三方依赖（自写 JSON Schema 子集校验）。
**理由**：避免引入 ajv 等依赖造成 CI 环境差异；本项目 Schema 用到的关键字有限（type/required/enum/pattern/minimum/maxItems/oneOf），自写校验器可控且报错信息更贴合中文内容审校需求。
**影响面**：`scripts/validate.mjs`。

### D-011 | 2026-11-18 | 内容生产的批次化流水线
**决策**：内容按"菜系 × 批次"生产，每批 10-20 道，写入 `data/recipes/{region}/{cuisine}/`，每批结束即跑 validate，通过后 `git commit`。
**理由**：单次会话上下文有限；批次化保证任何中断都能从 `progress.json` 精确续做，且校验失败的影响面被限制在一批之内。
**影响面**：`tasks/TASKS.md` 内容任务粒度。

### D-012 | 2026-11-18 | 搜索实现
**决策**：SQLite 阶段用 `LIKE` + 预建小写化搜索列（`search_text`）+ 相关性排序（菜名命中权重 3、食材 2、标签 1）；PostgreSQL 阶段可平滑切换 `pg_trgm` / `tsvector`。
**理由**：SQLite FTS5 对中文分词支持弱，需要额外分词；中文场景下 2-gram 切分已能满足站内检索，且不引入分词依赖。
**影响面**：`apps/api` 搜索路由、`packages/db`。

### D-013 | 2026-11-18 | 依赖安装策略
**决策**：前端不引入 UI 组件库，只用 Tailwind 手写组件。
**理由**：站点页面数量可控（约 10 个模板），组件库会带来体积与样式覆盖成本；手写可确保 SEO 语义结构与可访问性完全可控。
**影响面**：`apps/web`。

### D-014 | 2026-11-18 | 校验脚本的严格度取舍
**决策**：`amount` 允许 `null` 仅当 `unit = "to-taste"`；`to-taste` 限 9 类调味食材白名单。
**理由**：用户明确点名"适量滥用"是质量问题。白名单是能落地执行的边界，比"建议不要用"有效。
**影响面**：`scripts/validate.mjs`、`data/ingredients.json`。

## 2026-11-18 构建期不依赖 API（改为运行时渲染）

- 决策：所有取数页面（首页、分类、菜系、搜索、食材、详情、打印）统一 `export const dynamic = 'force-dynamic'`，`app/sitemap.ts` 同样改为动态生成。
- 原因：`next build` 在静态生成阶段会请求 `http://127.0.0.1:4000`，容器构建期与本地无 API 时必然 `fetch failed`，既污染构建输出，也会把空数据固化进静态页。
- 代价：放弃 ISR 的全页静态化，改为每次请求 SSR（数据实为本地 SQLite，查询毫秒级）；如需 CDN 静态化，后续可在有 API 的构建环境中改回 ISR。
- 备注：`ng build` 后 API 不可用时页面仍能返回 200 骨架，不再出现构建失败。

## 2026-11-18 better-sqlite3 与 Node 版本

- 现象：Node 24 下 `ERR_DLOPEN_FAILED`，原生模块未针对该 ABI 编译。
- 决策：`npm rebuild better-sqlite3` 作为标准修复步骤写入 README / DEPLOY；容器固定 `node:20-bookworm-slim` 并在构建期安装 python3/make/g++ 保证可从源码编译。

## D-20261118-03 运行脚本固定使用 Node 24（D:\Node\node.exe）
- 背景：Marvis 宿主自带 Node 22.12.0（NODE_MODULE_VERSION 127），而 better-sqlite3 预编译二进制按 Node 24（137）安装，宿主 node 直接运行导入脚本会报 ERR_DLOPEN_FAILED。
- 决策：脚本与测试（validate/import/test）统一使用 D:\Node\node.exe（v24.13.0）；README 中写明 engines: node >= 20，并给出 Windows 下的 PATH 前置写法。
- 理由：改 node 侧比每次 rebuild better-sqlite3 更稳定，也避免 CI 与本地不一致；Docker 镜像统一用 node:22-slim 并在镜像内安装依赖（镜像内版本一致，不受宿主影响）。

## 2026-11-18 本轮决策

1. **进度统计纳入残余品类**
   - 决策：`scripts/gen-progress.mjs` 在 core/ext 格之外，追加 `kind: "extra"` 的格子，target=0、actual=实际数。
   - 理由：此前只有 core+ext 品类的菜谱可计入进度，导致 `data/recipes` 有 66 道而 progress 只记 58 道，交接时会误判欠产。

2. **同菜去重**
   - 决策：删除早期样板 `cn/shandong/congsao-haishen.json`，保留信息更完整的 `congshao-haishen.json`，并把全库 4 处引用改指新 id。
   - 理由：同一道菜两个 id 会让搜索与菜系列表出现重复条目，违反「唯一 id + 无重复内容」质量门槛。

3. **食材词典禁止泛称词条**
   - 决策：`瘦肉`、`鸡` 等泛称不进词典；统一使用 `猪里脊`、`鸡腿肉` 等具体部位名。
   - 理由：词典词条会参与「步骤提到的食材必须在配料表」检查，泛称词条会让大量既有菜谱的步骤文本触发误报，破坏全库校验稳定性。

4. **交接文件**
   - 决策：新增 `tasks/SESSION_STATE.md`，把单批生产套路、校验红线、已完成/未完成阶段、下批推荐格子写死在仓库里。
   - 理由：满足「状态必须存在文件里、不依赖对话记忆」的要求，新会话可直接按文件续跑。
