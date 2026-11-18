import Link from 'next/link';
import type { Metadata } from 'next';
import { api } from '@/lib/api';
import { categoryZh } from '@/components/RecipeCard';

export const metadata: Metadata = {
  title: '品类总览',
  description: '按餐桌上的位置浏览：前菜、汤、主菜、主食、小吃、甜点、饮品、酱汁等品类。'
};

export const dynamic = 'force-dynamic';

export default async function CategoriesPage() {
  const data: any = await api.categories();
  const items: any[] = data?.items ?? [];
  return (
    <>
      <h1 className="text-2xl font-bold">品类总览</h1>
      <p className="mt-2 text-slate-600">共 {items.length} 个品类。</p>
      <ul className="mt-4 grid gap-2 sm:grid-cols-3">
        {items.map((c) => (
          <li key={c.slug}>
            <Link href={`/categories/${c.slug}`} className="flex items-center justify-between rounded border border-slate-200 px-3 py-2 no-underline hover:border-brand-500">
              <span className="text-slate-800">{categoryZh[c.slug] ?? c.zh ?? c.slug}</span>
              {typeof c.count === 'number' ? <span className="text-xs text-slate-500">{c.count} 道</span> : null}
            </Link>
          </li>
        ))}
      </ul>
      {!items.length ? <p className="mt-6 text-slate-500">暂无数据，请确认 API 可访问 /api/v1/categories。</p> : null}
    </>
  );
}
