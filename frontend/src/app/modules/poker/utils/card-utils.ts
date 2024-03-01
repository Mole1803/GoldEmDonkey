import {CardDto} from "../models/card-dto";

export class CardUtils {
    static getCardAsString(card:CardDto):string{
    let erg:string="";
    switch (card.colour){
      case 1:
        erg="kreuz";
        break;
      case 2:
        erg="pik";
        break;
      case 3:
        erg="herz";
        break;
      case 4:
        erg="karo";
        break;
    }
    switch (card.value){
      case 11:
        erg+="B"
        break;
      case 12:
        erg+="D"
        break;
      case 13:
        erg+="K"
        break;
      case 14:
        erg+="A"
        break;
      default:
        erg+=card.value.toString()
    }
    return erg;
  }
}
