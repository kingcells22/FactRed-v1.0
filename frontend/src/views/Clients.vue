<template>
  <div class="relative min-h-screen text-gray-200 p-4 md:p-6">
    <div class="mb-6 flex flex-col md:flex-row justify-between items-center gap-4">
      <div class="relative w-full md:w-96 group">
        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-gray-500 group-hover:text-orange-500 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
            <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
          </svg>
        </span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Buscar por nombre, cedula o IP..."
          class="w-full pl-10 pr-4 py-3 bg-[#1e2328] border border-[#3e464f] text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent shadow-sm transition-all duration-300 placeholder-gray-500"
        />
      </div>
      <button
        @click="openModal"
        class="w-full md:w-auto bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500 text-white font-semibold py-3 px-6 rounded-xl flex items-center justify-center transition-all duration-300 shadow-lg shadow-orange-600/20 transform hover:-translate-y-0.5 active:translate-y-0"
      >
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mr-2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        Nuevo Cliente
      </button>
    </div>

    <div class="mb-4 flex justify-end">
      <div class="bg-[#272d33] px-4 py-2 rounded-full shadow-sm border border-[#3e464f] flex items-center gap-2">
        <span class="text-xs font-bold text-gray-400 uppercase tracking-wide">Tasa BCV:</span>
        <span class="font-mono text-green-500 font-bold">{{ exchangeRate }} Bs/$</span>
      </div>
    </div>

    <div class="bg-[#272d33] rounded-2xl shadow-xl border border-[#3e464f] overflow-hidden w-full">
      <div class="overflow-x-auto w-full">
        <table class="min-w-full divide-y divide-[#3e464f]">
          <thead class="bg-[#1e2328]">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider">Cliente</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider">Documento</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider">Plan Contratado</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider">Estado</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider text-center">Acciones ISP</th>
              <th class="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider text-center">Editar</th>
            </tr>
          </thead>
          <tbody class="bg-[#272d33] divide-y divide-[#3e464f]/50">
            <tr v-if="clientStore.loading" class="text-center">
              <td colspan="6" class="py-12">
                <div class="flex justify-center items-center space-x-2 animate-pulse">
                  <div class="w-2 h-2 bg-orange-500 rounded-full"></div>
                  <div class="w-2 h-2 bg-orange-500 rounded-full animation-delay-200"></div>
                  <div class="w-2 h-2 bg-orange-500 rounded-full animation-delay-400"></div>
                </div>
                <span class="text-gray-500 text-sm mt-3 block">Cargando clientes de la red...</span>
              </td>
            </tr>
            <tr v-else-if="clientStore.clients.length === 0" class="text-center">
              <td colspan="6" class="py-12 text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-12 h-12 mx-auto mb-2 text-gray-600">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                </svg>
                No hay clientes registrados en el sistema.
              </td>
            </tr>
            <tr v-for="client in clientStore.clients" :key="client.id" class="group hover:bg-[#353c44] transition-colors duration-200">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-12 w-12 rounded-xl bg-[#1e2328] border border-[#3e464f] flex items-center justify-center text-orange-500 font-bold text-lg shadow-inner group-hover:scale-105 transition-transform group-hover:border-orange-500/50">
                    {{ client.first_name[0] }}{{ client.last_name[0] }}
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-bold text-gray-100">
                      {{ client.first_name }} {{ client.last_name }}
                    </div>
                    <div class="text-xs text-gray-400 flex items-center mt-0.5">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3 h-3 mr-1">
                        <path fill-rule="evenodd" d="M2 3.5A1.5 1.5 0 0 1 3.5 2h1.148a1.5 1.5 0 0 1 1.465 1.175l.716 3.223a1.5 1.5 0 0 1-1.052 1.767l-.933.267c-.41.117-.643.555-.48.95a11.542 11.542 0 0 0 6.254 6.254c.395.163.833-.07.95-.48l.267-.933a1.5 1.5 0 0 1 1.767-1.052l3.223.716A1.5 1.5 0 0 1 18 15.352V16.5a1.5 1.5 0 0 1-1.5 1.5H15c-1.149 0-2.263-.15-3.326-.43A13.022 13.022 0 0 1 2.43 8.326 13.019 13.019 0 0 1 2 5V3.5Z" clip-rule="evenodd" />
                      </svg>
                      {{ client.contact_number }}
                    </div>
                    <div v-if="client.ip_address" class="text-xs text-orange-400 font-mono flex items-center mt-1.5 bg-[#1e2328] border border-[#3e464f] px-2 py-0.5 rounded shadow-sm w-fit">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-3 h-3 mr-1">
                        <path fill-rule="evenodd" d="M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Zm-1.5 0a6.5 6.5 0 1 1-11-4.99V10h1.833l.917-1.833H9.75v1.833h1.833V8.167h1.692A6.5 6.5 0 0 1 16.5 10Zm-8.458-3.083V5.5h1.291v1.417h-1.29Z" clip-rule="evenodd" />
                      </svg>
                      {{ client.ip_address }}
                    </div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-300">
                {{ client.identity_doc }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex flex-col">
                  <span class="text-sm font-bold text-gray-200">{{ client.plan_type }}</span>
                  <span class="text-xs text-green-500 font-medium mt-0.5">
                    ${{ client.plan_amount }} /
                    <span class="text-gray-500">{{ (client.plan_amount * exchangeRate).toFixed(2) }} Bs</span>
                  </span>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-3 py-1 inline-flex text-xs font-bold rounded-full border shadow-sm"
                  :class="{
                    'bg-green-500/10 text-green-500 border-green-500/20': client.service_status === 'Active',
                    'bg-red-500/10 text-red-500 border-red-500/20': client.service_status === 'Suspended',
                    'bg-gray-700/50 text-gray-400 border-gray-600': client.service_status === 'Cancelled'
                  }"
                >
                  <svg viewBox="0 0 8 8" fill="currentColor" class="w-2 h-2 mr-1.5 self-center animate-pulse" :class="{
                    'text-green-500': client.service_status === 'Active',
                    'text-red-500': client.service_status === 'Suspended',
                    'text-gray-400': client.service_status === 'Cancelled'
                  }">
                    <circle cx="4" cy="4" r="3" />
                  </svg>
                  {{ client.service_status === "Active" ? "Activo" : client.service_status === "Suspended" ? "Suspendido" : "Cancelado" }}
                </span>
              </td>
              
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex space-x-2 justify-center">
                  <button
                    v-if="client.service_status === 'Active'"
                    @click="suspendClient(client)"
                    class="text-orange-500 hover:text-white bg-orange-500/10 hover:bg-orange-600 p-2 rounded-lg transition-colors border border-orange-500/20 shadow-sm"
                    title="Suspender Servicio"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25v13.5m-7.5-13.5v13.5" />
                    </svg>
                  </button>

                  <button
                    v-if="['Suspended', 'Cancelled'].includes(client.service_status)"
                    @click="activateClient(client)"
                    class="text-green-500 hover:text-white bg-green-500/10 hover:bg-green-600 p-2 rounded-lg transition-colors border border-green-500/20 shadow-sm"
                    title="Reactivar Servicio"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5.25 5.653c0-.856.917-1.398 1.667-.986l11.54 6.347a1.125 1.125 0 0 1 0 1.972l-11.54 6.347a1.125 1.125 0 0 1-1.667-.986V5.653Z" />
                    </svg>
                  </button>

                  <button
                    v-if="client.service_status !== 'Cancelled'"
                    @click="cancelClient(client)"
                    class="text-gray-400 hover:text-white bg-[#1e2328] hover:bg-red-600 p-2 rounded-lg transition-colors border border-[#3e464f] shadow-sm"
                    title="Cancelar Contrato"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636" />
                    </svg>
                  </button>
                </div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex space-x-2 justify-center opacity-70 group-hover:opacity-100 transition-opacity">
                  <button
                    @click="alertPayment(client)"
                    class="text-yellow-500 hover:text-white p-2 hover:bg-yellow-600 rounded-lg transition-colors bg-[#1e2328] border border-[#3e464f]"
                    title="Recordatorio de Pago"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
                    </svg>
                  </button>
                  <button
                    @click="openEditModal(client)"
                    class="text-blue-400 hover:text-white p-2 hover:bg-blue-600 rounded-lg transition-colors bg-[#1e2328] border border-[#3e464f]"
                    title="Editar"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" />
                    </svg>
                  </button>
                  <button
                    @click="deleteClient(client.id!)"
                    class="text-red-400 hover:text-white p-2 hover:bg-red-600 rounded-lg transition-colors bg-[#1e2328] border border-[#3e464f]"
                    title="Eliminar"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div class="fixed inset-0 bg-black/80 transition-opacity backdrop-blur-sm" @click="closeModal"></div>
      <div class="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div class="relative transform overflow-hidden rounded-2xl bg-[#272d33] text-left shadow-2xl transition-all sm:my-8 sm:w-full sm:max-w-xl border border-[#3e464f]">
          
          <div class="bg-[#1e2328] px-6 py-4 border-b border-[#3e464f] flex justify-between items-center">
            <h3 class="text-lg font-bold text-white flex items-center" id="modal-title">
              <span class="bg-orange-500/10 text-orange-500 border border-orange-500/20 p-2 rounded-lg mr-3 shadow-sm">
                 <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                </svg>
              </span>
              {{ isEditing ? 'Editar Cliente' : 'Nuevo Cliente' }}
            </h3>
            <button @click="closeModal" class="text-gray-400 hover:text-white transition-colors bg-[#353c44] hover:bg-red-500 border border-[#3e464f] p-2 rounded-full shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <form @submit.prevent="handleSubmit" class="px-6 py-6 space-y-5">
            <div v-if="errorMsg" class="bg-red-500/10 border-l-4 border-red-500 text-red-400 p-4 rounded-md mb-4 text-sm flex items-start shadow-inner">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5 mr-2 flex-shrink-0">
                <path fill-rule="evenodd" d="M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Zm-8-5a.75.75 0 0 1 .75.75v4.5a.75.75 0 0 1-1.5 0v-4.5A.75.75 0 0 1 10 5Zm0 10a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" clip-rule="evenodd" />
              </svg>
              <p>{{ errorMsg }}</p>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">Nombre</label>
                <input v-model="form.first_name" required class="w-full px-4 py-2 bg-[#1e2328] border border-[#3e464f] text-white rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none" placeholder="Ej. Juan" />
              </div>
              <div>
                <label class="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">Apellido</label>
                <input v-model="form.last_name" required class="w-full px-4 py-2 bg-[#1e2328] border border-[#3e464f] text-white rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none" placeholder="Ej. Pérez" />
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">Cedula / Pasaporte</label>
                <input v-model="form.identity_doc" required class="w-full px-4 py-2 bg-[#1e2328] border border-[#3e464f] text-white rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none" placeholder="V-12345678" />
              </div>
              <div>
                <label class="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">Telefono (WhatsApp)</label>
                <input v-model="form.contact_number" required placeholder="+584121234567" class="w-full px-4 py-2 bg-[#1e2328] border border-[#3e464f] text-white rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none" />
              </div>
            </div>

            <div>
              <label class="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">Direccion</label>
              <input v-model="form.address" required class="w-full px-4 py-2 bg-[#1e2328] border border-[#3e464f] text-white rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none" placeholder="Ubicación de la instalación" />
            </div>

            <div class="bg-[#1e2328] p-4 rounded-xl border border-[#3e464f] shadow-inner">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-orange-400 text-xs font-bold mb-2 uppercase tracking-wide flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>
                    Nodo de Conexión
                  </label>
                  <select v-model="form.network_device_id" required class="w-full px-4 py-2 bg-[#272d33] border border-[#3e464f] text-white rounded-lg focus:ring-2 focus:ring-orange-500 outline-none cursor-pointer">
                    <option value="" disabled selected>Seleccione un equipo...</option>
                    <option v-for="sw in availableSwitches" :key="sw.id" :value="sw.id" class="bg-[#272d33] text-white">
                      {{ sw.name }} ({{ sw.vendor }})
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block text-orange-400 text-xs font-bold mb-2 uppercase tracking-wide">Direccion IP</label>
                  <input v-model="form.ip_address" required class="w-full px-4 py-2 bg-[#272d33] border border-[#3e464f] text-orange-400 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all outline-none font-mono" placeholder="192.168.1.X" />
                </div>
              </div>
            </div>

            <div class="bg-[#1e2328] p-4 rounded-xl border border-[#3e464f] shadow-inner">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">Plan (Simetrico)</label>
                  <select v-model="selectedPlanIndex" @change="updatePlanDetails" class="w-full px-4 py-2 bg-[#272d33] border border-[#3e464f] text-white rounded-lg focus:ring-2 focus:ring-orange-500 outline-none cursor-pointer">
                    <option v-for="(plan, index) in plans" :key="index" :value="index" class="bg-[#272d33] text-white">
                      {{ plan.name }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">Costo Mensual</label>
                  <div class="flex flex-col">
                    <div class="text-xl font-bold text-white">
                      ${{ form.plan_amount }}
                    </div>
                    <div class="text-xs text-green-500 font-medium bg-green-500/10 px-2 py-0.5 rounded-full w-fit border border-green-500/20 mt-1">
                      ~ {{ (form.plan_amount * exchangeRate).toFixed(2) }} Bs
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <label class="block text-gray-400 text-xs font-bold mb-2 uppercase tracking-wide">Dia de Corte</label>
              <div class="flex items-center">
                <input v-model.number="form.billing_day" type="number" min="1" max="28" required class="w-24 px-4 py-2 bg-[#1e2328] border border-[#3e464f] text-white rounded-lg focus:ring-2 focus:ring-orange-500 outline-none" />
                <span class="text-xs text-gray-500 ml-3 uppercase font-bold tracking-widest">de cada mes</span>
              </div>
            </div>

            <div class="bg-[#1e2328] -mx-6 -mb-6 px-6 py-4 flex justify-end gap-3 mt-6 border-t border-[#3e464f]">
              <button type="button" @click="closeModal" class="px-5 py-2.5 text-gray-400 hover:text-white font-medium hover:bg-[#353c44] rounded-lg transition-colors border border-transparent hover:border-[#3e464f]">
                Cancelar
              </button>
              <button type="submit" :disabled="clientStore.loading" class="px-5 py-2.5 bg-orange-600 hover:bg-orange-700 text-white font-bold rounded-lg shadow-lg shadow-orange-600/20 hover:shadow-orange-600/40 transition-all transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center">
                <span v-if="clientStore.loading" class="animate-spin mr-2">
                  <svg class="w-5 h-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
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

const showModal = ref(false);
const isEditing = ref(false);
const editingId = ref<number | null>(null);
const errorMsg = ref<string | null>(null);
const searchQuery = ref('');

const exchangeRate = ref(0);
const availableSwitches = ref<any[]>([]); // Lista de equipos

const plans = [
    { name: '100 Mbps (Fibra)', price: 15 },
    { name: '250 Mbps (Fibra)', price: 20 },
    { name: '350 Mbps (Fibra)', price: 25 },
    { name: '600 Mbps (Fibra)', price: 35 },
    { name: '1 Gbps (Fibra)', price: 45 },
];

const selectedPlanIndex = ref(0);
const defaultPlan = plans[0];

const form = reactive({
    first_name: '',
    last_name: '',
    identity_doc: '',
    address: '',
    plan_type: defaultPlan.name,
    plan_amount: defaultPlan.price,
    contact_number: '+58 ',
    billing_day: 5,
    service_status: 'Active',
    ip_address: '',
    network_device_id: '' as unknown as number // Para obligarlo a elegir
});

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
        fetchExchangeRate(),
        fetchSwitches() // Cargar switches al inicio
    ]);
});

