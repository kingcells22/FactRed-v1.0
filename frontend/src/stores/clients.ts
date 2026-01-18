import { defineStore } from 'pinia';
import api from '../api';
import { ref } from 'vue';

export interface Client {
    id?: number;
    first_name: string;
    last_name: string;
    identity_doc: string;
    address: string;
    plan_type: string;
    plan_amount: number;
    contact_number: string;
    ip_address?: string;
    service_status?: string;
    billing_day: number;
}

export const useClientStore = defineStore('clients', () => {
    const clients = ref<Client[]>([]);
    const loading = ref(false);
    const error = ref<string | null>(null);

    const fetchClients = async (search: string = '') => {
        loading.value = true;
        try {
            // Append search query if exists
            const url = search ? `/clients?search=${search}` : '/clients';
            const response = await api.get(url);
            clients.value = response.data;
        } catch (err) {
            error.value = 'Error al cargar clientes';
            console.error(err);
        } finally {
            loading.value = false;
        }
    };

    const addClient = async (client: Client) => {
        loading.value = true;
        try {
            const response = await api.post('/clients', client);
            // clients.value.push(response.data); // Refresh handling usually better by refetch or smart push
            await fetchClients(); 
            return response.data;
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Error al crear cliente';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    const updateClient = async (id: number, client: Partial<Client>) => {
        loading.value = true;
        try {
             await api.put(`/clients/${id}`, client);
             await fetchClients();
        } catch(err: any){
             error.value = err.response?.data?.detail || 'Error al actualizar';
             throw err;
        } finally {
             loading.value = false;
        }
    }

    const deleteClient = async (id: number) => {
        loading.value = true;
        try {
            await api.delete(`/clients/${id}`);
            await fetchClients();
        } catch (err: any) {
             error.value = 'Error eliminar cliente';
             throw err;
        } finally {
            loading.value = false;
        }
    }

    return {
        clients,
        loading,
        error,
        fetchClients,
        addClient,
        updateClient,
        deleteClient
    };
});
