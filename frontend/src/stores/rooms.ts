import {defineStore} from 'pinia';
import type {Center, Room} from '@/types';

const mockApiResponse = {
    count: 4,
    next: null,
    previous: null,
    results: [
        {
            id: 'a1b2c3d4-e5f6-7890-1234-567890abcdef',
            tags: [{id: 'tag-1', name: 'Wi-Fi'}, {id: 'tag-2', name: 'Проектор'}, {id: 'tag-3', name: 'Флипчарт'}],
            title: "Конференц-зал 'Атриум'",
            description: "Просторный зал для больших мероприятий.",
            capacity: 50,
            image: 'https://cdn.prod.website-files.com/67069e5f7c7aab0dc21ade12/67372a109671c9cd16a05a73_Rooms%20Header%20(1).png',
            is_active: true,
            center: {id: 'center-1', name: 'Урванский район'},
            responsible: 101,
        },
        {
            id: 'b2c3d4e5-f6a7-8901-2345-67890abcdef1',
            tags: [{id: 'tag-1', name: 'Wi-Fi'}, {id: 'tag-4', name: 'Маркерная доска'}],
            title: "Переговорная 'Лофт'",
            description: "Уютная комната для небольших команд.",
            capacity: 10,
            image: 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/31/37/9b/87/caption.jpg?w=1200&h=1200&s=1',
            is_active: true,
            center: {id: 'center-2', name: 'Чегемский район'},
            responsible: 102,
        },
        {
            id: 'c3d4e5f6-a7b8-9012-3456-7890abcdef23',
            tags: [{id: 'tag-1', name: 'Wi-Fi'}, {id: 'tag-5', name: 'Кухня'}],
            title: "Коворкинг 'Тишина'",
            description: "Место для спокойной и продуктивной работы.",
            capacity: 25,
            image: null, // Имитация отсутствия картинки
            is_active: true,
            center: {id: 'center-1', name: 'Урванский район'},
            responsible: 101,
        },
        {
            id: 'd4e5f6a7-b8c9-0123-4567-890abcdef34',
            tags: [{id: 'tag-6', name: 'PlayStation'}, {id: 'tag-7', name: 'Настольные игры'}],
            title: "Игровая комната",
            description: "Зона отдыха и развлечений.",
            capacity: 15,
            image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT-9bsuXoQhirimO_bLZ8t8hBC6ZqBEwB8W7g&s',
            is_active: false, // Имитация неактивного помещения
            center: {id: 'center-3', name: 'Эльбрусский район'},
            responsible: 103,
        }
    ]
};

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
                if (!centersMap.has(room.center.id)) {
                    centersMap.set(room.center.id, room.center);
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
                await new Promise(resolve => setTimeout(resolve, 500));
                this.rooms = mockApiResponse.results;

            } catch (err) {
                this.error = 'Не удалось загрузить помещения. Попробуйте позже.';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
    },
});