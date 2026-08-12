import type { Category, Dish } from '../types'

/**
 * 菜单数据服务 —— 请求 FastAPI 后端（/api 走 vite proxy → :8000）。
 * 签名与第一阶段 mock 实现保持一致，页面层无需改动。
 */

const BASE = '/api/menu'

async function request<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`请求失败 ${res.status}`)
  return res.json() as Promise<T>
}

export function getCategories(): Promise<Category[]> {
  return request<Category[]>(`${BASE}/categories`)
}

export function getDishes(): Promise<Dish[]> {
  return request<Dish[]>(`${BASE}/dishes`)
}

export function getDishesByCategory(categoryId: string): Promise<Dish[]> {
  return request<Dish[]>(`${BASE}/categories/${categoryId}/dishes`)
}

export async function getDishMap(): Promise<Map<string, Dish>> {
  const all = await getDishes()
  return new Map(all.map((d) => [d.id, d]))
}
