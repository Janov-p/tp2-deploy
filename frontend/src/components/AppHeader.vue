<template>
  <header class="app-header">
    <div class="header-content">
      <router-link to="/profile" class="profile-link">
        <div class="profile-icon">
          <span v-if="user">{{ user.name.charAt(0).toUpperCase() }}</span>
          <span v-else>?</span>
        </div>
      </router-link>
      <button @click="handleLogout" class="logout-button">Logout</button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const { user, logout } = authStore;

function handleLogout() {
  logout();
  router.push('/login');
}
</script>

<style scoped>
.app-header {
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-link {
  text-decoration: none;
  color: inherit;
}

.profile-icon {
  width: 40px;
  height: 40px;
  background-color: #4CAF50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.profile-icon:hover {
  background-color: #45a049;
}

.logout-button {
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.logout-button:hover {
  background-color: #c82333;
}
</style> 