<script setup>
    import { reactive, ref, computed, watch } from 'vue'

    const prompt = ref('These are the words you need to type'.split(" "))
    const input = ref('th')
    const past = ref('These are'.split(" "))

    const current = computed(() => {
        return prompt.value[past.value.length]
    })

    const future = computed(() => {
        return prompt.value.slice(past.value.length + 1)
    })

    const currentHasError = computed(() => {
        return current.value.indexOf(input.value) != 0
    })

    watch(input, (currentValue, prevValue) => {
        const lastChar = currentValue[currentValue.length - 1]
        if (lastChar == " " && currentValue == current.value + ' ') {
            past.value.push(current.value)
            input.value = ''
        }
    })
</script>

<template>
    <div>
        Prompt: {{ prompt.join(" ") }}
    </div>
    <div>
        Past: {{ past.join(" ") }}
    </div>
    <div>
        Current: {{ current }}
    </div>
    <div>
        Future: {{ future.join(" ") }}
    </div>
    <div>
        Has error: {{ currentHasError }}
    </div>

    <div>
        <input
            type="text"
            v-model="input"
            class="input"
        >
    </div>
</template>