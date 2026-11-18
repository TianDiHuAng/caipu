import test from 'node:test';
import assert from 'node:assert/strict';
import { scoreRecipe } from '../scripts/audit.mjs';

const good = {
  id: 'demo',
  name: { zh: '示范菜', en: 'Demo Dish' },
  ingredients: [
    { group: 'main', items: [{ name: '牛里脊', amount: 300, unit: 'g' }] },
    { group: 'seasoning', items: [{ name: '盐', amount: 3, unit: 'g' }] }
  ],
  time: { prep_min: 10, cook_min: 10, total_min: 20 },
  steps: [
    { n: 1, text: '牛肉逆纹切片，加盐抓匀静置十分钟。', time_min: 10, visual_cue: '肉片表面发亮' },
    { n: 2, text: '热锅下油，牛肉大火快炒至变色。', time_min: 3, visual_cue: '边缘微焦' },
    { n: 3, text: '调味后翻炒均匀即可出锅装盘。', time_min: 2, visual_cue: '酱汁收紧' },
    { n: 4, text: '静置一分钟让肉汁回流再切片食用。', time_min: 1, visual_cue: '切面无大量汁水' }
  ],
  tips: ['牛肉逆纹切更嫩。', '全程大火快炒。'],
  common_mistakes: ['顺纹切片导致口感发柴。'],
  substitutions: [{ original: '牛里脊', substitute: '肥牛', ratio: '1:1', note: '油脂更多' }],
  variations: ['加黑胡椒做成黑椒牛柳。'],
  serving_suggestion: '配米饭食用。',
  storage: '冷藏一天。',
  nutrition_estimate: { is_estimate: true },
  food_safety_notes: ['牛肉需炒至中心温度 63℃ 以上。'],
  origin_note: '家常快炒做法，各地做法略有差异。'
};

test('完整菜谱应得 A 级', () => {
  const r = scoreRecipe(good);
  assert.ok(r.total >= 90, `实际 ${r.total}`);
  assert.equal(r.grade, 'A');
});

test('缺省字段越多分数越低', () => {
  const poor = {
    ...good,
    steps: [{ n: 1, text: '炒熟。', time_min: 1 }],
    tips: [],
    common_mistakes: [],
    substitutions: [],
    variations: [],
    food_safety_notes: [],
    origin_note: ''
  };
  const r = scoreRecipe(poor);
  assert.ok(r.total < 70, `实际 ${r.total}`);
  assert.ok(['C', 'D'].includes(r.grade));
});

test('肉类缺少温度说明要扣安全性分', () => {
  const r = scoreRecipe({ ...good, food_safety_notes: ['注意卫生。'] });
  const safety = r.dims.find((d) => d.name === '安全性');
  assert.ok(safety.score < safety.weight);
});
