import { reactive } from 'vue'
import { io, Socket } from "socket.io-client"
import { ServerToClientEvents, ClientToServerEvents } from './types/socketEvents'

interface Store {
  clientStartTime: number | undefined
  socket: Socket<ServerToClientEvents, ClientToServerEvents>
  prompt: string
}



export const store = reactive<Store>({
  clientStartTime: undefined,
  socket: io("wss://ocb.ryandeba.com", { secure: true }),
  prompt: "These are some placeholder words. They are really great words. You should type them up quickly, unless you're a loser."
})