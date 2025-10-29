<script setup lang="ts">
import AppPage from "@/components/AppPage.vue"
import {useRoute, useRouter} from "vue-router"
import {useRoomsStore} from "@/stores/rooms"
import {computed, onMounted, ref, watch} from "vue"
import BookingCalendar from "@/components/booking/BookingCalendar.vue"
import TimeSlotPicker from "@/components/booking/TimeSlotPicker.vue"
import {useBookingStore} from "@/stores/booking"
import {api} from '@/api';


type ApiInterval = {
  start_at: string
  end_at: string
}


type HourRange = {
  start: number
  end: number
}

const route = useRoute()
const router = useRouter()
const roomsStore = useRoomsStore()
const bookingStore = useBookingStore()

const roomId = route.params.id as string
const room = computed(() => roomsStore.getRoomById(roomId))

const WORK_START = 9
const WORK_END = 18

const selectedDate = ref<Date | null>(null)
const selectedTime = ref<{
  start: number | null
  end: number | null
}>({start: null, end: null})

const busyByDate = ref<Map<string, HourRange[]>>(new Map())
const fullyBookedDates = ref<Set<string>>(new Set())

const pad = (n: number) => String(n).padStart(2, "0")

// YYYY-MM-DD в зоне Europe/Moscow
const mskDateKey = (d: Date) =>
    new Intl.DateTimeFormat("en-CA", {
      timeZone: "Europe/Moscow",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    }).format(d)

// HH:MM в зоне Europe/Moscow
const mskHHMM = () =>
    new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/Moscow",
      hour: "2-digit",
      minute: "2-digit",
      hour12: false
    }).format(new Date())

const todayKeyMsk = computed(() => mskDateKey(new Date()))
const dateKeyFromDate = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

// парсим ISO как МСК (игнорируем Z)
function parseIsoAsMsk(iso: string) {
  const m = iso.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,3})?)?Z$/);
  if (!m) throw new Error(`Bad ISO: ${iso}`);
  const [_, ys, ms, ds, hs, mins, secs] = m;
  return {year: +ys, month: +ms, day: +ds, hour: +hs, minute: +mins, second: +(secs ?? 0)};
}

function mergeRanges(ranges: HourRange[]): HourRange[] {
  if (ranges.length === 0) return [];
  const s = ranges.slice().sort((a, b) => a.start - b.start);
  const out: HourRange[] = [s[0]];
  for (let i = 1; i < s.length; i++) {
    const last = out[out.length - 1], cur = s[i];
    if (cur.start <= last.end) last.end = Math.max(last.end, cur.end);
    else out.push({...cur});
  }
  return out;
}

function isFullyBooked(ranges: HourRange[]): boolean {
  const merged = mergeRanges(ranges);
  let cursor = WORK_START;
  for (const r of merged) {
    if (r.start > cursor) return false;
    cursor = Math.max(cursor, r.end);
  }
  return cursor >= WORK_END;
}

async function fetchBusyIntervals(roomId: string): Promise<ApiInterval[]> {
  return await api.getRoomBusy(roomId);
}

function processBusy(api: ApiInterval[]) {
  const tmp = new Map<string, HourRange[]>()

  for (const item of api) {
    const s = parseIsoAsMsk(item.start_at)
    const e = parseIsoAsMsk(item.end_at)
    const key = `${s.year}-${pad(s.month)}-${pad(s.day)}`

    let startHour = s.hour
    let endHour = e.hour

    if (s.minute > 0 || s.second > 0) startHour = Math.floor(startHour)
    if (e.minute > 0 || e.second > 0) endHour = Math.ceil(endHour)

    const clamped = {start: Math.max(WORK_START, startHour), end: Math.min(WORK_END, endHour)}

    if (clamped.end <= clamped.start) continue

    if (!tmp.has(key)) tmp.set(key, [])

    tmp.get(key)!.push(clamped);
  }

  const full = new Set<string>()
  const map = new Map<string, HourRange[]>()

  for (const [key, arr] of tmp.entries()) {

    const merged = mergeRanges(arr)
    if (isFullyBooked(merged)) full.add(key); else map.set(key, merged)

  }

  busyByDate.value = map
  fullyBookedDates.value = full
}

onMounted(async () => {
  if (roomsStore.rooms.length === 0)
    await roomsStore.fetchRooms()
  bookingStore.setRoom(roomId)
  const apiData = await fetchBusyIntervals(roomId)
  processBusy(apiData)

});

const minDateKey = todayKeyMsk


const minStartHourForSelected = computed<number | null>(() => {

  if (!selectedDate.value) return null

  const selectedKeyMsk =
      new Intl.DateTimeFormat("en-CA", {
        timeZone: "Europe/Moscow",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      }).format(selectedDate.value)

  const todayKeyMsk =
      new Intl.DateTimeFormat("en-CA", {
        timeZone: "Europe/Moscow",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
      }).format(new Date())

  if (selectedKeyMsk !== todayKeyMsk) return null

  const nowHHMM = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Moscow",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(new Date())

  const [hhStr, mmStr] = nowHHMM.split(":")
  const hh = +hhStr
  const mm = +mmStr


  const earliestRaw = hh + 1 + (mm > 0 ? 1 : 0)

  if (earliestRaw >= WORK_END) return WORK_END

  return Math.max(WORK_START, earliestRaw);
});

const disabledDates = computed(() => Array.from(fullyBookedDates.value))

const selectedDateKey = computed(
    () => (selectedDate.value ? dateKeyFromDate(selectedDate.value) : null)
)

const busyRangesForSelected = computed<HourRange[]>(() => {
  if (!selectedDateKey.value) return []
  return busyByDate.value.get(mskDateKey(selectedDate.value!)) ?? []
})


watch(selectedDate, () => {
  selectedTime.value = {start: null, end: null}
})


watch([selectedDate, () => fullyBookedDates.value], () => {
  if (!selectedDate.value) return

  const key = mskDateKey(selectedDate.value)

  if (fullyBookedDates.value.has(key) || key < todayKeyMsk.value) {
    selectedDate.value = null
    bookingStore.clearPeriod()

  }
})


const bookingPeriod = computed(() => {

  if (!selectedDate.value || selectedTime.value.start === null
      || selectedTime.value.end === null)

    return null

  bookingStore.setPeriodFromMsk(selectedDate.value, selectedTime.value.start, selectedTime.value.end)

  return {start_at: bookingStore.start_at!, end_at: bookingStore.end_at!}
});

const canContinue = computed(() => !!bookingPeriod.value && !!room.value)

const goNext = () => router.push(`/app/booking/information/${room.value!.id}`)

</script>

<template>
  <AppPage title="Дата и время" :class="{ 'pb-18': canContinue }">
    <span class="border-t mt-4 tg-border"></span>

    <BookingCalendar
        v-model="selectedDate"
        :disabled-dates="disabledDates"
        :min-date-key="minDateKey"
    />

    <Transition name="fade">
      <div v-if="selectedDate">
        <TimeSlotPicker
            :busy-ranges="busyRangesForSelected"
            :work-start="9"
            :work-end="18"
            :min-start-hour="minStartHourForSelected"
            @update:time="selectedTime = $event"
        />
      </div>
    </Transition>

    <Transition name="slide-up">
      <div v-if="canContinue"
           class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50">
        <button
            @click="goNext"
            class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors">
          <span class="truncate">Продолжить</span>
        </button>
      </div>
    </Transition>
  </AppPage>
</template>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .25s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-up-enter-active, .slide-up-leave-active {
  transition: transform .3s ease;
}

.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(100%);
}
</style>