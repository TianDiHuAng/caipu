// 菜谱内容质量规则：对应 STYLE.md「质量门槛」8 条与若干一致性规则
import { buildNameIndex, buildKeyIndex } from './loaders.mjs';

const PLACEHOLDER_PATTERNS = [
  { re: /TODO|FIXME|TBD/i, label: '占位符 TODO/FIXME' },
  { re: /待补|待完善|待定|后续补充|后续可|以后再说/, label: '占位表述' },
  { re: /同上|同前|见上|参照上文/, label: '省略表述' },
  { re: /…{2,}|\.{3,}/, label: '省略号' },
  { re: /^\s*$/, label: '空文本' }
];

const OIL_KEYS = new Set([
  'rapeseed-oil', 'peanut-oil', 'vegetable-oil', 'olive-oil',
  'lard', 'coconut-oil', 'sesame-oil', 'chili-oil'
]);

const PROTEIN_PER_PIECE = {
  egg: 55, meat: 90, poultry: 100, seafood: 70, vegetable: 130,
  fruit: 150, grain: 60, legume: 80, fungus: 20, dairy: 100, other: 60
};

const MENTION_SCOPE = new Set([
  'meat', 'poultry', 'seafood', 'egg', 'legume', 'fungus', 'grain',
  'vegetable', 'fruit', 'dairy', 'nut'
]);

const ANIMAL_CATEGORIES = new Set(['meat', 'poultry', 'seafood']);

/** 单位换算为近似克重 */
export function toGrams(amount, unit, entry) {
  if (unit === 'to-taste') return 0;
  const n = Number(amount) || 0;
  switch (unit) {
    case 'g':
    case 'ml':
      return n;
    case 'piece':
      return n * (PROTEIN_PER_PIECE[entry?.category] ?? 60);
    case 'clove':
      return n * 5;
    case 'slice':
      return n * 15;
    case 'stalk':
      return n * 20;
    case 'pinch':
      return n * 1;
    default:
      return n;
  }
}

function collectText(recipe) {
  const parts = [];
  for (const s of recipe.steps || []) {
    parts.push(s.text || '', s.tip || '', s.visual_cue || '');
  }
  parts.push(...(recipe.tips || []));
  parts.push(...(recipe.common_mistakes || []));
  parts.push(...(recipe.substitutions || []));
  parts.push(...(recipe.variations || []));
  parts.push(recipe.serving_suggestion || '', recipe.storage || '',
    recipe.food_safety_notes || '', recipe.origin_note || '');
  return parts.join('\n');
}

/** 构造名称→条目索引，并按名称长度降序（用于最长匹配） */
function makeMatcher(dict) {
  const names = [];
  for (const item of dict.items) {
    names.push([item.zh, item]);
    for (const a of item.aliases || []) if (a.length >= 2) names.push([a, item]);
  }
  names.sort((a, b) => b[0].length - a[0].length);
  return names;
}

/** 在文本中做最长优先匹配，返回命中的条目集合 */
function matchIngredients(text, matcher) {
  const hit = new Set();
  const consumed = new Uint8Array(text.length);
  for (const [name, item] of matcher) {
    let from = 0;
    for (;;) {
      const idx = text.indexOf(name, from);
      if (idx === -1) break;
      from = idx + name.length;
      let free = true;
      for (let i = idx; i < idx + name.length; i++) {
        if (consumed[i]) { free = false; break; }
      }
      if (!free) continue;
      for (let i = idx; i < idx + name.length; i++) consumed[i] = 1;
      hit.add(item);
    }
  }
  return hit;
}

/**
 * 单道菜谱的全部规则检查（不含跨文件检查）
 * @returns {string[]} 错误信息
 */
