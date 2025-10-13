<script setup lang="ts"> import {useTelegram} from '@/composables/useTelegram'
import {useBookingStore} from '@/stores/booking'
import {useRouter} from 'vue-router'
import {onMounted} from "vue";

const {isTelegramEnvironment, webApp} = useTelegram()
const booking = useBookingStore()
const router = useRouter()

function closeMiniApp() {
  if (isTelegramEnvironment()) {
    webApp.value?.close?.()
  } else {
    router.replace({name: 'home'})
  }
}

function goHome() {
  router.replace({name: 'home'})
}

onMounted(()=>{
  booking.resetAll()
})
</script>

<template>
  <section class="flex flex-col h-auto h-screen pb-20 text-center items-center justify-center mx-4">
    <img class="w-35 h-35 rounded-full" src="@/assets/images/logo.jpg" alt="Rounded avatar"/>

    <h1 class="text-2xl tg-text font-bold mt-8 mb-2">Спасибо за заявку!</h1>
    <h1 class="tg-text tg-hint">Мы уже передали её администратору.<br>
      Как только бронирование будет подтверждено или отклонено — пришлём вам уведомление.
    </h1>

    <div class="flex flex-col gap-4 mt-8">
      <button @click="closeMiniApp" type="button"
              class="tg-btn cursor-pointer font-bold rounded-full px-5 py-4">
        Закрыть
      </button>
      <button type="button"
              @click="goHome"
              class="tg-btn-invert-outline cursor-pointer font-bold rounded-full px-5 py-2">
        Выйти в главное меню
      </button>
    </div>
  </section>
</template>

<style scoped>

</style>