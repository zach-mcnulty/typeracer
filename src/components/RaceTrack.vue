<script setup lang="ts">
// TODO: show a version of the prompt for each racer with a cool parralax effect
import { ref, watch, computed } from 'vue'
import { store } from '../store/store.ts'
import type { Racer } from '../App.vue';

const props = defineProps<{ racers: Racer[] }>()

const track = ref()
const trackWidth = ref(0)
const car = ref([])
const carWidth = ref(0)

const racersPixelsFromLeft = computed(() => {
  return props.racers.map(r => {
    return (trackWidth.value * ((r.progress ?? 0) / 100)) - (carWidth.value * ((r.progress ?? 0) / 100))
  })
})

watch(() => [track.value, car.value], ([track, car]) => {
  if (car.length > 0) {
    const img = car[0];

    img.onload = function() {
      const rect = img.getBoundingClientRect();
      carWidth.value = rect.width;

      trackWidth.value = track.getBoundingClientRect().width;
    };

    // Handle cases where the image might already be loaded (e.g., if cached)
    if (img.complete) {
      img.onload();
    }
  }
}, {immediate: true})
</script>

<template>
  <div class="flex">
    <div class="flex flex-col w-full" ref="track">
      <div class="relative border-b-2 w-full" v-for="(r, i) in racers" :key="r.sid">
        {{ r.username }}
        {{ store.socket.id == r.sid ? '(You)' : '' }}
        <img
          src="../assets/27186974_ca46_2u5r_220404.svg"
          style="height:50px; transform: scaleX(-1); position: relative;"
          :style="'left: ' + racersPixelsFromLeft[i] + 'px'"
          ref="car"
        >
      </div>
    </div>

    <div id="finish-line" class="ml-auto"></div>
  </div>
</template>

<style scoped>
#finish-line {
  background: repeating-conic-gradient(#fff 0 25%, #000 0 50%) 50% / 25px 25px;
  width: 10%;
}
</style>