const fetchExchangeRate = async () => {
    try {
        const res = await api.get('/util/exchange-rate');
        exchangeRate.value = res.data.rate || 344.87;
    } catch (e) {
        exchangeRate.value = 344.87; 
    }
}

const fetchSwitches = async () => {
    try {
        const res = await api.get('/util/switches');
        availableSwitches.value = res.data;
    } catch (e) {
        console.error("Error cargando switches", e);
    }
}

const updatePlanDetails = () => {
    const plan = plans[selectedPlanIndex.value];
    if (plan) {
        form.plan_type = plan.name;
        form.plan_amount = plan.price;
    }
};

const openModal = () => {
    isEditing.value = false;
    editingId.value = null;
    errorMsg.value = null;
    resetForm();
    showModal.value = true;
};

const openEditModal = (client: any) => {
    isEditing.value = true;
    editingId.value = client.id || null;
    errorMsg.value = null;
    
    Object.assign(form, client);
    
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
    form.network_device_id = '' as unknown as number;
    form.billing_day = 5;
    form.service_status = 'Active';
    selectedPlanIndex.value = 0;
    updatePlanDetails();
}

// --- ACCIONES ISP ---
const suspendClient = async (client: any) => {
    if(!confirm(`¿Estas seguro de SUSPENDER (Cortar Internet) a ${client.first_name}?`)) return;
    try {
        await api.post(`/clients/${client.id}/suspend`);
        alert(`Servicio de ${client.first_name} suspendido en el Nodo.`);
        await clientStore.fetchClients(); 
    } catch (e) {
        alert("Error al suspender servicio. Verifique conexion con el Nodo.");
    }
}

