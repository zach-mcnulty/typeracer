<script setup lang="ts">
import {ref, watch, computed} from 'vue';
import type { Racer } from "../App.vue";
import { store } from '../store/store.ts'
import trumpMobile from '../assets/basic-orange.svg';
import avocadoGreen from '../assets/basic-lightgreen.svg';

interface RaceTrackRacerProps extends Racer {
  trackWidth: number
}

const props = defineProps<RaceTrackRacerProps>();

const car = ref<HTMLImageElement>();
const carWidth = ref(0);

const racersPixelsFromLeft = computed(() => {
  return (props.trackWidth * ((props.progress ?? 0) / 100)) - (carWidth.value * ((props.progress ?? 0) / 100))
})

const unwatch = watch(racersPixelsFromLeft, () => {
  if (car.value && !carWidth.value) {
    const img = car.value as HTMLImageElement;
    carWidth.value = img.getBoundingClientRect().width;
    carWidth.value && unwatch();
  }
})

const animateError = ref(false);
watch(() => props.errors, (cur, prev) => {
  if ((props.errors ?? 0) > 0) {
    animateError.value = true;
    setTimeout(()=>animateError.value = false, 500);
  }
})

const carImage = ref(trumpMobile)

// TODO: don't do this (have the server assign hex colors and let users get a new random color)
if (
  (localStorage.getItem('name') == 'Ryan' && props.sid == store.socket.id)
  || (localStorage.getItem('name') == 'Zach' && props.sid != store.socket.id)
) {
  carImage.value = avocadoGreen
}
</script>

<template>
  <div
    class="relative border-b-2 w-full"
    :class="{
      'bg-blue-200 dark:bg-blue-800': sid == store.socket.id,
      'bg-red-200': animateError
    }"
  >
    {{ username }}
    {{ store.socket.id == sid ? '(You)' : '' }}
    <img
      :src="carImage"
      :class="{spin: animateError}"
      :style="'left: ' + racersPixelsFromLeft + 'px'"
      style="height: 50px; position: relative; z-index: 1;"
      ref="car"
    >

    <div class="checkered-flag absolute h-full right-0 top-0" :class="{
      'w-0': (progress || 0) < 100,
      'w-full': progress == 100
    }"></div>

  </div>
</template>

<style scoped>
  .spin {
    animation: spin-once 0.5s linear;
  }

  @keyframes spin-once {
    0% {
      transform: rotate(0deg) scale(1);
    }
    50% {
      transform: rotate(180deg) scale(1.5);
    }
    100% {
      transform: rotate(360deg) scale(1);
    }
  }
</style>