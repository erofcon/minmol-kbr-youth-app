import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AppCheckingView from "@/views/AppCheckingView.vue";
import RoomsView from "@/views/RoomsView.vue";
import RoomDetailView from "@/views/RoomDetailView.vue";
import BookingUserForm from "@/views/BookingUserForm.vue";
import BookingPreview from "@/views/BookingPreview.vue";
import BookingDateTime from "@/views/BookingDateTime.vue";
import BookingSuccessView from "@/views/BookingSuccessView.vue";
import EventListView from "@/views/EventListView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/checking',
            name: 'checking',
            component: AppCheckingView,
        },
        {
            path: '/',
            redirect: '/checking',
        },
        {
            path: '/app',
            children: [
                {
                    path: '',
                    name: 'home',
                    component: HomeView,
                },
                {
                    path: 'rooms',
                    name: 'rooms',
                    component: RoomsView,

                },
                {
                    path: 'room/:id',
                    name: 'room_detail',
                    component: RoomDetailView,
                },
                {
                    path: 'booking/:id',
                    name: 'booking_datetime',
                    component: BookingDateTime,
                },
                {
                    path: 'booking/information/:id',
                    name: 'booking_information',
                    component: BookingUserForm,
                    meta: {keepAlive: true},
                },
                {
                    path: 'booking/preview/:id',
                    name: 'booking_preview',
                    component: BookingPreview,
                },
                {
                    path: 'event_list/',
                    name: 'event_list',
                    component: EventListView

                }
            ],
        },
        {
            path: '/booking_success',
            name: 'booking_success',
            component: BookingSuccessView,
            meta: {
                disableSwipeBack: true
            }
        },
    ],
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition;
        } else {
            return {top: 0};
        }
    }
})


export default router
