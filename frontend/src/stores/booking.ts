import {defineStore} from 'pinia';
import type {BookingPayload} from "@/types";

function pad(n: number) {
    return String(n).padStart(2, '0');
}

function buildApiIsoFromMsk(date: Date, hour: number, minute = 0) {
    const y = date.getFullYear();
    const m = date.getMonth() + 1;
    const d = date.getDate();
    return `${y}-${pad(m)}-${pad(d)}T${pad(hour)}:${pad(minute)}:00.000Z`;
}

export const useBookingStore = defineStore('booking', {
    state: () => ({
        room_id: null as string | null,
        start_at: null as string | null,
        end_at: null as string | null,
        applicant_name: '',
        applicant_phone: '',
        event_name: '',
        event_purpose: '',
        target_audience: '',
        invited_speakers: '',
        required_equipment: '',
    }),

    getters: {
        isReady: (s) => !!s.room_id && !!s.start_at && !!s.end_at,
        payload(state): BookingPayload | null {
            if (!state.room_id || !state.start_at || !state.end_at) return null;
            return {
                room_id: state.room_id,
                start_at: state.start_at,
                end_at: state.end_at,
                applicant_name: state.applicant_name,
                applicant_phone: state.applicant_phone,
                event_name: state.event_name,
                event_purpose: state.event_purpose,
                target_audience: state.target_audience,
                invited_speakers: state.invited_speakers,
                required_equipment: state.required_equipment,
            };
        },
    },

    actions: {
        setRoom(id: string) {
            this.room_id = id;
        },
        setPeriodFromMsk(date: Date, startHour: number, endHour: number) {
            this.start_at = buildApiIsoFromMsk(date, startHour);
            this.end_at = buildApiIsoFromMsk(date, endHour);
        },
        clearPeriod() {
            this.start_at = null;
            this.end_at = null;
        },
        resetAll() {
            this.room_id = null;
            this.clearPeriod();
            this.applicant_name = '';
            this.applicant_phone = '';
            this.event_name = '';
            this.event_purpose = '';
            this.target_audience = '';
            this.invited_speakers = '';
            this.required_equipment = '';
        },
    },
});


// import {defineStore} from 'pinia';
// import type {BookingPayload} from "@/types";
//
// function pad(n: number) {
//     return String(n).padStart(2, '0');
// }
//
// function buildApiIsoFromMsk(date: Date, hour: number, minute = 0) {
//     const y = date.getFullYear();
//     const m = date.getMonth() + 1;
//     const d = date.getDate();
//     return `${y}-${pad(m)}-${pad(d)}T${pad(hour)}:${pad(minute)}:00.000Z`;
// }
//
// export const useBookingStore = defineStore('booking', {
//     state: () => ({
//         room_id: null as string | null,
//         start_at: null as string | null,
//         end_at: null as string | null,
//
//         applicant_name: '',
//         applicant_tg_username: '',
//         applicant_phone: '',
//         event_name: '',
//         event_purpose: '',
//         target_audience: '',
//         invited_speakers: '',
//         required_equipment: '',
//     }),
//
//     getters: {
//         isReady: (s) => !!s.room_id && !!s.start_at && !!s.end_at,
//         payload(state): BookingPayload | null {
//             if (!state.room_id || !state.start_at || !state.end_at) return null;
//             return {
//                 room_id: state.room_id,
//                 start_at: state.start_at,
//                 end_at: state.end_at,
//                 applicant_name: state.applicant_name,
//                 applicant_tg_username: state.applicant_tg_username,
//                 applicant_phone: state.applicant_phone,
//                 event_name: state.event_name,
//                 event_purpose: state.event_purpose,
//                 target_audience: state.target_audience,
//                 invited_speakers: state.invited_speakers,
//                 required_equipment: state.required_equipment,
//             };
//         },
//     },
//
//     actions: {
//         setRoom(id: string) {
//             this.room_id = id;
//         },
//
//         setPeriodFromMsk(date: Date, startHour: number, endHour: number) {
//             this.start_at = buildApiIsoFromMsk(date, startHour);
//             this.end_at = buildApiIsoFromMsk(date, endHour);
//         },
//         clearPeriod() {
//             this.start_at = null;
//             this.end_at = null;
//         },
//         resetAll() {
//             this.room_id = null;
//             this.clearPeriod();
//             this.applicant_name = '';
//             this.applicant_tg_username = '';
//             this.applicant_phone = '';
//             this.event_name = '';
//             this.event_purpose = '';
//             this.target_audience = '';
//             this.invited_speakers = '';
//             this.required_equipment = '';
//         },
//     },
// });