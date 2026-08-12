<script setup lang="ts">
import { onActivated, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getOrders } from '../api/order'
import { getDishMap } from '../api/menu'
import { formatPrice, formatTime } from '../utils/format'
import type { Dish, Order } from '../types'

const router = useRouter()
const orders = ref<Order[]>([])
const dishMap = ref<Map<string, Dish>>(new Map())
const loading = ref(true)

async function load(): Promise<void> {
  loading.value = true
  try {
    const [list, map] = await Promise.all([getOrders(), getDishMap()])
    orders.value = list
    dishMap.value = map
  } finally {
    loading.value = false
  }
}

onMounted(load)
// 从下单成功页 / 结算页返回时刷新，保证看到最新订单
onActivated(load)

function dishNames(items: Order['items']): string {
  return items
    .map((it) => `${dishMap.value.get(it.dishId)?.name ?? it.dishId}×${it.quantity}`)
    .join('，')
}
</script>

<template>
  <van-nav-bar title="我的订单" left-arrow fixed placeholder @click-left="router.back()" />

  <van-loading v-if="loading" class="page-loading" vertical>
    加载中…
  </van-loading>

  <van-empty
    v-else-if="orders.length === 0"
    description="还没有订单，去点一份吧"
    class="empty-box"
  >
    <van-button round type="primary" size="small" @click="router.push('/menu')">
      去点餐
    </van-button>
  </van-empty>

  <div v-else class="order-list">
    <div v-for="order in orders" :key="order.id" class="order-card">
      <div class="order-head">
        <span class="order-id">{{ order.id }}</span>
        <van-tag :type="order.status === 'completed' ? 'success' : 'warning'">
          {{ order.status === 'completed' ? '已完成' : '待取餐' }}
        </van-tag>
      </div>

      <div class="order-items">{{ dishNames(order.items) }}</div>

      <div class="order-foot">
        <span class="order-time">{{ formatTime(order.createdAt) }}</span>
        <span class="order-price">{{ formatPrice(order.totalPrice) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-loading {
  padding: 120px 0;
}

.empty-box {
  padding-top: 140px;
}

.order-list {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-card {
  background: #fff;
  border-radius: 16px;
  padding: 14px 16px;
  box-shadow: 0 4px 16px rgba(240, 82, 42, 0.06);
}

.order-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.order-id {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-main);
}

.order-items {
  font-size: 13px;
  color: var(--text-sub);
  margin: 8px 0;
  line-height: 1.5;
}

.order-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--divider);
  padding-top: 10px;
}

.order-time {
  font-size: 12px;
  color: var(--text-sub);
}

.order-price {
  color: var(--brand);
  font-weight: 800;
  font-size: 15px;
}
</style>
