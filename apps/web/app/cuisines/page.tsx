import Link from 'next/link';
import type { Metadata } from 'next';
import { api } from '@/lib/api';

export const metadata: Metadata = { title: '菜系总览', description: '按地域与风格浏览中国八大菜系、地方菜与世界各国菜系。' };

export const dynamic = 'force-dynamic';

export default async function CuisinesPage() {
  const data: any = await api.cuisines();
  const items: any[] = data?.items ?? [];
  const cn = items.filter((c) => c.region === 'cn' || (c.slug ?? '').startsWith('cn-'));
  const world = items.filter((c) => !(c.region === 'cn' || (c.slug ?? '').startsWith('cn-')));
  const group = (list: any[], title: string) =>
    list.length ? (
      <section className="mt-8">
        <h2 className="text-xl font-semibold">{title}</h2>
        <ul className="mt-3 grid gap-2 sm:grid-cols-3">
          {list.map((c) => (
            <li key={c.slug}>
              <Link href={`/cuisines/${c.slug}`} className="flex items-center justify-between rounded border border-slate-200 px-3 py-2 no-underline hover:border-brand-500">
                <span className="text-slate-800">{c.zh ?? c.name}</span>
                {typeof c.count === 'number' ? <span className="text-xs text-slate-500">{c.count} 道</span> : null}
              </Link>
            </li>
          ))}
        </ul>
      </section>
    ) : null;

  return (
    <>
      <h1 className="text-2xl font-bold">菜系总览</h1>
      <p className="mt-2 text-slate-600">共 {items.length} 个菜系。菜系用于描述地域与流派，品类用于描述在餐桌上的位置。</p>
      {group(cn, '中国菜系')}
      {group(world, '世界菜系')}
      {!items.length ? <p className="mt-6 text-slate-500">暂无数据，请确认 API 已启动并可访问 /api/v1/cuisines。</p> : null}
    </>
  );
}
