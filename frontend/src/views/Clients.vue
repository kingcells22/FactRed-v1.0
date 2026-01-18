<template>
  <div class="relative min-h-screen text-slate-800 p-6">
    <!-- Header Actions -->
    <div
      class="mb-6 flex flex-col md:flex-row justify-between items-center gap-4"
    >
      <div class="relative w-full md:w-96 group">
        <span
          class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500 group-hover:text-blue-500 transition-colors"
        >
          🔍
        </span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por nombre, cédula o IP..."
          class="w-full pl-10 pr-4 py-3 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm transition-all duration-300 hover:shadow-md"
        />
      </div>
      <button
        @click="openModal"
        class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-xl flex items-center transition-all duration-300 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 active:translate-y-0"
      >
        <span class="mr-2 text-xl">+</span> Nuevo Cliente
      </button>
    </div>

    <!-- Tasa info -->
    <div class="mb-4 flex justify-end">
      <div
        class="bg-white px-4 py-2 rounded-full shadow-sm border border-gray-100 flex items-center gap-2"
      >
        <span class="text-xs font-bold text-gray-500 uppercase tracking-wide"
          >Tasa BCV:</span
        >
        <span class="font-mono text-green-600 font-bold"
          >{{ exchangeRate }} Bs/$</span
        >
      </div>
    </div>

    <!-- Client Table -->
    <div
      class="bg-white/95 backdrop-blur-xl rounded-2xl shadow-xl overflow-hidden border border-gray-100"
    >
      <table class="min-w-full divide-y divide-gray-100">
        <thead class="bg-gray-50/50">
          <tr>
            <th
              class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider"
            >
              Cliente
            </th>
            <th
              class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider"
            >
              Documento
            </th>
            <th
              class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider"
            >
              Plan Contratado
            </th>
            <th
              class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider"
            >
              Estado
            </th>
            <th
              class="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider"
            >
              Acciones
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-100">
          <tr v-if="clientStore.loading" class="text-center">
            <td colspan="5" class="py-12">
              <div
                class="flex justify-center items-center space-x-2 animate-pulse"
              >
                <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
                <div
                  class="w-2 h-2 bg-blue-500 rounded-full animation-delay-200"
                ></div>
                <div
                  class="w-2 h-2 bg-blue-500 rounded-full animation-delay-400"
                ></div>
              </div>
              <span class="text-gray-400 text-sm mt-2 block"
                >Cargando clientes...</span
              >
            </td>
          </tr>
          <tr v-else-if="clientStore.clients.length === 0" class="text-center">
            <td colspan="5" class="py-12 text-gray-500">
              <div class="text-4xl mb-2">📂</div>
              No hay clientes registrados.
            </td>
          </tr>
          <tr
            v-for="client in clientStore.clients"
            :key="client.id"
            class="group hover:bg-slate-50/80 transition-colors duration-200"
          >
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center">
                <div
                  class="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center text-blue-700 font-bold text-lg shadow-inner group-hover:scale-110 transition-transform"
                >
                  {{ client.first_name[0] }}{{ client.last_name[0] }}
                </div>
                <div class="ml-4">
                  <div class="text-sm font-bold text-gray-900">
                    {{ client.first_name }} {{ client.last_name }}
                  </div>
                  <div class="text-xs text-gray-500 flex items-center mt-0.5">
                    <span class="mr-1">📱</span> {{ client.contact_number }}
                  </div>
                  <!-- IP Display -->
                  <div v-if="client.ip_address" class="text-xs text-blue-600 font-mono flex items-center mt-1 bg-blue-50 px-1.5 py-0.5 rounded w-fit">
                    <span class="mr-1">🌐</span> {{ client.ip_address }}
                  </div>
                </div>
              </div>
            </td>
            <td
              class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-600 rounded-lg mx-2 w-fit px-2 py-1"
            >
              {{ client.identity_doc }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex flex-col">
                <span class="text-sm font-semibold text-gray-900">{{
                  client.plan_type
                }}</span>
                <span class="text-xs text-green-600 font-medium">
                  ${{ client.plan_amount }} /
                  <span class="text-gray-500"
                    >{{
                      (client.plan_amount * exchangeRate).toFixed(2)
                    }}
                    Bs</span
                  >
                </span>
              </div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full border"
                :class="
                  client.service_status === 'Active'
                    ? 'bg-green-50 text-green-700 border-green-200'
                    : 'bg-red-50 text-red-700 border-red-200'
                "
              >
                <span
                  class="w-1.5 h-1.5 rounded-full mr-1.5 mt-1.5"
                  :class="
                    client.service_status === 'Active'
                      ? 'bg-green-500'
                      : 'bg-red-500'
                  "
                ></span>
                {{
                  client.service_status === "Active" ? "Activo" : "Suspendido"
                }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
              <div
                class="flex space-x-2 opacity-60 group-hover:opacity-100 transition-opacity"
              >
                <button
                  @click="alertPayment(client)"
                  class="text-yellow-600 hover:text-yellow-900 p-2 hover:bg-yellow-50 rounded-lg transition-colors"
                  title="Enviar Recordatorio de Pago"
                >
                  🔔
                </button>
                <button
                  @click="openEditModal(client)"
                  class="text-indigo-600 hover:text-indigo-900 p-2 hover:bg-indigo-50 rounded-lg transition-colors"
                  title="Editar"
                >
                  ✏️
                </button>
                <button
                  @click="deleteClient(client.id!)"
                  class="text-red-600 hover:text-red-900 p-2 hover:bg-red-50 rounded-lg transition-colors"
                  title="Eliminar"
                >
                  🗑️
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Create Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 overflow-y-auto"
      aria-labelledby="modal-title"
      role="dialog"
      aria-modal="true"
    >
      <!-- Backdrop -->
      <div
        class="fixed inset-0 bg-gray-900/60 transition-opacity backdrop-blur-sm"
        @click="closeModal"
      ></div>

      <div
        class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0"
      >
        <div
          class="relative transform overflow-hidden rounded-2xl bg-white text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-lg border border-gray-100"
        >
          <!-- Header -->
          <div
            class="bg-gradient-to-r from-slate-50 to-white px-6 py-4 border-b border-gray-100 flex justify-between items-center"
          >
            <h3
              class="text-lg font-bold text-gray-900 flex items-center"
              id="modal-title"
            >
              <span class="bg-blue-100 text-blue-600 p-2 rounded-lg mr-3"
                >👤</span
              >
              Nuevo Cliente
            </h3>
            <button
              @click="closeModal"
              class="text-gray-400 hover:text-gray-600 transition-colors bg-gray-50 hover:bg-gray-100 p-2 rounded-full"
            >
              ✕
            </button>
          </div>

          <form @submit.prevent="handleSubmit" class="px-6 py-6 space-y-5">
            <!-- Error Alert -->
            <div
              v-if="errorMsg"
              class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-md mb-4 text-sm flex items-start"
            >
              <span class="mr-2">⚠️</span>
              <p>{{ errorMsg }}</p>
            </div>

            <!-- Name Fields -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label
                  class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                  >Nombre</label
                >
                <input
                  v-model="form.first_name"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
                  placeholder="Ej. Juan"
                />
              </div>
              <div>
                <label
                  class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                  >Apellido</label
                >
                <input
                  v-model="form.last_name"
                  required
                  class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
                  placeholder="Ej. Pérez"
                />
              </div>
            </div>

            <!-- Doc Info -->
            <div>
              <label
                class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                >Cédula / Pasaporte</label
              >
              <input
                v-model="form.identity_doc"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
                placeholder="V-12345678"
              />
            </div>

            <!-- Contact -->
            <div>
              <label
                class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                >Teléfono (WhatsApp)</label
              >
              <input
                v-model="form.contact_number"
                required
                placeholder="+584121234567"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
              />
            </div>

            <div>
              <label
                class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                >Dirección</label
              >
              <input
                v-model="form.address"
                required
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none"
                placeholder="Ubicación de la instalación"
              />
            </div>

            <!-- IP Address -->
             <div>
              <label
                class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                >Dirección IP (Mikrotik/ONU)</label
              >
              <input
                v-model="form.ip_address"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all outline-none font-mono"
                placeholder="192.168.1.X"
              />
            </div>

            <!-- Plan Selection -->
            <div class="bg-slate-50 p-4 rounded-xl border border-slate-200">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label
                    class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                    >Plan (Simétrico)</label
                  >
                  <select
                    v-model="selectedPlanIndex"
                    @change="updatePlanDetails"
                    class="w-full px-4 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none cursor-pointer"
                  >
                    <option
                      v-for="(plan, index) in plans"
                      :key="index"
                      :value="index"
                    >
                      {{ plan.name }}
                    </option>
                  </select>
                </div>
                <div>
                  <label
                    class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                    >Costo Mensual</label
                  >
                  <div class="flex flex-col">
                    <div class="text-xl font-bold text-gray-800">
                      ${{ form.plan_amount }}
                    </div>
                    <div
                      class="text-xs text-green-600 font-medium bg-green-50 px-2 py-0.5 rounded-full w-fit"
                    >
                      ≈ {{ (form.plan_amount * exchangeRate).toFixed(2) }} Bs
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <label
                class="block text-gray-700 text-xs font-bold mb-2 uppercase tracking-wide"
                >Día de Corte</label
              >
              <input
                v-model.number="form.billing_day"
                type="number"
                min="1"
                max="28"
                required
                class="w-24 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              />
              <span class="text-xs text-gray-500 ml-2">de cada mes</span>
            </div>

            <!-- Footer -->
            <div
              class="bg-gray-50 -mx-6 -mb-6 px-6 py-4 flex justify-end gap-3 mt-6 border-t border-gray-100"
            >
              <button
                type="button"
                @click="closeModal"
                class="px-5 py-2.5 text-gray-600 hover:text-gray-800 font-medium hover:bg-gray-200 rounded-lg transition-colors"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="clientStore.loading"
                class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition-all transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
              >
                <span v-if="clientStore.loading" class="animate-spin mr-2"
                  >⏳</span
                >
                Guardar Cliente
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive, watch } from 'vue';
import { useClientStore, type Client } from '../stores/clients';
import api from '../api';

const clientStore = useClientStore();

// UI State
const showModal = ref(false);
const isEditing = ref(false);
const editingId = ref<number | null>(null);
const errorMsg = ref<string | null>(null);
const searchQuery = ref('');

// Exchange Rate
const exchangeRate = ref(0);

// Defined Plans
const plans = [
    { name: '100 Mbps (Fibra)', price: 15 },
    { name: '250 Mbps (Fibra)', price: 20 },
    { name: '350 Mbps (Fibra)', price: 25 },
    { name: '600 Mbps (Fibra)', price: 35 },
    { name: '1 Gbps (Fibra)', price: 45 },
];

const selectedPlanIndex = ref(0);

// Safe initialization
const defaultPlan = plans[0] || { name: 'N/A', price: 0 };

const form = reactive<Client>({
    first_name: '',
    last_name: '',
    identity_doc: '',
    address: '',
    plan_type: defaultPlan.name,
    plan_amount: defaultPlan.price,
    contact_number: '+58 ',
    billing_day: 5,
    service_status: 'Active',
    ip_address: '' // New Field
});

// Manual Debounce for Search
let searchTimeout: any;
watch(searchQuery, (newVal) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(async () => {
        await clientStore.fetchClients(newVal);
    }, 500);
});

