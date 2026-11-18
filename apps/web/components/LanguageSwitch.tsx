'use client';

import Link from 'next/link';
import { usePathname, useSearchParams } from 'next/navigation';
import { t, type Locale } from '@/lib/i18n';

/** 语言切换：保留当前页面的查询参数，只改 lang 参数 */
export function LanguageSwitch({ locale }: { locale: Locale }) {
  const pathname = usePathname() || '/';
  const params = useSearchParams();
  const next: Locale = locale === 'en' ? 'zh' : 'en';
  const qs = new URLSearchParams(params?.toString() ?? '');
  qs.set('lang', next);
  return (
    <Link
      href={`${pathname}?${qs.toString()}`}
      className="text-sm text-brand-700 no-underline hover:underline"
      aria-label={next === 'en' ? 'Switch to English' : '切换到中文'}
    >
      {t('langSwitch', locale)}
    </Link>
  );
}
