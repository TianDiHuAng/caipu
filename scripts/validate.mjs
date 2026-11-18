#!/usr/bin/env node
// 菜谱校验入口：node scripts/validate.mjs [--file a.json] [--dir 路径] [--quiet] [--no-dup]
import fs from 'node:fs';
import path from 'node:path';
import {
  ROOT, loadTaxonomy, loadIngredients, loadSchema, walkRecipeFiles, relPath,
  checkTaxonomyConsistency
} from './lib/loaders.mjs';
import { validate } from './lib/schema-lite.mjs';
import { runRecipeRules, runGlobalRules, runDuplicateCheck, buildContext } from './lib/rules.mjs';

const argv = process.argv.slice(2);
const hasFlag = (f) => argv.includes(f);
const argValue = (f) => {
  const i = argv.indexOf(f);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : null;
};

const quiet = hasFlag('--quiet');
const skipDup = hasFlag('--no-dup');
const singleFile = argValue('--file');
const targetDir = argValue('--dir');

const taxonomy = loadTaxonomy();
const dict = loadIngredients();
const schema = loadSchema();
const ctx = buildContext(taxonomy, dict);

const fatal = checkTaxonomyConsistency(taxonomy, dict);

let files;
if (singleFile) files = [path.resolve(ROOT, singleFile)];
else if (targetDir) files = walkRecipeFiles(path.resolve(ROOT, targetDir));
else files = walkRecipeFiles();

const records = [];
let parseFail = 0;

for (const f of files) {
  let data;
  try {
    data = JSON.parse(fs.readFileSync(f, 'utf8').replace(/^\uFEFF/, ''));
  } catch (e) {
    fatal.push(`${relPath(f)}: JSON 解析失败 — ${e.message}`);
    parseFail++;
    continue;
  }
  records.push({ file: f, rel: relPath(f), data });
}

const report = [];
let schemaFail = 0;
let ruleFail = 0;
let totalIssues = 0;

for (const rec of records) {
  const sErrs = validate(schema, rec.data);
  if (sErrs.length) {
    schemaFail++;
    report.push({ rel: rec.rel, id: rec.data?.id, kind: 'SCHEMA', issues: sErrs.slice(0, 25) });
    totalIssues += sErrs.length;
  }
}

// 只有 schema 通过的菜谱才跑内容规则，避免一个字段类型错导致几十条下游噪音
const schemaOk = records.filter((r) => validate(schema, r.data).length === 0);
for (const rec of schemaOk) {
  const rErrs = runRecipeRules(rec.data, ctx);
  if (rErrs.length) {
    ruleFail++;
    report.push({ rel: rec.rel, id: rec.data.id, kind: 'RULES', issues: rErrs.slice(0, 25) });
    totalIssues += rErrs.length;
  }
}

const globalErrs = runGlobalRules(records);
const dupErrs = skipDup ? [] : runDuplicateCheck(records);

const out = [];
out.push(`校验范围: ${files.length} 个文件（成功解析 ${records.length}）`);
out.push(`分类体系: ${taxonomy.cuisines.length} 菜系 / ${taxonomy.categories.length} 品类；食材词典: ${dict.items.length} 项`);

if (fatal.length) {
  out.push(`\n[FATAL] 基础数据错误 ${fatal.length} 项：`);
  for (const e of fatal) out.push('  - ' + e);
}

if (report.length) {
  out.push(`\n[问题文件] ${report.length} 个（schema 失败 ${schemaFail}，规则失败 ${ruleFail}）：`);
  for (const r of report) {
    out.push(`\n· ${r.rel}${r.id ? ' (' + r.id + ')' : ''} [${r.kind}]`);
    for (const i of r.issues) out.push('   - ' + i);
  }
}

if (globalErrs.length) {
  out.push(`\n[全局错误] ${globalErrs.length} 项：`);
  for (const e of globalErrs.slice(0, 60)) out.push('  - ' + e);
  if (globalErrs.length > 60) out.push(`  ... 其余 ${globalErrs.length - 60} 项省略`);
}

if (dupErrs.length) {
  out.push(`\n[文本雷同] ${dupErrs.length} 项：`);
  for (const e of dupErrs) out.push('  - ' + e);
}

const failed = fatal.length + report.length + globalErrs.length + dupErrs.length;
out.push('');
out.push(failed === 0
  ? `✅ 全部通过：${records.length} 道菜谱，0 错误`
  : `❌ 未通过：${failed} 类问题，累计 ${totalIssues + globalErrs.length + dupErrs.length} 条`);

if (!quiet) console.log(out.join('\n'));
else console.log(failed === 0 ? `✅ ${records.length} 道菜谱全部通过` : `❌ ${failed} 类问题`);

process.exit(failed === 0 ? 0 : 1);
