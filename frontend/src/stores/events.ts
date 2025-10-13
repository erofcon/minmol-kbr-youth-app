// src/stores/events.ts
import {defineStore} from 'pinia';
import type {Event} from '@/types';

const mockApiResponse = {
    results: [
        {
            id: 'wq2321eqwqweq',
            image: 'https://молод07.рф/storage/uploads/events1/cover/1h3kfYmlwJeFqpthqv8X2lQlMq7BQb43E5QBq3pb.jpg',
            title: 'В Нальчике пройдет КВН на кабардинском языке',
            description: 'Весёлое состязание молодежных команд состоится в Доме молодежи 19 сентября. Команды из разных уголков республики сразятся за звание самых находчивых и остроумных. Зрителей ждет море юмора, яркие выступления и незабываемая атмосфера праздника. Приходите поддержать свои любимые команды!',
            location: 'Нальчик, пр. Кулиева, 12',
            period: '19.09.2025 — 19.09.2025'
        },
        {
            id: 'wq2321eqwqsdfsdfsdweq',
            image: 'https://minmol.kbr.ru/upload/iblock/4ba/hy8mulmpptjwankudiv8nuge8yddspl8/42f66b91_24b7_474a_91d7_c831810f7ae1.jpeg',
            title: '«Проводники смыслов» в Кабардино-Балкарии.',
            description: 'С 19 по 21 августа в трёх муниципальных образованиях республики прошла федеральная обучающая программа. Она собрала молодёжных лидеров и наставников, готовых транслировать ' +
                'традиционные ценности и вовлекать молодёжь в социально значимые проекты. Участники прошли интенсивный курс лекций, тренингов и практических занятий.',
            location: 'Нальчик, пр. Кулиева, 12',
            period: '23.10.2025 — 25.10.2025'
        },
        {
            id: 'event-3',
            image: null,
            title: 'Круглый стол по цифровой грамотности',
            description: 'Обсуждение актуальных вопросов безопасности в сети и современных цифровых трендов. Эксперты поделятся советами, как защитить свои данные, распознавать фейковые новости и эффективно использовать цифровые инструменты для учебы и работы. Мероприятие будет транслироваться онлайн.',
            location: 'Онлайн',
            period: '30.11.2025'
        }
    ]
};

export const useEventsStore = defineStore('events', {
    state: () => ({
        events: [] as Event[],
        loading: false,
        error: null as string | null,
    }),
    getters: {
        getEventById(state) {
            return (eventId: string): Event | undefined => {
                return state.events.find(event => event.id === eventId);
            }
        }
    },
    actions: {
        async fetchEvents() {
            this.loading = true;
            this.error = null;
            try {
                // Имитируем задержку сети
                await new Promise(resolve => setTimeout(resolve, 600));
                this.events = mockApiResponse.results;
            } catch (err) {
                this.error = 'Не удалось загрузить мероприятия. Попробуйте позже.';
                console.error(err);
            } finally {
                this.loading = false;
            }
        },
    },
});