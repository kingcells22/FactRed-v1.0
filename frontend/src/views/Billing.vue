<template>
  <div class="space-y-8">
    <!-- Header Section -->
    <div class="bg-gradient-to-r from-blue-900 to-indigo-900 rounded-3xl p-8 text-white shadow-2xl relative overflow-hidden">
        <div class="absolute inset-0 bg-blue-500/10 opacity-10"></div>
        <div class="relative z-10 flex flex-col md:flex-row justify-between items-center gap-6">
            <div>
                <h2 class="text-3xl font-bold flex items-center">
                    <span class="mr-3 text-4xl">💰</span> Gestión de Facturación
                </h2>
                <p class="text-blue-200 mt-2">Ejecuta cortes y gestiona suspensiones automáticas.</p>
            </div>
            <div class="bg-white/10 backdrop-blur-md p-4 rounded-xl border border-white/20">
                <span class="block text-xs uppercase tracking-wider text-blue-200">Fecha del Servidor</span>
                <span class="text-xl font-mono font-bold">{{ new Date().toLocaleDateString() }}</span>
            </div>
        </div>
    </div>

    <!-- Actions Panel -->
    <div class="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
        <div class="p-6 border-b border-gray-100 bg-gray-50/50">
            <h3 class="text-lg font-bold text-gray-800 flex items-center">
                <span class="w-2 h-8 bg-blue-600 rounded-full mr-3"></span>
                Acciones de Corte
            </h3>
        </div>
        
        <div class="p-8 flex flex-col md:flex-row gap-8 items-center justify-between">
            <div class="flex-1">
                <p class="text-gray-600 mb-4 leading-relaxed">
                    Este proceso analizará a todos los clientes. Si hoy coincide con su 
                    <span class="font-bold text-gray-800">Día de Corte</span>, se generará la factura. 
                    Si tienen facturas vencidas, se suspenderá el servicio automáticamente.
                </p>
                <div class="flex items-center gap-2 text-sm text-yellow-600 bg-yellow-50 px-3 py-2 rounded-lg w-fit">
                    <span class="text-lg">⚠️</span>
                    <span>Las notificaciones de WhatsApp son simuladas en esta versión.</span>
                </div>
            </div>

            <button 
                @click="handleRunProcess" 
                :disabled="billingStore.loading"
                class="group relative overflow-hidden bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold py-4 px-10 rounded-2xl shadow-lg hover:shadow-green-500/40 transition-all duration-300 transform hover:-translate-y-1 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                <span class="relative z-10 flex items-center text-lg">
                    <span v-if="billingStore.loading" class="animate-spin mr-3 text-2xl">⚙️</span>
                    <span v-else class="mr-3 text-2xl">⚡</span>
                    {{ billingStore.loading ? 'Procesando...' : 'Ejecutar Corte y Verificación' }}
                </span>
                <div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
            </button>
        </div>
    </div>

    <!-- Console Log Mockup -->
    <div class="rounded-2xl shadow-2xl overflow-hidden bg-[#1e1e1e] border border-gray-800 font-mono text-sm leading-relaxed">
        <div class="flex items-center justify-between px-4 py-3 bg-[#252526] border-b border-gray-700">
            <div class="flex gap-2">
                <div class="w-3 h-3 rounded-full bg-red-500"></div>
                <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
            </div>
            <span class="text-gray-400 text-xs">system_output.log</span>
        </div>
        <div class="p-6 h-64 overflow-y-auto custom-scrollbar">
            <template v-if="billingStore.processResult">
                <div class="mb-4">
                    <span class="text-green-400">➜</span> <span class="text-cyan-300">[SUCCESS]</span> Proceso completado.
                </div>
                <div v-for="(log, index) in billingStore.processResult.details" :key="index" class="pl-4 border-l-2 border-gray-700 mb-1">
                    <span class="text-gray-500">{{ new Date().toLocaleTimeString() }}</span> 
                    <span class="text-gray-300 ml-2">{{ log }}</span>
                </div>
                <!-- Fix for logic when array is empty -->
                 <div v-if="billingStore.processResult.details && billingStore.processResult.details.length === 0">
                    <span class="text-gray-500">{{ new Date().toLocaleTimeString() }}</span> 
                    <span class="text-yellow-300 ml-2">No hubo acciones pendientes para hoy.</span>
                </div>
            </template>
            <div v-else class="flex flex-col items-center justify-center h-full text-gray-600 opacity-50">
                <span class="text-4xl mb-4">⌨️</span>
                <p>Esperando ejecución...</p>
            </div>
        </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useBillingStore } from "../stores/billing";

const billingStore = useBillingStore();

const handleRunProcess = async () => {
  await billingStore.runDailyProcess();
};
</script>
