import {CardDto} from "./card-dto";

export class PlayerDto {
    cards: CardDto[]
    chips: number
    name: string
    id: string
  constructor(cards:CardDto[],chips:number,name:string,id:string) {
      this.cards=cards
      this.chips=chips
      this.name=name
      this.id=id
  }
}
