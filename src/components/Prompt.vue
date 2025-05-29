<script setup>
import { reactive, ref, computed, watch, inject, watchEffect } from 'vue';

const props = defineProps({
  isMine: {
    type: Boolean,
    default: true
  },
  user: {
    type: Object
  }
})

const prompt = ref('These are the words you need to type');
const cumulativeInput = ref('')
const currentInput = ref('');
const youWin = ref(false);

const socket = inject('socket');

socket.on('update_prompt', (data) => prompt.value = data)

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

const errorIndexOfCurrentWord = computed(() => {
  let i = 0;

  for (i = 0; i < currentInput.value.length; i++) {
    if (currentWord.value[i] != currentInput.value[i]) {
      return i
    }
  }
})

const successPromptInput = computed(() => {
  if (errorIndexOfCurrentWord.value === undefined) {
    return currentWord.value.substring(0, currentInput.value.length)
  }
  return currentWord.value.substring(0, errorIndexOfCurrentWord.value)
})

const errorPromptInput = computed(() => {
  // Gotta figure out what's eligible to be an error, then slice off of that
  if (errorIndexOfCurrentWord.value !== undefined) {
    return prompt.value
      .slice(startIndexOfCurrentWord.value + successPromptInput.value.length)
      .slice(0, currentInput.value.length - errorIndexOfCurrentWord.value)
  }
})

const neutralPromptInput = computed(() => {
  return prompt.value
    .slice(startIndexOfCurrentWord.value + currentInput.value.length)
})

const inputForServer = computed(() => {
  return cumulativeInput.value + currentInput.value;
})

watch(inputForServer, (currentValue) => {
  if (props.isMine) {
    socket.emit("update_input", {
      cumulativeInput: cumulativeInput.value,
      currentInput: currentInput.value
    });
  }
})

watch(currentInput, (currentValue, prevValue) => {
  if (cumulativeInput.value + currentValue == prompt.value) return youWin.value = true;

  const lastChar = currentValue[currentValue.length - 1];
  if (lastChar == ' ' && !isError.value) {
    cumulativeInput.value += currentValue
    currentInput.value = '';
  }
});

watch(() => props.user, (user) => {
  if (!user.input) {
    return;
  }
  
  cumulativeInput.value = user.input.cumulativeInput;
  currentInput.value = user.input.currentInput;

})
</script>

<template>
  <div class="card bg-base-200 w-96 shadow-sm">
    <div class="card-body">
      <div>
        <!-- <span>{{ prompt }}</span> -->

        <span class="text-success">{{ cumulativeInput }}</span>

        <span class="text-success">{{ successPromptInput }}</span>
        <span class="text-error">{{ errorPromptInput }}</span>
        <span class="text-neutral-content">{{ neutralPromptInput }}</span>

        <!--
        <span style="color: yellow;">{{ currentWord }}</span>
        
        <span class="text-neutral-content">{{ prompt.substring(cumulativeInput.length + currentWord.length) }}</span>
        -->
      </div>

      <div v-if="isMine">
        <input type="text" v-model="currentInput" class="input" />
      </div>
    </div>
  </div>
</template>
