<script setup lang="ts">
// TODO: cool avatars, logo, progress bars, etc
// TODO: github actions for backend repo changes = FTP file to server
// TODO: enum on backend for race statuses
import { onBeforeMount, ref, watch } from "vue"
import { store } from './store/store.ts'
import Prompt from './components/Prompt.vue'
import { RaceStatus } from "./store/types/raceStatus.ts"

interface Racer {
  sid: string
  progress?: number
}

const users = ref([]);
const countdown = ref(10)
const raceStatus = ref<RaceStatus>(RaceStatus.INACTIVE);
const racers = ref<Racer[]>([])

const updateUsers = data => {
  users.value = data;
}

const createRace = () => {
  store.socket.emit('create_race');
}

onBeforeMount(() => {
  store.socket.on('update_countdown', (data) => countdown.value = data)
  store.socket.on('update_race_status', (key) => {
    //raceStatus.value = RaceStatus[key]
  })
  raceStatus.value = RaceStatus.IN_PROGRESS
  store.socket.on('update_racers', (data) => racers.value = data)
  store.socket.on('update_racer_progress', ({ sid, progress }) => {
    let racer = racers.value.find(r => r.sid == sid)
    racer && (racer.progress = progress);
  })
  store.socket.on('update_prompt', (data) => store.prompt = data)
})

watch(raceStatus, (status) => {
  if (status == RaceStatus.IN_PROGRESS) {
    store.startTime = new Date().getTime()
  }
})

store.socket.on("update_users", updateUsers);
</script>

<template>
  <div class="flex justify-center relative">
    <template v-if="raceStatus === RaceStatus.INACTIVE">
      <button
        type="button"
        class="btn"
        @click="createRace"
        v-if="raceStatus == RaceStatus.INACTIVE"
      >
        Start race with {{ users.length }} racer(s)
      </button>
    </template>

    <template v-if="[RaceStatus.COUNTDOWN, RaceStatus.IN_PROGRESS].indexOf(raceStatus) > -1">
      <Prompt :disabled="raceStatus != RaceStatus.IN_PROGRESS"></Prompt>
    </template>

    <span
      v-if="[RaceStatus.COUNTDOWN, RaceStatus.TERMINATED, RaceStatus.FINISHED].indexOf(raceStatus) > -1"
      class="absolute top-50 left-50 text-9xl"
    >
      {{ countdown }}
    </span>

    <template v-if="raceStatus === RaceStatus.FINISHED">
      TODO: show rankings or whatever
    </template>

    <template v-if="raceStatus === RaceStatus.TERMINATED">
      TODO: race was terminated
    </template>
  </div>

  <div class="flex">
    <input v-for="racer in racers" :key="racer.sid" type="range" name="" id="" max="100" :value="racer.progress ?? 0">
  </div>
</template>