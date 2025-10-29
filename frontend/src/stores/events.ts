import {defineStore} from 'pinia';
import type {Event} from '@/types';
import {publicApi} from "@/api/publicApi";

// Вспомогательная функция для исправления данных от API
const correctEventData = (event: Event): Event => {
    // Проверяем, существует ли поле cover и содержит ли оно дубликат
    if (event.cover && event.cover.includes('/storage/storage/')) {
        // Заменяем двойное вхождение на одинарное
        event.cover = event.cover.replace('/storage/storage/', '/storage/');
    }
    return event;
};


export const useEventsStore = defineStore('events', {
    state: () => ({
        events: [] as Event[],
        eventsById: new Map<number, Event>(),
        loading: false,
        loadingMore: false,
        error: null as string | null,
        currentPage: 0,
        lastPage: 1,
        total: 0,
    }),
    getters: {
        getEventById(state) {
            return (eventId: number): Event | undefined => {
                return state.eventsById.get(eventId);
            }
        },
        hasMore(state): boolean {
            return state.currentPage < state.lastPage;
        }
    },
    actions: {
        async fetchFirstPage(searchQuery: string = '') {
            this.loading = true;
            this.error = null;
            try {
                const response = await publicApi.getEvents({page: 1, search: searchQuery});

                // Применяем исправление к каждому элементу
                this.events = response.data.map(correctEventData);

                this.eventsById.clear();
                this.events.forEach(event => this.eventsById.set(event.id, event));

                const {pagination} = response;
                this.currentPage = pagination.current_page;
                this.lastPage = pagination.last_page;
                this.total = pagination.total;
            } catch (err: any) {
                this.error = err?.message || 'Не удалось загрузить мероприятия. Попробуйте позже.';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
        async fetchMoreEvents(searchQuery: string = '') {
            if (!this.hasMore || this.loadingMore) return;

            this.loadingMore = true;
            try {
                const nextPage = this.currentPage + 1;
                const response = await publicApi.getEvents({page: nextPage, search: searchQuery});

                // Применяем исправление к новым элементам
                const newEvents = response.data.map(correctEventData);

                this.events.push(...newEvents);
                newEvents.forEach(event => this.eventsById.set(event.id, event));

                this.currentPage = response.pagination.current_page;

            } catch (err: any) {
                console.error('Failed to load more events:', err);
            } finally {
                this.loadingMore = false;
            }
        },
        async fetchEventById(id: number) {
            if (this.eventsById.has(id)) {
                return;
            }
            this.loading = true;
            try {
                const response = await publicApi.getEventById(id);
                // Применяем исправление к одному элементу
                const correctedEvent = correctEventData(response.data);
                this.eventsById.set(id, correctedEvent);
            } catch (err: any) {
                this.error = err?.message || `Не удалось загрузить мероприятие с ID ${id}.`;
                console.error(err);
            } finally {
                this.loading = false;
            }
        }
    },
});