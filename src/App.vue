<script setup lang="ts">
// TODO: speedometer, ts all the things, cool avatars, server stuff
import { onBeforeMount, ref, provide } from "vue";
import Prompt from './components/Prompt.vue';

const socket = io("wss://ocb.ryandeba.com", {secure: true});
const users = ref([]);
const countdown = ref(10)
const raceStatus = ref("");
const racers = ref([])

provide('socket', socket);

const updateUsers = data => {
  users.value = data;
}

const createRace = () => {
  socket.emit('create_race');
}

onBeforeMount(() => {
  socket.on('update_countdown', (data) => countdown.value = data)
  socket.on('update_race_status', (data) => raceStatus.value = data)
  socket.on('update_racers', (data) => racers.value = data)
  socket.on('update_racer_progress', ({ sid, progress }) => {
    racers.value.find(r => r.sid == sid).progress = progress;
  })
})

socket.on("update_users", updateUsers);
</script>

<template>
  <div class="flex justify-center">
    <div class="mr-2">Countdown: {{ countdown }}</div>
    <div class="mr-2">Status: {{ raceStatus }}</div>
    <div>Users: {{ users.length }}</div>
    <br>
    <pre>Racers: {{ racers }}</pre>
  </div>

  <div class="flex justify-center">
    {{ users }}
  </div>
  
  <button
    type="button"
    class="btn"
    @click="createRace"
    v-if="raceStatus == 'INACTIVE'"
  >
    Start race
  </button>

  <hr>

  <div class="flex justify-center">
    <Prompt></Prompt>
  </div>
  
  <div class="flex">
    <input v-for="racer in racers" :key="racer.sid" type="range" name="" id="" max="100" :value="racer.progress ?? 0">
  </div>
</template>

<style scoped>
</style>