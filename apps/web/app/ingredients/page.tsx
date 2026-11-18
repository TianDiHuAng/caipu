import type { Metadata } from 'next';
import Link from 'next/link';
import { api } from '@/lib/api';

export const metadata: Metadata = { title: '食材反查', description: '输入家里现有的食材，反查可以用它做的菜谱。' };

export const dynamic = 'force-dynamic';

export default async function IngredientsPage({ searchParams }: { searchParams: { q?: string } }) {
  const q = searchParams.q?.trim();
  const data: any = q ? await api.ingredients(q) : null;
  const items: any[] = data?.items ?? [];

  return (
    <>
      <h1 className="text-2xl font-bold">食材反查</h1>
      <p className="mt-2 text-slate-600">
        输入一种食材（如「五花肉」「番茄」「豆腐」），查看哪些菜谱用到了它。食材名称以食材词典为准，别名会自动归并。
      </p>
      <form method="get" action="/ingredients" className="mt-4 flex max-w-xl gap-2">
        <input name="q" defaultValue={q ?? ''} placeholder="食材名称" className="min-w-0 flex-1 rounded border border-slate-300 px-3 py-2" aria-label="食材名称" />
        <button type="submit" className="rounded bg-brand-600 px-4 py-2 text-white hover:bg-brand-700">查找</button>
      </form>

      {q ? (
        items.length ? (
          <ul className="mt-4 grid gap-2 sm:grid-cols-3">
            {items.map((it) => (
              <li key={it.key}>
                <Link href={`/ingredients/${it.key}`} className="block rounded border border-slate-200 px-3 py-2 no-underline hover:border-brand-500">
                  <span className="text-slate-800">{it.zh ?? it.key}</span>
                  {it.en ? <span className="ml-1 text-xs text-slate-500">{it.en}</span> : null}
                  {it.allergens?.length ? <span className="ml-2 text-xs text-amber-700">过敏原</span> : null}
                </Link>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-4 text-slate-500">词典中未找到「{q}」。可尝试更通用的名称，如「猪肉」「鸡肉」「面粉」。</p>
        )
      ) : (
        <p className="mt-4 text-sm text-slate-500">提示：菜谱详情页配料表中的食材名称同样可点击进入反查页。</p>
      )}
    </>
  );
}
