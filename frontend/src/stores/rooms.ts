import {defineStore} from 'pinia';
import type {Center, Room} from '@/types';
import {api} from '@/api';

export const useRoomsStore = defineStore('rooms', {
    state: () => ({
        rooms: [] as Room[],
        loading: false,
        error: null as string | null,
    }),

    getters: {
        uniqueCenters(state): Center[] {
            const centersMap = new Map<string, Center>();
            state.rooms.forEach(room => {
                const c = room.center;
                if (c?.id && !centersMap.has(c.id)) {
                    centersMap.set(c.id, c);
                }
            });
            return Array.from(centersMap.values());
        },
        getRoomById(state) {
            return (roomId: string): Room | undefined => {
                return state.rooms.find(room => room.id === roomId);
            }
        }
    },

    actions: {
        async fetchRooms() {
            this.loading = true;
            this.error = null;
            try {
                const data = await api.getRooms();
                this.rooms = data.results;
            } catch (err: any) {
                this.error = err?.message || 'Не удалось загрузить помещения. Попробуйте позже.';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
    },
});