const activateClient = async (client: any) => {
    if(!confirm(`¿Reactivar servicio a ${client.first_name}? (Se aplicará el plan ${client.plan_type})`)) return;
    try {
        await api.post(`/clients/${client.id}/activate`);
        alert(`Servicio de ${client.first_name} ACTIVADO en el Nodo.`);
        await clientStore.fetchClients(); 
    } catch (e) {
        alert("Error al activar servicio. Verifique conexion con el Nodo.");
    }
}

const cancelClient = async (client: any) => {
    if(!confirm(`?? PELIGRO: ¿Cancelar contrato de ${client.first_name}? Se borraran sus reglas de velocidad.`)) return;
    try {
        await api.post(`/clients/${client.id}/cancel`);
        alert(`Contrato cancelado y removido del Nodo.`);
        await clientStore.fetchClients(); 
    } catch (e) {
        alert("Error al cancelar servicio");
    }
}

const deleteClient = async (id: number) => {
    if(!confirm("¿Estas seguro de eliminar este cliente de la base de datos y del Nodo?")) return;
    try {
        await api.delete(`/clients/${id}`);
        await clientStore.fetchClients(); 
    } catch (e) {
        alert("Error al eliminar");
    }
}

const alertPayment = (client: any) => {
    alert(`?? Recordatorio de pago enviado a ${client.first_name} ${client.last_name} (${client.contact_number})`);
}

const docPattern = /^([VEJ])-(\d{5,9})$/;

const handleSubmit = async () => {
    errorMsg.value = null;
    if (!docPattern.test(form.identity_doc)) {
        errorMsg.value = "Documento invalido. Formato requerido: V-12345678, E-123..., J-123...";
        return;
    }
    const cleanPhone = form.contact_number.replace(/[\s-]/g, '');
    if (!/^\+584\d{9}$/.test(cleanPhone)) {
         errorMsg.value = "Telefono invalido. Debe ser: +58 4xx-xxx-xxxx";
         return;
    }
    
    if (!form.network_device_id) {
         errorMsg.value = "Debe seleccionar un Nodo de Conexion para el cliente.";
         return;
    }

    try {
        if (isEditing.value && editingId.value) {
            await api.put(`/clients/${editingId.value}`, form);
        } else {
            await api.post('/clients/', form);
        }
        closeModal();
        await clientStore.fetchClients();
    } catch (e: any) {
        console.error(e);
        if (e.response && e.response.data && e.response.data.detail) {
            errorMsg.value = e.response.data.detail;
        } else {
            errorMsg.value = "Error desconocido al comunicarse con el servidor o el Nodo.";
        }
    }
};
</script>