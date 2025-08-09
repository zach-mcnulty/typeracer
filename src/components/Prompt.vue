<script setup lang="ts">
import { toEditorSettings } from "typescript";
import { store } from '../store/store.ts'
import { ref, computed, watch } from "vue";
import Speedometer from "./Speedometer.vue"

const input = ref("");
const checkeredFlag = ref(false);

const indexOfCursor = computed(() => indexOfStartOfCurrentWord.value + input.value.length);
const indexOfStartOfCurrentWord = ref(0)
const indexOfEndOfCurrentWord = computed(() => {
  const start = indexOfStartOfCurrentWord.value;
  let end = store.prompt.indexOf(' ', start);
  end = end == -1 ? store.prompt.length : ++end;

  return end;
});
const indexOfError = computed<number | void>(() => {
  let i = 0;
  while (i < input.value.length) {
    if (expectedWord.value[i] !== input.value[i]) {
      return i + indexOfStartOfCurrentWord.value;
    }

    i++;
  }
});
const expectedWord = computed(() => store.prompt.slice(indexOfStartOfCurrentWord.value, indexOfEndOfCurrentWord.value));

watch(input, () => {
  if (input.value === expectedWord.value) {
    if (indexOfCursor.value == store.prompt.length) {
      checkeredFlag.value = true;
    }
    indexOfStartOfCurrentWord.value = indexOfCursor.value;
    input.value = "";
  }

  let progressIndex = typeof indexOfError.value == 'number' ? indexOfError.value : indexOfCursor.value;
  store.socket.emit("update_racer_progress", (progressIndex / store.prompt.length) * 100);
})
</script>

<template>
  <div class="card bg-base-200 w-96 shadow-sm">
    <div class="card-body">
      <div>
        <span
          v-for="(char, i) in store.prompt"
          :key="i"
          class="text-neutral-content relative text-lg"
          :class="{
            'text-success!':
              i < indexOfStartOfCurrentWord ||
              (typeof indexOfError == 'number' && i < indexOfError) ||
              (typeof indexOfError == 'undefined' && i < indexOfCursor),
            'text-error!':
              typeof indexOfError == 'number' &&
              i >= indexOfError && i < indexOfCursor,
            'super-duper-cursor-of-doom': i == indexOfCursor
          }"
        >
          {{ char }}
        </span>
      </div>

      <input type="text" v-model="input" class="input" />
      <Speedometer :num-all-typed-entries="indexOfEndOfCurrentWord + input.length"></Speedometer>
    </div>
  </div>
</template>

<style>
.super-duper-cursor-of-doom::before {
  content: '';
  width: 1px;
  height: 100%;
  background: black;
  position: absolute;
  top: 0;
  left: 0;
  animation: blink 1s step-start 0s infinite;
}

@keyframes blink {
  50% {
    opacity: 0.0;
  }
}
</style>