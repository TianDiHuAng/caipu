#!/usr/bin/env node
// 由 tasks/engineering.json + tasks/progress.json 生成 tasks/TASKS.md
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, readJson } from './lib/loaders.mjs';

const eng = readJson(path.join(ROOT, 'tasks', 'engineering.json'));
const prog = readJson(path.join(ROOT, 'tasks', 'progress.json'));
const taxonomy = readJson(path.join(ROOT, 'data', 'taxonomy.json'));

const catZh = new Map(taxonomy.categories.map((c) => [c.slug, c.zh]));
const catEn = new Map(taxonomy.categories.map((c) => [c.slug, c.en]));

const lines = [];
const now = new Date().toISOString();

let engTotal = 0;
let engDone = 0;
for (const p of eng.phases) for (const it of p.items) { engTotal++; if (it.done) engDone++; }

const t = prog.totals;
lines.push('# 任务清单');
lines.push('');
lines.push(`> 本文件由 \`scripts/sync-tasks.mjs\` 自动生成，请勿直接编辑。`);
lines.push(`> 工程任务源：\`tasks/engineering.json\`；内容任务源：\`tasks/progress.json\`。`);
lines.push(`> 生成时间：${now}`);
lines.push('');
lines.push(`**总览**：工程任务 ${engDone}/${engTotal}；菜谱内容 ${t.actual}/${t.target}（${(t.coverage * 100).toFixed(1)}%），共 ${t.cells} 个「菜系 × 品类」格子，${t.cuisines} 个菜系。`);
lines.push('');

for (const p of eng.phases) {
  lines.push(`## ${p.title}`);
  lines.push('');
  if (p.items.length === 0) {
    lines.push('_内容任务见下方「阶段 4」章节，每个格子一行。_');
    lines.push('');
    continue;
  }
  for (const it of p.items) {
    lines.push(`- [${it.done ? 'x' : ' '}] \`${it.id}\` ${it.title}`);
  }
  lines.push('');
}

// 内容任务
const p4 = eng.phases.find((p) => p.id === 'P4');
lines.push(`## ${p4.title}`);
lines.push('');
for (const regionKey of ['cn', 'intl']) {
  const list = prog.regions[regionKey];
  const label = regionKey === 'cn' ? '中国菜系' : '外国菜系';
  const rTarget = list.reduce((a, x) => a + x.target, 0);
  const rDone = list.reduce((a, x) => a + x.actual, 0);
  lines.push(`### ${label}（${rDone}/${rTarget}）`);
  lines.push('');
  for (const c of list) {
    lines.push(`<details><summary><b>${c.zh} ${c.slug}</b> — ${c.tier} 级，${c.actual}/${c.target}</summary>`);
    lines.push('');
    for (const cell of c.cells) {
      const done = cell.actual >= cell.target;
      const mark = done ? 'x' : ' ';
      lines.push(`- [${mark}] \`P4-${c.slug}/${cell.category}\` ${catZh.get(cell.category) || cell.category}（${catEn.get(cell.category) || ''}）目标 ${cell.target}，已完成 ${cell.actual}`);
    }
    lines.push('');
    lines.push('</details>');
    lines.push('');
  }
}

lines.push('---');
lines.push('');
lines.push('### 抽检任务规则');
lines.push('');
lines.push('每完成约 10 个内容批次，自动新增一个「抽检任务」：随机抽取 5% 已写菜谱，以审稿人视角重读并打分（准确性、完整性、可操作性、安全性），不合格的重写。抽检记录写入 `tasks/REVIEW.md`。');
lines.push('');

fs.writeFileSync(path.join(ROOT, 'tasks', 'TASKS.md'), lines.join('\n'), 'utf8');
console.log(`TASKS.md 已生成：工程 ${engDone}/${engTotal}，内容 ${t.actual}/${t.target}`);
