<script setup lang="ts">
import AppPage from "@/components/AppPage.vue"
import {useBookingStore} from "@/stores/booking.ts";
import {useRoute, useRouter} from "vue-router";
import {useRoomsStore} from "@/stores/rooms.ts";
import {computed} from "vue";


const route = useRoute()
const router = useRouter()
const roomsStore = useRoomsStore()

const roomId = route.params.id as string
const bookingStore = useBookingStore()

const room = computed(() => roomsStore.getRoomById(roomId))

const formattedBookingPeriod = computed(() => {
  const start = new Date(bookingStore.start_at);
  const end = new Date(bookingStore.end_at);

  const options = {
    day: 'numeric',
    month: 'short',
    weekday: 'short',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC' // если дата в UTC; уберите, если локальная
  };

  const startStr = start.toLocaleString('ru-RU', options);
  const endStr = end.toLocaleString('ru-RU', options);

  return `${startStr} — ${endStr}`;
});

const goNext = () => {
  router.replace({name: 'booking_success'})
}

</script>

<template>
  <AppPage title="Подтверждение">
    <span class="border-t mt-4 tg-border"></span>

    <div class="mx-2">
      <div class="mt-4 pb-3 border-b tg-border">
        <h1 class="font-bold text-lg tg-text mb-2 ">Информация о заявке</h1>
        <p>{{ bookingStore.applicant_name }}</p>
        <p>{{ bookingStore.applicant_phone }}</p>
        <p>{{ bookingStore.event_name }}</p>
      </div>

      <div class="mt-4 pb-3 border-b tg-border">
        <h1 class="font-bold tg-text text-lg  mb-2">Помещение</h1>
        <p>{{ room.title }}</p>
        <p>г. Нальчик, ул. Кулиева 2</p>
      </div>

      <div class="mt-4 pb-3 border-b tg-border">
        <h1 class="font-bold tg-text text-lg  mb-2">Ваша бронь</h1>
        <p>{{ formattedBookingPeriod }}</p>
      </div>
    </div>

    <div class="p-4 my-4 text-sm tg-text rounded-lg  tg-secondary-bg" role="alert">
      <span class="font-medium">Внимание!</span> Бронирование помещении бесплатно только для бесплатных
      и не коммерческих мероприятии.
    </div>


    <div
        class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50">
      <button
          @click="goNext"
          class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors"
      >
        <span class="truncate">Отправить запрос</span>
      </button>
    </div>


  </AppPage>
</template>

<style scoped>

</style>