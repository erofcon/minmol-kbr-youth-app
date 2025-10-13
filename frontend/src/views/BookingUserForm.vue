<script setup lang="ts">
import AppPage from "@/components/AppPage.vue"
import {computed, onMounted, reactive, ref, watch} from "vue"
import {useRoute, useRouter} from "vue-router"
import {useBookingStore} from "@/stores/booking"

const initialized = ref(false)

const router = useRouter()
const bookingStore = useBookingStore()

const route = useRoute()

const roomId = route.params.id as string

const firstName = ref("")
const lastName = ref("")
const phoneDigits = ref("");
const eventName = ref("")
const purpose = ref("")
const audience = ref("")
const speakers = ref("")
const equipment = ref("")


const touched = reactive({
  firstName: false,
  lastName: false,
  phone: false,
  eventName: false,
  purpose: false,
  audience: false,
  speakers: false,
  equipment: false,
})

// валидации
const phoneRe = /^\+7\d{10}$/

const fullPhoneNumber = computed(() => {
  return phoneDigits.value ? `+7${phoneDigits.value}` : ""
})


const handlePhoneInput = (event: Event) => {
  const input = event.target as HTMLInputElement
  let value = input.value

  const digits = value.replace(/[^\d]/g, "");

  if (digits.startsWith('7') || digits.startsWith('8')) {
    phoneDigits.value = digits.substring(1, 11)
  } else {
    phoneDigits.value = digits.substring(0, 10)
  }

};

const errors = computed(() => ({
  firstName: firstName.value.trim() ? null : "Необходимо указать имя",
  lastName: lastName.value.trim() ? null : "Необходимо указать фамилию",
  phone: phoneRe.test(fullPhoneNumber.value) ? null : "Необходимо указать телефон в формате +7XXXXXXXXXX",
  eventName: eventName.value.trim() ? null : "Необходимо указать название мероприятия",
  purpose: purpose.value.trim() ? null : "Необходимо указать цель/тему",
  audience: audience.value.trim() ? null : "Необходимо указать целевую аудиторию и количество участников",
  speakers: speakers.value.trim() ? null : "Необходимо указать приглашенных спикеров",
  equipment: equipment.value.trim() ? null : "Необходимо указать заполнить список оборудования",
}))

const isValidForm = computed(() => Object.values(errors.value).every((e) => e === null))


const markTouched = (key: keyof typeof touched) => {
  touched[key] = true
}

const goNext = () => {
  if (!isValidForm.value) {
    Object.keys(touched).forEach((k) => (touched[k as keyof typeof touched] = true))
    return
  }


  bookingStore.applicant_name = `${firstName.value.trim()} ${lastName.value.trim()}`.replace(/\s+/g, " ").trim()
  bookingStore.applicant_phone = fullPhoneNumber.value
  bookingStore.event_name = eventName.value.trim()
  bookingStore.event_purpose = purpose.value.trim()
  bookingStore.target_audience = audience.value.trim()
  bookingStore.invited_speakers = speakers.value.trim()
  bookingStore.required_equipment = equipment.value.trim()

  router.push(`/app/booking/preview/${roomId}`)
}


function splitFullName(full: string) {
  const trimmed = (full || '').trim()
  if (!trimmed) return {first: '', last: ''}
  const parts = trimmed.split(/\s+/)
  return {first: parts[0] || '', last: parts.slice(1).join(' ')}
}

onMounted(() => {
  const {first, last} = splitFullName(bookingStore.applicant_name)
  if (!firstName.value) firstName.value = first
  if (!lastName.value) lastName.value = last

  if (!phoneDigits.value && bookingStore.applicant_phone) {
    const digits = bookingStore.applicant_phone.replace(/[^\d]/g, "")
    phoneDigits.value = digits.startsWith('7') ? digits.slice(1, 11) : digits.slice(0, 10)
  }

  eventName.value = bookingStore.event_name || ''
  purpose.value = bookingStore.event_purpose || ''
  audience.value = bookingStore.target_audience || ''
  speakers.value = bookingStore.invited_speakers || ''
  equipment.value = bookingStore.required_equipment || ''

  initialized.value = true
})

