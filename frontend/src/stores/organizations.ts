import {defineStore} from 'pinia';
import type {District, Organization} from '@/types';
import {api} from '@/api';

export const useOrganizationsStore = defineStore('organizations', {
    state: () => ({
        organizations: [] as Organization[],
        loading: false,
        error: null as string | null,
    }),
    getters: {
        uniqueDistricts(state): District[] {
            const districtsMap = new Map<string, District>();
            state.organizations.forEach(org => {
                if (org.district?.id && !districtsMap.has(org.district.id)) {
                    districtsMap.set(org.district.id, org.district);
                }
            });
            return Array.from(districtsMap.values());
        },
    },
    actions: {
        async fetchOrganizations() {
            this.loading = true;
            this.error = null;
            try {
                const data = await api.getCenters();
                this.organizations = data.results;
            } catch (err: any) {
                console.error('Centers API error', err);
                this.error = err?.message || 'Не удалось загрузить организации. Попробуйте позже.';
                this.organizations = [];
            } finally {
                this.loading = false;
            }
        },
    },
});