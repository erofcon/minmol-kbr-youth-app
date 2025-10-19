<script setup lang="ts"> import AppPage from "@/components/AppPage.vue";
import {computed, onMounted} from "vue";
import {useMyBookingsStore} from "@/stores/myBookings";
import SkeletonBookingCard from "@/components/skeletons/SkeletonBookingCard.vue";

const store = useMyBookingsStore();
onMounted(() => {
  if (store.items.length === 0) store.fetchFirst();
});
const statusLabel: Record<string, string> = {
  PENDING: 'В ожидании',
  APPROVED: 'Одобрено',
  REJECTED: 'Отклонено',
  CANCELED: 'Отменено',
};
const statusClass: Record<string, string> = {
  PENDING: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  APPROVED: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  REJECTED: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  CANCELED: 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
};

function formatRange(startIso: string, endIso: string) {
  const start = new Date(startIso);
  const end = new Date(endIso);
  const opts: Intl.DateTimeFormatOptions = {
    day: 'numeric', month: 'short', weekday: 'short', hour: '2-digit', minute: '2-digit', timeZone: 'UTC'
  }
  return `${start.toLocaleString('ru-RU', opts)} — ${end.toLocaleString('ru-RU', opts)}`;
}

const hasItems = computed(() => store.items.length > 0);
</script>

<template>
  <AppPage title="Мои бронирования" :class="{ 'pb-18': store.hasMore }">
    <span class="border-t mt-4 tg-border"></span>
    <!-- Загрузка -->
    <div v-if="store.loading" class="mt-6 grid grid-cols-1 gap-4">
      <SkeletonBookingCard v-for="n in 3" :key="n"/>
    </div>

    <!-- Ошибка -->
    <div v-else-if="store.error" class="text-center py-10">
      <p class="tg-text font-semibold">Не удалось загрузить ваши бронирования</p>
      <p class="text-sm tg-hint mt-1">{{ store.error }}</p>
      <button
          @click="store.fetchFirst"
          class="mt-4 tg-btn cursor-pointer font-bold rounded-full px-5 py-2"
      >
        Повторить
      </button>
    </div>

    <!-- Пусто -->
    <div v-else-if="!hasItems" class="text-center py-14">
      <p class="tg-text font-semibold">Заявок пока нет</p>
      <p class="text-sm tg-hint mt-1">Когда вы создадите бронирование, оно появится здесь.</p>
    </div>

    <!-- Список -->
    <div v-else class="mt-6 grid grid-cols-1 gap-4">
      <div
          v-for="b in store.items"
          :key="b.id"
          @click="$router.push({ name: 'booking_detail', params: { id: b.id } })"
          class="relative tg-secondary-bg rounded-2xl p-4 flex items-center space-x-4 overflow-hidden"
      >
        <div class="flex-shrink-0">
          <img
              v-if="b.room?.image"
              :src="b.room.image"
              alt=""
              class="w-16 h-16 rounded-xl object-cover"
          />
          <div v-else class="w-16 h-16 rounded-xl tg-bg flex items-center justify-center">
            <svg class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"
                 stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
          </div>
        </div>

        <div class="flex-grow min-w-0">
          <div class="flex items-center justify-between gap-2">
            <h2 class="font-bold truncate tg-text">
              {{ b.room?.title || 'Помещение' }}
            </h2>
            <span
                class="flex-shrink-0 text-xs font-semibold px-2 py-1 rounded-full"
                :class="statusClass[b.status]"
            >
          {{ statusLabel[b.status] || b.status }}
        </span>
          </div>

          <div class="mt-1 flex items-center text-sm tg-hint gap-2">
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
              <path
                  d="M19 3H5C3.897 3 3 3.897 3 5v14c0 1.103.897 2 2 2h14c1.103 0 2-.897 2-2V5c0-1.103-.897-2-2-2zm0 16H5V8h14v11z"/>
              <path d="M7 10h5v5H7z"/>
            </svg>
            <span class="truncate">{{ formatRange(b.start_at, b.end_at) }}</span>
          </div>

          <div v-if="b.room?.center?.name" class="mt-1 flex items-center text-sm tg-hint gap-2">
            <svg class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
              <path
                  d="M12 2C8.14 2 5 5.14 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.86-3.14-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5S10.62 6.5 12 6.5s2.5 1.12 2.5 2.5S13.38 11.5 12 11.5z"/>
            </svg>
            <span class="truncate">{{ b.room.center.name }}</span>
          </div>

          <div v-if="b.status === 'REJECTED' && b.rejection_reason" class="mt-2 text-xs tg-hint">
            <span class="font-semibold">Причина:</span> {{ b.rejection_reason }}
          </div>
        </div>
      </div>

      <div v-if="store.loadingMore" class="text-center tg-hint text-sm py-2">Загрузка…</div>
    </div>

    <Transition name="slide-up">
      <div v-if="store.hasMore" class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50">
        <button
            @click="store.fetchMore"
            class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors"
        >
          <span class="truncate">Загрузить ещё</span>
        </button>
      </div>
    </Transition>
  </AppPage>
</template>
<style scoped>
.slide-up-enter-active, .slide-up-leave-active {
  transition: transform .3s ease;
}

.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(100%);
} </style>