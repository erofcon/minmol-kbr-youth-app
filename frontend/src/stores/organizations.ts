import {defineStore} from 'pinia';
import type {Organization, District} from '@/types';

const mockApiResponse = {
    results: [
        {
            id: 'org-1',
            name: 'Молодежный центр "Нальчик"',
            district: {id: 'district-1', name: 'Нальчик'},
            emblem: 'https://avatars.mds.yandex.net/i?id=eff1c3b87577f1454d2fc458532b6e3416f80009-5453486-images-thumbs&n=13',
            address: 'ул. Пушкина, д. 10',
            phone: '+79281234567',
        },
        {
            id: 'org-2',
            name: 'Волонтеры Победы КБР',
            district: {id: 'district-1', name: 'Нальчик'},
            emblem: 'https://iliad.ru/wp-content/themes/litho/resize.php?width=420&stretch=true&height=auto&photo=aHR0cHM6Ly9pbGlhZC5ydS93cC1jb250ZW50L3VwbG9hZHMvbWluaWF0X3Jvc20uanBn',
            address: 'ул. Ленина, д. 5',
            phone: '+79287654321',
        },
        {
            id: 'org-3',
            name: 'Студенческий совет "Прогресс"',
            district: {id: 'district-2', name: 'Прохладненский район'},
            emblem: null,
            address: 'г. Прохладный, ул. Свободы, д. 1',
            phone: null,
        },
        {
            id: 'org-4',
            name: 'Клуб "Баксан"',
            district: {id: 'district-3', name: 'Баксанский район'},
            emblem: 'https://static.tildacdn.com/tild6163-3333-4134-a436-663130613965/Group_37.svg',
            address: null,
            phone: '+79280001122',
        }
    ]
};

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
                if (!districtsMap.has(org.district.id)) {
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
                await new Promise(resolve => setTimeout(resolve, 700));
                this.organizations = mockApiResponse.results;
            } catch (err) {
                this.error = 'Не удалось загрузить организации. Попробуйте позже.';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
    },
});