<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="bg-white/90 backdrop-blur-xl p-8 rounded-3xl shadow-2xl w-full max-w-md border border-white/20 animate-fade-in-up">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-black text-slate-800 tracking-tight">FactRed Admin</h1>
        <p class="text-slate-500 mt-2">Inicia sesi&oacute;n para gestionar la red</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wide">Usuario</label>
          <input 
            v-model="username" 
            type="text" 
            class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            placeholder="admin"
            required
          >
        </div>
        
        <div>
          <label class="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wide">Contrase&ntilde;a</label>
          <input 
            v-model="password" 
            type="password" 
            class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            placeholder="campo obligatorio"
            required
          >
        </div>

        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg text-sm text-center font-bold">
          {{ error }}
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-4 rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all transform active:scale-95 disabled:opacity-70"
        >
          {{ loading ? 'Ingresando...' : 'Entrar al Sistema' }}
        </button>
      </form>
      
      <div class="mt-6 text-center">
         <p class="text-xs text-slate-400">Sistema optimizado para Starlink + Mikrotik</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; // <-- IMPORTANTE: Ahora usamos axios para hablar con el backend

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

// IP DE TU SERVIDOR BACKEND
const API_URL = "http://172.31.45.56:8000";

const handleLogin = async () => {
    error.value = '';
    loading.value = true;
    
    try {
        // 1. Le tocamos la puerta al nuevo archivo auth.py
        const response = await axios.post(`${API_URL}/login`, {
            username: username.value,
            password: password.value
        });
        
        // 2. Si el backend dice OK (200), guardamos la sesión y pasamos
        if (response.status === 200) {
            localStorage.setItem('isAuthenticated', 'true');
            router.push('/');
        }
    } catch (err: any) {
        console.error(err);
        // Mostrar el error real del backend o uno genérico
        error.value = err.response?.data?.detail || 'Error al conectar con el servidor';
    } finally {
        loading.value = false;
    }
}
</script>