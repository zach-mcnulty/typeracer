<script setup lang="ts">
// TODO: cool avatars, logo, progress bars, etc
// TODO: github actions for backend repo changes = FTP file to server
// TODO: enum on backend for race statuses
import { onBeforeMount, ref, watch } from "vue"
import { store } from './store/store.ts'
import Prompt from './components/Prompt.vue'
import RaceTrack from './components/RaceTrack.vue'
import { RaceStatus } from "./store/types/raceStatus.ts"

export interface User {
  sid: string
  username: string
  ready?: boolean
}

export interface Racer extends User {
  progress?: number
}

const users = ref<User[]>([]);
const countdown = ref(null)
const raceStatus = ref<RaceStatus>(RaceStatus.INACTIVE);
const racers = ref<Racer[]>([])

const updateUsers = data => {
  users.value = data;
}

const createRace = () => {
  store.socket.emit('create_race');
}

const toggleReady = (user: User) => {
  if (user.sid != store.socket.id) {
    return
  }

  store.socket.emit('toggle_ready')
}

onBeforeMount(() => {
  store.socket.on('update_countdown', (data: number) => {
    countdown.value = data
  })
  store.socket.on('update_race_status', (key) => {
    raceStatus.value = RaceStatus[key]
  })
  store.socket.on('update_racers', onUpdateRacers)
  store.socket.on('update_racer_progress', ({ sid, progress }) => {
    let racer = racers.value.find(r => r.sid == sid)
    racer && (racer.progress = progress);
  })
  store.socket.on('update_prompt', (data) => store.prompt = data)
})

const onUpdateRacers = (data: {sid: string, progress: number}[]) => {
  let usernamesBySid: {[key: string]: string} = {}

  users.value.forEach(u => {
    usernamesBySid[u.sid] = u.username
  })

  racers.value = data.map(r => {
    return {
      ...r,
      username: usernamesBySid[r.sid]
    }
  })
}

watch(raceStatus, (status) => {
  if (status == RaceStatus.IN_PROGRESS) {
    store.startTime = new Date().getTime()
  }
})

store.socket.on("update_users", updateUsers);
</script>

<template>
  <div class="navbar bg-black mb-5">
    <img src="./assets/typeracer.png" alt="" style="max-height: 50px;">
  </div>

  <div class="flex justify-center relative">
    <template v-if="raceStatus === RaceStatus.INACTIVE">
      <div class="self-center justify-self-center">
        <button
          class="btn"
          @click="createRace"
        >
            Start race with {{ users.filter(u => u.ready).length }} racers
        </button>

        <table>
          <tr>
            <td></td>
          </tr>
        </table>
      </div>
    </template>

    <div v-if="[RaceStatus.COUNTDOWN, RaceStatus.IN_PROGRESS].indexOf(raceStatus) > -1" class="flex flex-col">
      <RaceTrack :racers="racers" />
      <Prompt :disabled="raceStatus != RaceStatus.IN_PROGRESS"></Prompt>
    </div>

    <span
      v-if="countdown"
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

  <div class="overflow-x-auto">
    <table class="table">
      <thead>
        <tr>
          <th>Username</th>
          <th>Ready?</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="u in users"
          :class="{'bg-blue-200': u.sid == store.socket.id}"
        >
          <td>{{ u.username }}</td>
          <td>
            <input
              type="checkbox"
              :checked="u.ready"
              :disabled="u.sid != store.socket.id || u.ready"
              class="checkbox checkbox-lg"
              @input.prevent="toggleReady(u)"
            >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style>
.tr-card {
  padding: 24px;
  border-radius: 12px;
  background: #000;
}

 input[type="checkbox"][disabled] {
    pointer-events: none;
    opacity: 1;
  }
</style>