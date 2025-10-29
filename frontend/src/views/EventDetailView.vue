<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {useEventsStore} from "@/stores/events";
import AppPage from "@/components/AppPage.vue";
import SkeletonRoomDetail from "@/components/skeletons/SkeletonRoomDetail.vue";

const eventsStore = useEventsStore();
const route = useRoute();
const eventId = Number(route.params.id);

const event = computed(() => eventsStore.getEventById(eventId));
const loading = ref(false);

const formattedPeriod = computed(() => {
  if (!event.value) return '';
  const start = new Date(event.value.start);
  const end = new Date(event.value.end);
  const options: Intl.DateTimeFormatOptions = { year: 'numeric', month: 'long', day: 'numeric' };

  const startDateStr = start.toLocaleDateString('ru-RU', options);
  if (start.getTime() === end.getTime()) {
    return startDateStr;
  }
  const endDateStr = end.toLocaleDateString('ru-RU', options);
  return `${startDateStr} — ${endDateStr}`;
});

onMounted(async () => {
  if (!event.value) {
    loading.value = true;
    await eventsStore.fetchEventById(eventId);
    loading.value = false;
  }
});

const openEventOnMainSite = () => {
  if (event.value) {
    const eventUrl = `https://молод07.рф/event/${event.value.id}`;
    window.open(eventUrl, '_blank');
  }
}
</script>

<template>
  <AppPage title="Подробнее о мероприятии">
    <div v-if="loading || (!event && !eventsStore.error)">
      <SkeletonRoomDetail/>
    </div>

    <div v-else-if="eventsStore.error && !event" class="text-center py-10">
      <p class="tg-text font-semibold">Не удалось загрузить мероприятие</p>
      <p class="text-sm tg-hint mt-1">{{ eventsStore.error }}</p>
    </div>

    <div v-else-if="event" class="mt-8" :class="{ 'pb-24': event }">
      <div class="flex flex-col items-center justify-center">
        <img v-if="event.cover" class="w-full h-48 rounded-2xl object-cover mb-6" :src="event.cover"
             :alt="'Фото ' + event.title">
        <div v-else
             class="rounded-2xl h-48 w-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center mb-6">
          <svg class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-center tg-text">{{ event.title }}</h1>
      </div>

      <div class="mx-2 space-y-5 mt-8">
        <!-- *** ИЗМЕНЕНИЕ ЗДЕСЬ *** -->
        <div class="pb-3 border-b tg-border">
          <h2 class="font-bold tg-text text-lg">Описание</h2>
          <!-- Используем v-html для рендеринга HTML из API -->
          <!-- Классы prose стилизуют абзацы, отступы и т.д. -->
          <div class="mt-1 tg-text prose dark:prose-invert max-w-none" v-html="event.description"></div>
        </div>

        <div class="pb-3 border-b tg-border">
          <h2 class="font-bold tg-text text-lg">Даты проведения</h2>
          <p class="mt-1 tg-text">{{ formattedPeriod }}</p>
        </div>

        <div class="pb-3 border-b tg-border">
          <h2 class="font-bold tg-text text-lg">Место проведения</h2>
          <p class="mt-1 tg-text">{{ event.address }} ({{ event.settlement }})</p>
        </div>

        <div v-if="event.supervisor_name" class="pb-3 border-b tg-border">
          <h2 class="font-bold tg-text text-lg">Организатор</h2>
          <p class="mt-1 tg-text">{{ event.supervisor_name }} {{ event.supervisor_l_name }}</p>
          <a v-if="event.supervisor_phone" :href="'tel:'+event.supervisor_phone" class="tg-link">{{ event.supervisor_phone }}</a>
        </div>

        <div v-if="event.web || event.vk || event.telegram" class="pb-3">
          <h2 class="font-bold tg-text text-lg">Ссылки</h2>
          <div class="flex flex-col gap-1 mt-2">
            <a v-if="event.web" :href="event.web" target="_blank" class="tg-link">Сайт мероприятия</a>
            <a v-if="event.vk" :href="event.vk" target="_blank" class="tg-link">Группа ВКонтакте</a>
            <a v-if="event.telegram" :href="'https://t.me/' + event.telegram.replace('@','')" target="_blank" class="tg-link">
              Канал в Telegram
            </a>
          </div>
        </div>
      </div>

      <Transition name="slide-up">
        <div v-if="event"
             class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50">
          <button
              @click="openEventOnMainSite"
              class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors">
            <span class="truncate">Подать заявку на сайте</span>
          </button>
        </div>
      </Transition>
    </div>

  </AppPage>
</template>

<style scoped>
/* Стили для Tailwind Typography, чтобы они не конфликтовали с вашими */
:deep(.prose) {
  /* Сброс цвета, чтобы он наследовался от родителя (.tg-text) */
  color: inherit;
}
:deep(.prose a) {
  color: var(--tg-link-color);
}
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>