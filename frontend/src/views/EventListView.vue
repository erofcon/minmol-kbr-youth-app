<script setup lang="ts">

import AppPage from "@/components/AppPage.vue";

const events = [
  {
    id: 'wq2321eqwqweq',
    image: 'https://молод07.рф/storage/uploads/events1/cover/1h3kfYmlwJeFqpthqv8X2lQlMq7BQb43E5QBq3pb.jpg',
    title: 'В Нальчике пройдет КВН на кабардинском языке',
    description: 'Весёлое состязание молодежных команд состоится в Доме молодежи 19 сентября',
    location: 'Нальчик, пр. Кулиева, 12',
    period: '19.09.2025 — 19.09.2025'
  }
]

</script>

<template>
  <AppPage title="Мероприятия">
    <div class="relative w-full mt-6">
      <input
          type="text"
          v-model="searchQuery"
          placeholder="Поиск по названию ..."
          class="w-full rounded-full ps-5 pr-4 py-4 tg-secondary-bg tg-text text-sm focus:outline-none focus:ring-1 focus:ring-[var(--tg-button-color)]"
      />
      <span class="absolute inset-y-0 end-0 flex items-center pe-3">
          <svg class="w-4 h-4 tg-hint me-4" fill="none" viewBox="0 0 20 20"><path stroke="currentColor"
                                                                                  stroke-linecap="round"
                                                                                  stroke-linejoin="round"
                                                                                  stroke-width="2"
                                                                                  d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"/></svg>
        </span>

      <div class="grid grid-cols-1 gap-6 my-6">
        <div v-for="event in events" :key="event.id">
          <div
              class="relative tg-secondary-bg tg-text rounded-2xl p-4 flex
              items-center space-x-4 shadow-sm hover:shadow-md
              transition-all duration-300 cursor-pointer"
          >
            <div class="flex-shrink-0">
              <img v-if="event.image" class="w-28 h-28 md:w-32 md:h-32 object-cover rounded-xl"
                   :src="event.image"
                   :alt="'Фото ' + event.title">
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
              <h2 class="text-lg font-bold truncate">{{ event.title }}</h2>
              <div class="flex items-center text-sm">
                <svg class="h-5 w-5 mr-1.5" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960"
                     width="24px"
                     fill="currentColor">
                  <path
                      d="M480-480q33 0 56.5-23.5T560-560q0-33-23.5-56.5T480-640q-33 0-56.5 23.5T400-560q0 33 23.5 56.5T480-480Zm0 400Q319-217 239.5-334.5T160-552q0-150 96.5-239T480-880q127 0 223.5 89T800-552q0 100-79.5 217.5T480-80Z"/>
                </svg>
                <span class="text-xs">{{ event.location }}</span>
              </div>

              <div class="flex items-center text-sm mt-2">
                <svg class="h-5 w-5 mr-1.5" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960"
                     width="24px"
                     fill="currentColor">
                  <path
                      d="M320-400q-17 0-28.5-11.5T280-440q0-17 11.5-28.5T320-480q17 0 28.5 11.5T360-440q0 17-11.5 28.5T320-400Zm160 0q-17 0-28.5-11.5T440-440q0-17 11.5-28.5T480-480q17 0 28.5 11.5T520-440q0 17-11.5 28.5T480-400Zm160 0q-17 0-28.5-11.5T600-440q0-17 11.5-28.5T640-480q17 0 28.5 11.5T680-440q0 17-11.5 28.5T640-400ZM200-80q-33 0-56.5-23.5T120-160v-560q0-33 23.5-56.5T200-800h40v-80h80v80h320v-80h80v80h40q33 0 56.5 23.5T840-720v560q0 33-23.5 56.5T760-80H200Zm0-80h560v-400H200v400Z"/>
                </svg>
                <span class="text-xs">{{ event.period }}</span>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<style scoped>

</style>