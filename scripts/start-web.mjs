#!/usr/bin/env node
// 以 standalone 方式启动 Next.js 站点。
// next.config.mjs 使用 output: 'standalone'，`next start` 在这种模式下不提供路由，
// 因此本地与容器内统一走 .next/standalone/apps/web/server.js，并在启动前把静态资源补齐。
import { cp, access } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import path from 'node:path';
import process from 'node:process';

const ROOT = path.resolve(new URL('..', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const WEB = path.join(ROOT, 'apps', 'web');
const STANDALONE_APP = path.join(WEB, '.next', 'standalone', 'apps', 'web');

async function exists(p) {
  try {
    await access(p);
    return true;
  } catch {
    return false;
  }
}

if (!(await exists(path.join(STANDALONE_APP, 'server.js')))) {
  console.error('未找到 standalone 产物，请先执行 npm run build:web');
  process.exit(1);
}

// 1) 复制 .next/static 到 standalone 目录，否则页面无 CSS/JS
await cp(path.join(WEB, '.next', 'static'), path.join(STANDALONE_APP, '.next', 'static'), {
  recursive: true,
  force: true
});

// 2) 复制 public（如果存在）
const publicDir = path.join(WEB, 'public');
if (await exists(publicDir)) {
  await cp(publicDir, path.join(STANDALONE_APP, 'public'), { recursive: true, force: true });
}

// 端口优先取 WEB_PORT，避免与 API 的 PORT 冲突；容器内通过 HOST_BIND=0.0.0.0 对外监听
const port = process.env.WEB_PORT || process.env.PORT || '3000';
const hostname = process.env.HOST_BIND || '127.0.0.1';
const child = spawn(process.execPath, ['server.js'], {
  cwd: STANDALONE_APP,
  stdio: 'inherit',
  env: {
    ...process.env,
    PORT: String(port),
    HOSTNAME: hostname,
    // 服务端渲染时向 API 取数使用内部地址
    API_BASE_URL: process.env.API_BASE_URL || 'http://127.0.0.1:4000'
  }
});

for (const sig of ['SIGINT', 'SIGTERM']) {
  process.on(sig, () => child.kill(sig));
}
child.on('exit', (code) => process.exit(code ?? 0));
