import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import { api, SITE, type Recipe } from '@/lib/api';
import { IngredientTable } from '@/components/IngredientTable';
import { RecipeGrid, flavorZh, categoryZh } from '@/components/RecipeCard';


type Props = { params: { id: string } };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const r = await api.recipe(params.id);
  if (!r) return { title: '菜谱未找到' };
  const name = r.name?.zh ?? r.id;
  const desc = `${name} 的做法：${r.steps?.length ?? 0} 个步骤、${r.tips?.length ?? 0} 条要点，含火候、时间与判断熟度的线索。`;
  return {
    title: name,
    description: desc,
    alternates: { canonical: `/recipes/${r.id}` },
    openGraph: { title: name, description: desc, type: 'article', url: `${SITE.url}/recipes/${r.id}` }
  };
}

function jsonLd(r: Recipe) {
  const total = r.time?.total_min;
  const data = {
    '@context': 'https://schema.org',
    '@type': 'Recipe',
    name: r.name?.zh,
    alternateName: r.name?.en,
    description: `${r.name?.zh ?? ''} 的做法与要点`,
    recipeCategory: (r.category ?? []).map((c) => categoryZh[c] ?? c),
    recipeCuisine: r.cuisine?.style,
    keywords: (r.tags ?? []).join(','),
    totalTime: total ? `PT${total}M` : undefined,
    prepTime: r.time?.prep_min ? `PT${r.time.prep_min}M` : undefined,
    cookTime: r.time?.cook_min ? `PT${r.time.cook_min}M` : undefined,
    recipeYield: r.servings ? `${r.servings} 人份` : undefined,
    recipeIngredient: ['main', 'aux', 'seasoning'].flatMap((k) =>
      ((r.ingredients as any)?.[k] ?? []).map((i: any) => `${i.name} ${i.amount ?? ''}${i.unit ?? ''}`)
    ),
    recipeInstructions: (r.steps ?? []).map((s) => ({ '@type': 'HowToStep', position: s.n, text: s.text })),
    datePublished: r.created_at,
    dateModified: r.updated_at,
    inLanguage: 'zh-CN'
  };
  return JSON.stringify(data).replace(/</g, '\\u003c');
}

export const dynamic = 'force-dynamic';

