<script setup lang="ts">
  import { ref, computed, watch } from "vue";

  const props = defineProps<{ countdown?: number}>()

  const disabled = ref(false)

  const lights = computed(() => {
    let countdown = props.countdown;

    return [
      {classes: countdown <= 3 && !disabled.value ? "bg-red-500 shadow-red-500 shadow-[0_0_30px]" : "bg-red-900"},
      {classes: countdown <= 2 && !disabled.value ? "bg-red-500 shadow-red-500 shadow-[0_0_30px]" : "bg-red-900"},
      {classes: countdown <= 1 && !disabled.value ? "bg-yellow-500 shadow-yellow-500 shadow-[0_0_30px]" : "bg-yellow-900"},
      {classes: countdown <= 0 && !disabled.value ? "bg-green-500 shadow-green-500 shadow-[0_0_30px]" : "bg-green-900"},
    ]
  })

  watch(() => props.countdown, (countdown) => {
    if (countdown == 0) {
      setTimeout(() => {
        disabled.value = true
      }, 1000)
    }
  })
</script>

<template>
  <div class="flex justify-center gap-2 rounded border border-neutral-500 w-min mx-auto p-2">
    <div
      v-for="(l, i) in lights"
      :key="i"
      class="rounded-full w-12 aspect-square border border-4"
      :class="l.classes"
    ></div>
  </div>
</template>