import axios from "axios";

// const baseURL = (import.meta.env.API_BASE_URL || '/api/v1').replace(/\/+$/, '')

// const baseURL = 'http://127.0.0.1:8000/api/v1'
const baseURL = 'https://merrily-genuine-panther.cloudpub.ru//api/v1'

function getInitData(): string {
    try {
        return window.Telegram?.WebApp?.initData || '';
    } catch {
        return '';
    }
}


const http = axios.create({
    baseURL,
    timeout: 15000,
    headers: {'Content-Type': 'application/json'},
});

http.interceptors.request.use((config) => {
    const initData = getInitData();
    if (initData) {
        config.headers = config.headers || {};
        (config.headers as any)['X-Telegram-Init-Data'] = initData;
    }
    return config;
});

http.interceptors.response.use(
    (res) => res,
    (error) => {
        const status = error?.response?.status;
        const data = error?.response?.data;
        const message = data?.detail || data?.error || error.message || 'Network error';
        return Promise.reject({status, message, data});
    }
);


export default http;