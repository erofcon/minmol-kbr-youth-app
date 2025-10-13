<script setup lang="ts">
import {computed, ref, watch} from "vue"
import type {HourRange} from "@/types";


const props = withDefaults(defineProps<{
  busyRanges?: HourRange[]
  workStart?: number
  workEnd?: number
  minStartHour?: number | null
}>(), {
  busyRanges: () => [],
  workStart: 9,
  workEnd: 18,
  minStartHour: null,
})

const emit = defineEmits(["update:time"])

const startTime = ref<number | null>(null)
const endTime = ref<number | null>(null)

const selectedPeriod = ref<'full' | 'first' | 'second' | null>(null)

function mergeRanges(ranges: HourRange[]): HourRange[] {

  if (ranges.length === 0) return []

  const s = ranges.slice().sort((a, b) => a.start - b.start)
  const out: HourRange[] = [s[0]]

  for (let i = 1; i < s.length; i++) {

    const last = out[out.length - 1], cur = s[i]
    if (cur.start <= last.end) last.end = Math.max(last.end, cur.end)
    else out.push({...cur})

  }

  return out
}

function invertToFree(ranges: HourRange[], start: number, end: number): HourRange[] {

  const merged = mergeRanges(ranges
      .map(r => ({start: Math.max(start, r.start), end: Math.min(end, r.end)}))
      .filter(r => r.end > r.start))

  const free: HourRange[] = []

  let cursor = start

  for (const r of merged) {
    if (r.start > cursor) free.push({start: cursor, end: r.start})
    cursor = Math.max(cursor, r.end)
  }
  if (cursor < end) free.push({start: cursor, end})

  return free
}

const freeRanges = computed(() =>
    invertToFree(props.busyRanges ?? [], props.workStart, props.workEnd))

const availableStartHours = computed<number[]>(() => {

  const out: number[] = []

  for (const r of freeRanges.value) {
    for (let h = r.start; h < r.end; h++) out.push(h)
  }

  const filtered = out.filter(h => h < props.workEnd)
  return props.minStartHour == null ? filtered : filtered.filter(h => h >= props.minStartHour!)

})

const availableEndHours = computed<number[]>(() => {

  if (startTime.value === null) return []

  const range = freeRanges.value.find(r => startTime.value! >= r.start && startTime.value! < r.end)

  if (!range) return []

  const out: number[] = []
  for (let h = startTime.value! + 1; h <= range.end; h++) out.push(h)

  return out
})

const periods = computed(() => ([
  {id: 'full' as const, label: 'Целый день', start: props.workStart, end: props.workEnd},
  {id: 'first' as const, label: 'Первая половина дня', start: props.workStart, end: 13},
  {id: 'second' as const, label: 'Вторая половина дня', start: 13, end: props.workEnd},
]))

const formatHour = (h: number) => `${String(h).padStart(2, "0")}:00`

const isPeriodAvailable = (p: { start: number; end: number }) => {

  if (props.minStartHour != null && p.start < props.minStartHour) return false

  return (props.busyRanges ?? []).every(b => p.end <= b.start || p.start >= b.end)
}

const selectPeriod = (pId: 'full' | 'first' | 'second', start: number, end: number) => {

  if (!isPeriodAvailable({start, end})) return

  if (selectedPeriod.value === pId) {

    selectedPeriod.value = null
    startTime.value = null
    endTime.value = null

  } else {
    selectedPeriod.value = pId
    startTime.value = start
    endTime.value = end

  }
}

const selectStart = (h: number) => {

  if (!availableStartHours.value.includes(h)) return

  selectedPeriod.value = null

  if (startTime.value === h) {

    startTime.value = null
    endTime.value = null
    return
  }

  startTime.value = h
  endTime.value = null
}

const selectEnd = (h: number) => {

  if (!availableEndHours.value.includes(h)) return
  selectedPeriod.value = null
  endTime.value = h

}

watch([startTime, endTime], () => {

  emit("update:time", {start: startTime.value, end: endTime.value})

})


watch(() => props.minStartHour, (minH) => {

  if (minH == null) return

  if (startTime.value != null && startTime.value < minH) {
    selectedPeriod.value = null
    startTime.value = null
    endTime.value = null
  }
})

</script>

<template>
  <div class="w-full mx-auto p-4 rounded-lg">
    <h2 class="text-lg font-bold tg-text mb-3">Выберите время</h2>

    <div class="flex gap-2 mt-2 overflow-auto w-full whitespace-nowrap">

      <button
          v-for="p in periods"
          :key="p.id"
          type="button"
          @click="selectPeriod(p.id, p.start, p.end)"
          class="text-sm cursor-pointer font-bold rounded-full px-4 py-2 transition-colors"
          :disabled="!isPeriodAvailable({start:p.start, end:p.end})"
          :class="[
          selectedPeriod === p.id ? 'tg-btn' : 'tg-secondary-bg',
          !isPeriodAvailable({start:p.start, end:p.end}) ? 'opacity-50 cursor-not-allowed' : ''
        ]"
      >
        {{ p.label }}
      </button>

    </div>

    <div class="mt-6">
      <h3 class="font-semibold tg-hint mb-3">Время начала</h3>
      <div class="grid grid-cols-4 sm:grid-cols-5 gap-2">
        <button
            v-for="h in availableStartHours"
            :key="`start-${h}`"
            type="button"
            @click="selectStart(h)"
            class="text-sm cursor-pointer font-medium rounded-lg p-2 transition-colors"
            :class="startTime === h ? 'tg-btn' : 'tg-secondary-bg'"
        >
          {{ formatHour(h) }}
        </button>
      </div>
      <p v-if="availableStartHours.length === 0" class="tg-hint text-sm mt-2">Нет доступных периодов для
        бронирования</p>
    </div>

    <div class="mt-6" v-if="startTime !== null">
      <h3 class="font-semibold tg-hint mb-3">Время окончания</h3>
      <div class="grid grid-cols-4 sm:grid-cols-5 gap-2">
        <button
            v-for="h in availableEndHours"
            :key="`end-${h}`"
            type="button"
            @click="selectEnd(h)"
            class="text-sm font-medium rounded-lg p-2 transition-colors"
            :class="endTime === h ? 'tg-btn' : 'tg-secondary-bg'"
        >
          {{ formatHour(h) }}
        </button>
      </div>
      <p v-if="availableEndHours.length === 0" class="tg-hint text-sm mt-2">Выберите другое время начала</p>
    </div>
  </div>
</template>