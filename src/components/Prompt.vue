<script setup>
import { reactive, ref, computed, watch } from 'vue';

const prompt = ref('These are the words you need to type');
const cumulativeInput = ref('These are the ')
const currentInput = ref('');
const youWin = ref(false);

const startIndexOfCurrentWord = computed(() => cumulativeInput.value.length)
const endIndexOfCurrentWord = computed(() => {
  let indexOfNextSpace = prompt.value.substring(startIndexOfCurrentWord.value).indexOf(' ');

  if (indexOfNextSpace == -1) {
    return prompt.value.length
  }

  return prompt.value.substring(startIndexOfCurrentWord.value).indexOf(' ') + cumulativeInput.value.length
})
const currentWord = computed(() => prompt.value.substring(startIndexOfCurrentWord.value, endIndexOfCurrentWord.value + 1))
const isError = computed(() => currentWord.value.indexOf(currentInput.value) != 0)

const successPromptInput = computed(() => {
  let i = 0;

  for (i = 0; i <= currentInput.value.length; i++) {
    if (currentWord.value[i] != currentInput.value[i]) {
      break
    }
  }

  return currentWord.value.substring(0, i)
})

watch(currentInput, (currentValue, prevValue) => {
  if (cumulativeInput.value + currentValue == prompt.value) return youWin.value = true;

  const lastChar = currentValue[currentValue.length - 1];
  if (lastChar == ' ' && !isError.value) {
    cumulativeInput.value += currentValue
    currentInput.value = '';
  }
});
</script>

<template>
  <div class="card bg-base-200 w-96 shadow-sm">
    <div class="card-body">
      <div>
        <!-- <span>{{ prompt }}</span> -->

        <span class="text-success">{{ cumulativeInput }}</span>

        <span class="text-success">{{ successPromptInput }}</span>
        <!-- TODO
        <span class="text-error">{{ errorPromptInput }}<</span>
        <span class="text-neutral-content">{{ neutralPromptInput }}<</span>-->

        <span>{{ currentWord }}</span>
        
        <span class="text-neutral-content">{{ prompt.substring(cumulativeInput.length + currentWord.length) }}</span>
      </div>

      <input type="text" v-model="currentInput" class="input" />

      <br />
      <div>cumulativeInput: {{ cumulativeInput }}</div>
      <div>start: {{ startIndexOfCurrentWord }}</div>
      <div>end: {{ endIndexOfCurrentWord }}</div>
      <div>currentWord: {{ currentWord }}</div>
      <div>is error: {{ isError }}</div>
      <div>you win: {{ youWin }}</div>
    </div>
  </div>
</template>
