import fs from 'node:fs';
import { buildApp } from '../apps/api/src/app.ts';

const app = await buildApp({ logger: false });
await app.ready();

const g = async (u) => {
  const r = await app.inject({ method: 'GET', url: u });
  return [r.statusCode, r.body];
};

const show = async (u, max = 700) => {
  const [st, body] = await g(u);
  console.log('\n=====', u, st);
  console.log(body.slice(0, max));
};

await show('/api/v1/recipes?pageSize=1');
await show('/api/v1/recipes/nope');
await show('/api/v1/recipes/random?size=2', 500);
await show('/api/v1/filters', 300);
await show('/api/v1/cuisines/sichuan', 500);

const p = JSON.parse(fs.readFileSync('tasks/progress.json', 'utf8').replace(/^\uFEFF/, ''));
console.log('\n===== progress keys', Object.keys(p));
if (p.cells) console.log(JSON.stringify(p.cells[0]));
else console.log(JSON.stringify(p).slice(0, 500));

await app.close();
