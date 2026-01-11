<script setup lang="ts">
import { onBeforeMount, ref, watch } from 'vue';
import { store } from './store/store.ts';
import Prompt from './components/Prompt.vue';
import RaceTrack from './components/RaceTrack.vue';
import { RaceStatus } from './store/types/raceStatus.ts';
import RacersGrid from './components/RacersGrid.vue';
import RaceSignal from './components/RaceSignal.vue';

export interface User {
  sid: string;
  username: string;
  ready?: boolean;
}

export interface Racer extends User {
  progress?: number;
  wpm?: number;
  duration?: number;
  errors?: number;
}

const users = ref<User[]>([]);
const countdown = ref(undefined);
const raceStatus = ref<RaceStatus>(RaceStatus.INACTIVE);
const racers = ref<Racer[]>([]);

const updateUsers = (data) => {
  users.value = data;
};

const createRace = () => {
  store.socket.emit('create_race');
};

onBeforeMount(() => {
  store.socket.on('update_countdown', (data: number) => {
    countdown.value = data;
  });
  store.socket.on('update_race_status', (key) => {
    raceStatus.value = RaceStatus[key];
  });
  store.socket.on('update_racers', onUpdateRacers);

  store.socket.on('update_racer_status', ({ sid, wpm, errors, progress, duration }) => {
    const racer = racers.value.find((r) => r.sid == sid);

    if (!racer) {
      return
    }

    racer.wpm = wpm
    racer.errors = errors
    racer.progress = progress
    racer.duration = duration
  });

  store.socket.on('update_prompt', (data) => (store.prompt = data));
});

const onUpdateRacers = (data: { sid: string; progress: number }[]) => {
  let usernamesBySid: { [key: string]: string } = {};

  users.value.forEach((u) => {
    usernamesBySid[u.sid] = u.username;
  });

  racers.value = data.map((r) => {
    return {
      ...r,
      username: usernamesBySid[r.sid],
    };
  });
};

watch(raceStatus, (status) => {
  if (status == RaceStatus.IN_PROGRESS) {
    store.clientStartTime = new Date().getTime();
    store.startClientInterval();
  }
});

watch(() => store.progress, (p) => {
  if (p == 100) {
    store.emitStatusUpdate();
    store.stopClientInterval();
  }
})

store.socket.on('update_users', updateUsers);
</script>

<template>
  <div class="navbar justify-between bg-black mb-5">
    <img src="./assets/typeracer.png" alt="" style="max-height: 50px" />
    <button
      v-if="raceStatus == RaceStatus.INACTIVE"
      class="btn"
      @click="createRace"
    >
      Start race with {{ users.filter((u) => u.ready).length }} racers
    </button>
    <span v-if="countdown" class="text-white text-2xl">
      {{ countdown }}
    </span>
  </div>

  <div class="flex flex-col mx-auto justify-center w-full max-w-200">
    <template v-if="raceStatus == RaceStatus.INACTIVE">
      <RacersGrid :users :racers :race-status />
    </template>

    <template
      v-if="
        [RaceStatus.COUNTDOWN, RaceStatus.IN_PROGRESS].indexOf(raceStatus) > -1
      "
      class="flex flex-col"
    >
      <RaceSignal :countdown="countdown" />
      <RaceTrack :racers="racers" />
      <Prompt :disabled="raceStatus != RaceStatus.IN_PROGRESS"></Prompt>
    </template>

    <template v-if="raceStatus === RaceStatus.TERMINATED">
      TODO: race was terminated
    </template>

    <template v-else-if="raceStatus == RaceStatus.FINISHED">
      <RacersGrid :users :racers :race-status />
    </template>
  </div>
</template>

<style>
.tr-card {
  padding: 24px;
  border-radius: 12px;
  background: #000;
}

input[type='checkbox'][disabled] {
  pointer-events: none;
  opacity: 1;
}
</style>

// update naming // error tracking //
