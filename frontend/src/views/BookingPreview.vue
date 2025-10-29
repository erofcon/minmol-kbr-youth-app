<script setup lang="ts">
import AppPage from "@/components/AppPage.vue"
import {useBookingStore} from "@/stores/booking.ts";
import {useRoute, useRouter} from "vue-router";
import {useRoomsStore} from "@/stores/rooms.ts";
// *** ИЗМЕНЕНИЕ: Добавляем onMounted ***
import {computed, ref, onMounted} from "vue";
import {api} from '@/api';
import ErrorComponent from "@/components/ErrorComponent.vue";

const route = useRoute()
const router = useRouter()
const roomsStore = useRoomsStore()
const bookingStore = useBookingStore()
const roomId = route.params.id as string

const room = computed(() => roomsStore.getRoomById(roomId))


onMounted(async () => {
  if (roomsStore.rooms.length === 0) {
    await roomsStore.fetchRooms();
  }
});

const formattedBookingPeriod = computed(() => {
  const start = new Date(bookingStore.start_at!);
  const end = new Date(bookingStore.end_at!);
  const options: Intl.DateTimeFormatOptions = {
    day: 'numeric',
    month: 'short',
    weekday: 'short',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC'
  };

  return `${start.toLocaleString('ru-RU', options)} — ${end.toLocaleString('ru-RU', options)}`
})


const loading = ref(false)
const errorText = ref<string | null>(null)
const goNext = async () => {
  if (loading.value) return;
  if (!bookingStore.payload) return;

  loading.value = true;
  errorText.value = null;

  try {
    await api.createBooking(bookingStore.payload);
    router.replace({name: 'booking_success'});
  } catch (e: any) {
    errorText.value = 'Не удалось отправить заявку. Возможно, помещение уже занято.' +
        ' Проверьте данные и попробуйте снова.';
    console.error(e);
  } finally {
    loading.value = false;
  }
}

</script>

<template>
  <AppPage title="Подтверждение" :class="{ 'pb-18': true }">
    <span class="border-t mt-4 tg-border"></span>

    <ErrorComponent v-if="errorText" class="mt-4" :error-text="errorText"/>

    <div class="mx-2">
      <div class="mt-4 pb-3 border-b tg-border">
        <h1 class="font-bold text-lg tg-text mb-2 ">Информация о заявке</h1>
        <p>{{ bookingStore.applicant_name }}</p>
        <p>{{ bookingStore.applicant_phone }}</p>
        <p>{{ bookingStore.event_name }}</p>
      </div>

      <!-- *** ИЗМЕНЕНИЕ: Добавляем v-if="room" и блок v-else для скелетона *** -->
      <div v-if="room" class="mt-4 pb-3 border-b tg-border">
        <h1 class="font-bold tg-text text-lg  mb-2">Помещение</h1>
        <p>{{ room.title }}</p>
        <p v-if="room.center?.address">{{ room.center.address }}</p>
      </div>
      <!-- Показываем скелетон, пока room не загружен -->
      <div v-else class="mt-4 pb-3 border-b tg-border animate-pulse">
        <div class="h-6 w-1/3 rounded-lg tg-secondary-bg mb-2"></div>
        <div class="h-4 w-4/5 rounded-lg tg-secondary-bg"></div>
      </div>

      <div class="mt-4 pb-3 border-b tg-border">
        <h1 class="font-bold tg-text text-lg  mb-2">Ваша бронь</h1>
        <p>{{ formattedBookingPeriod }}</p>
      </div>
    </div>

    <div class="p-4 my-4 text-sm tg-text rounded-lg  tg-secondary-bg" role="alert">
      <span class="font-medium">Внимание!</span> Бронирование помещений бесплатно только для бесплатных
      и не коммерческих мероприятий.
    </div>


    <div
        class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50">
      <button
          @click="goNext"
          :disabled="loading"
          class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors disabled:opacity-75 disabled:cursor-wait"
      >
        <template v-if="loading">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>Отправка...</span>
        </template>
        <template v-else>
          <span class="truncate">Отправить запрос</span>
        </template>
      </button>
    </div>

  </AppPage>
</template>

<style scoped>

</style>