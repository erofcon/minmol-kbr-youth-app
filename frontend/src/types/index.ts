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

export interface Event {
    id: string;
    image: string | null;
    title: string;
    description: string;
    location: string;
    period: string;
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