#!/usr/bin/env bash
# 容器入口：建库 → 导入菜谱 → 起 API → 起网站（前台）
set -euo pipefail
cd /app

DB="${CAIPU_DB_PATH:-/app/data/db/caipu.sqlite}"
mkdir -p "$(dirname "$DB")"

if [ "${SEED_IF_EMPTY:-1}" = "1" ] && [ ! -s "$DB" ]; then
  echo "[entrypoint] 未发现数据库，初始化 schema ..."
  npm run db:init
  echo "[entrypoint] 导入 data/recipes ..."
  npm run import
fi

if [ "${FORCE_IMPORT:-0}" = "1" ]; then
  echo "[entrypoint] FORCE_IMPORT=1，重新导入菜谱数据 ..."
  npm run import
fi

echo "[entrypoint] 启动 API :${PORT:-4000}"
npm run start:api &
API_PID=$!

# 等 API 就绪，避免网站首个请求打到未启动的接口
for i in $(seq 1 60); do
  if node -e "fetch('http://127.0.0.1:${PORT:-4000}/api/v1/meta').then(r=>process.exit(r.ok?0:1)).catch(()=>process.exit(1))"; then
    echo "[entrypoint] API 就绪"
    break
  fi
  sleep 1
done

echo "[entrypoint] 启动网站 :${WEB_PORT:-3000}"
WEB_PORT="${WEB_PORT:-3000}" npm run start:web &
WEB_PID=$!

term() {
  kill -TERM "$WEB_PID" "$API_PID" 2>/dev/null || true
  wait "$WEB_PID" "$API_PID" 2>/dev/null || true
  exit 0
}
trap term INT TERM

# 任一进程退出则整体退出，交给容器重启策略
wait -n "$API_PID" "$WEB_PID"
