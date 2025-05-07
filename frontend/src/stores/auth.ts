import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { User, LoginResponse } from '@/services/api';
import { authService } from '@/services/api';

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  async function login(email: string, password: string) {
    try {
      loading.value = true;
      error.value = null;
      console.log('Auth store: Attempting login...');
      
      const response = await authService.login({ email, password });
      console.log('Auth store: Login response:', response);
      
      if (response.user) {
        user.value = response.user;
        console.log('Auth store: User set:', user.value);
      } else {
        throw new Error('No user data in response');
      }
      
      return response;
    } catch (e: any) {
      console.error('Auth store: Login error:', e);
      error.value = e.response?.data?.message || 'An error occurred during login';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function register(name: string, email: string, password: string) {
    try {
      loading.value = true;
      error.value = null;
      const response = await authService.register({ name, email, password });
      return response;
    } catch (e: any) {
      error.value = e.response?.data?.message || 'An error occurred during registration';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  async function fetchUser() {
    try {
      loading.value = true;
      error.value = null;
      console.log('Auth store: Fetching user data...');
      const response = await authService.getCurrentUser();
      console.log('Auth store: User data received:', response);
      user.value = response;
      return response;
    } catch (e: any) {
      console.error('Auth store: Error fetching user:', e);
      error.value = e.response?.data?.message || 'Failed to fetch user data';
      throw e;
    } finally {
      loading.value = false;
    }
  }

  function logout() {
    console.log('Auth store: Logging out...');
    authService.logout();
    user.value = null;
  }

  function isAuthenticated() {
    const hasToken = !!localStorage.getItem('token');
    console.log('Auth store: Checking authentication:', hasToken);
    return hasToken;
  }

  return {
    user,
    loading,
    error,
    login,
    register,
    fetchUser,
    logout,
    isAuthenticated
  };
}); 