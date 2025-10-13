<!-- src/App.vue -->
<script setup lang="ts">
import {RouterView, useRouter} from 'vue-router'
import {useTelegram} from '@/composables/useTelegram'
import {useEdgeSwipeBack} from '@/composables/useEdgeSwipeBack'
import {ref} from 'vue'

useTelegram()
useEdgeSwipeBack({
  minDx: 80,
  maxDy: 120,
  minVelocity: 0.5
})

const router = useRouter();
const transitionName = ref('fade');

router.beforeEach((to, from) => {
  const toDepth = to.meta.depth || 0;
  const fromDepth = from.meta.depth || 0;

  if (toDepth > fromDepth) {

    transitionName.value = 'slide-left';
  } else if (toDepth < fromDepth) {

    transitionName.value = 'slide-right';
  } else {

    transitionName.value = 'fade';
  }
});
</script>

<template>
  <RouterView v-slot="{ Component, route }">
    <Transition :name="transitionName" mode="out-in">
      <KeepAlive v-if="route.meta.keepAlive">
        <component :is="Component" :key="route.path"/>
      </KeepAlive>
      <component v-else :is="Component" :key="route.path"/>
    </Transition>
  </RouterView>
</template>

<style>
/* Стили для анимаций будут в main.css */
</style>