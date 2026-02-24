import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Dashboard from '../views/Dashboard.vue';
import Clients from '../views/Clients.vue';
import Billing from '../views/Billing.vue';
import Setup from '../views/Setup.vue'; 
import Switches from '../views/Switches.vue'; // <--- 1. IMPORTAMOS LA NUEVA VISTA DE SWITCHES

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
      path: '/setup',
      name: 'setup',
      component: Setup,
      meta: { title: 'Instalación', public: true, hideLayout: true }
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
    },
    // --- 2. AGREGAMOS LA RUTA SWITCHES ---
    {
      path: '/switches',
      name: 'switches',
      component: Switches,
      meta: { title: 'Gestión Switches' } // No lleva "public: true" para que esté protegida
    }
  ],
});

// Tu guardia de seguridad (Intacto)
router.beforeEach((to, _from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';
  
  // Si la ruta NO es pública y NO estás autenticado -> Login
  if (!to.meta.public && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;