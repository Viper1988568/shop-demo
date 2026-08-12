<template>
  <div class="app-shell">
    <router-view v-slot="{ Component }">
      <keep-alive include="MenuView">
        <component :is="Component" />
      </keep-alive>
    </router-view>
  </div>
</template>
