import { cookies, headers } from 'next/headers';
import type { Locale } from './i18n';

/** 服务端读取当前界面语言：中间件注入的 x-locale 优先，其次 cookie，默认中文 */
export function getLocale(): Locale {
  const fromHeader = headers().get('x-locale');
  if (fromHeader === 'en' || fromHeader === 'zh') return fromHeader;
  return cookies().get('lang')?.value === 'en' ? 'en' : 'zh';
}