export function runRecipeRules(recipe, ctx) {
  const { taxonomy, dict, nameIndex, keyIndex, matcher, schemaErrors } = ctx;
  const errs = [];
  const push = (m) => errs.push(m);

  const cuisineCfg = taxonomy.cuisines.find((c) => c.slug === recipe.cuisine?.style);
  const allText = collectText(recipe);
  // 配料引用检查只针对「烹饪步骤本体」（步骤文本/提示/感官线索），
  // 不包含 tips、variations、substitutions、serving_suggestion 等旁述字段，
  // 否则「鸡胸肉可替代鸡腿肉」这类合理旁述会被误判为缺失配料。
  const stepScopeText = (recipe.steps || [])
    .map((s) => `${s.text || ''} ${s.tip || ''} ${s.visual_cue || ''}`)
    .join('\n');

  // ---------- R2 占位符与文本规范 ----------
  const textFields = [
    ['serving_suggestion', recipe.serving_suggestion],
    ['storage', recipe.storage],
    ['food_safety_notes', recipe.food_safety_notes],
    ['origin_note', recipe.origin_note],
    ['name.zh', recipe.name?.zh],
    ['name.en', recipe.name?.en]
  ];
  for (const [label, val] of textFields) {
    if (typeof val !== 'string') continue;
    for (const { re, label: pl } of PLACEHOLDER_PATTERNS) {
      if (re.test(val)) push(`${label}: 命中${pl}`);
    }
  }
  for (const s of recipe.steps || []) {
    if (s.text && /适量/.test(s.text)) push(`steps[${s.n}]: 步骤文本不得出现"适量"，须给具体用量`);
    if (s.text && s.text.length < 12) push(`steps[${s.n}]: 步骤文本过短（${s.text.length} 字），需含动作+火候+时间+感官线索`);
    if (!s.visual_cue || s.visual_cue.length < 8) push(`steps[${s.n}]: visual_cue 过短，需写明外观/气味/口感判断依据`);
    if (!s.tip || s.tip.length < 6) push(`steps[${s.n}]: tip 过短`);
  }
  for (const t of recipe.tips || []) {
    if (t.length < 8) push(`tips: 条目过短：「${t}」`);
  }

  // ---------- R3 用量合理性 ----------
  const servings = recipe.servings || 1;
  const time = recipe.time || {};
  const sumPrepCook = (time.prep_min || 0) + (time.cook_min || 0);
  if (Math.abs(sumPrepCook - (time.total_min || 0)) > 5) {
    push(`time: prep(${time.prep_min})+cook(${time.cook_min})=${sumPrepCook} 与 total(${time.total_min}) 相差超过 5 分钟`);
  }
  if ((recipe.steps || []).length > 0) {
    const stepTime = (recipe.steps || []).reduce((a, s) => a + (s.time_min || 0), 0);
    if (time.total_min && stepTime > time.total_min * 2 + 10) {
      push(`time: 步骤时间合计 ${stepTime} 分远超 total ${time.total_min} 分（含并行工序时请下调步骤时长）`);
    }
  }

  let mainGram = 0, saltGram = 0, oilMl = 0, toTasteCount = 0;
  const usedNames = new Set();
  const declaredItems = new Set();
  const allergenSet = new Set();

  for (const group of recipe.ingredients || []) {
    for (const it of group.items || []) {
      const entry = nameIndex.get(it.name);
      if (!entry) {
        push(`ingredients: 「${it.name}」未在 data/ingredients.json 登记，请先补录词典`);
        continue;
      }
      declaredItems.add(entry);
      for (const a of entry.allergens) allergenSet.add(a);

      const grams = toGrams(it.amount, it.unit, entry);
      if (it.unit === 'to-taste') {
        toTasteCount++;
        if (!it.note || !/\d/.test(it.note)) {
          push(`ingredients: 「${it.name}」使用 to-taste 时 note 必须给出参考用量范围（含数字）`);
        }
        if (!['盐', '白糖', '生抽', '食用油', '香油', '白胡椒', '黑胡椒', '味精', '香醋'].includes(it.name)) {
          push(`ingredients: 「${it.name}」不在 to-taste 白名单内，必须给精确用量`);
        }
      } else if (!(Number(it.amount) > 0)) {
        push(`ingredients: 「${it.name}」用量必须为正数，当前 ${it.amount}`);
      }

      if (group.group === 'main') mainGram += grams;
      if (entry.key === 'salt') saltGram += grams;
      if (OIL_KEYS.has(entry.key)) oilMl += Math.max(grams, 0);

      // 该配料是否在烹饪步骤中被使用
      const candidates = [it.name, entry.zh, ...(entry.aliases || [])].filter((x) => x && x.length >= 1);
      if (candidates.some((c) => stepScopeText.includes(c))) usedNames.add(entry);
      else push(`ingredients: 「${it.name}」在全部步骤与提示中均未被使用`);
    }
  }

  const perMain = mainGram / servings;
  if (perMain < 60) push(`用量: 每份主料约 ${Math.round(perMain)}g，低于 60g 下限（份量或用量可能写错）`);
  if (perMain > 700) push(`用量: 每份主料约 ${Math.round(perMain)}g，超过 700g 上限`);
  const saltPerServing = saltGram / servings;
  if (saltPerServing > 6.5) push(`用量: 每份盐约 ${saltPerServing.toFixed(1)}g，超过 6g 上限`);
  const isFried = /炸|油温|复炸/.test(allText);
  const oilLimit = (isFried ? 90 : 45) * servings;
  if (oilMl > oilLimit) push(`用量: 总油量 ${Math.round(oilMl)}ml 超过上限 ${Math.round(oilLimit)}ml（${isFried ? '油炸' : '常规'}）`);

  // ---------- R4 步骤与配料互相引用 ----------
  // 已声明配料的全部写法，用于「包含关系豁免」：如文本中的「葱段」已被配料「大葱」覆盖
  const declaredNames = [];
  for (const entry of declaredItems) {
    declaredNames.push(entry.zh, ...(entry.aliases || []));
  }
  const coveredByDeclared = (item) => {
    const own = [item.zh, ...(item.aliases || [])].filter((x) => x && x.length >= 2);
    return declaredNames.some((d) => d && own.some((n) => d.includes(n) || n.includes(d)));
  };
  const mentioned = matchIngredients(stepScopeText, matcher);
  for (const item of mentioned) {
    if (!MENTION_SCOPE.has(item.category)) continue;
    if (declaredItems.has(item)) continue;
    if (usedNames.has(item)) continue;
    if (coveredByDeclared(item)) continue;
    push(`steps: 文本提到「${item.zh}」，但配料表中没有该食材`);
  }

  // ---------- R5 过敏原一致性 ----------
  const declared = [...(recipe.allergens || [])].sort();
  const expected = [...allergenSet].sort();
  const missing = expected.filter((a) => !declared.includes(a));
  const extra = declared.filter((a) => !expected.includes(a));
  if (missing.length) push(`allergens: 缺少由配料推导出的过敏原 ${missing.join(', ')}`);
  if (extra.length) push(`allergens: 多出配料中不存在的过敏原 ${extra.join(', ')}`);

  // ---------- R6 饮食标签与配料一致性 ----------
  const diet = new Set(recipe.diet_tags || []);
  const hasAnimal = [...declaredItems].some((e) => ANIMAL_CATEGORIES.has(e.category));
  const hasEggOrDairy = [...declaredItems].some((e) => e.category === 'egg' || e.category === 'dairy');
  const hasHoney = [...declaredItems].some((e) => e.key === 'honey');
  const hasPork = [...declaredItems].some((e) => /猪|培根|火腿|腊肉/.test(e.zh));
  const hasAlcohol = [...declaredItems].some((e) => /酒|味醂/.test(e.key) || /酒/.test(e.zh));
  if (diet.has('vegan')) {
    if (hasAnimal || hasEggOrDairy || hasHoney) push('diet_tags: 标记 vegan，但配料含动物性食材、蛋奶或蜂蜜');
    if (allergenSet.size && (allergenSet.has('fish') || allergenSet.has('crustacean') || allergenSet.has('mollusk') || allergenSet.has('meat'))) {
      push('diet_tags: 标记 vegan，但过敏原含水产');
    }
  }
  if (diet.has('vegetarian') && hasAnimal) push('diet_tags: 标记 vegetarian，但配料含肉/禽/水产');
  if (diet.has('pescatarian') && [...declaredItems].some((e) => e.category === 'meat' || e.category === 'poultry')) {
    push('diet_tags: 标记 pescatarian，但配料含畜肉或禽肉');
  }
  if (diet.has('gluten-free') && allergenSet.has('gluten')) push('diet_tags: 标记 gluten-free，但过敏原含麸质');
  if (diet.has('dairy-free') && allergenSet.has('milk')) push('diet_tags: 标记 dairy-free，但过敏原含乳');
  if (diet.has('halal') && (hasPork || hasAlcohol)) push('diet_tags: 标记 halal，但配料含猪肉或酒类');
  if (diet.has('low-carb') && (recipe.category || []).some((c) => /^staple-|bakery|dessert/.test(c))) {
    push('diet_tags: 标记 low-carb，但品类为主食/烘焙/甜点');
  }

  // ---------- R7 结构门槛 ----------
  const isDrink = (recipe.category || []).includes('drink');
  const minSteps = isDrink ? 3 : 4;
  if ((recipe.steps || []).length < minSteps) push(`steps: 至少需要 ${minSteps} 步，当前 ${(recipe.steps || []).length} 步`);
  (recipe.steps || []).forEach((s, i) => {
    if (s.n !== i + 1) push(`steps[${i}]: n 序号应为 ${i + 1}，实际 ${s.n}`);
  });

  // ---------- R8 分类一致性 ----------
  if (cuisineCfg) {
    if (cuisineCfg.unsupported.some((c) => (recipe.category || []).includes(c))) {
      push(`category: ${cuisineCfg.zh} 不支持品类 ${(recipe.category || []).filter((c) => cuisineCfg.unsupported.includes(c)).join(', ')}`);
    }
  } else {
    push(`cuisine.style: 「${recipe.cuisine?.style}」不在 taxonomy 菜系表中`);
  }
  if (recipe.cuisine?.region !== 'cn' && recipe.cuisine?.region !== 'intl') {
    push(`cuisine.region: 必须是 cn 或 intl`);
  } else if (cuisineCfg && cuisineCfg.region !== recipe.cuisine.region) {
    push(`cuisine.region: 与 taxonomy 中 ${cuisineCfg.slug} 的 ${cuisineCfg.region} 不一致`);
  }
  const knownCats = new Set(taxonomy.categories.map((c) => c.slug));
  for (const c of recipe.category || []) {
    if (!knownCats.has(c)) push(`category: 「${c}」不是合法品类`);
  }

  // ---------- R9 食品安全 ----------
  const risky = [...declaredItems].filter((e) => /豆角|四季豆|木薯|河豚|菌|菇|木耳|银耳|生蚝|牡蛎|蛤|生食|鸡肝|猪肝|鸡蛋|蛋黄|鸭蛋/.test(e.zh));
  if (risky.length && !/安全|彻底加热|中心温度|熟透|不要生食|冷藏/.test(recipe.food_safety_notes || '')) {
    push(`food_safety_notes: 含高风险食材（${risky.map((e) => e.zh).join('、')}），必须写明安全处理要求`);
  }

  if (schemaErrors && schemaErrors.length) {
    // schema 错误在 validate 主流程单独汇报，这里不重复
  }

  return errs;
}

