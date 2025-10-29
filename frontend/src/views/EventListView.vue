<script setup lang="ts">
import {onMounted, ref, watch} from "vue";
import {useRouter} from "vue-router";
import AppPage from "@/components/AppPage.vue";
import {useEventsStore} from "@/stores/events";
import SkeletonEventCard from "@/components/skeletons/SkeletonEventCard.vue";
import type {Event} from "@/types";
import EventCard from "@/components/events/EventCard.vue";
import {useDebounceFn} from '@vueuse/core';

const eventsStore = useEventsStore();
const router = useRouter();

const searchQuery = ref('');
const selectedEvent = ref<Event | null>(null);

// Загрузка данных при монтировании компонента
onMounted(() => {
  // Загружаем только если список пуст
  if (eventsStore.events.length === 0) {
    eventsStore.fetchFirstPage();
  }
});

// Функция для поиска с задержкой, чтобы не слать запросы на каждую букву
const debouncedSearch = useDebounceFn(() => {
  selectedEvent.value = null; // сбрасываем выбор при новом поиске
  eventsStore.fetchFirstPage(searchQuery.value);
}, 500); // задержка 500 мс

watch(searchQuery, debouncedSearch);


const selectEvent = (event: Event) => {
  selectedEvent.value = (selectedEvent.value?.id === event.id) ? null : event;
};

const navigateToDetail = () => {
  if (selectedEvent.value) {
    router.push(`/app/event/${selectedEvent.value.id}`);
  }
};

const loadMore = () => {
  eventsStore.fetchMoreEvents(searchQuery.value);
}

</script>

<template>
  <AppPage title="Мероприятия" :class="{ 'pb-40': selectedEvent || eventsStore.hasMore }">

    <div class="relative w-full mt-6">
      <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск по названию..."
          class="w-full rounded-full ps-5 pr-4 py-4 tg-secondary-bg tg-text text-sm focus:outline-none focus:ring-1 focus:ring-[var(--tg-button-color)]"
      />
      <span class="absolute inset-y-0 end-0 flex items-center pe-3">
          <svg class="w-4 h-4 tg-hint me-4" fill="none" viewBox="0 0 20 20"><path stroke="currentColor"
                                                                                  stroke-linecap="round"
                                                                                  stroke-linejoin="round"
                                                                                  stroke-width="2"
                                                                                  d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/></svg>
        </span>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="eventsStore.loading" class="mt-6">
      <div class="grid grid-cols-1 gap-6 my-6">
        <SkeletonEventCard v-for="n in 3" :key="`sk-${n}`"/>
      </div>
    </div>

    <!-- Состояние ошибки -->
    <div v-else-if="eventsStore.error && eventsStore.events.length === 0" class="text-center py-10">
      <p class="tg-text font-semibold">Произошла ошибка</p>
      <p class="text-sm tg-hint mt-1">{{ eventsStore.error }}</p>
      <button @click="eventsStore.fetchFirstPage(searchQuery)" class="mt-4 tg-btn cursor-pointer font-bold rounded-full px-5 py-2">
        Повторить
      </button>
    </div>

    <!-- Список мероприятий -->
    <div v-else>
      <div class="grid grid-cols-1 gap-6 my-6">
        <div v-for="event in eventsStore.events" :key="event.id" @click="selectEvent(event)">
          <EventCard :event="event" :is-selected="selectedEvent?.id === event.id" />
        </div>
      </div>

      <!-- Сообщение, если ничего не найдено -->
      <div v-if="eventsStore.events.length === 0" class="text-center py-10">
        <p class="tg-text">Мероприятия не найдены.</p>
        <p class="text-sm tg-hint">Попробуйте изменить поисковый запрос.</p>
      </div>

      <!-- Загрузка доп. данных -->
      <div v-if="eventsStore.loadingMore" class="text-center tg-hint text-sm py-2">
        Загрузка…
      </div>
    </div>

    <!-- Кнопки внизу экрана -->
    <div class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50 flex flex-col gap-2">
      <Transition name="slide-up">
        <button
            v-if="selectedEvent"
            @click="navigateToDetail"
            class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors">
          <span class="truncate">Подробнее о «{{ selectedEvent.title }}»</span>
        </button>
      </Transition>
      <Transition name="slide-up">
        <button
            v-if="eventsStore.hasMore && !eventsStore.loadingMore"
            @click="loadMore"
            :class="selectedEvent ? 'tg-btn-invert-outline py-2' : 'tg-btn py-3'"
            class="w-full cursor-pointer font-bold rounded-xl text-lg flex items-center justify-center transition-colors">
          <span class="truncate">Загрузить ещё</span>
        </button>
      </Transition>
    </div>

  </AppPage>
</template>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>