import { reactive, watch } from 'vue'
import { io, Socket } from "socket.io-client"
import { ServerToClientEvents, ClientToServerEvents } from './types/socketEvents'

interface Store {
  clientStartTime: number
  socket: Socket<ServerToClientEvents, ClientToServerEvents>
  prompt: string
  wpm: number
  errors: number
  progress: number
  duration: number
  _interval?: NodeJS.Timeout

  emitStatusUpdate: () => void
  startClientInterval: () => void
  stopClientInterval: () => void
}

export interface StatusUpdate {
  wpm: number
  errors: number
  progress: number
  duration: number
}

export const store = reactive<Store>({
  clientStartTime: 0,
  socket: io("wss://ocb.ryandeba.com", { secure: true }),
  prompt: '',
  wpm: 0,
  errors: 0,
  progress: 0,
  duration: 0,
  _interval: undefined,
  emitStatusUpdate: () => {
    const status: StatusUpdate = {
      wpm: store.wpm,
      errors: store.errors,
      progress: store.progress,
      duration: store.duration
    }

    store.socket.emit('update_racer_status', status);
  },
  startClientInterval: () => {
    store._interval = setInterval(store.emitStatusUpdate, 1000);
  },
  stopClientInterval: () => clearInterval(store._interval)
})