export default async function RecipeDetail({ params }: Props) {
  const [r, related] = await Promise.all([api.recipe(params.id), api.related(params.id)]);
  if (!r) notFound();

  return (
    <article>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: jsonLd(r) }} />
      <nav aria-label="面包屑" className="text-sm text-slate-500">
        <Link href="/">首页</Link> / <Link href={`/cuisines/${r.cuisine?.style}`}>{r.cuisine?.style}</Link> /{' '}
        <span>{r.name?.zh}</span>
      </nav>

      <header className="mt-2">
        <h1 className="text-2xl font-bold sm:text-3xl">{r.name?.zh}</h1>
        {r.name?.en ? <p className="mt-1 text-slate-500">{r.name.en}</p> : null}
        <ul className="mt-3 flex flex-wrap gap-2 text-xs text-slate-700">
          <li className="rounded bg-brand-50 px-2 py-1 text-brand-700">难度 {r.difficulty}/5</li>
          {r.time?.prep_min ? <li className="rounded bg-slate-100 px-2 py-1">准备 {r.time.prep_min} 分钟</li> : null}
          {r.time?.cook_min ? <li className="rounded bg-slate-100 px-2 py-1">加热 {r.time.cook_min} 分钟</li> : null}
          {r.time?.total_min ? <li className="rounded bg-slate-100 px-2 py-1">总计 {r.time.total_min} 分钟</li> : null}
          {r.servings ? <li className="rounded bg-slate-100 px-2 py-1">{r.servings} 人份</li> : null}
          {(r.flavor ?? []).map((f) => (
            <li key={f} className="rounded bg-slate-100 px-2 py-1">{flavorZh[f] ?? f}</li>
          ))}
        </ul>
        <p className="mt-3 text-sm">
          <Link href={`/recipes/${r.id}/print`} className="no-print">打印视图</Link>
          {r.allergens?.length ? <span className="ml-4 text-slate-600">过敏原：{r.allergens.join('、')}</span> : null}
        </p>
      </header>

      <section className="mt-6">
        <h2 className="text-xl font-semibold">配料</h2>
        <div className="mt-2">
          <IngredientTable groups={r.ingredients ?? {}} baseServings={r.servings ?? 2} />
        </div>
        {r.equipment?.length ? <p className="mt-2 text-sm text-slate-600">器具：{r.equipment.join('、')}</p> : null}
      </section>

      <section className="mt-8">
        <h2 className="text-xl font-semibold">做法</h2>
        <ol className="mt-2 space-y-4">
          {(r.steps ?? []).map((s) => (
            <li key={s.n} className="rounded border border-slate-200 p-3">
              <p className="font-medium">
                第 {s.n} 步
                {s.time_min ? <span className="ml-2 text-xs font-normal text-slate-500">{s.time_min} 分钟</span> : null}
                {s.heat ? <span className="ml-2 text-xs font-normal text-slate-500">{s.heat}</span> : null}
              </p>
              <p className="mt-1 text-slate-700">{s.text}</p>
              {s.tip ? <p className="mt-1 text-sm text-brand-700">要点：{s.tip}</p> : null}
              {s.visual_cue ? <p className="mt-1 text-sm text-slate-600">判断完成：{s.visual_cue}</p> : null}
            </li>
          ))}
        </ol>
      </section>

      {r.tips?.length ? (
        <section className="mt-8">
          <h2 className="text-xl font-semibold">关键要点</h2>
          <ul className="mt-2 list-disc pl-5 text-slate-700">
            {r.tips.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </section>
      ) : null}

      {r.common_mistakes?.length ? (
        <section className="mt-8">
          <h2 className="text-xl font-semibold">常见失误</h2>
          <ul className="mt-2 list-disc pl-5 text-slate-700">
            {r.common_mistakes.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </section>
      ) : null}

      {r.substitutions?.length ? (
        <section className="mt-8">
          <h2 className="text-xl font-semibold">食材替代</h2>
          <table className="mt-2 w-full border-collapse text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-left text-xs text-slate-500">
                <th className="py-1">原食材</th><th className="py-1">替代</th><th className="py-1">比例</th><th className="py-1">说明</th>
              </tr>
            </thead>
            <tbody>
              {(r.substitutions as any[]).map((s, i) => {
                const row = Array.isArray(s) ? s : [s.from, s.to, s.ratio, s.note];
                return (
                  <tr key={i} className="border-b border-slate-100 align-top">
                    <td className="py-1.5 pr-2">{row[0]}</td><td className="py-1.5 pr-2">{row[1]}</td>
                    <td className="py-1.5 pr-2">{row[2]}</td><td className="py-1.5 text-slate-600">{row[3]}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </section>
      ) : null}

      {r.variations?.length ? (
        <section className="mt-8">
          <h2 className="text-xl font-semibold">做法变化</h2>
          <ul className="mt-2 list-disc pl-5 text-slate-700">
            {r.variations.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </section>
      ) : null}

      <section className="mt-8 grid gap-4 sm:grid-cols-2">
        {r.serving_suggestion ? (
          <div className="rounded border border-slate-200 p-3">
            <h2 className="font-semibold">上桌建议</h2>
            <p className="mt-1 text-sm text-slate-700">{r.serving_suggestion}</p>
          </div>
        ) : null}
        {r.storage ? (
          <div className="rounded border border-slate-200 p-3">
            <h2 className="font-semibold">保存与复热</h2>
            <p className="mt-1 text-sm text-slate-700">{r.storage}</p>
          </div>
        ) : null}
      </section>

      {r.food_safety_notes?.length ? (
        <section className="mt-8 rounded border border-amber-300 bg-amber-50 p-3">
          <h2 className="font-semibold text-amber-900">食品安全提示</h2>
          <ul className="mt-1 list-disc pl-5 text-sm text-amber-900">
            {r.food_safety_notes.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </section>
      ) : null}

      {r.nutrition_estimate ? (
        <section className="mt-8">
          <h2 className="text-xl font-semibold">营养估算</h2>
          <p className="mt-1 text-sm text-slate-600">
            {(r.nutrition_estimate as any).basis}：热量约 {(r.nutrition_estimate as any).calories_kcal} kcal，蛋白质{' '}
            {(r.nutrition_estimate as any).protein_g} g，脂肪 {(r.nutrition_estimate as any).fat_g} g，碳水{' '}
            {(r.nutrition_estimate as any).carbs_g} g，钠 {(r.nutrition_estimate as any).sodium_mg} mg。
          </p>
          <p className="mt-1 text-xs text-slate-500">
            以上为估算值，不构成营养或医疗建议。{(r.nutrition_estimate as any).disclaimer}
          </p>
        </section>
      ) : null}

      {r.origin_note ? (
        <section className="mt-8">
          <h2 className="text-xl font-semibold">来历与背景</h2>
          <p className="mt-1 text-sm text-slate-700">{r.origin_note}</p>
        </section>
      ) : null}

      {(related?.items ?? []).length ? (
        <section className="mt-10 no-print">
          <h2 className="text-xl font-semibold">相关菜谱</h2>
          <div className="mt-3">
            <RecipeGrid items={related!.items} />
          </div>
        </section>
      ) : null}
    </article>
  );
}
