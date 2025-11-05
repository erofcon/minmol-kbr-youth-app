export interface Tag {
    id: string
    name: string
}

export interface Center {
    id: string
    name: string
}

export interface Room {
    id: string
    tags: Tag[]
    title: string
    description: string
    capacity: number
    image: string | null
    center: Center | null
    responsible: number
    address: string
}

export interface BookingPayload {
    room_id: string
    start_at: string
    end_at: string
    applicant_name: string
    applicant_phone: string
    event_name: string
    event_purpose: string
    target_audience: string
    invited_speakers: string
    required_equipment: string
}

export interface HourRange {
    start: number
    end: number
}

// Обновленный тип Event, соответствующий новому API
export interface Event {
    id: number;
    title: string;
    short_description: string;
    description: string;
    category: string;
    type: string;
    cover: string | null;
    address: string;
    settlement: string;
    start: string; // YYYY-MM-DD
    end: string;   // YYYY-MM-DD
    supervisor_name?: string;
    supervisor_l_name?: string;
    supervisor_phone?: string;
    supervisor_email?: string;
    web?: string;
    telegram?: string;
    vk?: string;
    roles?: string[];
    docs?: string[];
    images?: string[];
    videos?: string[];
    created_at: string;
    user?: {
        id: number;
        name: string;
    };
}


export interface PublicApiPaginated<T> {
    status: 'success';
    data: T[];
    pagination: {
        current_page: number;
        last_page: number;
        per_page: number;
        total: number;
    };
}


export interface District {
    id: string;
    name: string;
}

export interface Organization {
    id: string;
    name: string;
    district: District;
    emblem: string | null;
    address: string | null;
    phone: string | null;
}