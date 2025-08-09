<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";
import { store } from "../store/store"

const props = defineProps<{
  numAllTypedEntries: number
}>()

let currentTimeInterval
const currentTime = ref(0)

onMounted(() => {
  currentTimeInterval = setInterval(() => {
    currentTime.value = new Date().getTime()
  }, 1000)
})

onUnmounted(() => {
  clearInterval(currentTimeInterval)
})

const speed = computed<number>(() => {
  if (typeof store.startTime == 'number') {
    const seconds = (currentTime.value - store.startTime) / 1000;
    const minutes = seconds / 60;
    return (props.numAllTypedEntries / 5) / minutes;
  }

  return 0
})

const ticks = new Array(6 * 3 + 8);
const needleRotate = computed(() => speed.value / 0.54 - 110)
</script>

<template>
  <div class="gauge">
    <div class="inner-gauge">
      <div class="needle" :style="{transform: `rotate(${needleRotate}deg)`}"></div>
      <div class="tick-wrapper">
        <span
          v-for="(tick, i) in ticks"
          :key="i"
          class="tick"
          :style="{transform: `rotate(${i * 8.8 - 110}deg)`}"
        >
          <span v-if="i % 4 == 0" :style="{transform: `rotate(${-(i * 8.8 - 110)}deg)`, position: `absolute`}">
            {{ i * 5 }}
          </span>
        </span>
      </div>

    </div>
  </div>

  {{ speed }}
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
  transition: 0.2s all;
  z-index: 99;
}
</style>