onMounted(async () => {
    await Promise.all([
        clientStore.fetchClients(),
        fetchExchangeRate()
    ]);
});

const fetchExchangeRate = async () => {
    try {
        const res = await api.get('/util/exchange-rate');
        if (res.data.rate) {
            exchangeRate.value = res.data.rate;
        } else {
             exchangeRate.value = 344.87;
        }
    } catch (e) {
        console.error("Error fetching rate", e);
        exchangeRate.value = 344.87; // User requested value
    }
}

const updatePlanDetails = () => {
    const plan = plans[selectedPlanIndex.value];
    if (plan) {
        form.plan_type = plan.name;
        form.plan_amount = plan.price;
    }
};

// Modal Logic
const openModal = () => {
    isEditing.value = false;
    editingId.value = null;
    errorMsg.value = null;
    resetForm();
    showModal.value = true;
};

const openEditModal = (client: Client) => {
    isEditing.value = true;
    editingId.value = client.id || null;
    errorMsg.value = null;
    
    // Populate form
    Object.assign(form, client);
    
    // Match plan index if possible
    const planIdx = plans.findIndex(p => p.name === client.plan_type);
    if (planIdx !== -1) selectedPlanIndex.value = planIdx;
    
    showModal.value = true;
}

const closeModal = () => {
    showModal.value = false;
    errorMsg.value = null;
    resetForm();
};

