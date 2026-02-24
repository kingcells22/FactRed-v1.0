<template>
  <div class="space-y-6 animate-fade-in-up">
    <div class="bg-[#272d33] rounded-3xl p-6 md:p-8 text-white shadow-xl border border-[#4a545e] relative overflow-hidden">
        <div class="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-orange-600 rounded-full blur-3xl opacity-20 animate-pulse"></div>
        <div class="relative z-10">
            <h2 class="text-2xl md:text-3xl font-bold mb-2 tracking-tight text-white">Panel de Control</h2>
            <p class="text-gray-400 text-sm md:text-base">Resumen de infraestructura y facturacion.</p>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-[#272d33] p-6 rounded-2xl shadow-lg border border-[#3e464f] hover:border-orange-500/50 transition-all duration-300 group cursor-default">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-400 font-bold uppercase tracking-wider group-hover:text-orange-500 transition-colors">Clientes Activos</p>
            <h3 class="text-4xl font-extrabold text-white mt-2 group-hover:scale-105 transition-transform origin-left">{{ activeClients }}</h3>
          </div>
          <div class="p-4 bg-[#1e2328] rounded-2xl text-orange-500 border border-[#353c44] group-hover:bg-orange-600 group-hover:text-white transition-all duration-300 transform group-hover:rotate-12 shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-[#272d33] p-6 rounded-2xl shadow-lg border border-[#3e464f] hover:border-red-500/50 transition-all duration-300 group cursor-default">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-400 font-bold uppercase tracking-wider group-hover:text-red-500 transition-colors">Por Cobrar</p>
            <h3 class="text-4xl font-extrabold text-white mt-2 group-hover:scale-105 transition-transform origin-left">$0.00</h3>
          </div>
          <div class="p-4 bg-[#1e2328] rounded-2xl text-red-500 border border-[#353c44] group-hover:bg-red-600 group-hover:text-white transition-all duration-300 transform group-hover:-rotate-12 shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
        <div class="mt-4 flex items-center text-sm">
          <span class="text-white font-bold flex items-center mr-2 bg-red-500 px-2 py-1 rounded-lg shadow-sm">0 facturas</span>
          <span class="text-gray-400 font-medium">vencidas</span>
        </div>
      </div>

      <div class="bg-[#272d33] p-6 rounded-2xl shadow-lg border border-[#3e464f] hover:border-green-500/50 transition-all duration-300 group cursor-default">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-xs text-gray-400 font-bold uppercase tracking-wider group-hover:text-green-500 transition-colors">Nodos Online</p>
            <h3 class="text-lg font-extrabold mt-2 group-hover:scale-105 transition-transform origin-left text-green-500">
                {{ networkStatus?.cores?.length || 0 }} Equipos
            </h3>
          </div>
          <div class="p-4 bg-[#1e2328] rounded-2xl text-green-500 border border-[#353c44] group-hover:bg-green-600 group-hover:text-white transition-all duration-300 transform group-hover:rotate-180 shadow-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        
        <div v-if="!networkStatus?.cores || networkStatus.cores.length === 0" class="col-span-full bg-[#272d33] rounded-2xl p-8 text-center border border-[#3e464f]">
            <p class="text-gray-300 font-bold text-lg">Sin equipos registrados.</p>
            <p class="text-gray-500 text-sm mt-2">Ve a "Gestion Switches" para comenzar.</p>
        </div>

        <div v-for="core in networkStatus?.cores" :key="core.wan_ip" class="bg-[#272d33] rounded-2xl shadow-xl border border-[#3e464f] hover:border-orange-500/50 transition-all duration-300 p-5 md:p-6 text-white flex flex-col justify-between group">
            <div>
                <h3 class="text-xl font-bold mb-4 flex items-center">
                    <span :class="core.status === 'Online' ? 'bg-green-500 shadow-[0_0_10px_#22c55e]' : 'bg-red-500 shadow-[0_0_10px_#ef4444]'" class="w-3 h-3 rounded-full mr-3 inline-block"></span> 
                    {{ core.name }} <span class="text-sm font-normal text-gray-400 ml-2">({{ core.vendor }})</span>
                </h3>
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 md:gap-4">
                    <div class="bg-[#1e2328] p-3 md:p-4 rounded-xl border border-[#353c44] group-hover:border-[#4a545e] transition-colors">
                        <p class="text-xs text-gray-500 uppercase font-bold tracking-wider flex items-center gap-2">
                            <svg class="w-3 h-3 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"/></svg>
                            WAN IP
                        </p>
                        <p class="text-sm md:text-md font-mono text-orange-400 mt-1 font-medium">{{ core.wan_ip }}</p>
                    </div>
                    <div class="bg-[#1e2328] p-3 md:p-4 rounded-xl border border-[#353c44] group-hover:border-[#4a545e] transition-colors">
                        <p class="text-xs text-gray-500 uppercase font-bold tracking-wider flex items-center gap-2">
                            <svg class="w-3 h-3 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z"/></svg>
                            {{ core.vendor === 'Fortinet' ? 'Uptime' : 'Load' }}
                        </p>
                        <p :class="core.vendor === 'Fortinet' ? 'text-yellow-500 text-sm mt-1 truncate' : 'text-green-500 text-sm md:text-md mt-1 font-bold'">
                            {{ core.vendor === 'Fortinet' ? core.uptime : core.cpu_load }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="mt-5 pt-4 border-t border-[#353c44]">
                <p class="text-xs text-gray-400 uppercase font-bold mb-3 flex items-center gap-2 tracking-wider">
                    <svg class="w-4 h-4 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                    Interfaces LAN
                </p>
                <div class="flex flex-wrap gap-2">
                    <span v-if="!core.interfaces || core.interfaces.length === 0" class="text-xs text-gray-500 italic">Sin interfaces LAN.</span>
                    <span v-for="iface in core.interfaces" :key="iface.name" class="bg-[#1e2328] text-gray-300 text-xs px-3 py-1.5 rounded-lg border border-[#353c44] font-mono flex items-center shadow-inner">
                        {{ iface.name }} <span class="text-gray-600 mx-1">|</span> <span class="text-orange-400 font-bold">{{ iface.ip }}</span>
                    </span>
                </div>
            </div>
        </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from "vue";
import { useClientStore } from "../stores/clients";
import axios from 'axios';

const clientStore = useClientStore();
const networkStatus = ref<any>(null);
const API_URL = "http://172.31.45.56:8000";

onMounted(async () => {
  try { await clientStore.fetchClients(); } catch(e) {}
  
  try {
    const res = await axios.get(`${API_URL}/util/network/status`);
    networkStatus.value = res.data;
  } catch (e) {
    console.error("Error fetching network status", e);
    networkStatus.value = { cores: [] };
  }
});

const activeClients = computed(() => {
  if (!clientStore.clients) return 0;
  return clientStore.clients.filter((c: any) => c.service_status === 'Active').length; 
});
</script>