import {defineStore} from 'pinia';
import {api, type ApiBooking, type Paginated} from '@/api';

export const useMyBookingsStore = defineStore('myBookings', {

    state: () => ({

        items: [] as ApiBooking[],
        loading: false,
        loadingMore: false,
        error: null as string | null,
        next: null as string | null,
    }),

    getters: {
        hasMore: (s) => !!s.next,
    },

    actions: {

        async fetchFirst() {
            this.loading = true;
            this.error = null;
            this.items = [];
            this.next = null;
            try {
                const data = await api.getMyBookings();
                this.items = data.results || [];
                this.next = data.next;
            } catch (e: any) {
                console.error('getMyBookings error', e);
                this.error = e?.message || 'Не удалось загрузить бронирования';
            } finally {
                this.loading = false;
            }
        },

        async fetchMore() {
            if (!this.next || this.loadingMore) return;
            this.loadingMore = true;
            try {

                const data = await (await fetch(this.next, {
                    headers: {
                        'Accept': 'application/json',
                        'X-Telegram-Init-Data': (window as any)?.Telegram?.WebApp?.initData || '',
                    },
                })).json() as Paginated<ApiBooking>;
                this.items = [...this.items, ...(data.results || [])];
                this.next = data.next;
            } catch (e: any) {
                console.error('getMyBookings next error', e);
            } finally {
                this.loadingMore = false;
            }
        },
    },
});