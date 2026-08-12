<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getDishes } from '../api/menu'
import { formatPrice } from '../utils/format'
import type { Dish } from '../types'

const router = useRouter()
const dishes = ref<Dish[]>([])

const hotDishes = computed(() =>
  [...dishes.value].sort((a, b) => b.monthlySales - a.monthlySales).slice(0, 4),
)

onMounted(async () => {
  dishes.value = await getDishes()
})

const features = [
  { icon: '🧑‍🍳', title: '现点现做', desc: '厨房即出，滚烫上桌' },
  { icon: '🌶️', title: '六种辣度', desc: '从不辣到特辣任选' },
  { icon: '🥬', title: '新鲜食材', desc: '当日采购，拒绝预制' },
]
</script>

<template>
  <!-- 品牌横幅 -->
  <div class="hero">
    <div class="hero-top">
      <div class="hero-logo">
        <span class="hero-logo-icon">🍜</span>
        <span class="hero-logo-name">川香小馆</span>
      </div>
      <van-icon
        name="orders-o"
        size="20"
        class="hero-icon"
        @click="router.push('/orders')"
      />
    </div>

    <div class="hero-body">
      <div class="hero-slogan">无辣不欢<br />好菜即刻上桌</div>
      <div class="hero-sub">现点现做 · 下单立出 · 热辣滚烫</div>

      <van-button class="hero-btn" round block @click="router.push('/menu')">
        开始点餐 <van-icon name="arrow" />
      </van-button>
    </div>

    <span class="hero-deco">🌶️</span>
    <span class="hero-deco-2">🥢</span>
  </div>

  <!-- 三大亮点 -->
  <div class="features">
    <div v-for="f in features" :key="f.title" class="feature card">
      <div class="feature-icon">{{ f.icon }}</div>
      <div class="feature-title">{{ f.title }}</div>
      <div class="feature-desc">{{ f.desc }}</div>
    </div>
  </div>

  <!-- 招牌推荐 -->
  <div class="hot-section">
    <div class="hot-head">
      <span class="hot-title">🔥 人气招牌</span>
      <span class="hot-more" @click="router.push('/menu')">去点餐 ›</span>
    </div>

    <div class="hot-list">
      <div
        v-for="dish in hotDishes"
        :key="dish.id"
        class="hot-card card"
        @click="router.push('/menu')"
      >
        <div class="dish-thumb hot-thumb">
          <span class="dish-thumb-emoji">{{ dish.image }}</span>
        </div>
        <div class="hot-name">{{ dish.name }}</div>
        <div class="hot-meta">月售 {{ dish.monthlySales }}</div>
        <div class="hot-price">{{ formatPrice(dish.price) }}</div>
      </div>
    </div>
  </div>

  <div class="footer-tip">川香小馆 · 用心做好每一道川菜</div>
</template>

<style scoped>
/* ===== 品牌横幅 ===== */
.hero {
  position: relative;
  margin: 12px;
  padding: 22px 20px 24px;
  border-radius: 24px;
  background: linear-gradient(135deg, #ff7a4d 0%, #f0522a 55%, #e84a20 100%);
  color: #fff;
  overflow: hidden;
  box-shadow: 0 10px 28px rgba(240, 82, 42, 0.32);
}

.hero-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hero-logo {
  display: flex;
  align-items: center;
  gap: 8px;
}

.hero-logo-icon {
  font-size: 24px;
}

.hero-logo-name {
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 1px;
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

.hero-body {
  position: relative;
  z-index: 1;
  margin-top: 26px;
}

.hero-slogan {
  font-size: 30px;
  font-weight: 800;
  line-height: 1.35;
  letter-spacing: 1px;
}

.hero-sub {
  margin-top: 10px;
  font-size: 13px;
  opacity: 0.92;
  letter-spacing: 0.5px;
}

.hero-btn {
  margin-top: 22px;
  width: 160px;
  height: 44px;
  color: var(--brand-deep);
  background: #fff;
  border: none;
  font-weight: 700;
  border-radius: 999px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.16);
  transition: transform 0.12s ease;
}

.hero-btn:active {
  transform: scale(0.96);
}

.hero-deco {
  position: absolute;
  right: -10px;
  top: 54px;
  font-size: 90px;
  opacity: 0.16;
  transform: rotate(15deg);
}

.hero-deco-2 {
  position: absolute;
  right: 56px;
  bottom: -18px;
  font-size: 60px;
  opacity: 0.14;
  transform: rotate(-12deg);
}

/* ===== 三大亮点 ===== */
.features {
  margin: 4px 12px 0;
  display: flex;
  gap: 10px;
}

.feature {
  flex: 1;
  padding: 14px 10px;
  text-align: center;
}

.feature-icon {
  font-size: 26px;
}

.feature-title {
  margin-top: 8px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-main);
}

.feature-desc {
  margin-top: 4px;
  font-size: 11px;
  color: var(--text-sub);
}

/* ===== 招牌推荐 ===== */
.hot-section {
  margin: 20px 12px 0;
}

.hot-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.hot-title {
  font-size: 17px;
  font-weight: 800;
  color: var(--text-main);
}

.hot-more {
  font-size: 13px;
  color: var(--brand);
  font-weight: 600;
}

.hot-list {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  scrollbar-width: none;
  padding-bottom: 4px;
}

.hot-list::-webkit-scrollbar {
  display: none;
}

.hot-card {
  flex: 0 0 128px;
  padding: 10px;
}

.hot-thumb {
  width: 100%;
  height: 100px;
  border-radius: 12px;
}

.hot-name {
  margin-top: 8px;
  font-size: 13px;
  font-weight: 700;
  color: var(--text-main);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.hot-meta {
  margin-top: 3px;
  font-size: 11px;
  color: var(--text-sub);
}

.hot-price {
  margin-top: 4px;
  color: var(--brand);
  font-weight: 800;
  font-size: 15px;
}

.footer-tip {
  margin: 26px 0 20px;
  text-align: center;
  font-size: 12px;
  color: #c4bdb7;
}
</style>
