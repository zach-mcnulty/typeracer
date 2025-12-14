<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { store } from "../store/store"
import Gauge from "./Gauge.vue";


// TODO: Improve jankiness (speedometer freaks out at the start)
// Add numbers to the ticks

const props = defineProps<{
  numAllTypedEntries: number
  superDuperPauserOfDoom: boolean
}>()

let currentTimeInterval: NodeJS.Timeout | undefined;
const currentTime = ref(0)

onMounted(() => {
  currentTimeInterval = setInterval(() => {
    currentTime.value = new Date().getTime()
  }, 500)
})

onUnmounted(() => {
  clearInterval(currentTimeInterval)
})

const speed = computed<number>(() => {
  if (
    typeof store.clientStartTime == 'number'
    && currentTime.value - store.clientStartTime > 1000 // currentTime only updates in an interval, so wait a second so the initial speed is somewhat reasonable
  ) {
    const seconds = (currentTime.value - store.clientStartTime) / 1000;
    const minutes = seconds / 60;
    return (props.numAllTypedEntries / 5) / minutes;
  }

  return 0
})

const ticks = new Array(6 * 3 + 8);
const needleRotate = computed(() => speed.value / 0.54 - 110)

watch(() => props.superDuperPauserOfDoom, (bool) => {
  if (bool) {
    clearInterval(currentTimeInterval)
    store.socket.emit("update_racer_wpm", speed.value)
    store.socket.emit("update_racer_duration", new Date().getTime() - store.clientStartTime)
  }
})
</script>

<template>
  <Gauge
    :value="speed"
  ></Gauge>
</template>

<style scoped>
.gauge {
  width: 100%;
  aspect-ratio: 1;
  background:green;
  border-radius: 50%;
  position: relative;
  clip-path: rect(0% 100% 75% 0%)
}

.inner-gauge {
  width: 94%;
  aspect-ratio: 1;
  background:white;
  border-radius: 50%;
  position: relative;
  left: 3%;
  top: 3%;
  clip-path: rect(0% 100% 73.5% 0%)
}

.tick-wrapper {
  width: 94%;
  aspect-ratio: 1;
  background:lightgray;
  border-radius: 50%;
  font-family: 'Courier New', Courier, monospace;
  color: black;
  font-size: 1.5rem;
  position: relative;
  left: 3%;
  top: 3%;
  clip-path: rect(0% 100% 73.5% 0%);
}

.tick {
  position: absolute;
  top: 0;
  left: calc(50%);
  transform-origin: bottom center;
  height: 50%;
  width: 0.2rem;
  background-color: black;
  clip-path: rect(0% 100% 100% 0%)
}

.needle {
  position: absolute;
  left: calc(50% - 5px);
  transform-origin: bottom;
  width: 10px;
  background: red;
  height: 50%;
  transition: 1s all;
  z-index: 99;
}
</style>