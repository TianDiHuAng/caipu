import { buildApp } from './app.js';

const port = Number(process.env.PORT) || 4000;
const host = process.env.HOST || '0.0.0.0';

const app = await buildApp({ logger: true });
try {
  await app.listen({ port, host });
  app.log.info(`API 已启动：http://localhost:${port}/api/v1/meta`);
} catch (err) {
  app.log.error(err);
  process.exit(1);
}
