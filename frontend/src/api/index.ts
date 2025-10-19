import http from './http';
import type {Organization, Room} from '@/types';


export interface HealthResponse {
    ok: boolean;
    server_time: string;
    user: {
        id: number;
        username?: string;
        first_name?: string;
        last_name?: string;
        language_code?: string;
        is_premium?: boolean;
    };
}

export interface Paginated<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

export interface ApiBusy {
    start_at: string;
    end_at: string;
}

export type BookingStatus = 'PENDING' | 'APPROVED' | 'REJECTED' | 'CANCELED';

export interface ApiBooking {
    id: string;
    room: {
        id: string;
        title: string;
        image?: string | null;
        center?: { id?: string; name?: string; address?: string | null } | null;
        tags?: { id: string; name: string }[];
    } | null;
    status: BookingStatus;
    start_at: string;
    end_at: string;
    applicant_name: string;
    applicant_phone: string;
    event_name: string;
    event_purpose: string;
    target_audience: string;
    invited_speakers: string;
    required_equipment: string;
    rejection_reason?: string;
    created_at: string;
}


export const api = {
    health() {
        return http.get<HealthResponse>('/health/').then(r => r.data);
    },

    async getRooms(params?: any) {
        const res = await http.get<Paginated<any>>('/rooms/', {params});
        const data = res.data;

        if (!data || !Array.isArray(data.results)) {
            throw new Error('Unexpected response from /rooms/ (ожидался JSON с полем results[])');
        }

        const results: Room[] = data.results.map((it: any) => ({
            id: it.id,
            tags: it.tags || [],
            title: it.title,
            description: it.description,
            capacity: it.capacity,
            image: it.image ?? null,
            center: (it.center && typeof it.center === 'object')
                ? {id: String(it.center.id), name: it.center.name}
                : null,
            responsible: it.responsible ?? 0,
        }));

        return {...data, results};
    },

    getRoomBusy(roomId: string, params?: { start?: string; end?: string }) {
        return http.get<ApiBusy[]>(`/rooms/${roomId}/busy/`, {params}).then(r => r.data);
    },

    createBooking(payload: {
        room_id: string;
        start_at: string;
        end_at: string;
        applicant_name: string;
        applicant_phone: string;
        event_name: string;
        event_purpose: string;
        target_audience: string;
        invited_speakers: string;
        required_equipment: string;
    }) {
        return http.post('/bookings/', payload).then(r => r.data);
    },

    getMyBookings(params?: any) {
        return http.get<Paginated<ApiBooking>>('/bookings/', {params}).then(r => r.data);
    },

    async getCenters(params?: any) {
        const res = await http.get<Paginated<any>>('/centers/', {params});
        const data = res.data;
        if (!data || !Array.isArray(data.results)) {
            throw new Error('Unexpected response from /centers/ (ожидался JSON с полем results[])');
        }

        const results: Organization[] = data.results.map((it: any) => ({
            id: String(it.id),
            name: it.name,
            district: {
                id: String(it.district?.id),
                name: it.district?.name || '',
            },
            emblem: it.emblem ?? null,
            address: it.address ?? null,
            phone: it.phone ?? null,
        }));

        return {...data, results};

    },

    getBooking(id: string) {
        return http.get<ApiBooking>(`/bookings/${id}/`).then(r => r.data);
    },

}
