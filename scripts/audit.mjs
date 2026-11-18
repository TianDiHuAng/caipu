#!/usr/bin/env node
// 抽检（P6-02）：每个菜系随机抽取 5%（向上取整、每菜系至少 1 道），按评审判定规则打分，
// 输出 tasks/AUDIT_REPORT.md。评分只做机械可核查项，语义判断由人工/Agent 复核后填备注。
//
// 用法：
//   node scripts/audit.mjs            # 抽样并写报告
//   node scripts/audit.mjs --seed=42  # 固定随机种子，便于复现
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, walkRecipeFiles, readJson } from './lib/loaders.mjs';

const seedArg = process.argv.find((a) => a.startsWith('--seed='));
const seed = seedArg ? Number(seedArg.split('=')[1]) : 20260101;

// 可复现的伪随机（mulberry32）
function rng(s) {
  let a = s >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
const rand = rng(seed);

/** 单道菜的机械评分（满分 100，各维度按权重扣分） */
export function scoreRecipe(r) {
  const dims = [];
  const add = (name, weight, ratio, note) => dims.push({ name, weight, score: Math.round(weight * ratio), note });

  // 1 准确性：字段完整 + 用时自洽
  const stepTime = (r.steps || []).reduce((a, s) => a + (s.time_min || 0), 0);
  const total = r.time?.total_min || 0;
  let acc = 1;
  if (total < stepTime) acc -= 0.3;
  if (!r.origin_note || r.origin_note.length < 15) acc -= 0.2;
  if (!r.name?.en) acc -= 0.2;
  add('准确性', 25, Math.max(acc, 0));

  // 2 完整性：结构字段数量
  const need = [
    (r.ingredients || []).length >= 2,
    (r.steps || []).length >= 4,
    (r.tips || []).length >= 2,
    (r.common_mistakes || []).length >= 1,
    (r.substitutions || []).length >= 1,
    (r.variations || []).length >= 1,
    !!r.serving_suggestion,
    !!r.storage,
    (r.allergens || []).length >= 0 && !!r.nutrition_estimate?.is_estimate
  ];
  add('完整性', 25, need.filter(Boolean).length / need.length);

  // 3 可操作性：每步都有时间与感官线索
  const steps = r.steps || [];
  const withCue = steps.filter((s) => s.visual_cue && s.visual_cue.length >= 6).length;
  const withTime = steps.filter((s) => (s.time_min || 0) > 0).length;
  const opsRatio = steps.length ? (withCue / steps.length + withTime / steps.length) / 2 : 0;
  add('可操作性', 30, opsRatio);

  // 4 安全性：高风险食材是否写明处理，肉类是否给温度
  const text = JSON.stringify(r.ingredients || []);
  const risky = /豆角|四季豆|木薯|河豚|菌|菇|木耳|银耳|生蚝|牡蛎|蛤|鸡蛋|蛋黄|鸭蛋|猪肝|鸡肝/.test(text);
  const meaty = /牛肉|牛里脊|猪里脊|五花肉|猪排骨|鸡腿肉|鸡胸肉|整鸡|鸭|鱼|虾|蟹/.test(text);
  const safetyText = (r.food_safety_notes || []).join(' ');
  let safe = 1;
  if (risky && !/安全|彻底加热|中心温度|熟透|不要生食|冷藏/.test(safetyText)) safe -= 0.5;
  if (meaty && !/中心温度|熟透|彻底/.test(safetyText)) safe -= 0.3;
  if ((r.food_safety_notes || []).length === 0) safe = 0;
  add('安全性', 20, Math.max(safe, 0));

  const total100 = dims.reduce((a, d) => a + d.score, 0);
  const grade = total100 >= 90 ? 'A' : total100 >= 80 ? 'B' : total100 >= 70 ? 'C' : 'D';
  return { total: total100, grade, dims };
}

const byCuisine = new Map();
for (const f of walkRecipeFiles()) {
  let d;
  try {
    d = readJson(f);
  } catch {
    continue;
  }
  const k = d?.cuisine?.style;
  if (!k) continue;
  if (!byCuisine.has(k)) byCuisine.set(k, []);
  byCuisine.get(k).push({ file: path.relative(ROOT, f), data: d });
}

const rows = [];
for (const [cuisine, list] of [...byCuisine.entries()].sort()) {
  const k = Math.max(1, Math.ceil(list.length * 0.05));
  const pool = [...list];
  const picked = [];
  for (let i = 0; i < k && pool.length; i++) {
    picked.push(pool.splice(Math.floor(rand() * pool.length), 1)[0]);
  }
  for (const p of picked) {
    const s = scoreRecipe(p.data);
    rows.push({ cuisine, id: p.data.id, grade: s.grade, total: s.total, dims: s.dims, file: p.file });
  }
}

const bad = rows.filter((r) => r.grade === 'C' || r.grade === 'D');
const avg = rows.length ? Math.round(rows.reduce((a, r) => a + r.total, 0) / rows.length) : 0;

const lines = [];
lines.push('# 抽检报告（5% 随机）');
lines.push('');
lines.push(`- 生成时间：${new Date().toISOString()}`);
lines.push(`- 随机种子：${seed}（同种子可复现同一批样本）`);
lines.push(`- 覆盖菜系：${byCuisine.size} 个，抽样 ${rows.length} 道，平均分 ${avg}`);
lines.push(`- 需重写（C/D）：${bad.length} 道`);
lines.push('');
lines.push('## 评分口径');
lines.push('');
lines.push('| 维度 | 权重 | 核查内容 |');
lines.push('| --- | --- | --- |');
lines.push('| 准确性 | 25 | 用时总和不小于各步之和、有 origin_note、有英文名 |');
lines.push('| 完整性 | 25 | 配料分组、步骤≥4、tips≥2、常见错误、替代、变体、配餐、保存、营养估算 |');
lines.push('| 可操作性 | 30 | 每一步都有时间与视觉线索 |');
lines.push('| 安全性 | 20 | 高风险食材有处理说明、肉类有中心温度 |');
lines.push('');
lines.push('## 抽检明细');
lines.push('');
lines.push('| 菜系 | 菜谱 id | 得分 | 等级 | 扣分项 |');
lines.push('| --- | --- | --- | --- | --- |');
for (const r of rows.sort((a, b) => a.cuisine.localeCompare(b.cuisine) || a.total - b.total)) {
  const lost = r.dims.filter((d) => d.score < d.weight).map((d) => `${d.name} ${d.score}/${d.weight}`).join('；');
  lines.push(`| ${r.cuisine} | ${r.id} | ${r.total} | ${r.grade} | ${lost || '无'} |`);
}
lines.push('');
lines.push('## 结论');
lines.push('');
if (!bad.length) lines.push(`- 本批 ${rows.length} 道全部达到 B 级及以上，无需重写。`);
else lines.push(`- ${bad.map((b) => `${b.cuisine}/${b.id}（${b.grade}）`).join('、')} 需按明细重写。`);
lines.push('- 语义层（正宗性、地方做法是否被随意改良）由 Agent 复核后在本文件追加备注。');

const out = path.join(ROOT, 'tasks', 'AUDIT_REPORT.md');
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, lines.join('\n') + '\n', 'utf8');
console.log(JSON.stringify({ cuisines: byCuisine.size, sampled: rows.length, avg, needRewrite: bad.map((b) => `${b.cuisine}/${b.id}`) }, null, 2));
