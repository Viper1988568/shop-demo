import type { CartItem, Order, OrderStatus } from '../types'

/**
 * 订单数据服务 —— 请求 FastAPI 后端（/api 走 vite proxy → :8000）。
 * 订单持久化在服务端 SQLite；签名与第一阶段 mock 实现保持一致。
 */

const BASE = '/api/orders'

async function request<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init)
  if (!res.ok) throw new Error(`请求失败 ${res.status}`)
  return res.json() as Promise<T>
}

export interface SubmitOrderInput {
  items: CartItem[]
  remark: string
}

export function submitOrder(input: SubmitOrderInput): Promise<Order> {
  return request<Order>(BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(input),
  })
}

export function getOrders(status?: OrderStatus): Promise<Order[]> {
  const query = status ? `?status=${status}` : ''
  return request<Order[]>(`${BASE}${query}`)
}

export async function getOrderById(id: string): Promise<Order | null> {
  const res = await fetch(`${BASE}/${id}`)
  if (res.status === 404) return null
  if (!res.ok) throw new Error(`请求失败 ${res.status}`)
  return res.json() as Promise<Order>
}

export function markOrderCompleted(id: string): Promise<void> {
  return request<void>(`${BASE}/${id}/complete`, { method: 'PATCH' })
}
