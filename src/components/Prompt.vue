<script setup lang="ts">
import { store } from '../store/store.ts'
import { ref, computed, watch, useTemplateRef } from "vue";
import Speedometer from "./Speedometer.vue"

const props = defineProps<{ disabled: boolean}>()

const promptRef = useTemplateRef("prompt")

const userInput = ref("");
const checkeredFlag = ref(false);

const indexOfCursor = computed(() => indexOfStartOfCurrentWord.value + userInput.value.length);
const indexOfStartOfCurrentWord = ref(0)
const indexOfEndOfCurrentWord = computed(() => {
  const start = indexOfStartOfCurrentWord.value;
  let end = store.prompt.indexOf(' ', start);
  end = end == -1 ? store.prompt.length : ++end;

  return end;
});
const indexOfError = computed<number | void>(() => {
  let i = 0;
  while (i < userInput.value.length) {
    if (expectedWord.value[i] !== userInput.value[i]) {
      return i + indexOfStartOfCurrentWord.value;
    }

    i++;
  }
});
const expectedWord = computed<string>(() => store.prompt.slice(indexOfStartOfCurrentWord.value, indexOfEndOfCurrentWord.value));
const progress = computed<number>(() => {
  let progressIndex = typeof indexOfError.value == 'number' ? indexOfError.value : indexOfCursor.value;
  return (progressIndex / store.prompt.length) * 100
})

watch(userInput, () => {
  if (userInput.value === expectedWord.value) {
    if (indexOfCursor.value == store.prompt.length) {
      checkeredFlag.value = true;
    }
    indexOfStartOfCurrentWord.value = indexOfCursor.value;
    userInput.value = "";
  }

  store.socket.emit("update_racer_progress", progress.value);
})

watch(() => props.disabled, () => {
  if (!props.disabled) {
    promptRef.value?.focus()
  }
})
</script>

<template>
  <div class="card bg-base-200 w-96 shadow-sm">
    <div class="card-body">
      <div class="mono">
        <span
          v-for="(char, i) in store.prompt"
          :key="i"
          class="text-neutral-content relative text-lg"
          :class="{
            'text-success!':
              i < indexOfStartOfCurrentWord ||
              (typeof indexOfError == 'number' && i < indexOfError) ||
              (typeof indexOfError == 'undefined' && i < indexOfCursor),
            'bg-error!':
              typeof indexOfError == 'number' &&
              i >= indexOfError && i < indexOfCursor,
            'super-duper-cursor-of-doom': i == indexOfCursor
          }"
          style="white-space: preserve;"
        >
          {{ char }}
        </span>
      </div>

      <input
        v-model="userInput"
        type="text"
        :readonly="disabled"
        autofocus
        class="input"
        ref="prompt"
      />
      <Speedometer
        :num-all-typed-entries="indexOfStartOfCurrentWord + userInput.length"
        :super-duper-pauser-of-doom="progress === 100"
      ></Speedometer>
    </div>
  </div>
</template>

<style>
.super-duper-cursor-of-doom {
  background: oklch(from var(--color-info) l c h / 0.50);
  animation: blink 1s step-end 0s infinite;
}

@keyframes blink {
  50% {
    background: none;
  }
}

.mono {
  font-family: "Roboto Mono", monospace;
}
</style>