import {PlayerDto} from "./player-dto";
import {RoundDto} from "./round-dto";

export class RoundPlayerDto {
  at_play: boolean
  in_round: boolean
  set_chips: number
  card1: string
  card2: string
  player: PlayerDto
  round: RoundDto

  constructor(set_chips:number, at_play:boolean,in_round: boolean,player: PlayerDto, round: RoundDto, card1:string,card2:string) {
    this.set_chips = set_chips
    this.at_play = at_play
    this.in_round = in_round
    this.player = player
    this.round = round
    this.card1=card1
    this.card2=card2
  }
}
