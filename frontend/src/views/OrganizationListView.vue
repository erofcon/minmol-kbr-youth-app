<script setup lang="ts">
import {computed, onMounted, ref} from "vue";
import AppPage from "@/components/AppPage.vue";
import {useOrganizationsStore} from "@/stores/organizations";
import SkeletonOrgCard from "@/components/skeletons/SkeletonOrgCard.vue";

const orgStore = useOrganizationsStore();
const searchQuery = ref('');
const selectedDistrictId = ref<string | null>(null);

onMounted(() => {
  if (orgStore.organizations.length === 0) {
    orgStore.fetchOrganizations();
  }
});

const districts = computed(() => orgStore.uniqueDistricts);

const filteredOrganizations = computed(() => {
  if (!orgStore.organizations) return [];

  return orgStore.organizations.filter(org => {
    const matchesDistrict = !selectedDistrictId.value || selectedDistrictId.value === org.district.id;

    const lowerCaseQuery = searchQuery.value.toLowerCase().trim();
    if (!lowerCaseQuery) {
      return matchesDistrict;
    }

    const matchesName = org.name.toLowerCase().includes(lowerCaseQuery);
    return matchesDistrict && matchesName;
  });
});

const selectDistrict = (id: string) => {
  selectedDistrictId.value = selectedDistrictId.value === id ? null : id;
};

</script>

<template>
  <AppPage title="Молодежные организации">
    <div v-if="orgStore.loading" class="mt-6">
      <div class="grid grid-cols-1 gap-6 my-6">
        <SkeletonOrgCard v-for="n in 4" :key="n"/>
      </div>
    </div>

    <div v-else-if="orgStore.error" class="text-center py-10 text-red-500">
      {{ orgStore.error }}
    </div>

    <div v-else>
      <div class="relative w-full mt-6">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск по названию..."
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
            v-for="district in districts"
            :key="district.id"
            @click="selectDistrict(district.id)"
            type="button"
            class="text-sm cursor-pointer font-bold rounded-full px-3 py-1.5 transition-colors"
            :class="selectedDistrictId === district.id ? 'tg-btn' : 'tg-secondary-bg'"
        >
          {{ district.name }}
        </button>
      </div>

      <div class="grid grid-cols-1 gap-4 my-6">
        <div v-for="org in filteredOrganizations" :key="org.id"
             class="relative tg-secondary-bg tg-text rounded-2xl p-4 flex items-center space-x-4 shadow-sm">
          <div class="flex-shrink-0">
            <img v-if="org.emblem" class="w-20 h-20 rounded-full object-cover" :src="org.emblem"
                 :alt="'Эмблема ' + org.name">
            <div v-else class="w-20 h-20 tg-bg rounded-full flex items-center justify-center">
              <svg class="h-10 w-10 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
                   stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21"/>
              </svg>
            </div>
          </div>
          <div class="flex-grow flex flex-col space-y-1 min-w-0">
            <h2 class="text-base font-bold truncate">{{ org.name }}</h2>
            <div class="flex items-center text-sm tg-hint">
              <svg class="h-4 w-4 mr-1.5 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"/>
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z"/>
              </svg>
              <span class="text-xs truncate">{{ org.district.name }}</span>
            </div>
            <div v-if="org.address" class="flex items-center text-sm tg-hint">
              <svg class="h-4 w-4 mr-1.5 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M2.25 12l8.954-8.955c.44-.439 1.152-.439 1.591 0L21.75 12M4.5 9.75v10.125c0 .621.504 1.125 1.125 1.125H9.75v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21h4.125c.621 0 1.125-.504 1.125-1.125V9.75M8.25 21h7.5"/>
              </svg>
              <span class="text-xs truncate">{{ org.address }}</span>
            </div>

            <div v-if="org.phone" class="flex items-center text-sm tg-hint">
              <svg class="h-4 w-4 mr-1.5 flex-shrink-0" xmlns="http://www.w3.org/2000/svg" fill="none"
                   viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 0 0 2.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 0 1-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 0 0-1.091-.852H4.5A2.25 2.25 0 0 0 2.25 4.5v2.25Z"/>
              </svg>
              <a :href="'tel:' + org.phone" class="text-xs truncate hover:underline">{{ org.phone }}</a>
            </div>

          </div>
        </div>
        <div v-if="filteredOrganizations.length === 0" class="text-center py-10">
          <p class="tg-text">Организации не найдены.</p>
          <p class="text-sm tg-hint">Попробуйте изменить поисковый запрос или фильтры.</p>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<style scoped>
.overflow-auto::-webkit-scrollbar {
  display: none;
}

.overflow-auto {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>