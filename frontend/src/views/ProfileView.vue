<template>
  <div class="profile-container">
    <h2>Profile</h2>
    <div v-if="authStore.loading" class="loading">Loading...</div>
    <div v-else-if="authStore.error" class="error-message">{{ authStore.error }}</div>
    <div v-else-if="authStore.user" class="profile-info">
      <div class="info-group">
        <label>Name:</label>
        <span>{{ authStore.user.name }}</span>
      </div>
      <div class="info-group">
        <label>Email:</label>
        <span>{{ authStore.user.email }}</span>
      </div>
      <div class="info-group">
        <label>Member since:</label>
        <span>{{ new Date(authStore.user.created_at).toLocaleDateString() }}</span>
      </div>
      <button @click="handleLogout" class="logout-button">Logout</button>
    </div>
    <div v-else class="error-message">No user data available</div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

onMounted(async () => {
  console.log('=== Profile Page Load ===');
  console.log('1. Component mounted');
  console.log('2. Checking authentication state:', {
    isAuthenticated: authStore.isAuthenticated(),
    hasToken: !!localStorage.getItem('token'),
    token: localStorage.getItem('token'),
    currentUser: authStore.user
  });

  if (!authStore.isAuthenticated()) {
    console.log('3. Not authenticated, redirecting to login');
    router.push('/login');
    return;
  }

  console.log('3. User is authenticated, proceeding with data fetch');
  try {
    console.log('4. Initiating API request to /auth/me...');
    await authStore.fetchUser();
    console.log('5. API request completed successfully');
    console.log('6. User data received:', authStore.user);
  } catch (e) {
    console.error('5. API request failed:', e);
    console.log('6. Redirecting to login due to error');
    router.push('/login');
  }
});

async function handleLogout() {
  console.log('Logout initiated');
  authStore.logout();
  router.push('/login');
}
</script>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: white;
}

.profile-info {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-group {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.info-group label {
  font-weight: bold;
  min-width: 100px;
}

.loading {
  text-align: center;
  color: #666;
}

.error-message {
  color: #dc3545;
  text-align: center;
  padding: 1rem;
}

.logout-button {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  align-self: flex-start;
}

.logout-button:hover {
  background-color: #c82333;
}
</style> 