<script setup lang="ts">
import AppPage from "@/components/AppPage.vue"
import {useBookingStore} from "@/stores/booking.ts";
import {useRoute, useRouter} from "vue-router";
import {useRoomsStore} from "@/stores/rooms.ts";
import {computed, ref} from "vue";
import {api} from '@/api';
import ErrorComponent from "@/components/ErrorComponent.vue";

const route = useRoute()
const router = useRouter()
const roomsStore = useRoomsStore()
const bookingStore = useBookingStore()
const roomId = route.params.id as string

const room = computed(() => roomsStore.getRoomById(roomId))

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
  if (!bookingStore.payload)
    return loading.value = true

  errorText.value = null

  try {
    await api.createBooking(bookingStore.payload)
    router.replace({name: 'booking_success'})
  } catch (e: any) {
    errorText.value = 'Не удалось отправить заявку. Возможно помещение уже занято.' +
        ' Проверьте данные и попробуйте снова.'

    console.error(e)
  } finally {
    loading.value = false
  }
}

</script>

<template>
  <AppPage title="Подтверждение">
    <span class="border-t mt-4 tg-border"></span>

    <ErrorComponent v-if="errorText" class="mt-4" :error-text="errorText"/>

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