/** 跨文件检查：id 唯一、related_ids 有效、路径与字段一致 */
export function runGlobalRules(records) {
  const errs = [];
  const byId = new Map();
  for (const r of records) {
    const id = r.data?.id;
    if (!id) continue;
    if (byId.has(id)) errs.push(`${r.rel}: id「${id}」与 ${byId.get(id)} 重复`);
    else byId.set(id, r.rel);

    const expectSuffix = `/data/recipes/${r.data.cuisine?.region}/${r.data.cuisine?.style}/${id}.json`;
    if (!('/' + r.rel).endsWith(expectSuffix)) {
      errs.push(`${r.rel}: 文件路径应与 cuisine 和 id 一致，期望 data/recipes/${r.data.cuisine?.region}/${r.data.cuisine?.style}/${id}.json`);
    }
  }
  for (const r of records) {
    for (const rid of r.data?.related_ids || []) {
      if (!byId.has(rid)) errs.push(`${r.rel}: related_ids 中的「${rid}」不存在`);
      if (rid === r.data.id) errs.push(`${r.rel}: related_ids 不能包含自身`);
    }
  }
  return errs;
}

/** 跨菜谱文本雷同检测：20 字滑窗，出现在 5 个以上菜谱即判定雷同 */
export function runDuplicateCheck(records, windowSize = 20, threshold = 5) {
  const map = new Map();
  for (const r of records) {
    const d = r.data;
    const chunks = [];
    for (const s of d.steps || []) chunks.push(s.text || '');
    chunks.push(...(d.tips || []), ...(d.common_mistakes || []));
    chunks.push(d.serving_suggestion || '', d.origin_note || '');
    const text = chunks.join('').replace(/[\s，。、；：！？,.;:!?"'“”‘’（）()]/g, '');
    const seen = new Set();
    for (let i = 0; i + windowSize <= text.length; i++) {
      const w = text.slice(i, i + windowSize);
      if (seen.has(w)) continue;
      seen.add(w);
      if (!map.has(w)) map.set(w, new Set());
      map.get(w).add(d.id);
    }
  }
  const errs = [];
  let reported = 0;
  for (const [w, ids] of map) {
    if (ids.size >= threshold && reported < 40) {
      errs.push(`文本雷同: 「${w}」出现在 ${ids.size} 个菜谱（${[...ids].slice(0, 5).join(', ')}）`);
      reported++;
    }
  }
  return errs;
}

export function buildContext(taxonomy, dict) {
  return {
    taxonomy,
    dict,
    nameIndex: buildNameIndex(dict),
    keyIndex: buildKeyIndex(dict),
    matcher: makeMatcher(dict)
  };
}
