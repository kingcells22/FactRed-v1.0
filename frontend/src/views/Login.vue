<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="bg-white/90 backdrop-blur-xl p-8 rounded-3xl shadow-2xl w-full max-w-md border border-white/20 animate-fade-in-up">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-black text-slate-800 tracking-tight">FactRed Admin</h1>
        <p class="text-slate-500 mt-2">Inicia sesión para gestionar la red</p>
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
          <label class="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wide">Contraseña</label>
          <input 
            v-model="password" 
            type="password" 
            class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
            placeholder="••••••"
            required
          >
        </div>

        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg text-sm text-center font-bold">
          {{ error }}
        </div>

        <button 
          type="submit" 
          class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-4 rounded-xl shadow-lg hover:shadow-xl hover:scale-[1.02] transition-all transform active:scale-95"
        >
          Entrar al Sistema
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

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');

const handleLogin = () => {
    // Simple mock auth
    if(username.value === 'admin' && password.value === 'admin'){
        localStorage.setItem('isAuthenticated', 'true');
        router.push('/');
    } else {
        error.value = 'Credenciales inválidas';
    }
}
</script>
