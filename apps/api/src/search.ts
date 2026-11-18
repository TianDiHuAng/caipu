/**
 * 搜索词扩展：同义词、拼音全拼与首字母。
 *
 * 设计取舍：中文站点的搜索痛点不是拼写纠错，而是「用户说的名字和数据库里的名字不一样」
 * （番茄/西红柿、土豆/马铃薯/洋芋、川菜/四川菜），以及「用户用拼音输入」。
 * 因此这里做两件事：
 * 1) 同义词：食材词典的 aliases 是唯一真相，另加少量菜系/品类口语别名；
 * 2) 拼音：把中文查询转成全拼与首字母，用于匹配 id / name_en（slug 本身即拼音）。
 * 不做模糊纠错与分词，避免引入不可控的召回噪音。
 */
import fs from 'node:fs';
import path from 'node:path';
import { pinyin } from 'pinyin-pro';

type SynonymTable = Map<string, string[]>;

let cached: SynonymTable | null = null;

/** 菜系/品类的口语别名：口语说法 → 规范 slug 关键词 */
const EXTRA_SYNONYMS: Record<string, string[]> = {
  川菜: ['sichuan', '四川'],
  四川菜: ['sichuan'],
  鲁菜: ['shandong', '山东菜'],
  粤菜: ['cantonese', '广东菜'],
  苏菜: ['jiangsu', '江苏菜'],
  浙菜: ['zhejiang', '浙江菜'],
  闽菜: ['fujian', '福建菜'],
  湘菜: ['hunan', '湖南菜'],
  徽菜: ['anhui', '安徽菜'],
  京菜: ['beijing', '北京菜'],
  本帮菜: ['shanghai', '上海菜'],
  东北菜: ['dongbei'],
  西北菜: ['xibei'],
  客家菜: ['hakka'],
  潮汕菜: ['chaoshan'],
  日料: ['japanese', '日本菜'],
  韩餐: ['korean', '韩国菜'],
  西餐: ['western'],
  甜品: ['dessert'],
  下饭菜: ['main-meat', 'main-tofu'],
  快手菜: ['quick'],
  减脂餐: ['low-cal'],
  健身餐: ['low-cal', 'high-protein']
};

function loadSynonyms(): SynonymTable {
  if (cached) return cached;
  const table: SynonymTable = new Map();
  const candidates = [
    path.resolve(process.cwd(), 'data/ingredients.json'),
    path.resolve(process.cwd(), '../../data/ingredients.json')
  ];
  const file = candidates.find((p) => fs.existsSync(p));
  if (file) {
    const dict = JSON.parse(fs.readFileSync(file, 'utf8'));
    for (const item of dict.items ?? []) {
      const all = [item.zh, ...(item.aliases ?? [])].filter(Boolean);
      for (const name of all) {
        const others = all.filter((x) => x !== name);
        table.set(name, others);
      }
    }
  }
  for (const [k, v] of Object.entries(EXTRA_SYNONYMS)) {
    table.set(k, [...(table.get(k) ?? []), ...v]);
  }
  cached = table;
  return table;
}

const hasChinese = (s: string) => /[\u3400-\u9fff]/.test(s);

export interface ExpandedQuery {
  /** 原始词与同义词，用于 LIKE 匹配 */
  terms: string[];
  /** 拼音全拼（仅当查询含中文时有值） */
  fullPinyin: string[];
  /** 拼音首字母（仅当查询含中文时有值） */
  initials: string[];
}

export function expandQuery(raw: string): ExpandedQuery {
  const q = raw.trim();
  if (!q) return { terms: [], fullPinyin: [], initials: [] };

  const synonyms = loadSynonyms().get(q) ?? [];
  const terms = [q, ...synonyms.filter((s) => s !== q)].slice(0, 12);

  let fullPinyin: string[] = [];
  let initials: string[] = [];
  if (hasChinese(q)) {
    const full = pinyin(q, { toneType: 'none', type: 'array' }).join('');
    const short = pinyin(q, { pattern: 'first', toneType: 'none', type: 'array' }).join('');
    if (full) fullPinyin = [full];
    if (short) initials = [short];
  } else {
    // 英文/拼音查询时同时尝试去掉空格的写法
    const compact = q.replace(/\s+/g, '');
    if (compact !== q) fullPinyin = [compact];
  }

  return { terms, fullPinyin, initials };
}
