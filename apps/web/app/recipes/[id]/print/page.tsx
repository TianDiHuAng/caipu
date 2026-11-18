import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { api } from '@/lib/api';
import { PrintButton } from '@/components/PrintButton';


type Props = { params: { id: string } };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const r = await api.recipe(params.id);
  return { title: r ? `${r.name?.zh} · 打印视图` : '打印视图', robots: { index: false, follow: false } };
}

export const dynamic = 'force-dynamic';

export default async function PrintView({ params }: Props) {
  const r = await api.recipe(params.id);
  if (!r) notFound();
  const groups: Array<['main' | 'aux' | 'seasoning', string]> = [
    ['main', '主料'], ['aux', '辅料'], ['seasoning', '调料']
  ];
  return (
    <article className="text-slate-900">
      <div className="no-print mb-4 flex items-center gap-4 text-sm">
        <Link href={`/recipes/${r.id}`}>返回菜谱</Link>
        <PrintButton />
      </div>
      <h1 className="text-2xl font-bold">{r.name?.zh}</h1>
      <p className="mt-1 text-sm text-slate-600">
        {r.servings} 人份 · 难度 {r.difficulty}/5 · 总计 {r.time?.total_min} 分钟 · {r.cuisine?.style}
      </p>

      <h2 className="mt-4 border-b border-slate-300 pb-1 text-lg font-semibold">配料</h2>
      {groups.map(([key, label]) => {
        const rows = ((r.ingredients as any)?.[key] ?? []) as any[];
        if (!rows.length) return null;
        return (
          <div key={key} className="mt-2">
            <h3 className="text-sm font-semibold text-slate-600">{label}</h3>
            <ul className="mt-1 grid grid-cols-2 gap-x-6 text-sm">
              {rows.map((i, idx) => (
                <li key={idx} className="flex justify-between border-b border-dotted border-slate-200 py-0.5">
                  <span>{i.name}</span>
                  <span>{i.amount} {i.unit}</span>
                </li>
              ))}
            </ul>
          </div>
        );
      })}

      <h2 className="mt-4 border-b border-slate-300 pb-1 text-lg font-semibold">做法</h2>
      <ol className="mt-2 space-y-2 text-sm">
        {(r.steps ?? []).map((s) => (
          <li key={s.n}>
            <span className="font-semibold">{s.n}.</span> {s.text}
            {s.time_min ? <span className="text-slate-600">（{s.time_min} 分钟）</span> : null}
            {s.visual_cue ? <span className="text-slate-600"> 完成标志：{s.visual_cue}</span> : null}
          </li>
        ))}
      </ol>

      {r.tips?.length ? (
        <>
          <h2 className="mt-4 border-b border-slate-300 pb-1 text-lg font-semibold">要点</h2>
          <ul className="mt-2 list-disc pl-5 text-sm">{r.tips.map((t, i) => <li key={i}>{t}</li>)}</ul>
        </>
      ) : null}

      {r.food_safety_notes?.length ? (
        <p className="mt-3 border border-slate-400 p-2 text-sm">
          <strong>安全提示：</strong>{r.food_safety_notes.join('；')}
        </p>
      ) : null}
      {r.allergens?.length ? <p className="mt-2 text-sm">过敏原：{r.allergens.join('、')}</p> : null}
    </article>
  );
}
