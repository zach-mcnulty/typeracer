<script setup lang="ts">
// TODO: show a version of the prompt for each racer with a cool parralax effect
// TODO: wait a second after all racers are finished before switch race status  (so final racer can see their checkered flag)
import { ref, watch, computed, onMounted, nextTick } from 'vue'
import { store } from '../store/store.ts'
import type { Racer } from '../App.vue';

const props = defineProps<{ racers: Racer[] }>()

const track = ref()
const trackWidth = ref(0)
const cars = ref([])
const carWidth = ref(0)

const racersPixelsFromLeft = computed(() => {
  return props.racers.map(r => {
    return (trackWidth.value * ((r.progress ?? 0) / 100)) - (carWidth.value * ((r.progress ?? 0) / 100))
  })
})

const unwatch = watch(racersPixelsFromLeft, () => {
  if (cars.value.length && !carWidth.value) {
    const img = cars.value[0] as HTMLImageElement;
    carWidth.value = img.getBoundingClientRect().width;
    carWidth.value && unwatch();
  }
})

onMounted(() => {
  trackWidth.value = track.value.getBoundingClientRect().width;
})
</script>

<template>
  <div class="flex">
    <div class="flex flex-col w-full" ref="track">
      <div
        class="relative border-b-2 w-full"
        v-for="(r, i) in racers"
        :key="r.sid"
      >
        {{ r.username }}
        {{ store.socket.id == r.sid ? '(You)' : '' }}
        <img
          src="../assets/27186974_ca46_2u5r_220404.svg"
          style="height: 50px; transform: scaleX(-1); position: relative;z-index: 1;"
          :style="'left: ' + racersPixelsFromLeft[i] + 'px'"
          ref="cars"
        >

        <div class="checkered-flag absolute h-full right-0 top-0" :class="{
          'w-0': (r?.progress || 0) < 100,
          'w-full': r?.progress == 100
        }"></div>

      </div>
    </div>

    <div id="finish-line" class="ml-auto checkered-flag"></div>
  </div>
</template>

<style scoped>
  .checkered-flag {
    background: repeating-conic-gradient(#fff 0 25%, #000 0 50%) 50% / 25px 25px;
    transition: width 0.2s;
  }

  #finish-line {
    width: 10%;
  }
</style>