import { computed, ref, watch } from 'vue'
import { defineStore } from 'pinia'
import type { CartItem } from '../types'

/**
 * 购物车状态。
 * 只维护「菜品 id → 数量」；菜品的价格、名称展示由各页面结合菜单数据计算。
 * 变更自动持久化到 localStorage，刷新不丢。
 */

const STORAGE_KEY = 'shop-demo:cart'

function readStoredCart(): CartItem[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? (JSON.parse(raw) as CartItem[]) : []
  } catch {
    return []
  }
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>(readStoredCart())

  watch(
    items,
    (val) => {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(val))
    },
    { deep: true },
  )

  const totalCount = computed(() =>
    items.value.reduce((sum, it) => sum + it.quantity, 0),
  )

  function quantityOf(dishId: string): number {
    return items.value.find((it) => it.dishId === dishId)?.quantity ?? 0
  }

  function add(dishId: string, quantity = 1): void {
    const existing = items.value.find((it) => it.dishId === dishId)
    if (existing) existing.quantity += quantity
    else items.value.push({ dishId, quantity })
  }

  function setQuantity(dishId: string, quantity: number): void {
    const existing = items.value.find((it) => it.dishId === dishId)
    if (!existing) return
    if (quantity <= 0) {
      items.value = items.value.filter((it) => it.dishId !== dishId)
    } else {
      existing.quantity = quantity
    }
  }

  function clear(): void {
    items.value = []
  }

  return { items, totalCount, quantityOf, add, setQuantity, clear }
})
