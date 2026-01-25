<script setup lang="ts">
// TODO: show a version of the prompt for each racer with a cool parralax effect
import { ref, watch, computed, onMounted, nextTick } from 'vue'
import { store } from '../store/store.ts'
import type { Racer } from '../App.vue';
import RaceTrackRacer from './RaceTrackRacer.vue';

const props = defineProps<{ racers: Racer[] }>()

const track = ref()
const trackWidth = ref(0)

onMounted(() => {
  trackWidth.value = track.value.getBoundingClientRect().width;
})
</script>

<template>
  <div class="flex">
    <div class="flex flex-col w-full" ref="track">
      <RaceTrackRacer
        v-for="(r, i) in racers"
        :key="r.sid"
        v-bind="{...r, trackWidth}"
      ></RaceTrackRacer>
    </div>

    <div id="finish-line" class="ml-auto checkered-flag"></div>
  </div>
</template>

<style scoped>
  #finish-line {
    width: 10%;
  }
</style>