watch([firstName, lastName], ([f, l]) => {
  if (!initialized.value) return
  bookingStore.applicant_name = `${f} ${l}`.replace(/\s+/g, ' ').trim()
})

watch(phoneDigits, (d) => {
  if (!initialized.value) return
  bookingStore.applicant_phone = d ? `+7${d}` : ''
})

watch(eventName, (v) => {
  if (initialized.value) bookingStore.event_name = v
})
watch(purpose, (v) => {
  if (initialized.value) bookingStore.event_purpose = v
})
watch(audience, (v) => {
  if (initialized.value) bookingStore.target_audience = v
})
watch(speakers, (v) => {
  if (initialized.value) bookingStore.invited_speakers = v
})
watch(equipment, (v) => {
  if (initialized.value) bookingStore.required_equipment = v
})

</script>

<template>
  <AppPage title="Форма заявки" :class="{ 'pb-18': isValidForm }">
    <span class="border-t mt-4 tg-border"></span>

    <div class="flex flex-col mt-4 mx-2">
      <div class="mb-8">
        <label for="first_name" class="block mb-2 text-sm font-medium tg-text">Имя</label>
        <input
            type="text"
            id="first_name"
            v-model.trim="firstName"
            @blur="markTouched('firstName')"
            :class="[
            'w-full rounded-xl ps-5 pr-4 py-4 tg-secondary-bg tg-text text-sm focus:outline-none focus:ring-1',
            touched.firstName && errors.firstName ? 'ring-red-500' : 'focus:ring-[var(--tg-button-color)]'
          ]"
        />
        <p v-if="touched.firstName && errors.firstName" class="text-xs text-red-500 mt-1">{{ errors.firstName }}</p>

        <!-- Фамилия -->
        <label for="last_name" class="block mb-2 mt-4 text-sm font-medium tg-text">Фамилия</label>
        <input
            type="text"
            id="last_name"
            v-model.trim="lastName"
            @blur="markTouched('lastName')"
            :class="[
            'w-full rounded-xl ps-5 pr-4 py-4 tg-secondary-bg tg-text text-sm focus:outline-none focus:ring-1',
            touched.lastName && errors.lastName ? 'ring-red-500' : 'focus:ring-[var(--tg-button-color)]'
          ]"
        />
        <p v-if="touched.lastName && errors.lastName" class="text-xs text-red-500 mt-1">{{ errors.lastName }}</p>

        <!-- Телефон -->
        <label for="phone_number" class="block mb-2 mt-4 text-sm font-medium tg-text">Номер телефона</label>
        <div class="relative">
          <span class="absolute inset-y-0 left-0 flex items-center pl-5 text-sm tg-text">+7</span>
          <input
              type="tel"
              id="phone_number"
              :value="phoneDigits"
              @input="handlePhoneInput"
              inputmode="tel"
              placeholder="9674167114"
              maxlength="16"
              @blur="markTouched('phone')"
              :class="[
          'w-full rounded-xl pl-10 pr-4 py-4 tg-secondary-bg tg-text text-sm focus:outline-none focus:ring-1',
          touched.phone && errors.phone ? 'ring-red-500' : 'focus:ring-[var(--tg-button-color)]'
          ]"
          />
        </div>
        <p v-if="touched.phone && errors.phone" class="text-xs text-red-500 mt-1">{{ errors.phone }}</p>
        <!-- Название мероприятия -->
        <label for="event_name" class="block mb-2 mt-4 text-sm font-medium tg-text">Название мероприятия</label>
        <input
            type="text"
            id="event_name"
            v-model.trim="eventName"
            @blur="markTouched('eventName')"
            :class="[
            'w-full rounded-xl ps-5 pr-4 py-4 tg-secondary-bg tg-text text-sm focus:outline-none focus:ring-1',
            touched.eventName && errors.eventName ? 'ring-red-500' : 'focus:ring-[var(--tg-button-color)]'
          ]"
        />
        <p v-if="touched.eventName && errors.eventName" class="text-xs text-red-500 mt-1">{{ errors.eventName }}</p>

        <!-- Цель/тема -->
        <label for="purpose" class="block mb-2 mt-4 text-sm font-medium tg-text">Цель/тема</label>
        <textarea
            id="purpose"
            rows="3"
            v-model.trim="purpose"
            @blur="markTouched('purpose')"
            :class="[
            'block p-2.5 w-full resize-none h-20 text-sm tg-secondary-bg tg-text rounded-lg focus:outline-none focus:ring-1',
            touched.purpose && errors.purpose ? 'ring-red-500' : 'focus:ring-[var(--tg-button-color)]'
          ]"
        ></textarea>
        <p v-if="touched.purpose && errors.purpose" class="text-xs text-red-500 mt-1">{{ errors.purpose }}</p>

        <!-- Целевая аудитория -->
        <label for="audience" class="block mb-2 mt-4 text-sm font-medium tg-text">
          Целевая аудитория и предполагаемое количество участников
        </label>
        <textarea
            id="audience"
            rows="3"
            v-model.trim="audience"
            @blur="markTouched('audience')"
            :class="[
            'block p-2.5 w-full resize-none h-20 text-sm tg-secondary-bg tg-text rounded-lg focus:outline-none focus:ring-1',
            touched.audience && errors.audience ? 'ring-red-500' : 'focus:ring-[var(--tg-button-color)]'
          ]"
        ></textarea>
        <p v-if="touched.audience && errors.audience" class="text-xs text-red-500 mt-1">{{ errors.audience }}</p>

        <!-- Приглашенные спикеры -->
        <label for="speakers" class="block mb-2 mt-4 text-sm font-medium tg-text">Приглашенные спикеры</label>
        <textarea
            id="speakers"
            rows="3"
            v-model.trim="speakers"
            @blur="markTouched('speakers')"
            :class="[
            'block p-2.5 w-full resize-none h-20 text-sm tg-secondary-bg tg-text rounded-lg focus:outline-none focus:ring-1',
            touched.speakers && errors.speakers ? 'ring-red-500' : 'focus:ring-[var(--tg-button-color)]'
          ]"
        ></textarea>
        <p v-if="touched.speakers && errors.speakers" class="text-xs text-red-500 mt-1">{{ errors.speakers }}</p>

        <!-- Список оборудования -->
        <label for="equipment" class="block mb-2 mt-4 text-sm font-medium tg-text">Список необходимого
          оборудования</label>
        <textarea
            id="equipment"
            rows="3"
            v-model.trim="equipment"
            @blur="markTouched('equipment')"
            class=""
            :class="[
            'block p-2.5 w-full resize-none h-20 text-sm tg-secondary-bg tg-text rounded-lg focus:outline-none focus:ring-1',
            touched.equipment && errors.equipment ? 'ring-red-500' : 'focus:ring-[var(--tg-button-color)]'
          ]"
        ></textarea>
        <p v-if="touched.equipment && errors.equipment" class="text-xs text-red-500 mt-1">{{ errors.equipment }}</p>
      </div>
    </div>

    <!-- Кнопка появляется только при валидной форме -->
    <Transition name="slide-up">
      <div v-if="isValidForm"
           class="fixed bottom-0 left-0 right-0 p-4 tg-bg backdrop-blur-sm shadow-t-lg z-50">
        <button
            @click="goNext"
            class="w-full tg-btn cursor-pointer font-bold py-3 px-4 rounded-xl text-lg flex items-center justify-center transition-colors"
        >
          <span class="truncate">Продолжить</span>
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
}
</style>