<script setup lang="ts">
// TODO: show a version of the prompt for each racer with a cool parralax effect
import { ref } from 'vue'
import type { Racer } from '../App.vue';

defineProps<{ racers: Racer[] }>()
</script>

<template>
  <div class="flex">
    <div class="flex flex-col w-full">
      <div class="relative border-b-2 w-full" v-for="r in racers" :key="r.sid">
        {{ r.username }}
        <img
          src="../assets/27186974_ca46_2u5r_220404.svg"
          style="height:50px; transform: scaleX(-1); position: relative;"
          :style="'left: ' + r.progress + '%'"
        >
      </div>
    </div>

    <div class="ml-auto" style="background: repeating-conic-gradient(#fff 0 25%, #000 0 50%) 50% / 25px 25px; width: 10%;"></div>
  </div>

</template>