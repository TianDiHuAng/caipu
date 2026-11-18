# 部署文档

本项目提供两种运行方式：本机开发（Node 直跑）与容器化一键启动（Docker Compose）。
容器镜像内同时运行 API（:4000）与网站（:3000），网站由 Next.js standalone 产物启动，
静态资源由容器内的 `scripts/start-web.mjs` 自动补齐到 `.next/standalone`。

## 1. 环境要求

| 场景 | 要求 |
| --- | --- |
| 本机开发 | Node.js >= 20（建议 20 LTS）、npm >= 10、git |
| 容器运行 | Docker Engine >= 24 与 Docker Compose v2（`docker compose` 子命令） |
| 生产部署 | 可替换为 PostgreSQL（见第 5 节），或直接把 SQLite 文件放在持久卷上 |
| 端口 | 3000（网站）、4000（API），均可在 `.env` / compose 中改 |

## 2. 一键启动（推荐）

```bash
git clone <repo> caipu && cd caipu
docker compose up --build
```

启动后：

- 网站：http://localhost:3000
- API：http://localhost:4000/api/v1/meta
- 健康检查：http://localhost:4000/health

容器启动流程见 `scripts/docker-entrypoint.sh`：

1. 若 `data/db/caipu.db` 不存在则执行建库（`packages/db` 迁移）
2. 执行 `scripts/import.mjs` 把 `data/recipes/**/*.json` 导入数据库（幂等，可重复执行）
3. 启动 Fastify API（:4000）
4. 轮询 `/health` 就绪后启动 Next.js standalone 服务（:3000）

数据持久化：`caipu-db` 卷挂载到 `/app/data/db`，重建容器不会丢库；
菜谱源文件 `data/recipes` 以只读方式挂入容器，更新菜谱只需改宿主机 JSON 并重启容器。

### 常用命令

```bash
docker compose up -d --build          # 后台启动
docker compose logs -f web            # 查看网站日志
docker compose exec app npm run import  # 手动重新导入
docker compose down                   # 停止（保留数据卷）
docker compose down -v                # 停止并删除数据卷
```

## 3. 本机开发

```bash
npm install
npm run db:init        # 建库 + 迁移
npm run import         # 导入 data/recipes 下的 JSON
npm run dev:api        # API，http://localhost:4000
npm run dev:web        # 网站，http://localhost:3000（开发模式）
```

生产模式本地验证（不依赖 Docker）：

```bash
npm run build:web
npm run start:web      # 内部会装配 .next/standalone 静态资源
```

## 4. 环境变量

| 变量 | 默认值 | 说明 |
| --- | --- | --- |
| `PORT` | `4000` | API 监听端口 |
| `HOST` | `0.0.0.0` | API 绑定地址 |
| `WEB_PORT` | `3000` | 网站监听端口（`scripts/start-web.mjs` 读取） |
| `HOST_BIND` | `127.0.0.1` | 网站绑定地址，容器内必须为 `0.0.0.0` |
| `API_BASE_URL` | `http://127.0.0.1:4000` | 网站服务端请求 API 的地址 |
| `NEXT_PUBLIC_API_BASE_URL` | 同 `API_BASE_URL` | 浏览器端/静态页使用 |
| `DB_FILE` | `data/db/caipu.db` | SQLite 文件路径 |

## 5. 迁移到 PostgreSQL

数据访问统一收敛在 `packages/db`（Drizzle ORM），迁移步骤：

1. `packages/db` 中把 `sqliteTable` 换成 `pgTable`，并把 `INTEGER/TEXT` 映射为 `integer/text`、数组字段改为 `jsonb`
2. 连接串由 `DB_FILE` 换成 `DATABASE_URL`，`getDb()` 改用 `drizzle-orm/node-postgres`
3. 用 `drizzle-kit generate` 生成迁移并执行
4. 新增 `scripts/import-pg.mjs`（可直接复用 `scripts/import.mjs` 的读盘逻辑，只替换写入端）

API 层与网站层不需要改动，所有查询都通过 `packages/db` 的 schema 与 `apps/api/src/query.ts`。

## 6. 生产建议

- 前置 Nginx/Caddy 做 TLS 与 gzip/br，反向代理到 3000
- API 已输出 `Cache-Control: public, max-age=60, stale-while-revalidate=300` 与弱 ETag，可直接接入 CDN
- 网站为动态渲染（读取实时数据库），如需全静态可改为 `output: 'export'` 并配合静态 API
- 备份：定期复制 `data/db/caipu.db`（SQLite 用 `.backup` 或停服复制），或使用 PostgreSQL 的 PITR
- 健康检查：`GET /health`（容器已配置 healthcheck），可对接 K8s liveness/readiness

## 7. 故障排查

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 网站 502/空白 | API 未就绪 | `docker compose logs app`，确认 `/health` 返回 200 |
| 首页 500 且提示无数据 | 未导入菜谱 | `docker compose exec app npm run import` |
| 样式/JS 404 | standalone 静态资源缺失 | 确认使用 `npm run start:web` 而非 `node .next/standalone/server.js` |
| 端口占用 | 本机已有服务 | 修改 compose 的 `ports` 映射 |
