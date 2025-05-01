<template>
  <div class="flex flex-col min-h-screen items-center justify-center bg-gray-100">
    <div class="card w-96 bg-base-100 card-xs shadow-sm mb-3">
      <div class="card-body">
        <pre>{{ messages }}</pre>
      </div>
    </div>
    <form @submit.prevent="handleSubmit" class="bg-white p-6 rounded-2xl shadow-md space-y-4 w-full max-w-sm">
      <input
        v-model="text"
        type="text"
        placeholder="Enter something..."
        class="w-full px-4 py-2 border rounded-xl focus:outline-none focus:ring focus:border-blue-300"
      />
      <button
        type="submit"
        class="w-full bg-blue-500 text-white py-2 px-4 rounded-xl hover:bg-blue-600 transition"
      >
        Submit
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const messages = reactive([])
const text = ref('')

const socket = io("ws://137.184.228.22");
socket.on('connect', function() {
  socket.emit('message_from_browser', "HELLO I'M WORKING!!!!");
});

socket.on("message_from_server", data => {
  messages.push(data)
});

const handleSubmit = () => {
  socket.emit('message_from_browser', text.value);
  text.value = '';
}
</script>

<style>
/* No additional styles needed if Tailwind is set up correctly */
</style>
