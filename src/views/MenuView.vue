<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showToast } from 'vant'
import { getCategories, getDishes } from '../api/menu'
import { useCartStore } from '../stores/cart'
import { formatPrice } from '../utils/format'
import type { Category, Dish } from '../types'

const router = useRouter()
const cart = useCartStore()

const categories = ref<Category[]>([])
const dishes = ref<Dish[]>([])
const activeCategoryId = ref('')
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const [cates, all] = await Promise.all([getCategories(), getDishes()])
    categories.value = cates
    dishes.value = all
    activeCategoryId.value = cates[0]?.id ?? ''
  } finally {
    loading.value = false
  }
})

const activeDishes = computed(() =>
  dishes.value.filter((d) => d.categoryId === activeCategoryId.value),
)

const totalPrice = computed(() =>
  cart.items.reduce((sum, it) => {
    const dish = dishes.value.find((d) => d.id === it.dishId)
    return sum + (dish ? dish.price * it.quantity : 0)
  }, 0),
)

function increase(dishId: string): void {
  cart.add(dishId, 1)
}

function decrease(dishId: string): void {
  const current = cart.quantityOf(dishId)
  cart.setQuantity(dishId, current - 1)
}

function goCheckout(): void {
  if (cart.totalCount === 0) {
    showToast('还没有点任何菜')
    return
  }
  router.push('/checkout')
}
</script>

<template>
  <!-- 品牌横幅 -->
  <div class="hero">
    <div class="hero-left">
      <div class="hero-title">川香小馆</div>
      <div class="hero-sub">无辣不欢 · 好菜上新 · 下单立做</div>
    </div>
    <div class="hero-right">
      <van-icon
        name="orders-o"
        size="21"
        class="hero-icon"
        @click="router.push('/orders')"
      />
    </div>
    <span class="hero-deco">🥢</span>
  </div>

  <!-- 胶囊分类 -->
  <van-tabs
    v-model:active="activeCategoryId"
    sticky
    shrink
    class="category-tabs"
    :line-width="0"
  >
    <van-tab
      v-for="cate in categories"
      :key="cate.id"
      :title="cate.name"
      :name="cate.id"
    />
  </van-tabs>

  <van-loading v-if="loading" class="page-loading" vertical>
    菜单加载中…
  </van-loading>

  <!-- 菜品白卡片 -->
  <div v-else class="dish-card">
    <div
      v-for="dish in activeDishes"
      :key="dish.id"
      class="dish-row"
      :class="{ 'dish-row--soldout': dish.soldOut }"
    >
      <div class="dish-thumb">
        <span class="dish-thumb-emoji">{{ dish.image }}</span>
        <div v-if="dish.soldOut" class="dish-thumb-mask">已售罄</div>
      </div>

      <div class="dish-info">
        <div class="dish-name">
          {{ dish.name }}
          <van-tag
            v-if="dish.spicyLevel !== '不辣'"
            plain
            type="danger"
            class="spicy-tag"
          >
            {{ dish.spicyLevel }}
          </van-tag>
        </div>
        <div class="dish-desc">{{ dish.description }}</div>
        <div class="dish-meta">
          <span class="sales-dot">●</span>
          月售 {{ dish.monthlySales }}
        </div>
        <div class="dish-bottom">
          <span class="dish-price">{{ formatPrice(dish.price) }}</span>

          <div v-if="dish.soldOut" class="sold-out-btn">已售罄</div>

          <div v-else-if="cart.quantityOf(dish.id) === 0" class="add-btn" @click="increase(dish.id)">
            +
          </div>

          <van-stepper
            v-else
            :model-value="cart.quantityOf(dish.id)"
            min="1"
            integer
            @update:model-value="(v: number | string | undefined) => cart.setQuantity(dish.id, Number(v ?? 0))"
            @minus="decrease(dish.id)"
          />
        </div>
      </div>
    </div>
  </div>

  <!-- 底部结算栏 -->
  <van-submit-bar
    :price="Math.round(totalPrice * 100)"
    :button-text="`去结算 · ${cart.totalCount} 件`"
    button-type="primary"
    class="checkout-bar"
    @submit="goCheckout"
  >
    <template #default>
      <span class="cart-hint">合计</span>
    </template>
  </van-submit-bar>
</template>

<style scoped>
/* ===== 品牌横幅 ===== */
.hero {
  position: relative;
  margin: 12px 12px 0;
  padding: 26px 20px;
  border-radius: 20px;
  background: linear-gradient(120deg, #ff7a4d, #f0522a);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(240, 82, 42, 0.28);
}

.hero-title {
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 1px;
}

.hero-sub {
  margin-top: 6px;
  font-size: 12px;
  opacity: 0.92;
  letter-spacing: 0.5px;
}

.hero-right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.hero-icon {
  background: rgba(255, 255, 255, 0.22);
  border-radius: 50%;
  padding: 9px;
  cursor: pointer;
  transition: transform 0.12s ease;
}

.hero-icon:active {
  transform: scale(0.9);
}

.hero-deco {
  position: absolute;
  right: -6px;
  bottom: -14px;
  font-size: 72px;
  opacity: 0.16;
  transform: rotate(-12deg);
}

/* ===== 胶囊分类 ===== */
.category-tabs {
  background: var(--bg);
  padding: 12px 12px 2px;
}

.category-tabs :deep(.van-tabs__wrap) {
  height: auto;
}

.category-tabs :deep(.van-tab) {
  padding: 7px 16px;
  margin-right: 8px;
  border-radius: 999px;
  color: var(--text-sub);
  background: #fff;
  font-size: 13px;
  transition: all 0.15s ease;
}

.category-tabs :deep(.van-tab--active) {
  color: #fff;
  background: linear-gradient(120deg, var(--brand), var(--brand-deep));
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(240, 82, 42, 0.28);
}

.page-loading {
  padding: 120px 0;
}

/* ===== 菜品白卡片 ===== */
.dish-card {
  margin: 8px 12px 110px;
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 16px rgba(240, 82, 42, 0.05);
  overflow: hidden;
}

.dish-row {
  display: flex;
  gap: 12px;
  padding: 14px 14px;
}

.dish-row + .dish-row {
  border-top: 1px solid var(--divider);
}

.dish-row--soldout {
  opacity: 0.75;
}

.dish-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.spicy-tag {
  margin-left: 6px;
  vertical-align: 2px;
  background: #fff1ec;
  border-color: #ffd5c2;
  color: var(--brand);
}

.dish-meta {
  font-size: 12px;
  color: var(--text-sub);
  margin-top: 4px;
}

.sales-dot {
  color: #ffb88c;
  font-size: 10px;
  vertical-align: 1px;
  margin-right: 2px;
}

.dish-bottom {
  margin-top: auto;
  padding-top: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sold-out-btn {
  font-size: 12px;
  color: #c8c9cc;
  border: 1px solid var(--divider);
  border-radius: 999px;
  padding: 3px 12px;
}

.cart-hint {
  font-size: 13px;
  color: var(--text-sub);
}</style>
