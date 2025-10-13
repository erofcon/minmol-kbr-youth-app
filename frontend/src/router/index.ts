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
import EventDetailView from "@/views/EventDetailView.vue";
import OrganizationListView from "@/views/OrganizationListView.vue";


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/checking',
            name: 'checking',
            component: AppCheckingView,
            meta: {depth: 0}
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
                    meta: {disableSwipeBack: true, depth: 1}
                },
                {
                    path: 'rooms',
                    name: 'rooms',
                    component: RoomsView,
                    meta: {depth: 2}
                },
                {
                    path: 'room/:id',
                    name: 'room_detail',
                    component: RoomDetailView,
                    meta: {depth: 3}
                },
                {
                    path: 'booking/:id',
                    name: 'booking_datetime',
                    component: BookingDateTime,
                    meta: {depth: 4}
                },
                {
                    path: 'booking/information/:id',
                    name: 'booking_information',
                    component: BookingUserForm,
                    meta: {keepAlive: true, depth: 5},
                },
                {
                    path: 'booking/preview/:id',
                    name: 'booking_preview',
                    component: BookingPreview,
                    meta: {depth: 6}
                },
                {
                    path: 'event_list/',
                    name: 'event_list',
                    component: EventListView,
                    meta: {depth: 2}
                },
                {
                    path: 'event/:id',
                    name: 'event_detail',
                    component: EventDetailView,
                    meta: {depth: 3}
                },
                {
                    path: 'organizations',
                    name: 'organizations_list',
                    component: OrganizationListView,
                    meta: {depth: 2}
                }
            ],
        },
        {
            path: '/booking_success',
            name: 'booking_success',
            component: BookingSuccessView,
            meta: {
                disableSwipeBack: true,
                depth: 7
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
