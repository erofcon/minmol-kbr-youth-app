<script setup lang="ts">
import AppPage from "@/components/AppPage.vue"
import {computed, onMounted, ref} from "vue"
import type {Room} from "@/types"
import {useRoomsStore} from "@/stores/rooms"
import SkeletonRoomCard from "@/components/skeletons/SkeletonRoomCard.vue"
import router from "@/router";

const roomsStore = useRoomsStore()

const selectedCenterId = ref<string | null>(null)
const selectedRoom = ref<Room | null>(null)
const searchQuery = ref('')


onMounted(() => {
  roomsStore.fetchRooms()
});

const centers = computed(() => roomsStore.uniqueCenters)
const allRooms = computed(() => roomsStore.rooms)


const filteredRooms = computed(() => {
  if (!allRooms.value) return []

  const lowerCaseQuery = searchQuery.value.toLowerCase().trim()

  return allRooms.value.filter(room => {

    const matchesCenter = selectedCenterId.value === null || selectedCenterId.value === room.center.id
    if (!lowerCaseQuery) {
      return matchesCenter
    }
    const matchesTitle = room.title.toLowerCase().includes(lowerCaseQuery)
    const matchesTag = room.tags.some(tag =>
        tag.name.toLowerCase().includes(lowerCaseQuery)
    );
    return matchesCenter && (matchesTitle || matchesTag)
  })
})

const selectCenter = (id: string) => {
  if (selectedCenterId.value === id) {
    selectedCenterId.value = null
  } else {
    selectedCenterId.value = id
  }
}

const selectRoom = (room: Room) => {
  if (selectedRoom.value?.id === room.id) {
    selectedRoom.value = null
  } else {
    selectedRoom.value = room
  }
}

const navigateTo = (route: string) => {
  router.push(route)
}
</script>

<template>
  <AppPage title="Выбор помещения" :class="{ 'pb-18': selectedRoom }">

    <div v-if="roomsStore.loading">
      <div class="grid grid-cols-1 gap-6 my-6">
        <SkeletonRoomCard v-for="n in 3" :key="n"/>
      </div>
    </div>

    <div v-else-if="roomsStore.error" class="text-center py-10 text-red-500">
      {{ roomsStore.error }}
    </div>


    <div v-else>
      <div class="relative w-full mt-6">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск по названию или тегу..."
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

      <div class="flex gap-2 mt-4 overflow-auto w-full whitespace-nowrap">
        <button
            v-for="center in centers"
            :key="center.id"
            @click="selectCenter(center.id)"
            type="button"
            class="text-sm cursor-pointer font-bold rounded-full px-2 py-1"
            :class="selectedCenterId === center.id ? 'tg-btn' : 'tg-secondary-bg'"
        >
          {{ center.name }}
        </button>
      </div>

      <div class="grid grid-cols-1 gap-6 my-6">
        <div v-for="room in filteredRooms" :key="room.id">
          <div
              @click="selectRoom(room)"
              class="relative tg-secondary-bg tg-text rounded-2xl p-4 flex items-center space-x-4 shadow-sm hover:shadow-md transition-all duration-300 cursor-pointer"
              :class="{'ring-2 ring-blue-400 tg-btn shadow-lg': selectedRoom?.id === room.id }"
          >
            <div class="flex-shrink-0">
              <img v-if="room.image" class="w-28 h-28 md:w-32 md:h-32 object-cover rounded-xl" :src="room.image"
                   :alt="'Фото ' + room.title">
              <div v-else
                   class="w-28 h-28 md:w-32 md:h-32 bg-gray-200 dark:bg-gray-700 rounded-xl flex items-center justify-center">
                <svg class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                     stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round"
                        d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
            </div>
            <div class="flex-grow flex flex-col space-y-1.5 min-w-0">
              <h2 class="text-lg font-bold truncate">{{ room.title }}</h2>
              <div class="flex items-center text-sm">
                <svg class="h-4 w-4 mr-1.5" viewBox="0 0 20 20" fill="currentColor">
                  <path
                      d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
                </svg>
                <span>До {{ room.capacity }} человек</span>
              </div>
              <div class="flex flex-wrap gap-2 pt-1">
                <span v-for="tag in room.tags.slice(0, 3)" :key="tag.id"
                      class="bg-blue-50 text-blue-800 dark:bg-blue-900 dark:text-blue-300 text-xs font-medium px-2.5 py-0.5 rounded-full">{{
                    tag.name
                  }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-if="filteredRooms.length === 0" class="text-center py-10">
          <p class="tg-text">Помещения не найдены.</p>
          <p class="text-sm tg-hint">Попробуйте изменить поисковый запрос или фильтры.</p>
        </div>
      </div>
    </div>


    <Transition name="slide-up">
      <div v-if="selectedRoom"
           class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50">
        <button
            @click="navigateTo(`/app/room/${selectedRoom.id}`)"
            class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors">
          <span class="truncate">Забронировать «{{ selectedRoom.title }}»</span>
        </button>
      </div>
    </Transition>

  </AppPage>
</template>

<style scoped>
/* Стили для скрытия скроллбара у фильтров */
.overflow-x-auto::-webkit-scrollbar {
  display: none;
}

.overflow-x-auto {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* НОВЫЕ СТИЛИ: Анимация для появления кнопки */
.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}

</style>