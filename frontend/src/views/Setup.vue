<template>
  <div class="min-h-screen bg-slate-900 flex flex-col justify-center py-12 sm:px-6 lg:px-8 transition-all">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-white flex justify-center items-center gap-3">
        <div class="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center font-bold text-xl shadow-lg shadow-blue-500/50">F</div>
        FactRed Setup
      </h2>
      <p class="mt-2 text-center text-sm text-slate-400 font-medium tracking-widest uppercase">
        {{ step === 1 ? 'Paso 1: Conexion al Core' : 'Paso 2: Diagnostico y Orquestacion' }}
      </p>
    </div>

    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-lg">
      <div class="bg-white/95 backdrop-blur-xl py-8 px-4 shadow-2xl sm:rounded-2xl sm:px-10 border border-slate-200">
        
        <form v-if="step === 1" class="space-y-6 animate-fade-in-up" @submit.prevent="handleSubmit">
          
          <div>
            <h3 class="text-lg font-bold text-slate-800 border-b-2 border-slate-100 pb-2 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
              Datos del Equipo Core
            </h3>

            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mb-1">Fabricante / Marca</label>
            <select v-model="form.vendor" @change="updatePort"
              class="mt-1 block w-full border border-slate-300 rounded-xl shadow-sm p-3 focus:ring-2 focus:ring-blue-500 outline-none bg-white mb-4">
              <option value="mikrotik">MikroTik (RouterOS API)</option>
              <option value="fortinet">Fortinet (SSH)</option>
              <option value="cisco_ios">Cisco IOS (SSH)</option>
              <option value="huawei">Huawei (SSH)</option>
            </select>

            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide">IP del Equipo</label>
            <input type="text" v-model="form.mikrotik_ip" required 
              class="mt-1 block w-full border border-slate-300 rounded-xl shadow-sm p-3 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ej: 192.168.150.1" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide">Usuario</label>
              <input type="text" v-model="form.mikrotik_user" required 
                class="mt-1 block w-full border border-slate-300 rounded-xl shadow-sm p-3 focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide">Puerto {{ form.vendor === 'mikrotik' ? 'API' : 'SSH' }}</label>
              <input type="number" v-model="form.mikrotik_port" required 
                class="mt-1 block w-full border border-slate-300 rounded-xl shadow-sm p-3 focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide">Contraseña</label>
            <input type="password" v-model="form.mikrotik_password" 
              class="mt-1 block w-full border border-slate-300 rounded-xl shadow-sm p-3 focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>

          <div class="pt-4">
            <h3 class="text-lg font-bold text-slate-800 border-b-2 border-slate-100 pb-2 mb-4 flex items-center">
               <svg class="w-5 h-5 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path></svg>
              Seguridad FactRed
            </h3>
            
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide">Nueva Clave Admin</label>
            <input type="password" v-model="form.new_admin_password" required 
              class="mt-1 block w-full border border-slate-300 rounded-xl shadow-sm p-3 focus:ring-2 focus:ring-blue-500 outline-none" />
            
            <label class="block text-xs font-bold text-slate-500 uppercase tracking-wide mt-3">Confirmar Clave</label>
            <input type="password" v-model="form.confirm_password" required 
              class="mt-1 block w-full border border-slate-300 rounded-xl shadow-sm p-3 focus:ring-2 focus:ring-blue-500 outline-none" />
          </div>

          <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-xl text-sm text-center font-bold border border-red-200">
            {{ error }}
          </div>

          <div>
            <button type="submit" :disabled="loading"
              class="w-full flex justify-center py-4 px-4 rounded-xl shadow-lg text-sm font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:scale-[1.02] transition-all disabled:opacity-70">
              {{ loading ? 'Conectando...' : 'Guardar y Continuar ->' }}
            </button>
          </div>
        </form>

        <div v-if="step === 2" class="space-y-6 animate-fade-in-up text-center">
            <div v-if="isScanning" class="py-10">
                <div class="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-4"></div>
                <h3 class="text-xl font-bold text-slate-800">Auditando {{ form.vendor === 'fortinet' ? 'FortiGate' : form.vendor.toUpperCase() }}...</h3>
                <p class="text-slate-500 text-sm mt-2">Buscando interfaces, políticas y conectividad SSH.</p>
            </div>

            <div v-else class="text-left">
                <div class="bg-slate-50 p-6 rounded-2xl border border-slate-200 mb-6 relative overflow-hidden">
                    <h3 class="text-xl font-black text-slate-800 mb-2">
                        {{ scanData.is_virgin ? 'Equipo de Fabrica Detectado' : 'Equipo en Produccion Detectado' }}
                    </h3>
                    <p class="text-slate-600 text-sm mb-4">
                        {{ scanData.is_virgin 
                            ? 'Este equipo no tiene configuracion de red. FactRed puede crear el esqueleto ISP basico por ti.' 
                            : 'Detectamos configuracion existente. FactRed solo inyectara las reglas de seguridad sin afectar tu trafico actual.' }}
                    </p>
                </div>

                <div v-if="scanData.is_virgin" class="mb-6 bg-blue-50 p-4 rounded-xl border border-blue-100">
                    <label class="block text-xs font-bold text-blue-800 uppercase tracking-wide mb-2">Asignar Red LAN Principal</label>
                    <input type="text" v-model="installOptions.base_lan" 
                        class="w-full border border-blue-200 rounded-lg p-3 text-sm focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Ej: 192.168.10.1/24" />
                </div>

                <div v-if="injectError" class="bg-red-50 text-red-600 p-3 rounded-xl text-sm text-center font-bold border border-red-200 mb-4">
                    {{ injectError }}
                </div>

                <button @click="injectRules" :disabled="injecting"
                    class="w-full flex justify-center items-center py-4 px-4 rounded-xl shadow-lg text-sm font-bold text-white bg-gradient-to-r from-green-500 to-emerald-600 hover:scale-[1.02] transition-all disabled:opacity-70">
                    {{ injecting ? 'Inyectando Reglas...' : 'Inyectar Reglas y Finalizar' }}
                </button>
            </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import axios from 'axios';

