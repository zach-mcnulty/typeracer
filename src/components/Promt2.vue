<script setup>
import { ref, computed, watch, inject } from "vue";

const socket = inject('socket');

const prompt = ref("These are the words you need to type for prompt2.");
const input = ref("");
const checkeredFlag = ref(false);

const indexOfCursor = computed(() => indexOfStartOfCurrentWord.value + input.value.length);
const indexOfStartOfCurrentWord = ref(0)
const indexOfEndOfCurrentWord = computed(() => {
  const start = indexOfStartOfCurrentWord.value;
  let end = prompt.value.indexOf(' ', start);
  if (end == -1) end = prompt.length;

  return end;
});
const indexOfError = computed(() => {});
const expectedWord = computed(() => prompt.value.slice(indexOfStartOfCurrentWord.value, indexOfEndOfCurrentWord.value));

watch(input, () => {
    if (input.value === expectedWord.value) {
      // WIN CONDITION: if cursorLocation == prompt.length
      indexOfStartOfCurrentWord.value = indexOfCursor.value + 1;
      input.value = "";
    }
})
</script>

<template>
  <div>
    <span v-for="(char, i) in prompt" :key="i">
      {{ char }}
    </span>
  </div>


  <input v-model="input" type="text" />



</template>

<style>
input {
  border: 1px solid black;
}
</style>