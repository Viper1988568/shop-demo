<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getOrderById } from '../api/order'
import { formatPrice, formatTime } from '../utils/format'
import type { Order } from '../types'

const route = useRoute()
const router = useRouter()

const order = ref<Order | null>(null)
const loading = ref(true)

onMounted(async () => {
  const id = route.params.id as string
  order.value = await getOrderById(id)
  loading.value = false
})
</script>

<template>
  <van-nav-bar title="下单结果" fixed placeholder />

  <div class="success-box">
    <van-icon name="checked" color="#07c160" size="64" />
    <div class="success-title">下单成功</div>
    <div class="success-tip">商家正在为您备餐，请留意叫号</div>
  </div>

  <van-cell-group v-if="order" inset class="order-card">
    <van-cell title="订单号" :value="order.id" />
    <van-cell title="订单金额" :value="formatPrice(order.totalPrice)" />
    <van-cell title="下单时间" :value="formatTime(order.createdAt)" />
    <van-cell v-if="order.remark" title="备注" :value="order.remark" />
  </van-cell-group>

  <div class="actions">
    <van-button round block type="primary" @click="router.replace('/orders')">
      查看订单
    </van-button>
    <van-button round block type="primary" class="home-btn" @click="router.replace('/')">
      返回首页
    </van-button>
  </div>
</template>

<style scoped>
.success-box {
  padding: 44px 0 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.success-icon {
  width: 84px;
  height: 84px;
  border-radius: 50%;
  background: linear-gradient(135deg, #07c160, #06ad56);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(7, 193, 96, 0.35);
  animation: pop 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes pop {
  from {
    transform: scale(0.5);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.success-title {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-main);
}

.success-tip {
  font-size: 13px;
  color: var(--text-sub);
}

.order-card {
  margin: 12px auto;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(240, 82, 42, 0.06);
}

.actions {
  margin: 24px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 实心主按钮：渐变品牌色 + 白字 */
.actions :deep(.van-button--primary:not(.van-button--plain)) {
  background: linear-gradient(120deg, var(--brand), var(--brand-deep));
  box-shadow: 0 4px 14px rgba(240, 82, 42, 0.28);
}

/* 返回首页：橙色底 + 白字（纯橙、无阴影，与主按钮的渐变橙区分层次） */
.actions :deep(.van-button--primary.home-btn) {
  background: var(--brand);
  box-shadow: none;
}
</style>
