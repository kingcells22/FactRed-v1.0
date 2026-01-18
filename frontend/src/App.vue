<template>
  <div class="flex h-screen transition-colors duration-500">
    <!-- Sidebar (Hidden on Login) -->
    <aside v-if="!$route.meta.hideLayout" class="w-64 bg-slate-900 text-white flex flex-col shadow-2xl z-50">
      <div class="p-6">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-bold text-lg shadow-lg shadow-blue-500/50">F</div>
            <div>
                <h1 class="text-xl font-bold tracking-wider text-white">FactRed</h1>
                <p class="text-[10px] text-slate-400 font-medium uppercase tracking-widest">ISP System</p>
            </div>
        </div>
      </div>
      
      <nav class="flex-1 px-4 py-4 space-y-2">
        <router-link to="/" class="flex items-center p-3 rounded-xl hover:bg-slate-800 transition-all duration-300 group" active-class="bg-gradient-to-r from-blue-600 to-indigo-600 shadow-lg shadow-blue-500/30">
          <span class="mr-3 text-2xl group-hover:scale-110 transition-transform">📊</span> 
          <span class="font-medium">Dashboard</span>
        </router-link>
        <router-link to="/clients" class="flex items-center p-3 rounded-xl hover:bg-slate-800 transition-all duration-300 group" active-class="bg-gradient-to-r from-blue-600 to-indigo-600 shadow-lg shadow-blue-500/30">
          <span class="mr-3 text-2xl group-hover:scale-110 transition-transform">👥</span> 
          <span class="font-medium">Clientes</span>
        </router-link>
        <router-link to="/billing" class="flex items-center p-3 rounded-xl hover:bg-slate-800 transition-all duration-300 group" active-class="bg-gradient-to-r from-blue-600 to-indigo-600 shadow-lg shadow-blue-500/30">
          <span class="mr-3 text-2xl group-hover:scale-110 transition-transform">💰</span> 
          <span class="font-medium">Facturación</span>
        </router-link>
      </nav>

      <div class="p-4 mx-4 mb-4 rounded-xl bg-slate-800/50 border border-slate-700/50 backdrop-blur-sm">
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <div class="text-sm">
            <p class="font-bold text-slate-200">Admin</p>
            <p class="text-xs text-slate-500">Sesión Segura</p>
          </div>
        </div>
      </div>
      
      <!-- Logout Button -->
       <div class="px-4 pb-4">
        <button @click="handleLogout" class="w-full flex items-center justify-center p-2 rounded-lg bg-red-600/20 text-red-400 hover:bg-red-600 hover:text-white transition-all text-sm font-bold">
            <span class="mr-2">🚪</span> Cerrar Sesión
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto relative z-10">
      <header v-if="!$route.meta.hideLayout" class="bg-white/80 backdrop-blur-md shadow-sm p-4 flex justify-between items-center sticky top-0 z-20">
        <h2 class="text-xl font-semibold text-gray-800">
          {{ $route.meta.title || "FactRed" }}
        </h2>
        <div class="flex gap-4">
          <router-link
            to="/billing"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition flex items-center shadow-lg shadow-blue-500/30"
          >
            Nueva Factura
          </router-link>
        </div>
      </header>
      <div :class="!$route.meta.hideLayout ? 'p-6' : ''">
        <router-view></router-view>
      </div>
    </main>
    
    <!-- Particles Background -->
    <vue-particles
        id="tsparticles"
        :options="particlesOptions"
        class="absolute inset-0 z-0 pointer-events-none"
    />
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

const handleLogout = () => {
    if(confirm('¿Cerrar sesión?')) {
        localStorage.removeItem('isAuthenticated');
        router.push('/login');
    }
}

const particlesOptions = {
    background: {
        color: {
            value: "transparent",
        },
    },
    fpsLimit: 120,
    interactivity: {
        events: {
            onHover: {
                enable: true,
                mode: "grab",
            },
        },
        modes: {
            grab: {
                distance: 140,
                links: {
                    opacity: 0.5,
                },
            },
        },
    },
    particles: {
        color: {
            value: "#ffffff",
        },
        links: {
            color: "#ffffff",
            distance: 150,
            enable: true,
            opacity: 0.2,
            width: 1,
        },
        move: {
            direction: "none",
            enable: true,
            outModes: "bounce",
            random: false,
            speed: 1,
            straight: false,
        },
        number: {
            density: {
                enable: true,
                area: 800,
            },
            value: 60,
        },
        opacity: {
            value: 0.3,
        },
        shape: {
            type: "circle",
        },
        size: {
            value: { min: 1, max: 3 },
        },
    },
    detectRetina: true,
};
</script>
