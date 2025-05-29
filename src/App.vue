<script setup>
import { onBeforeMount, ref, provide } from "vue";
import Prompt from './components/Prompt.vue'

const socket = io("wss://ocb.ryandeba.com", {secure: true});
const users = ref([]);
const countdown = ref(10)

provide('socket', socket);

const updateUsers = data => {
  users.value = data;
}

const createRace = () => {
  socket.emit('create_race');
}

onBeforeMount(() => {
  socket.on('update_countdown', (data) => countdown.value = data)
})

socket.on("update_users", updateUsers);
</script>

<template>
  <div class="flex justify-center">
    <div>Countdown: {{ countdown }}</div>
    <div>Users: {{ users.length }}</div>
  </div>

  <div class="flex justify-center">
    {{ users }}
  </div>

  <button
    type="button"
    class="btn"
    @click="updateUsers(users.concat({username: 'Guest' + (users.length + 1)}))"
  >
    Add user
  </button>
  
  <button
    type="button"
    class="btn"
    @click="createRace"
  >
    Start race
  </button>

  <hr>

  <div class="flex justify-center">
    <Prompt></Prompt>
  </div>
  
  <div class="flex">
    <Prompt
      v-for="user in users.filter(u => u.sid != socket.id)"
      :is-mine="false"
      :user="user"
      :key="user.sid"
    ></Prompt>
  </div>
</template>

<style scoped>
</style>