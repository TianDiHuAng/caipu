import { buildApp } from '../apps/api/src/app.ts';
const app = await buildApp({ logger: false });
await app.ready();
const get = async (u) => (await app.inject({ method: 'GET', url: u })).json();

const f = await get('/api/v1/filters');
console.log('filters keys:', Object.keys(f));
for (const k of Object.keys(f)) console.log('  ', k, Array.isArray(f[k]) ? f[k].length : typeof f[k]);

const r = await get('/api/v1/recipes/random?size=2');
console.log('random size=2 ->', r.items.length, r.items.map((x) => x.id));
const r2 = await get('/api/v1/recipes/random');
console.log('random default ->', r2.items.length);
await app.close();
