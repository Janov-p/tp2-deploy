<template>
  <div class="default-layout">
    <AppHeader />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <component :is="Component" />
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import AppHeader from '@/components/AppHeader.vue';

onMounted(() => {
  console.log('=== DefaultLayout Mounted ===');
  console.log('Layout component is mounted');
});
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.main-content {
  padding-top: 80px; /* Height of the header + some spacing */
  max-width: 1200px;
  margin: 0 auto;
  padding-left: 1rem;
  padding-right: 1rem;
}
</style> 