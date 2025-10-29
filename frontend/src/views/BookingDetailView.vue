<script setup lang="ts">
import AppPage from "@/components/AppPage.vue";
import {computed, onMounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {api, type ApiBooking} from "@/api";

const route = useRoute();

const router = useRouter();
const id = route.params.id as string;

const booking = ref<ApiBooking | null>(null);
const loading = ref(true);
const errorText = ref<string | null>(null);

const statusLabel: Record<string, string> =
    {PENDING: 'В ожидании', APPROVED: 'Одобрено', REJECTED: 'Отклонено', CANCELED: 'Отменено',};


const statusClass: Record<string, string> =
    {
      PENDING: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
      APPROVED: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
      REJECTED: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
      CANCELED: 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
    };


function formatRange(startIso: string, endIso: string) {
  const start = new Date(startIso);
  const end = new Date(endIso);
  const opts: Intl.DateTimeFormatOptions = {
    day: 'numeric',
    month: 'short',
    weekday: 'short',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC'
  };
  return `${start.toLocaleString('ru-RU', opts)} — ${end.toLocaleString('ru-RU', opts)}`;
}

const hasRoom = computed(() => !!booking.value?.room);
const roomTitle = computed(() => booking.value?.room?.title || 'Помещение');
const centerName = computed(() => booking.value?.room?.center?.name || null);

async function load() {
  loading.value = true;
  errorText.value = null;
  try {
    booking.value = await api.getBooking(id);
  } catch (e: any) {
    errorText.value = e?.message || 'Не удалось загрузить заявку';
  } finally {
    loading.value = false;
  }
}

function openRoom() {
  const roomId = booking.value?.room?.id;
  if (roomId) {
    router.push({name: 'room_detail', params: {id: roomId}});
  }
}

onMounted(load); </script>
<template>
  <AppPage title="Заявка"><span class="border-t mt-4 tg-border"></span>

    <!-- Загрузка -->
    <div v-if="loading" class="mt-6 animate-pulse">
      <div class="relative tg-secondary-bg rounded-2xl p-4 flex items-center space-x-4 overflow-hidden">
        <div class="w-16 h-16 rounded-xl tg-bg"></div>
        <div class="flex-grow flex flex-col space-y-2 min-w-0">
          <div class="h-5 w-3/4 rounded tg-bg"></div>
          <div class="h-4 w-1/2 rounded tg-bg"></div>
          <div class="h-4 w-2/3 rounded tg-bg"></div>
        </div>
      </div>
    </div>

    <!-- Ошибка -->
    <div v-else-if="errorText" class="text-center py-10">
      <p class="tg-text font-semibold">Не удалось открыть заявку</p>
      <p class="text-sm tg-hint mt-1">{{ errorText }}</p>
      <button @click="load" class="mt-4 tg-btn cursor-pointer font-bold rounded-full px-5 py-2">Повторить</button>
    </div>

    <!-- Контент -->
    <div v-else-if="booking" class="mt-6 mx-2 space-y-6">
      <!-- Детали помещения (если есть) -->
      <div v-if="hasRoom" class="pb-3 border-b tg-border">
        <h3 class="font-bold tg-text text-lg mb-2">Помещение</h3>
        <p class="tg-text">{{ booking.room?.title }}</p>
        <p v-if="booking.room?.center?.address" class="tg-hint text-sm mt-1">
          {{ booking.room.center.address }}
        </p>
      </div>

      <!-- Детали заявки -->
      <div class="pb-3 border-b tg-border">
        <h3 class="font-bold tg-text text-lg mb-2">Детали заявки</h3>
        <div class="grid grid-cols-1 gap-2 text-sm">
          <div><span class="tg-hint">Дата: </span><span
              class="truncate">{{ formatRange(booking.start_at, booking.end_at) }}</span></div>
          <div><span>Статус: </span>
            <span class="flex-shrink-0 text-xs font-semibold px-2 py-1 rounded-full"
                  :class="statusClass[booking.status]">
          {{ statusLabel[booking.status] || booking.status }}
        </span>
          </div>
          <div><span class="tg-hint">Заявитель:</span> <span class="tg-text">{{ booking.applicant_name }}</span></div>
          <div><span class="tg-hint">Телефон:</span> <span class="tg-text">{{ booking.applicant_phone }}</span></div>
          <div><span class="tg-hint">Мероприятие:</span> <span class="tg-text">{{ booking.event_name }}</span></div>
          <div><span class="tg-hint">Цель/тема:</span> <span class="tg-text">{{ booking.event_purpose }}</span></div>
          <div><span class="tg-hint">Аудитория:</span> <span class="tg-text">{{ booking.target_audience }}</span></div>
          <div><span class="tg-hint">Спикеры:</span> <span class="tg-text">{{ booking.invited_speakers }}</span></div>
          <div><span class="tg-hint">Оборудование:</span> <span class="tg-text">{{ booking.required_equipment }}</span>
          </div>
        </div>

        <div v-if="booking.status === 'REJECTED' && booking.rejection_reason" class="mt-3 text-sm">
          <span class="tg-hint">Причина отклонения:</span>
          <p class="tg-text mt-1">{{ booking.rejection_reason }}</p>
        </div>
      </div>

      <!-- Дата создания -->
      <div class="">
        <h3 class="font-bold tg-text text-lg mb-2">Служебная информация</h3>
        <p class="text-sm tg-hint">Создана: {{ new Date(booking.created_at).toLocaleString('ru-RU') }}</p>
      </div>
    </div>

    <!-- Кнопка открыть помещение -->
    <Transition name="slide-up">
      <div
          v-if="booking?.room?.id"
          class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50"
      >
        <button
            @click="openRoom"
            class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors"
        >
          <span class="truncate">Открыть помещение</span>
        </button>
      </div>
    </Transition>

  </AppPage>
</template>
<style scoped> .slide-up-enter-active, .slide-up-leave-active {
  transition: transform .3s ease;
}

.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(100%);
} </style>