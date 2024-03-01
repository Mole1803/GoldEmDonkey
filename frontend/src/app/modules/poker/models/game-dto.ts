import {PlayerDto} from "./player-dto";

export class GameDto {
  id: string
  isActive: boolean
  hasStarted: boolean
  name: string
  players: PlayerDto[]


  constructor(id: string, isActive: boolean, hasStarted: boolean, name: string,players:PlayerDto[]) {
    this.id = id
    this.isActive = isActive
    this.hasStarted = hasStarted
    this.name = name
    this.players = players
  }
}
