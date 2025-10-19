<script setup lang="ts">
defineProps({
  errorText: String
})
</script>

<template>
    <div class="p-4 mb-4 text-sm tg-hint rounded-lg tg-secondary-bg" role="alert">
      <span class="tg-text font-bold">Произошла ошибка!</span>
      {{ errorText }}
    </div>

</template>

<style scoped>

</style>