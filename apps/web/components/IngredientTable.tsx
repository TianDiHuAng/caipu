'use client';

import { useMemo, useState } from 'react';
import type { IngredientGroup, IngredientRow } from '@/lib/api';

const GROUP_LABEL: Record<string, string> = { main: '主料', aux: '辅料', seasoning: '调料' };

function formatAmount(amount: number): string {
  if (amount >= 10) return String(Math.round(amount * 10) / 10);
  return String(Math.round(amount * 100) / 100);
}

/** 公制 → 家用计量的近似换算；密度未计，标注为近似值 */
function toHousehold(amount: number, unit?: string): string | null {
  if (!unit) return null;
  const u = unit.toLowerCase();
  if (u === 'ml') {
    if (amount >= 240) return `${formatAmount(amount / 240)} 杯`;
    if (amount >= 15) return `${formatAmount(amount / 15)} 汤匙`;
    return `${formatAmount(amount / 5)} 茶匙`;
  }
  if (u === 'g') {
    if (amount >= 200) return `约 ${formatAmount(amount / 200)} 杯（按水密度近似）`;
    if (amount >= 12) return `约 ${formatAmount(amount / 12)} 汤匙（按水密度近似）`;
    return `约 ${formatAmount(amount / 4)} 茶匙（按水密度近似）`;
  }
  return null;
}

export function IngredientTable({
  groups,
  baseServings
}: {
  groups: IngredientGroup[];
  baseServings: number;
}) {
  const [servings, setServings] = useState(baseServings);
  const [mode, setMode] = useState<'metric' | 'household'>('metric');
  const factor = useMemo(() => (baseServings > 0 ? servings / baseServings : 1), [servings, baseServings]);

  return (
    <div>
      <div className="no-print mb-3 flex flex-wrap items-end gap-3 rounded border border-slate-200 bg-slate-50 px-3 py-2 text-sm">
        <label className="flex items-center gap-2">
          份量
          <input
            type="number"
            min={1}
            max={40}
            value={servings}
            onChange={(e) => setServings(Math.min(40, Math.max(1, Number(e.target.value) || 1)))}
            className="w-16 rounded border border-slate-300 px-2 py-1"
            aria-label="份量（人份）"
          />
          人份（原始 {baseServings} 人份，倍数 {formatAmount(factor)}×）
        </label>
        <button
          type="button"
          onClick={() => setMode(mode === 'metric' ? 'household' : 'metric')}
          className="rounded border border-brand-500 px-2 py-1 text-brand-700 hover:bg-brand-50"
        >
          {mode === 'metric' ? '切换为家用计量（近似）' : '切换为公制（g/ml）'}
        </button>
      </div>

      {(groups ?? []).map((g) => {
        const rows = (g.items ?? []) as IngredientRow[];
        if (!rows.length) return null;
        const label = GROUP_LABEL[g.group] ?? g.group;
        return (
          <section key={g.group} className="mb-4">
            <h3 className="mb-1 text-sm font-semibold text-slate-500">{label}</h3>
            <table className="w-full border-collapse text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-left text-xs text-slate-500">
                  <th className="py-1">食材</th>
                  <th className="py-1">用量</th>
                  <th className="py-1">说明</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row, i) => {
                  const amount = typeof row.amount === 'number' ? row.amount * factor : row.amount;
                  const scaled = typeof amount === 'number' ? formatAmount(amount) : amount;
                  const household = typeof amount === 'number' ? toHousehold(amount, row.unit) : null;
                  return (
                    <tr key={`${g.group}-${i}`} className="border-b border-slate-100 align-top">
                      <td className="py-1.5 pr-2">
                        {row.name}
                        {row.optional ? <span className="ml-1 text-xs text-slate-400">（可选）</span> : null}
                      </td>
                      <td className="py-1.5 pr-2 whitespace-nowrap">
                        {mode === 'metric' || !household ? `${scaled} ${row.unit ?? ''}` : household}
                      </td>
                      <td className="py-1.5 text-slate-600">
                        {row.note}
                        {row.substitute ? <span className="ml-1 text-xs text-slate-500">可用 {row.substitute} 替代</span> : null}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </section>
        );
      })}
      <p className="text-xs text-slate-500">
        家用计量为近似换算（1 茶匙≈5 ml、1 汤匙≈15 ml、1 杯≈240 ml）；固体按水密度近似，烘焙等对精度敏感的场景请使用电子秤。
      </p>
    </div>
  );
}
