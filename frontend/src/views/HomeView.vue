<script setup lang="ts">
import LogoComponent from "@/components/LogoComponent.vue";
import {useRouter} from "vue-router";


const router = useRouter()

const navigateTo = (route: string) => {
  router.push(route)
}
</script>

<template>
  <section class="flex flex-col h-auto h-screen pb-20 text-center items-center justify-center mx-4">
    <LogoComponent/>
    <p class="max-w-xs tg-text font-bold">
      Ваш проводник в мир возможностей
    </p>

    <div class="flex flex-col gap-4 mt-8">
      <button @click="navigateTo('/app/my_bookings')" type="button"
              class="tg-btn-invert-outline cursor-pointer font-bold rounded-full px-5 py-2">
        Мои бронирования
      </button>
      <button @click="navigateTo('/app/rooms')" type="button"
              class="tg-btn cursor-pointer font-bold rounded-full px-5 py-4">
        Забронировать помещение
      </button>
      <button @click="navigateTo('/app/event_list')" type="button"
              class="tg-btn-invert-outline cursor-pointer font-bold rounded-full px-5 py-2">
        Показать мероприятия
      </button>
      <button @click="navigateTo('/app/organizations')" type="button"
              class="tg-btn-invert-outline cursor-pointer font-bold rounded-full px-5 py-2">
        Список молодежных организации
      </button>
    </div>

    <span class="text-xs tg-hint mt-16">© Министерство молодежи КБР</span>
  </section>
</template>
