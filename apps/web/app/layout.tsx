import type { Metadata } from 'next';
import Link from 'next/link';
import { Suspense } from 'react';
import { cookies } from 'next/headers';
import './globals.css';
import { SITE } from '@/lib/api';
import { dictFor, htmlLang, type Locale } from '@/lib/i18n';
import { LanguageSwitch } from '@/components/LanguageSwitch';

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title: { default: `${SITE.name} · ${SITE.tagline}`, template: `%s | ${SITE.name}` },
  description:
    '收录中国八大菜系与世界各地菜谱，含分步做法、火候时间、感官判断线索、替代方案、过敏原与食品安全提示。',
  keywords: ['菜谱', '食谱', '中国菜', '外国菜', '做法', 'recipe'],
  openGraph: {
    type: 'website',
    locale: 'zh_CN',
    siteName: SITE.name,
    title: SITE.name,
    description: SITE.tagline
  },
  robots: { index: true, follow: true },
  alternates: { canonical: '/', languages: { 'zh-CN': '/', en: '/?lang=en' } }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const cookieLang = cookies().get('lang')?.value;
  const locale: Locale = cookieLang === 'en' ? 'en' : 'zh';
  const t = dictFor(locale);
  const nav = [
    { href: '/', label: t('navHome') },
    { href: '/cuisines', label: t('navCuisines') },
    { href: '/categories', label: t('navCategories') },
    { href: '/ingredients', label: t('navIngredients') },
    { href: '/search', label: t('navSearch') }
  ];

  return (
    <html lang={htmlLang(locale)}>
      <body>
        <header className="border-b border-slate-200 bg-brand-50/60">
          <div className="mx-auto flex max-w-5xl flex-wrap items-center gap-x-6 gap-y-2 px-4 py-3">
            <Link href="/" className="text-lg font-bold text-brand-700 no-underline">
              {locale === 'en' ? t('site') : SITE.name}
            </Link>
            <nav aria-label="主导航" className="flex flex-wrap gap-4 text-sm">
              {nav.map((n) => (
                <Link key={n.href} href={n.href} className="text-slate-700 no-underline hover:text-brand-600">
                  {n.label}
                </Link>
              ))}
            </nav>
            <div className="ml-auto">
              <Suspense fallback={null}>
                <LanguageSwitch locale={locale} />
              </Suspense>
            </div>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-4 py-6">{children}</main>
        <footer className="mx-auto max-w-5xl px-4 py-8 text-sm text-slate-500">
          <p>
            {locale === 'en' ? t('site') : SITE.name} · {t('footerNote')}
          </p>
          <p className="mt-1">{t('footerDisclaimer')}</p>
        </footer>
      </body>
    </html>
  );
}
