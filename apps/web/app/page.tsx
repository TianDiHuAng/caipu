import Link from 'next/link';
import { api, SITE } from '@/lib/api';
import { RecipeGrid, categoryZh } from '@/components/RecipeCard';
import { getLocale } from '@/lib/locale-server';
import { dictFor } from '@/lib/i18n';


export const dynamic = 'force-dynamic';

export default async function HomePage() {
  const locale = getLocale();
  const t = dictFor(locale);
  const [latest, random, cuisines, categories] = await Promise.all([
    api.recipes({ pageSize: 9 }),
    api.random(6),
    api.cuisines(),
    api.categories()
  ]);
  const cuisineItems = (cuisines?.items ?? []).slice(0, 24);
  const categoryItems = (categories?.items ?? []).slice(0, 16);

  return (
    <>
      <section className="rounded-xl bg-brand-50 px-5 py-8">
        <h1 className="text-2xl font-bold text-brand-700 sm:text-3xl">{locale === 'en' ? t('heroTitle') : SITE.name}</h1>
        <p className="mt-2 max-w-2xl text-slate-700">{t('heroDesc')}</p>
        <form action="/search" method="get" className="mt-4 flex max-w-xl gap-2">
          <label htmlFor="q" className="sr-only">搜索菜名、食材或菜系</label>
          <input
            id="q"
            name="q"
            placeholder={t('searchPlaceholder')}
            className="min-w-0 flex-1 rounded-md border border-slate-300 px-3 py-2"
          />
          <button type="submit" className="rounded-md bg-brand-600 px-4 py-2 text-white hover:bg-brand-700">
            {t('searchButton')}
          </button>
        </form>
        <p className="mt-3 text-sm text-slate-600">
          {t('totalRecipes')} {(latest?.total ?? 0).toLocaleString('zh-CN')} {t('recipesUnit')} ·{' '}
          <Link href="/cuisines">{t('byCuisine')}</Link> · <Link href="/categories">{t('byCategory')}</Link> ·{' '}
          <Link href="/ingredients">{t('byIngredient')}</Link>
        </p>
      </section>

      <section className="mt-8">
        <h2 className="text-xl font-semibold">{t('cuisineNav')}</h2>
        <p className="mt-1 text-sm text-slate-500">{t('cuisineNavDesc')}</p>
        <ul className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
          {cuisineItems.map((c) => (
            <li key={c.slug}>
              <Link href={`/cuisines/${c.slug}`} className="block rounded border border-slate-200 px-3 py-2 no-underline hover:border-brand-500">
                <span className="font-medium text-slate-800">{c.zh}</span>
                {typeof c.count === 'number' ? <span className="ml-1 text-xs text-slate-500">({c.count})</span> : null}
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-8">
        <h2 className="text-xl font-semibold">{t('byCategory')}</h2>
        <ul className="mt-3 flex flex-wrap gap-2">
          {categoryItems.map((c) => (
            <li key={c.slug}>
              <Link href={`/categories/${c.slug}`} className="rounded-full border border-slate-200 px-3 py-1 text-sm no-underline hover:border-brand-500">
                {categoryZh[c.slug] ?? c.zh}
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-8">
        <h2 className="text-xl font-semibold">{t('latest')}</h2>
        <div className="mt-3">
          <RecipeGrid items={latest?.items ?? []} />
        </div>
        <p className="mt-3 text-sm">
          <Link href="/search?sort=latest">{t('viewAllLatest')}</Link>
        </p>
      </section>

      <section className="mt-8">
        <h2 className="text-xl font-semibold">{t('randomTitle')}</h2>
        <p className="mt-1 text-sm text-slate-500">{t('randomDesc')}</p>
        <div className="mt-3">
          <RecipeGrid items={random?.items ?? []} />
        </div>
      </section>
    </>
  );
}
