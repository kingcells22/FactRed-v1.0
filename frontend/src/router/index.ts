import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import Clients from '../views/Clients.vue';
import Billing from '../views/Billing.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { title: 'Iniciar Sesión', public: true, hideLayout: true }
    },
    {
      path: '/',
      name: 'dashboard',
      component: Dashboard,
      meta: { title: 'Dashboard' }
    },
    {
      path: '/clients',
      name: 'clients',
      component: Clients,
      meta: { title: 'Clientes' }
    },
    {
      path: '/billing',
      name: 'billing',
      component: Billing,
      meta: { title: 'Facturación' }
    }
  ],
});

// eslint-disable-next-line @typescript-eslint/no-unused-vars
router.beforeEach((to, _from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  if (!to.meta.public && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
