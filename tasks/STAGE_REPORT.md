# 阶段验收报告

> 每阶段结束由本 Agent 自行运行验收检查，结果写入本文件。只记录真实执行过的命令与输出摘要。

## 阶段 0 — 文档与任务系统

| 检查项 | 命令 | 结果 |
| --- | --- | --- |
| 校验脚本可运行 | `node scripts/validate.mjs` | 退出码 0，0 错误 |
| 分类体系生成 | `node scripts/gen-progress.mjs` | 59 菜系 / 26 品类 / 423 格子 / 目标 3259 道 |
| 任务清单生成 | `node scripts/sync-tasks.mjs` | TASKS.md 811 行，工程任务 8/51 |
| JSON Schema 自检 | `node scripts/validate.mjs --schema-only` | schema/recipe.schema.json 可加载 |

结论：通过。

## 阶段 1 — 骨架 / 数据库 / 导入 / API / 测试

| 检查项 | 命令 | 结果 |
| --- | --- | --- |
| 建库 | `npx tsx packages/db/src/init.ts --reset` | `{"cuisines":59,"categories":26,"ingredients":271}` |
| 导入 | `npx tsx scripts/import.ts --reset` | `{"files":3,"imported":3,"skipped":0,"recipes":3,"ingredients":43,"steps":18}` |
| 自动化测试 | `npm test` | tests 26 / pass 26 / fail 0 |
| API 冒烟 | `npx tsx scripts/smoke.mjs` | 17/17 通过 |
| 内容校验 | `node scripts/validate.mjs` | 3 道菜谱 0 错误 |

### 本阶段修复的真实缺陷

1. `@caipu/db` 未导出 schema 表对象，API 侧 `import { recipes }` 报错 → 追加 `export * from './schema.js'`。
2. `getDb()` 返回 `{db, sqlite, file, schema}` 包装对象，业务层却按 `db.select()` 调用 → 统一改为 `db.db.select()`（含跨行链式调用）。
3. `/filters` 与 `/meta` 的风味/饮食标签/过敏原从数据库统计推导，空库时筛选项全部消失 → 改为读取 `data/taxonomy.json` 全量并叠加计数。
4. `/recipes/random` 只认 `count` 参数，`size` 被忽略 → 同时接受 `size`/`count`，上限 30。
5. `/health` 缺少 `ok` 与 `ingredients` 计数，与文档不一致 → 对齐为统一结构。
6. `meta.ts` 编辑时误删 `drizzle-orm` 的 `asc` 导入导致 26 个测试全挂 → 恢复导入。

结论：通过。

## 阶段 2 — 50 道样板菜谱

| 检查项 | 命令 | 结果 |
| --- | --- | --- |
| 内容校验 | `npm run validate` | 50 文件 / 50 解析成功，50 道 0 错误 |
| Schema 与跨文件规则 | `npm test` | 26/26 通过（含 id 唯一、路径一致、related_ids 有效、文本雷同检测） |
| 导入 | `npm run import` | files 50 / imported 50 / recipes 50 / steps 286 |

覆盖：川 6、粤 6、鲁 4、苏 4、浙 4、闽 3、湘 3、徽 2、京 3、沪 2、东北 2、西北 2、云贵 2、客家/潮汕 2、日 3、韩 3、泰 2、越 2、意 4、法 3、印 3、美 3、墨 2、中东 2、烘焙与饮品 3，难度 1-5 俱全。

结论：通过。

## 阶段 3 — 网站核心页面与 SEO

| 检查项 | 命令 | 结果 |
| --- | --- | --- |
| 生产构建 | `npm run build`（apps/web） | 退出码 0，10 条路由全部生成，无构建期 API 请求 |
| 首页 | GET / | 200，62 KB |
| 分类树 / 分类详情 | GET /categories | 200，27 KB |
| 菜系列表 | GET /cuisines | 200，50 KB |
| 菜谱详情 | GET /recipes/baiqie-ji | 200，41 KB，页面含 schema.org Recipe 结构化数据 |
| 打印视图 | GET /recipes/baiqie-ji/print | 200，17 KB |
| 搜索页 | GET /search?q= | 200，71 KB |
| 食材反查 | GET /ingredients | 200，11 KB |
| sitemap / robots | GET /sitemap.xml、/robots.txt | 200 / 200 |

### 本阶段修复的真实缺陷

1. 构建期在静态生成阶段向 `127.0.0.1:4000` 取数，API 未启动时报 `TypeError: fetch failed`，导致构建噪声与空页面 → 数据页统一改为 `export const dynamic = 'force-dynamic'`，`sitemap.ts` 同步改为动态生成。
2. `better-sqlite3` 在 Node 24 下原生绑定缺失（`ERR_DLOPEN_FAILED`）→ `npm rebuild better-sqlite3` 重新编译后恢复；已在 README 与 DEPLOY 中记录。

结论：通过。

## 阶段 5 — 搜索优化 / 多语言 / 性能 / Docker / 文档

| 检查项 | 命令 | 结果 |
| --- | --- | --- |
| 搜索优化 | `apps/api/src/search.ts`、`query.ts` | 同义词表 + pinyin-pro 全拼/首字母扩展 + 权重排序；前端 `Highlight` 组件高亮命中词 |
| 多语言 | `lib/i18n.ts`、`middleware.ts`、`LanguageSwitch` | zh/en 字典、`?lang=` 与 cookie 切换，数据层 name{zh,en} |
| 性能 | `next.config.mjs` | compress、poweredByHeader=false、静态资源 immutable 缓存、安全响应头 |
| Docker | `docker compose config -q` | 配置校验通过；Dockerfile 多阶段 + tini + healthcheck |
| 文档 | README / docs/MOBILE_API.md / docs/DEPLOY.md | 均存在，含运行、新增菜谱、移动端对接、部署说明 |

### 未能在本机验证的部分

`docker compose up` 需 Docker 守护进程，本机仅安装 CLI（Docker Desktop 未安装，`docker info` 连接 npipe 失败）。已改用等价路径验证：本地分别启动 API（/health 200、/api/v1/meta 200、/api/v1/recipes 200）与站点（关键页面全部 200）。容器入口 `scripts/docker-entrypoint.sh` 的逻辑为「建库 → 导入 → 起 API → 等就绪 → 起站点」，与本地验证顺序一致。

结论：通过（镜像构建待有 Docker 守护进程的环境复核）。


## 阶段 6（部分完成，随内容增长迭代）

| 检查项 | 命令 | 结果 |
| --- | --- | --- |
| 全库校验 | `node scripts/validate.mjs` | 71 道，0 错误 |
| 自动化测试 | `npm test`（需 Node 24：`set PATH=D:\Node;%PATH%`） | 29 通过 / 0 失败 |
| 5% 抽检 | `npm run audit` | 26 个菜系各抽 1 道，平均分 96，无 C/D 级 |
| 数据导入 | `npx tsx scripts/import.ts` | 71 文件 / 71 菜谱 / 821 配料行 / 395 步骤 |
| 进度 | `npm run progress` | 目标 3274，已完成 82（2.5%） |

结论：工程质量门槛全部通过；内容数量仅完成 82/3274，阶段 4 仍在推进，阶段 6 的「全库巡检」需在内容达标后重跑。
