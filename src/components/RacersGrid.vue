<script setup lang="ts">
import { ref, reactive, computed } from "vue";
import { Racer, User } from "../App.vue";
import { RaceStatus } from "../store/types/raceStatus";
import { store } from '../store/store'

const props = defineProps<{
  users: User[]
  racers: Racer[]
  raceStatus: RaceStatus
}>()

const columns = reactive([
  { field: 'username', header: 'Username' },
  { field: 'ready', header: 'Ready?' },
  { field: 'wpm', header: 'WPM' },
  { field: 'duration', header: 'Duration' }
])

const visibleColumns = computed(() => {
  switch (props.raceStatus) {
    case RaceStatus.FINISHED:
    case RaceStatus.TERMINATED:
      return columns.filter(({ field }) => field !== 'ready')
    case RaceStatus.INACTIVE:
      return columns.filter(({ field }) => !['wpm', 'duration'].includes(field))
  }
})

const toggleReady = (user: User) => {
  if (user.sid != store.socket.id) {
    return
  }

  store.socket.emit('toggle_ready')
}

const refreshUsername = (user: User) => {
  store.socket.emit("refresh_username")
}
</script>

<template>
    <table class="table">
      <thead>
        <tr>
          <th v-for="column in visibleColumns" :key="column.field">
            {{ column.header }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="u in raceStatus == RaceStatus.INACTIVE ? users : racers"
          :class="{'bg-blue-200': u.sid == store.socket.id}"
        >
          <td v-for="column in visibleColumns" :key="column.field">
            <template v-if="column.field == 'ready'">
              <input
                type="checkbox"
                :checked="u.ready"
                :disabled="u.sid != store.socket.id"
                class="checkbox checkbox-lg"
                @input.prevent="toggleReady(u)"
              >
            </template>
            <template v-else-if="column.field == 'duration'">
              {{ `${(u.duration / 1000).toFixed(2)} secs.` }}
            </template>
            <template v-else-if="column.field == 'username'">
              {{ u.username }}

              <button class="btn btn-circle btn-xs btn-ghost" v-if="u.sid === store.socket.id" @click="refreshUsername">
                <img src="https://www.svgrepo.com/show/425978/refresh.svg" alt="" class="w-75 h-75">
              </button>
            </template>
            <template v-else>
              {{ u[column.field] }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>
</template>