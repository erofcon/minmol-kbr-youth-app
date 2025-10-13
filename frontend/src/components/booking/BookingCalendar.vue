<script setup lang="ts">
import {computed, ref} from "vue"

const props = defineProps<{
  modelValue: Date | null
  disabledDates?: string[] | Set<string>
  minDateKey?: string
}>()

const emit = defineEmits(["update:modelValue"])

const currentDate = ref(new Date());
const weekdays = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

const pad = (n: number) => String(n).padStart(2, "0")

const mskKey = (d: Date) =>
    new Intl.DateTimeFormat("en-CA", {
      timeZone: "Europe/Moscow",
      year: "numeric",
      month: "2-digit",
      day: "2-digit"
    }).format(d)

const disabledSet = computed(() => {

  if (!props.disabledDates) return new Set<string>()
  return Array.isArray(props.disabledDates) ? new Set(props.disabledDates) : props.disabledDates

})

const isSameDay = (a: Date, b: Date | null) =>
    !!b && a.getFullYear() === b.getFullYear()
    && a.getMonth() === b.getMonth() && a.getDate() === b.getDate()

const formattedCurrentMonth = computed(() => {

  const fmt = new Intl.DateTimeFormat("ru-RU", {month: "long", year: "numeric"})
  const s = fmt.format(currentDate.value)

  return s.charAt(0).toUpperCase() + s.slice(1)
});

const calendarGrid = computed(() => {

  const year = currentDate.value.getFullYear()

  const month = currentDate.value.getMonth()

  const first = new Date(year, month, 1)

  const last = new Date(year, month + 1, 0)

  const startDay = (first.getDay() + 6) % 7
  const daysInMonth = last.getDate()

  const cells: { date: Date; dayOfMonth: number; isCurrentMonth: boolean; disabled: boolean }[] = []

  const prevLast = new Date(year, month, 0).getDate()

  for (let i = startDay; i > 0; i--) {

    const d = new Date(year, month - 1, prevLast - i + 1)
    cells.push({date: d, dayOfMonth: d.getDate(), isCurrentMonth: false, disabled: true})

  }

  for (let day = 1; day <= daysInMonth; day++) {

    const d = new Date(year, month, day)
    const keyMsk = mskKey(d)
    const isBeforeMin = props.minDateKey ? keyMsk < props.minDateKey : false
    const disabled = disabledSet.value.has(keyMsk) || isBeforeMin
    cells.push({date: d, dayOfMonth: day, isCurrentMonth: true, disabled})

  }


  const remain = 42 - cells.length
  for (let day = 1; day <= remain; day++) {

    const d = new Date(year, month + 1, day)
    cells.push({date: d, dayOfMonth: day, isCurrentMonth: false, disabled: true})

  }

  return cells

})

const goToPreviousMonth = () =>
    currentDate.value = new Date(currentDate.value.getFullYear(),
        currentDate.value.getMonth() - 1, 1)

const goToNextMonth = () =>
    currentDate.value = new Date(currentDate.value.getFullYear(),
        currentDate.value.getMonth() + 1, 1)

const selectDate = (cell: { date: Date; isCurrentMonth: boolean; disabled: boolean }) => {

  if (!cell.isCurrentMonth || cell.disabled) return

  emit("update:modelValue", cell.date)
};

</script>

<template>

  <div class="w-full mx-auto p-4 rounded-lg">

    <div class="flex items-center justify-between pb-4">
      <button @click="goToPreviousMonth" class="p-2 cursor-pointer rounded-full tg-btn">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </button>
      <div class="flex items-center justify-center gap-2 text-xl font-bold tg-text">
        <span>{{ formattedCurrentMonth }}</span>
      </div>
      <button @click="goToNextMonth" class="p-2 cursor-pointer rounded-full tg-btn">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
        </svg>
      </button>
    </div>

    <div class="grid grid-cols-7 gap-1 text-center text-sm font-semibold tg-hint">
      <div v-for="w in weekdays" :key="w">{{ w }}</div>
    </div>

    <div class="grid grid-cols-7 gap-1 mt-2">
      <div v-for="(cell, i) in calendarGrid" :key="i" class="flex justify-center items-center">
        <button
            @click="selectDate(cell)"
            class="w-10 h-10 cursor-pointer flex items-center justify-center rounded-full transition-colors duration-200"
            :class="[
            !cell.isCurrentMonth ? 'text-gray-400 dark:text-gray-600 cursor-default'
                                 : (cell.disabled ? 'opacity-40 cursor-not-allowed pointer-events-none'
                                                  : 'tg-text hover:bg-blue-100 dark:hover:bg-gray-700'),
            isSameDay(cell.date, modelValue) ? 'tg-btn' : ''
          ]"
        >
          {{ cell.dayOfMonth }}
        </button>
      </div>
    </div>

    <div class="border-b tg-border mt-4"></div>
  </div>
</template>