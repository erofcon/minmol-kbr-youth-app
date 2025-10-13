<!-- src/views/EventDetailView.vue -->
<script setup lang="ts">
import {computed, onMounted} from "vue";
import {useRoute} from "vue-router";
import {useEventsStore} from "@/stores/events";
import AppPage from "@/components/AppPage.vue";
import SkeletonRoomDetail from "@/components/skeletons/SkeletonRoomDetail.vue";

const eventsStore = useEventsStore();
const route = useRoute();
const eventId = route.params.id as string;

const event = computed(() => eventsStore.getEventById(eventId));

onMounted(() => {
  if (eventsStore.events.length === 0) {
    eventsStore.fetchEvents();
  }
});

</script>

<template>
  <AppPage title="Подробнее о мероприятии">
    <div v-if="event" class="mt-8">
      <div class="flex flex-col items-center justify-center">
        <img v-if="event.image" class="w-full h-48 rounded-2xl object-cover mb-6" :src="event.image"
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

      <div class="mx-2">
        <div class="mt-8 pb-3 border-b tg-border">
          <h2 class="font-bold tg-text text-lg">Описание</h2>
          <p class="mt-1 tg-text whitespace-pre-wrap">{{ event.description }}</p>
        </div>

        <div class="mt-4 pb-3 border-b tg-border">
          <h2 class="font-bold tg-text text-lg">Место проведения</h2>
          <p class="mt-1 tg-text">{{ event.location }}</p>
        </div>

        <div class="mt-4 pb-3 mb-4 border-b tg-border">
          <h2 class="font-bold tg-text text-lg">Даты</h2>
          <p class="mt-1 tg-text">{{ event.period }}</p>
        </div>
      </div>

      <div
          class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50">
        <button
            class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors">
          <span class="truncate">Подать заявку</span>
        </button>
      </div>
    </div>
    <div v-else>
      <SkeletonRoomDetail/>
    </div>
  </AppPage>
</template>

<style scoped>
</style>