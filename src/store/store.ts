import { reactive } from 'vue'

interface Store {
  startTime: number | undefined
  socket: object
  prompt: string
}



export const store = reactive<Store>({
  startTime: undefined,
  socket: io("wss://ocb.ryandeba.com", { secure: true }),
  prompt: "These are some placeholder words"
})