const resetForm = () => {
    form.first_name = '';
    form.last_name = '';
    form.identity_doc = '';
    form.contact_number = '+58 ';
    form.address = '';
    form.ip_address = '';
    form.billing_day = 5;
    form.service_status = 'Active';
    selectedPlanIndex.value = 0;
    updatePlanDetails();
}

const deleteClient = async (id: number) => {
    if(!confirm("¿Estás seguro de eliminar este cliente?")) return;
    try {
        await clientStore.deleteClient(id);
    } catch (e) {
        alert("Error al eliminar");
    }
}

const alertPayment = (client: Client) => {
    // Mock action
    alert(`📢 Recordatorio de pago enviado a ${client.first_name} ${client.last_name} (${client.contact_number})`);
}

// Validations
const docPattern = /^([VEJ])-(\d{5,9})$/;

const handleSubmit = async () => {
    errorMsg.value = null;
    // Strict Validation
    if (!docPattern.test(form.identity_doc)) {
        errorMsg.value = "Documento inválido. Formato requerido: V-12345678, E-123..., J-123...";
        return;
    }
    const cleanPhone = form.contact_number.replace(/[\s-]/g, '');
    if (!/^\+584\d{9}$/.test(cleanPhone)) {
         errorMsg.value = "Teléfono inválido. Debe ser: +58 4xx-xxx-xxxx";
         return;
    }

    try {
        if (isEditing.value && editingId.value) {
            await clientStore.updateClient(editingId.value, { ...form });
        } else {
            await clientStore.addClient({ ...form });
        }
        closeModal();
    } catch (e: any) {
        console.error(e);
        if (e.response && e.response.data && e.response.data.detail) {
            errorMsg.value = e.response.data.detail;
        } else {
            errorMsg.value = "Error desconocido al comunicarse con el servidor.";
        }
    }
};
</script>
