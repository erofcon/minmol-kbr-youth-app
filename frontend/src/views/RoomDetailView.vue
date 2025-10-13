<script setup lang="ts">
import AppPage from "@/components/AppPage.vue";
import {useRoute} from "vue-router"
import {useRoomsStore} from "@/stores/rooms.ts";
import {computed, onMounted} from "vue";
import SkeletonRoomDetail from "@/components/skeletons/SkeletonRoomDetail.vue";
import router from "@/router";

const roomsStore = useRoomsStore()
const route = useRoute();

const roomId = route.params.id as string;

const room = computed(() => roomsStore.getRoomById(roomId));

onMounted(() => {
  if (roomsStore.rooms.length === 0) {
    roomsStore.fetchRooms();
  }
});

const navigateTo = (route: string) => {
  router.push(route)
}

</script>

<template>
  <AppPage title="Подробнее">
    <div v-if="room" class="mt-8">
      <div class="flex flex-col items-center justify-center">
        <img v-if="room.image" class="w-32 h-32 rounded-full object-cover" :src="room.image"
             :alt="'Фото ' + room.title">
        <div v-else
             class="rounded-full h-32 w-32 bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
          <svg class="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round"
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold mt-4 tg-text">{{ room.title }}</h1>
        <h1 class="font-bold mt-4 tg-text">{{ room.center.name }}</h1>
        <button
            @click="navigateTo(`/app/booking/${roomId}`)"
            type="button"
            class="tg-btn cursor-pointer mt-4 font-bold text-lg max-w-sm rounded-full w-full px-5 py-3">
          Забронировать помещение
        </button>
      </div>

      <div class="mx-4">
        <div class="mt-8 pb-3 border-b tg-border">
          <h1 class="font-bold tg-text ">Описание</h1>
          <p>{{ room.description }}</p>
        </div>

        <div class="mt-4 pb-3 border-b tg-border">
          <h1 class="font-bold tg-text ">Оснащение</h1>
          <ul class="mx-4">
            <li v-for="tag in room.tags" :key="tag.id">
              {{ tag.name }}
            </li>
          </ul>
        </div>

        <div class="mt-4 pb-3 border-b tg-border">
          <h1 class="font-bold tg-text ">Вместимость</h1>
          <p>До {{ room.capacity }} человек</p>
        </div>

        <div class="mt-4 pb-3 mb-4 border-b tg-border">
          <h1 class="font-bold tg-text ">Адрес</h1>
          <p>г. Нальчик, ул. Кулиева 2</p>
        </div>
      </div>
    </div>
    <div v-else>
      <SkeletonRoomDetail/>
    </div>
  </AppPage>
</template>

<style scoped>
li {
  list-style-type: circle;
}
</style>