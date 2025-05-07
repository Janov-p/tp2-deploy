import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: DefaultLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'home',
          component: () => import('../views/HomeView.vue')
        },
        {
          path: 'profile',
          name: 'profile',
          component: () => import('../views/ProfileView.vue')
        }
      ]
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresAuth: false }
    }
  ]
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  console.log('=== Router Navigation ===');
  console.log('1. Navigating to:', to.path);
  console.log('2. From:', from.path);
  console.log('3. Route meta:', to.meta);
  
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  console.log('4. Auth check:', {
    requiresAuth,
    isAuthenticated: authStore.isAuthenticated(),
    hasToken: !!localStorage.getItem('token')
  });

  if (requiresAuth && !authStore.isAuthenticated()) {
    console.log('5. Auth required but not authenticated, redirecting to login');
    next('/login')
  } else if (!requiresAuth && authStore.isAuthenticated()) {
    console.log('5. Already authenticated, redirecting to home');
    next('/')
  } else {
    console.log('5. Proceeding with navigation');
    next()
  }
})

export default router
