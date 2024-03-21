import {PlayerDto} from "./player-dto";
import {RoundDto} from "./round-dto";

export class RoundPlayerDto {
  idRound: string
  idPlayer:string
  atPlay: boolean
  hasPlayed: boolean
  setChips: number
  isActive: boolean
  position: number
  card1: number
  card2: number


  constructor(id_round:string,id_player:string, at_play:boolean,has_played: boolean,set_chips:number,is_active:boolean,position: number, card1:number,card2:number) {
    this.idRound=id_round
    this.idPlayer=id_player
    this.setChips = set_chips
    this.atPlay = at_play
    this.hasPlayed = has_played
    this.isActive = is_active
    this.position = position
    this.card1=card1
    this.card2=card2
  }
}
