import axios from "axios";
import type {PublicApiPaginated, Event as ApiEvent} from "@/types";

const baseURL = 'https://молод07.рф/api/public';

const publicHttp = axios.create({
    baseURL,
    timeout: 15000,
    headers: {'Content-Type': 'application/json'},
});

publicHttp.interceptors.response.use(
    (res) => res.data,
    (error) => {
        if (error.message === 'Network Error' && !error.response) {
            return Promise.reject({
                status: 'CORS',
                message: 'Ошибка CORS. Убедитесь, что сервер API разрешает запросы с вашего домена.',
                data: null
            });
        }
        const status = error?.response?.status;
        const data = error?.response?.data;
        // Более подробное сообщение об ошибке валидации
        const message = data?.message || error.message || 'Network error';
        return Promise.reject({status, message, data});
    }
);

interface GetEventsParams {
    page?: number;
    per_page?: number;
    search?: string;
    category?: string;
    type?: string;
    settlement?: string;
}

export const publicApi = {
    getEvents(params?: GetEventsParams) {
        // Создаем копию, чтобы не изменять оригинальный объект
        const queryParams = {...params};

        // *** ВОТ КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ ***
        // Если поле search пустое, удаляем его из параметров запроса.
        if (!queryParams.search) {
            delete queryParams.search;
        }

        return publicHttp.get<PublicApiPaginated<ApiEvent>>('/events', {params: queryParams});
    },
    getEventById(id: number | string) {
        return publicHttp.get<{ status: string, data: ApiEvent }>(`/events/${id}`).then(res => res.data);
    }
}