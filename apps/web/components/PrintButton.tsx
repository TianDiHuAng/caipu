'use client';

export function PrintButton() {
  return (
    <button
      type="button"
      onClick={() => window.print()}
      className="no-print rounded bg-brand-600 px-3 py-1.5 text-sm text-white hover:bg-brand-700"
    >
      打印 / 存为 PDF
    </button>
  );
}
