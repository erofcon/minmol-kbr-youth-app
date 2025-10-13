<script setup lang="ts">
import {RouterView} from 'vue-router'
import {useTelegram} from '@/composables/useTelegram'
import {useEdgeSwipeBack} from '@/composables/useEdgeSwipeBack'

useTelegram()
useEdgeSwipeBack({
  minDx: 80,       // Минимальная дистанция
  maxDy: 120,      // Макс отклонение по Y
  minVelocity: 0.5 // Минимальная скорость (px/ms)
})
</script>

<template>
  <RouterView v-slot="{ Component, route }">
    <KeepAlive v-if="route.meta.keepAlive">
      <component :is="Component" :key="route.path"/>
    </KeepAlive>
    <component v-else :is="Component" :key="route.path"/>
  </RouterView>

</template>