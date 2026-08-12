/** 金额展示：12.5 -> ¥12.50 */
export function formatPrice(price: number): string {
  return `¥${price.toFixed(2)}`
}

/** ISO 时间展示：2026-08-12 12:08 */
export function formatTime(iso: string): string {
  const d = new Date(iso)
  const pad = (n: number) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`
}
