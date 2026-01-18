import { defineStore } from 'pinia';
import api from '../api';
import { ref } from 'vue';

interface ProcessResult {
    processed: boolean;
    details: string[];
}

export const useBillingStore = defineStore('billing', () => {
    const loading = ref(false);
    const processResult = ref<ProcessResult | null>(null);
    const stats = ref({ pending_amount: 0, overdue_invoices: 0, suspended_clients: 0 });

    const runDailyProcess = async () => {
        loading.value = true;
        try {
            const response = await api.post('/billing/process-daily');
            processResult.value = response.data;
            await fetchStats(); // Refresh stats
        } catch (error) {
            console.error(error);
        } finally {
            loading.value = false;
        }
    };

    const fetchStats = async () => {
        try {
            const res = await api.get('/billing/stats');
            stats.value = res.data;
        } catch (e) {
            console.error("Error stats", e);
        }
    };

    return {
        loading,
        processResult,
        stats,
        runDailyProcess,
        fetchStats
    };
});
