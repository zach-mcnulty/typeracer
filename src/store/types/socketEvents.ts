import { RaceStatus } from "./raceStatus"

export interface ServerToClientEvents {
  'update_countdown': any
  'update_race_status': (key: keyof (typeof RaceStatus)) => void
  'update_racers': any
  'update_racer_progress': any
  'update_prompt': any
  'update_users'
}

export interface ClientToServerEvents {
  create_race: () => void;
  update_racer_progress: (n: number) => void;
}