const step = ref(1);
const loading = ref(false);
const error = ref('');
const isScanning = ref(true);
const injecting = ref(false);
const injectError = ref('');

const scanData = reactive({ is_virgin: false, interfaces_count: 0, nat_count: 0 });
const installOptions = reactive({ base_lan: '192.168.100.1/24' });

const API_URL = "http://172.31.45.56:8000";

const form = reactive({
  vendor: 'mikrotik',
  mikrotik_ip: '',
  mikrotik_user: 'admin',
  mikrotik_password: '',
  mikrotik_port: 8728,
  new_admin_password: '',
  confirm_password: ''
});

const updatePort = () => {
  if (form.vendor === 'mikrotik') {
    form.mikrotik_port = 8728;
  } else {
    form.mikrotik_port = 22; 
  }
};

const handleSubmit = async () => {
  error.value = '';
  loading.value = true;

  if (form.new_admin_password !== form.confirm_password) {
    error.value = "Las contraseñas no coinciden.";
    loading.value = false;
    return;
  }

  try {
    await axios.post(`${API_URL}/setup/install`, {
        vendor: form.vendor,
        mikrotik_ip: form.mikrotik_ip,
        mikrotik_user: form.mikrotik_user,
        mikrotik_password: form.mikrotik_password,
        mikrotik_port: Number(form.mikrotik_port),
        new_admin_password: form.new_admin_password
    });

    step.value = 2;
    runScanner();

  } catch (err: any) {
    error.value = err.response?.data?.detail || "Error de conexion.";
  } finally {
    loading.value = false;
  }
};

const runScanner = async () => {
    isScanning.value = true;
    try {
        const response = await axios.get(`${API_URL}/setup/scan-mikrotik`);
        scanData.is_virgin = response.data.is_virgin;
        scanData.interfaces_count = response.data.interfaces_count;
        scanData.nat_count = response.data.nat_count;
    } catch (err: any) {
        scanData.is_virgin = false;
    } finally {
        isScanning.value = false;
    }
};

const injectRules = async () => {
    injecting.value = true;
    injectError.value = '';
    try {
        await axios.post(`${API_URL}/setup/inject-rules`, {
            mode: scanData.is_virgin ? 'full' : 'partial',
            base_lan: installOptions.base_lan
        });
        alert("¡Instalacion Exitosa!");
        window.location.href = '/login'; 
    } catch (err: any) {
        injectError.value = "Error al inyectar reglas.";
    } finally {
        injecting.value = false;
    }
}
</script>