<script setup lang="ts">
import {useTelegramBackButton} from "@/composables/useTelegramBackButton.ts";
import {onMounted} from "vue";

const {showBackButton} = useTelegramBackButton()

const props = defineProps({
  title: String,
})

onMounted(() => {
  showBackButton()
})
</script>

<template>
  <section class="flex flex-col mx-4 mt-5 tg-text tg-bg">
    <div class="flex justify-between items-center">
      <h1 class="tg-text font-bold text-2xl">{{ props.title }}</h1>
      <img class="w-8 h-8 rounded-full" src="@/assets/images/logo.jpg" alt="Rounded avatar"/>
    </div>
    <slot></slot>
  </section>
</template>

<style scoped>

</style>