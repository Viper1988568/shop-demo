<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { getDishMap } from '../api/menu'
import { submitOrder } from '../api/order'
import { useCartStore } from '../stores/cart'
import { formatPrice } from '../utils/format'
import type { Dish } from '../types'

const router = useRouter()
const cart = useCartStore()

const dishMap = ref<Map<string, Dish>>(new Map())
const remark = ref('')
const submitting = ref(false)

onMounted(async () => {
  dishMap.value = await getDishMap()
})

const rows = computed(() =>
  cart.items.map((it) => ({
    ...it,
    dish: dishMap.value.get(it.dishId),
  })),
)

const totalPrice = computed(() =>
  cart.items.reduce((sum, it) => {
    const dish = dishMap.value.get(it.dishId)
    return sum + (dish ? dish.price * it.quantity : 0)
  }, 0),
)

async function placeOrder(): Promise<void> {
  if (cart.items.length === 0) return
  if (submitting.value) return

  submitting.value = true
  try {
    // 拷贝快照，避免下单成功后清空购物车影响已提交的数据
    const snapshot = cart.items.map((it) => ({ ...it }))
    const order = await submitOrder({ items: snapshot, remark: remark.value.trim() })
    cart.clear()
    router.replace(`/order/${order.id}/success`)
  } catch {
    showToast('下单失败，请重试')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <van-nav-bar title="确认订单" left-arrow fixed placeholder @click-left="router.back()" />

  <van-empty v-if="cart.items.length === 0" description="购物车是空的" class="empty-box">
    <van-button round type="primary" size="small" @click="router.push('/menu')">
      去点餐
    </van-button>
  </van-empty>

  <template v-else>
    <van-cell-group inset class="section">
      <van-cell v-for="row in rows" :key="row.dishId" :title="row.dish?.name ?? row.dishId">
        <template #icon>
          <span class="checkout-thumb">{{ row.dish?.image }}</span>
        </template>
        <template #label>
          <span class="checkout-price">{{ formatPrice(row.dish?.price ?? 0) }}</span>
        </template>
        <template #right-icon>
          <van-stepper
            :model-value="row.quantity"
            min="0"
            integer
            @update:model-value="(v: number | string | undefined) => cart.setQuantity(row.dishId, Number(v ?? 0))"
          />
        </template>
      </van-cell>
    </van-cell-group>

    <van-cell-group inset class="section">
      <van-field
        v-model="remark"
        type="textarea"
        rows="2"
        maxlength="50"
        show-word-limit
        placeholder="口味偏好、忌口等备注（选填）"
      />
    </van-cell-group>

    <van-submit-bar
      :price="Math.round(totalPrice * 100)"
      button-text="提交订单"
      :loading="submitting"
      @submit="placeOrder"
    />
  </template>
</template>

<style scoped>
.empty-box {
  padding-top: 140px;
}

.section {
  margin: 12px auto;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(240, 82, 42, 0.06);
}

.checkout-thumb {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #fff4ee, #ffe1cf);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 10px;
  flex-shrink: 0;
}

.checkout-price {
  color: var(--brand);
  font-weight: 700;
}
</style>
