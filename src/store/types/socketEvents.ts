import { RaceStatus } from "./raceStatus"
import { StatusUpdate } from '../store';

interface StatusUpdateWithSid extends StatusUpdate {
  sid: string
}

export interface ServerToClientEvents {
  'update_countdown': any
  'update_race_status': (key: keyof (typeof RaceStatus)) => void
  'update_racers': any
  'update_racer_progress': any
  'update_prompt': any
  'update_users': any,
  'update_racer_status': (status: StatusUpdateWithSid) => void
}

export interface ClientToServerEvents {
  create_race: () => void
  update_racer_progress: (n: number) => void
  update_racer_duration: (n: number) => void
  toggle_ready: () => void
  update_racer_wpm: any
  refresh_username: () => void
 update_racer_status: (status: StatusUpdate) => void
}