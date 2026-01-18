<template>
  <div class="space-y-6 animate-fade-in-up">
    <!-- Welcome Section -->
    <div class="bg-gradient-to-r from-slate-900 to-slate-800 rounded-3xl p-8 text-white shadow-2xl relative overflow-hidden">
        <div class="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-blue-500 rounded-full blur-3xl opacity-20 animate-pulse"></div>
        <div class="relative z-10">
            <h2 class="text-3xl font-bold mb-2">Panel de Control ISP</h2>
            <p class="text-slate-300">Monitoreo de red y facturación en tiempo real.</p>
        </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <!-- Card: Total Clientes -->
    <div class="bg-white/90 backdrop-blur-xl p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl transition-shadow duration-300 group cursor-default">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-xs text-gray-500 font-bold uppercase tracking-wider group-hover:text-blue-600 transition-colors">Clientes Activos</p>
          <h3 class="text-4xl font-extrabold text-gray-900 mt-2 group-hover:scale-105 transition-transform origin-left">{{ activeClients }}</h3>
        </div>
        <div class="p-4 bg-blue-50 rounded-2xl text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-all duration-300 transform group-hover:rotate-12">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </div>
      </div>
      <div class="mt-4 flex items-center text-sm">
        <span class="text-green-500 font-bold flex items-center mr-2 bg-green-50 px-2 py-1 rounded-lg">
            <span class="mr-1">↑</span> 3%
        </span>
        <span class="text-gray-400">vs mes anterior</span>
      </div>
    </div>

    <!-- Card: Facturación Pendiente -->
    <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl transition-shadow duration-300 group cursor-default">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-xs text-gray-500 font-bold uppercase tracking-wider group-hover:text-yellow-600 transition-colors">Por Cobrar</p>
          <h3 class="text-4xl font-extrabold text-gray-900 mt-2 group-hover:scale-105 transition-transform origin-left">${{ billingStore.stats.pending_amount.toFixed(2) }}</h3>
        </div>
        <div class="p-4 bg-yellow-50 rounded-2xl text-yellow-600 group-hover:bg-yellow-500 group-hover:text-white transition-all duration-300 transform group-hover:-rotate-12">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>
       <div class="mt-4 flex items-center text-sm">
        <span class="text-red-500 font-bold flex items-center mr-2 bg-red-50 px-2 py-1 rounded-lg">
            {{ billingStore.stats.overdue_invoices }} facturas
        </span>
        <span class="text-gray-400">vencidas</span>
      </div>
    </div>

    <!-- Card: Estado de Red -->
    <div class="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-xl transition-shadow duration-300 group cursor-default">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-xs text-gray-500 font-bold uppercase tracking-wider group-hover:text-green-600 transition-colors">Estado de Red</p>
          <h3 class="text-lg font-extrabold mt-2 group-hover:scale-105 transition-transform origin-left"
              :class="billingStore.stats.suspended_clients > 0 ? 'text-yellow-500' : 'text-green-500'">
              {{ billingStore.stats.suspended_clients > 0 ? billingStore.stats.suspended_clients + ' Suspendidos' : 'En Línea' }}
          </h3>
        </div>
        <div class="p-4 bg-green-50 rounded-2xl text-green-600 group-hover:bg-green-500 group-hover:text-white transition-all duration-300 transform group-hover:rotate-180">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
          </svg>
        </div>
      </div>
      <div class="mt-4 flex items-center text-sm text-gray-600">
        <span class="text-gray-400">Latencia promedio: </span>
        <span class="ml-2 font-mono font-bold text-slate-700 bg-slate-100 px-2 py-1 rounded">12ms</span>
      </div>
    </div>

    <!-- System/Mikrotik Status -->
    <div class="col-span-1 md:col-span-3 bg-slate-900 rounded-2xl shadow-xl border border-slate-800 p-6 text-white overflow-hidden relative group">
        <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-32 w-32" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
        </div>
        <div class="relative z-10">
            <h3 class="text-xl font-bold mb-4 flex items-center">
                <span class="mr-2 text-green-400">●</span> Integridad de Red (Mikrotik CHR)
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <p class="text-xs text-slate-400 uppercase font-bold">WAN IP (Starlink)</p>
                    <p class="text-lg font-mono text-blue-300">{{ networkStatus?.system?.wan_ip || '---' }}</p>
                </div>
                <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <p class="text-xs text-slate-400 uppercase font-bold">CPU Load</p>
                    <div class="flex items-center mt-1">
                        <div class="w-full bg-slate-700 rounded-full h-2 mr-2">
                            <div class="bg-green-500 h-2 rounded-full" :style="{ width: (networkStatus?.system?.cpu_load || 0) + '%' }"></div>
                        </div>
                        <span class="text-sm font-bold">{{ networkStatus?.system?.cpu_load || 0 }}%</span>
                    </div>
                </div>
                 <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <p class="text-xs text-slate-400 uppercase font-bold">Uptime</p>
                    <p class="text-lg font-mono text-yellow-300">{{ networkStatus?.system?.uptime || '---' }}</p>
                </div>
                 <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700">
                    <p class="text-xs text-slate-400 uppercase font-bold">Interfaces</p>
                    <div class="text-xs space-y-1 mt-1 font-mono">
                        <div v-for="iface in networkStatus?.interfaces" :key="iface.name" class="flex justify-between">
                            <span class="text-slate-500">{{ iface.name }}</span>
                            <span class="text-green-400">TX: {{ iface.tx }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed, ref } from "vue";
import { useClientStore } from "../stores/clients";
import { useBillingStore } from "../stores/billing";
import api from "../api";

const clientStore = useClientStore();
const billingStore = useBillingStore();
const networkStatus = ref<any>(null);

onMounted(async () => {
  clientStore.fetchClients();
  billingStore.fetchStats();
  try {
    const res = await api.get('/util/network/status');
    networkStatus.value = res.data;
  } catch (e) {
    console.error("Error fetching network status", e);
  }
});

const activeClients = computed(() => {
  // Count active
  return clientStore.clients.filter(c => c.service_status === 'Active').length; 
});
</script>
