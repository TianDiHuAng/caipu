# 中外菜谱库（caipu）

一个「数据 + API + 网站」三层的菜谱项目：菜谱以 JSON 为唯一真相源，导入 SQLite，
由 Fastify 提供版本化 REST API，Next.js 服务端渲染网站消费同一套接口。
App / 小程序可直接复用 `/api/v1`，详见 [docs/MOBILE_API.md](docs/MOBILE_API.md)。

## 目录结构

```
caipu/
├─ apps/
│  ├─ api/                 # Fastify + TypeScript，/api/v1
│  └─ web/                 # Next.js + Tailwind，SSR + SEO
├─ packages/
│  ├─ db/                  # Drizzle ORM schema、迁移、建库
│  └─ shared/              # 类型、份量换算、单位换算
├─ data/
│  ├─ recipes/{region}/{cuisine}/{id}.json   # 菜谱源数据
│  ├─ ingredients.json     # 食材词典（中英名/别名/过敏原/密度）
│  ├─ taxonomy.json        # 菜系与品类分类体系
│  └─ db/caipu.db          # 开发期 SQLite（可重建）
├─ schema/recipe.schema.json
├─ scripts/                # 校验、导入、同步任务、冒烟测试
├─ docs/                   # PRD / SCHEMA / TAXONOMY / STYLE / API / 部署 / 移动端
└─ tasks/                  # TASKS.md、progress.json、审查与验收记录
```

## 快速开始

```bash
npm install
npm run db:init          # 建库与迁移
npm run import           # 导入 data/recipes/**/*.json
npm run dev:api          # API  → http://localhost:4000
npm run dev:web          # 网站 → http://localhost:3000
```

一键容器启动：

```bash
docker compose up --build   # 网站 :3000，API :4000
```

## 常用脚本

| 命令 | 作用 |
| --- | --- |
| `npm test` | API 与导入脚本自动化测试 |
| `npm run validate` | 校验全部菜谱（8 项质量门槛，见下文） |
| `npm run import` | 把 JSON 导入数据库（幂等） |
| `npm run smoke` | 起服务后对关键接口做冒烟测试 |
| `npm run tasks:sync` | 由 `tasks/*.json` 重新生成 `tasks/TASKS.md` |
| `npm run build:web` / `npm run start:web` | 网站生产构建 / 生产启动 |

## 如何新增一道菜谱

1. 在 `docs/TAXONOMY.md` 找到对应的 `菜系 slug` 与 `品类 slug`，确认目标格子还有缺口（`tasks/progress.json`）。
2. 在 `data/recipes/{cn|intl}/{cuisine}/{id}.json` 新建文件，`id` 用英文短横线 slug，全局唯一。
3. 按 `docs/SCHEMA.md` 写满 31 个字段；`scripts/author.mjs` 提供紧凑草稿展开（自动补分组、总时长、过敏原、路径），可先写草稿再展开。
4. 运行 `npm run validate`，必须 0 错误；再 `npm run import` 落库。
5. 更新 `tasks/progress.json` 的已完成数，`npm run tasks:sync` 刷新任务清单。

写作规范（公制用量、步骤四要素、感官判断线索、食品安全、过敏原）见 [docs/STYLE.md](docs/STYLE.md)。

## 质量门槛

`scripts/validate` 会强制检查：

1. 符合 `schema/recipe.schema.json`
2. 无占位符（TODO、省略号、「略」、「同上」）；「适量」只允许用于盐/糖/酱油等白名单且必须带参考范围
3. 用量合理性：主料每份 60–700g、盐 ≤6.5g/人、常规用油 ≤45ml/份、油炸 ≤90ml/份
4. 步骤引用的食材必须在配料表中，配料表食材至少被一个步骤使用
5. 过敏原与 `data/ingredients.json` 词典一致；`diet_tags` 与配料不冲突
6. `id` 唯一、`related_ids` 有效
7. 步骤 ≥4 步（极简饮品除外）、`tips` ≥2、`common_mistakes` ≥1、每步 `visual_cue` 有实质内容
8. 跨菜谱文本去重（20 字滑窗出现在 5 道以上菜谱即判定雷同）

## 对接 App / 小程序

- 接口总览：[docs/API.md](docs/API.md)
- 端侧对接（分页、语言、缓存、份量换算、小程序/App 注意事项）：[docs/MOBILE_API.md](docs/MOBILE_API.md)
- 部署与迁移 PostgreSQL：[docs/DEPLOY.md](docs/DEPLOY.md)

## 许可证与内容声明

- 代码：供学习与自建站点使用。
- 菜谱文字：全部为原创重写，不复制任何网站/书籍原文；图片字段目前为占位，**不爬取、不盗用第三方图片**，替换时请保留 `image_credit` 署名。
- 营养数据为估算值，不构成医疗或膳食建议；药膳类内容仅记录传统说法。
