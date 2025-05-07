<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="handleSubmit" class="register-form">
      <div class="form-group">
        <label for="name">Name</label>
        <input
          type="text"
          id="name"
          v-model="name"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          required
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          required
          class="form-control"
        />
      </div>
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      <button type="submit" :disabled="loading" class="submit-button">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>
    </form>
    <p class="login-link">
      Already have an account?
      <router-link to="/login">Login here</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const name = ref('');
const email = ref('');
const password = ref('');
const loading = ref(false);
const error = ref('');

async function handleSubmit() {
  try {
    loading.value = true;
    await authStore.register(name.value, email.value, password.value);
    router.push('/login');
  } catch (e: any) {
    error.value = e.response?.data?.message || 'Failed to register';
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-control {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.submit-button {
  padding: 0.75rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.submit-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  margin: 0.5rem 0;
}

.login-link {
  margin-top: 1rem;
  text-align: center;
}

.login-link a {
  color: #4CAF50;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style> 