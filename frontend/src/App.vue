<template>
  <div v-if="isLoading" class="loading-screen">
    <div class="loader-content text-center">
      <h1 class="text-4xl font-bold text-white mb-4 tracking-widest">FactRed</h1>
      <p class="text-orange-500 animate-pulse text-lg font-medium">Iniciando sistema...</p>
    </div>
  </div>

  <div v-else class="flex h-screen transition-colors duration-500 bg-[#353c44] overflow-hidden">
    
    <div v-if="isSidebarOpen && !$route.meta.hideLayout" @click="isSidebarOpen = false" class="fixed inset-0 bg-black/80 z-40 md:hidden backdrop-blur-sm transition-opacity"></div>

    <aside v-if="!$route.meta.hideLayout" :class="[isSidebarOpen ? 'translate-x-0' : '-translate-x-full', 'fixed md:relative inset-y-0 left-0 w-64 bg-[#272d33] text-gray-200 flex flex-col shadow-2xl z-50 border-r border-[#1e2328] transition-transform duration-300 ease-in-out md:translate-x-0']">
      <div class="p-6 flex justify-between items-center border-b border-[#1e2328]">
        <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center font-bold text-lg shadow-[0_0_15px_rgba(234,88,12,0.4)]">F</div>
            <div>
                <h1 class="text-xl font-bold tracking-wider text-white">FactRed</h1>
                <p class="text-[10px] text-gray-400 font-medium uppercase tracking-widest">Enterprise ISP</p>
            </div>
        </div>
        <button @click="isSidebarOpen = false" class="md:hidden text-gray-400 hover:text-white">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
        </button>
      </div>
      
      <nav class="flex-1 px-4 py-4 space-y-2 overflow-y-auto">
        <router-link to="/" class="flex items-center p-3 rounded-xl hover:bg-[#353c44] transition-all duration-300 group" active-class="bg-gradient-to-r from-orange-600 to-red-600 shadow-lg shadow-orange-500/20 border border-orange-500/20 text-white">
          <svg class="w-5 h-5 mr-3 group-hover:text-orange-400 transition-colors text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
          <span class="font-medium group-hover:text-white transition-colors">Dashboard</span>
        </router-link>

        <router-link to="/clients" class="flex items-center p-3 rounded-xl hover:bg-[#353c44] transition-all duration-300 group" active-class="bg-gradient-to-r from-orange-600 to-red-600 shadow-lg shadow-orange-500/20 border border-orange-500/20 text-white">
          <svg class="w-5 h-5 mr-3 group-hover:text-orange-400 transition-colors text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
          <span class="font-medium group-hover:text-white transition-colors">Clientes</span>
        </router-link>

        <router-link to="/billing" class="flex items-center p-3 rounded-xl hover:bg-[#353c44] transition-all duration-300 group" active-class="bg-gradient-to-r from-orange-600 to-red-600 shadow-lg shadow-orange-500/20 border border-orange-500/20 text-white">
          <svg class="w-5 h-5 mr-3 group-hover:text-orange-400 transition-colors text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          <span class="font-medium group-hover:text-white transition-colors">Facturaci&oacute;n</span>
        </router-link>

        <router-link to="/switches" class="flex items-center p-3 rounded-xl hover:bg-[#353c44] transition-all duration-300 group" active-class="bg-gradient-to-r from-orange-600 to-red-600 shadow-lg shadow-orange-500/20 border border-orange-500/20 text-white">
          <svg class="w-5 h-5 mr-3 group-hover:text-orange-400 transition-colors text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
          </svg>
          <span class="font-medium group-hover:text-white transition-colors">Gesti&oacute;n Switches</span>
        </router-link>
      </nav>

      <div class="p-4 mx-4 mb-4 rounded-xl bg-[#1e2328] border border-[#353c44] shadow-inner">
        <div class="flex items-center gap-3">
          <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse shadow-[0_0_5px_#22c55e]"></div>
          <div class="text-sm">
            <p class="font-bold text-gray-200">Admin</p>
            <p class="text-xs text-gray-500">Conectado</p>
          </div>
        </div>
      </div>
      
      <div class="px-4 pb-4">
        <button @click="handleLogout" class="w-full flex items-center justify-center p-2 rounded-lg bg-red-500/10 text-red-500 hover:bg-red-600 hover:text-white transition-all text-sm font-bold border border-red-500/20 hover:border-red-600">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
            Cerrar Sesi&oacute;n
        </button>
      </div>
    </aside>

    <div class="flex-1 flex flex-col min-w-0 relative z-10">
      <header v-if="!$route.meta.hideLayout" class="md:hidden flex items-center justify-between p-4 bg-[#272d33] border-b border-[#1e2328] z-20">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center font-bold text-white shadow-lg">F</div>
          <span class="font-bold text-white tracking-wider">FactRed</span>
        </div>
        <button @click="isSidebarOpen = true" class="text-gray-300 hover:text-white p-1">
          <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
      </header>

      <main class="flex-1 overflow-auto p-4 md:p-6 scroll-smooth">
        <router-view></router-view>
      </main>
    </div>
    
    <vue-particles id="tsparticles" :options="particlesOptions" class="absolute inset-0 z-0 pointer-events-none" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const route = useRoute();
const isLoading = ref(true);
const isSidebarOpen = ref(false);

const API_URL = "http://172.31.45.56:8000";

watch(route, () => {
    isSidebarOpen.value = false;
});

onMounted(async () => {
  try {
    const { data } = await axios.get(`${API_URL}/setup/status`);
    if (!data.is_installed) {
      router.push('/setup');
    } else {
      if (route.path === '/setup') router.push('/login');
      if (route.path === '/') {
        const isAuthenticated = localStorage.getItem('isAuthenticated');
        router.push(isAuthenticated ? '/' : '/login');
      }
    }
  } catch (error) {
    console.error("Error:", error);
  } finally {
    setTimeout(() => { isLoading.value = false; }, 800);
  }
});

const handleLogout = () => {
    if(confirm('¿Confirmar cierre de sesión?')) {
        localStorage.removeItem('isAuthenticated');
        router.push('/login');
    }
}

const particlesOptions = {
    background: { color: { value: "transparent" } },
    fpsLimit: 60, 
    interactivity: {
        events: { onHover: { enable: true, mode: "grab" } },
        modes: { grab: { distance: 140, links: { opacity: 0.8 } } },
    },
    particles: {
        color: { value: "#ea580c" }, 
        links: { color: "#8b949e", distance: 150, enable: true, opacity: 0.15, width: 1 },
        move: { direction: "none", enable: true, outModes: "bounce", random: false, speed: 0.5, straight: false },
        number: { density: { enable: true, area: 800 }, value: 50 },
        opacity: { value: 0.4 },
        shape: { type: "circle" },
        size: { value: { min: 1, max: 2 } },
    },
    detectRetina: true,
};
</script>

<style scoped>
.loading-screen {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background-color: #353c44; display: flex; justify-content: center; align-items: center; z-index: 9999;
}
</style>