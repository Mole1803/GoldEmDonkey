import {PlayerDto} from "./player-dto";
import {RoundDto} from "./round-dto";

export class RoundPlayerDto {
  id_round: string
  id_player:string
  at_play: boolean
  has_played: boolean
  set_chips: number
  is_active: boolean
  position: number
  card1: number
  card2: number


  constructor(id_round:string,id_player:string, at_play:boolean,has_played: boolean,set_chips:number,is_active:boolean,position: number, card1:number,card2:number) {
    this.id_round=id_round
    this.id_player=id_player
    this.set_chips = set_chips
    this.at_play = at_play
    this.has_played = has_played
    this.is_active = is_active
    this.position = position
    this.card1=card1
    this.card2=card2
  }
}
