# 单镜像同时跑 API 与网站：一条命令即可 `docker compose up`
# 构建期需要编译 better-sqlite3（若无预编译包），运行期只依赖 sqlite 文件
FROM node:20-bookworm-slim AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1
RUN apt-get update && apt-get install -y --no-install-recommends python3 make g++ ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY package.json package-lock.json ./
COPY apps/api/package.json apps/api/
COPY apps/web/package.json apps/web/
COPY packages/shared/package.json packages/shared/
COPY packages/db/package.json packages/db/
RUN npm ci --include=dev
COPY . .
# 构建期页面全部为动态渲染，API 地址仅用于运行期，构建时给一个占位值即可
ENV API_BASE_URL=http://127.0.0.1:4000
RUN npm run build:web

FROM node:20-bookworm-slim AS runner
WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=4000 \
    HOST=0.0.0.0 \
    CAIPU_DB_PATH=/app/data/db/caipu.sqlite \
    API_BASE_URL=http://127.0.0.1:4000 \
    WEB_PORT=3000 \
    HOST_BIND=0.0.0.0
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates tini \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app /app
RUN chmod +x scripts/docker-entrypoint.sh
EXPOSE 3000 4000
VOLUME ["/app/data/db"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD node -e "fetch('http://127.0.0.1:4000/api/v1/meta').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"
ENTRYPOINT ["/usr/bin/tini", "--", "scripts/docker-entrypoint.sh"]
