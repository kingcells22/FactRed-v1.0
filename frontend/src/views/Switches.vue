<template>
  <div class="space-y-6 animate-fade-in-up relative text-gray-200">
    <div class="bg-[#272d33] rounded-3xl p-6 md:p-8 text-white shadow-xl border border-[#3e464f] relative overflow-hidden">
        <div class="absolute top-0 right-0 -mt-10 -mr-10 w-40 h-40 bg-orange-600 rounded-full blur-3xl opacity-20 animate-pulse"></div>
        <div class="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
                <h2 class="text-2xl md:text-3xl font-bold mb-2 flex items-center gap-3 text-white">
                    <svg class="w-8 h-8 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                    Gestion de Switches / ISPs
                </h2>
                <p class="text-gray-400">Administra los nodos de distribucion y proveedores de tu red.</p>
            </div>
            <button @click="showModal = true" class="w-full md:w-auto bg-orange-600 hover:bg-orange-500 text-white px-6 py-3 rounded-xl font-bold shadow-lg shadow-orange-600/20 transition-all flex items-center justify-center gap-2 border border-orange-500/50">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg>
                Agregar Equipo
            </button>
        </div>
    </div>

    <div class="bg-[#272d33] rounded-2xl shadow-xl border border-[#3e464f] overflow-hidden w-full">
        <div v-if="isLoading" class="p-8 text-center text-gray-400 font-bold animate-pulse flex flex-col items-center">
            <div class="w-8 h-8 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mb-3"></div>
            Cargando equipos de la base de datos...
        </div>
        
        <div v-else class="overflow-x-auto w-full">
            <table class="min-w-full text-left border-collapse">
                <thead class="bg-[#1e2328]">
                    <tr class="text-gray-400 text-xs uppercase tracking-wider">
                        <th class="p-4 font-bold whitespace-nowrap">Equipo / Nodo</th>
                        <th class="p-4 font-bold whitespace-nowrap">IP DE GESTION</th>
                        <th class="p-4 font-bold whitespace-nowrap">Marca</th>
                        <th class="p-4 font-bold whitespace-nowrap">Segmento LAN</th>
                        <th class="p-4 font-bold text-center whitespace-nowrap">Estado</th>
                        <th class="p-4 font-bold text-center whitespace-nowrap">Acciones</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-[#3e464f]/50 bg-[#272d33]">
                    <tr v-if="switches.length === 0">
                        <td colspan="6" class="p-8 text-center text-gray-500 font-medium">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 mx-auto mb-3 text-gray-600">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0V12a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 12V5.25" />
                            </svg>
                            No hay equipos registrados aun. Haz clic en "Agregar Equipo".
                        </td>
                    </tr>
                    <tr v-for="sw in switches" :key="sw.id" class="hover:bg-[#353c44] transition-colors group">
                        <td class="p-4 whitespace-nowrap">
                            <div class="font-bold text-gray-100">{{ sw.name }}</div>
                            <div class="text-xs text-gray-500">{{ sw.location }}</div>
                        </td>
                        <td class="p-4 font-mono text-sm text-orange-400 whitespace-nowrap">{{ sw.ip_address }}</td>
                        <td class="p-4 whitespace-nowrap">
                            <span class="bg-[#1e2328] text-gray-300 px-3 py-1 rounded-lg text-xs font-bold border border-[#3e464f] shadow-inner inline-block">
                                {{ sw.vendor }}
                            </span>
                        </td>
                        <td class="p-4 font-mono text-xs text-gray-400 whitespace-nowrap">{{ sw.lan_segment || '---' }}</td>
                        <td class="p-4 text-center whitespace-nowrap">
                            <span :class="sw.status === 'Online' ? 'bg-green-500/10 text-green-500 border-green-500/20' : 'bg-red-500/10 text-red-500 border-red-500/20'" class="px-3 py-1 rounded-full text-xs font-bold border flex items-center justify-center w-24 mx-auto shadow-sm">
                                <div :class="sw.status === 'Online' ? 'bg-green-500 shadow-[0_0_5px_#22c55e]' : 'bg-red-500 shadow-[0_0_5px_#ef4444]'" class="w-1.5 h-1.5 rounded-full mr-2"></div>
                                {{ sw.status }}
                            </span>
                        </td>
                        
                        <td class="p-4 text-center flex justify-center gap-2 whitespace-nowrap">
                            <button @click="openInitModal(sw)" class="text-gray-400 hover:text-orange-500 bg-[#1e2328] border border-[#3e464f] hover:border-orange-500/50 transition-colors p-2 rounded-lg shadow-sm" title="Inicializar Equipo (Reglas de Corte)">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                            </button>
                            <button @click="openEditModal(sw)" class="text-gray-400 hover:text-blue-400 bg-[#1e2328] border border-[#3e464f] hover:border-blue-400/50 transition-colors p-2 rounded-lg shadow-sm" title="Editar">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                            </button>
                            <button @click="deleteSwitch(sw.id)" class="text-gray-400 hover:text-red-500 bg-[#1e2328] border border-[#3e464f] hover:border-red-500/50 transition-colors p-2 rounded-lg shadow-sm" title="Eliminar">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                            </button>
                        </td>

                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-[#272d33] rounded-3xl p-6 md:p-8 w-full max-w-md shadow-2xl animate-fade-in-up border border-[#3e464f]">
            <h3 class="text-xl md:text-2xl font-bold text-white mb-6 flex items-center">
            <span class="bg-orange-500/10 text-orange-500 border border-orange-500/20 p-2 rounded-lg mr-3 shadow-sm">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path></svg>
            </span>
            {{ isEditing ? 'Editar Equipo' : 'Registrar Equipo' }}
        </h3>            
            <form class="space-y-4" @submit.prevent="submitForm">
                <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-1">Nombre (Ej: PROVEEDOR_ISP_A)</label>
                    <input type="text" v-model="form.name" required class="w-full bg-[#1e2328] text-white border border-[#3e464f] rounded-xl p-3 focus:ring-2 focus:ring-orange-500 outline-none placeholder-gray-600 transition-all" placeholder="PROVEEDOR_ISP_A" />
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-1">IP de Gestion</label>
                    <input type="text" v-model="form.ip_address" required class="w-full bg-[#1e2328] text-orange-400 font-mono border border-[#3e464f] rounded-xl p-3 focus:ring-2 focus:ring-orange-500 outline-none placeholder-gray-600 transition-all" placeholder="192.168.X.X" />
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-1">Usuario</label>
                        <input type="text" v-model="form.username" required class="w-full bg-[#1e2328] text-white border border-[#3e464f] rounded-xl p-3 focus:ring-2 focus:ring-orange-500 outline-none transition-all" />
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-1">Contraseña</label>
                        <input type="password" v-model="form.password" required class="w-full bg-[#1e2328] text-white border border-[#3e464f] rounded-xl p-3 focus:ring-2 focus:ring-orange-500 outline-none transition-all" />
                    </div>
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wide mb-1">Segmento LAN (Opcional)</label>
                    <input type="text" v-model="form.lan_segment" class="w-full bg-[#1e2328] text-gray-300 font-mono border border-[#3e464f] rounded-xl p-3 focus:ring-2 focus:ring-orange-500 outline-none placeholder-gray-600 transition-all" placeholder="Ej: 10.0.0.0/24" />
                </div>

                <div class="flex gap-3 pt-4 border-t border-[#3e464f] mt-6">
                    <button type="button" @click="closeModal" class="flex-1 bg-[#1e2328] hover:bg-[#353c44] text-gray-400 hover:text-white border border-[#3e464f] font-bold py-3 rounded-xl transition-colors">
                        Cancelar
                    </button>
                    <button type="submit" :disabled="isSaving" class="flex-1 bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 rounded-xl transition-colors shadow-lg shadow-orange-600/20 border border-orange-500/50 disabled:opacity-50">
                        {{ isSaving ? 'Guardando...' : 'Guardar' }}
                    </button>
                </div>
            </form>
        </div>
    </div>

    <div v-if="showInitModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
        <div class="bg-[#272d33] rounded-3xl p-6 md:p-8 w-full max-w-lg shadow-2xl animate-fade-in-up border border-[#3e464f]">
            <h3 class="text-xl md:text-2xl font-bold text-white mb-2 flex items-center">
                <span class="bg-orange-500/10 text-orange-500 border border-orange-500/20 p-2 rounded-lg mr-3 shadow-sm">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                </span>
                Inicializar Equipo
            </h3>
            <p class="text-gray-400 font-medium mb-6 text-sm">Diagnostico de Pre-vuelo para <span class="text-orange-500 font-bold border-b border-orange-500/30 pb-0.5">{{ selectedSwitch?.name }}</span></p>

            <div v-if="isCheckingInit" class="py-10 text-center flex flex-col items-center bg-[#1e2328] rounded-xl border border-[#3e464f] shadow-inner">
                <div class="w-10 h-10 border-4 border-orange-500 border-t-transparent rounded-full animate-spin mb-4 shadow-[0_0_10px_rgba(234,88,12,0.5)]"></div>
                <p class="text-gray-300 font-bold animate-pulse">Escaneando configuracion actual...</p>
                <p class="text-xs text-gray-500 mt-2 font-mono">Verificando grupos, reglas y NAT por SSH.</p>
            </div>

            <div v-else-if="initReport">
                <div :class="initReport.status === 'clean' ? 'bg-green-500/10 border-green-500/30' : 'bg-red-500/10 border-red-500/30'" class="border rounded-xl p-5 mb-6 shadow-inner">
                    <p :class="initReport.status === 'clean' ? 'text-green-400' : 'text-red-400'" class="font-bold text-sm mb-3 flex items-center">
                        <svg v-if="initReport.status === 'clean'" class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                        <svg v-else class="w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                        {{ initReport.message }}
                    </p>
                    <ul class="list-disc pl-5 text-xs space-y-2 text-gray-300 font-medium">
                        <li v-for="detail in initReport.details" :key="detail">{{ detail }}</li>
                    </ul>
                </div>

                <div class="flex gap-3 pt-4 border-t border-[#3e464f]">
                    <button type="button" @click="showInitModal = false" class="flex-1 bg-[#1e2328] hover:bg-[#353c44] text-gray-400 hover:text-white border border-[#3e464f] font-bold py-3 rounded-xl transition-colors">
                        Cancelar
                    </button>
                    <button type="button" @click="executeInit(selectedSwitch.id)" :disabled="isExecutingInit" class="flex-1 bg-orange-600 hover:bg-orange-700 text-white font-bold py-3 rounded-xl transition-colors shadow-lg shadow-orange-600/20 border border-orange-500/50 disabled:opacity-50">
                        {{ isExecutingInit ? 'Aplicando...' : (initReport.status === 'clean' ? 'Proceder' : 'Actualizar Reglas') }}
                    </button>
                </div>
            </div>
        </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import axios from 'axios';

const API_URL = "http://172.31.45.56:8000";

const switches = ref<any[]>([]);
const isLoading = ref(true);
const showModal = ref(false);
const isSaving = ref(false);

// --- VARIABLES DE EDICIÓN NUEVAS ---
const isEditing = ref(false);
const editingId = ref<number | null>(null);

const showInitModal = ref(false);
const isCheckingInit = ref(false);
const isExecutingInit = ref(false);
const selectedSwitch = ref<any>(null);
const initReport = ref<any>(null);

const form = reactive({
    name: '',
    ip_address: '',
    username: '',
    password: '',
    lan_segment: '',
    location: 'Nodo Principal'
});

// --- FUNCIÓN PARA ABRIR EDICIÓN ---
const openEditModal = (sw: any) => {
    isEditing.value = true;
    editingId.value = sw.id;
    
    form.name = sw.name;
    form.ip_address = sw.ip_address;
    form.username = sw.username || '';
    form.password = ''; // Por seguridad se deja en blanco
    form.lan_segment = sw.lan_segment || '';
    form.location = sw.location || 'Nodo Principal';
    
    showModal.value = true;
};

// --- CLOSE MODAL ACTUALIZADO ---
const closeModal = () => {
    showModal.value = false;
    isEditing.value = false; // Reseteamos el estado de edición
    editingId.value = null;
    form.name = ''; form.ip_address = ''; form.username = ''; form.password = ''; form.lan_segment = '';
};

const fetchSwitches = async () => {
    isLoading.value = true;
    try {
        const res = await axios.get(`${API_URL}/util/switches`);
        switches.value = res.data;
    } catch (error) {
        console.error("Error al obtener los equipos:", error);
    } finally {
        isLoading.value = false;
    }
};

// --- SUBMIT FORM ACTUALIZADO (CREAR / EDITAR) ---
const submitForm = async () => {
    isSaving.value = true;
    try {
        if (isEditing.value && editingId.value) {
            // Si estamos editando, hace petición PUT
            await axios.put(`${API_URL}/util/switches/${editingId.value}`, form);
        } else {
            // Si es nuevo, hace petición POST
            await axios.post(`${API_URL}/util/switches`, form);
        }
        closeModal();
        fetchSwitches(); 
    } catch (error) {
        console.error("Error guardando el equipo:", error);
        alert("Hubo un error al guardar el equipo.");
    } finally {
        isSaving.value = false;
    }
};

const deleteSwitch = async (id: number) => {
    if (confirm("¿Estas seguro de que deseas eliminar este equipo?")) {
        try {
            await axios.delete(`${API_URL}/util/switches/${id}`);
            fetchSwitches(); 
        } catch (error) {
            alert("Error al eliminar el equipo.");
        }
    }
};

const openInitModal = async (sw: any) => {
    selectedSwitch.value = sw;
    showInitModal.value = true;
    isCheckingInit.value = true;
    initReport.value = null;

    try {
        const res = await axios.get(`${API_URL}/util/switches/${sw.id}/check-init`);
        initReport.value = res.data;
    } catch (error) {
        console.error("Error escaneando el equipo:", error);
        initReport.value = {
            status: 'error',
            message: 'Error al comunicarse con el equipo.',
            details: ['Verifica que el equipo este encendido y las credenciales sean correctas.']
        };
    } finally {
        isCheckingInit.value = false;
    }
};

// --- LOGICA DE EJECUCION REAL ---
const executeInit = async (id: number) => {
    isExecutingInit.value = true;
    try {
        const res = await axios.post(`${API_URL}/util/switches/${id}/init`);
        
        let resultMsg = "? Operacion finalizada con exito:\n\n";
        res.data.log.forEach((line: string) => resultMsg += `• ${line}\n`);
        
        alert(resultMsg);
        showInitModal.value = false;
    } catch (error) {
        console.error("Error inicializando:", error);
        alert("Hubo un error al inyectar las reglas. Revisa la consola.");
    } finally {
        isExecutingInit.value = false;
    }
};

onMounted(() => {
    fetchSwitches();
});
</script>