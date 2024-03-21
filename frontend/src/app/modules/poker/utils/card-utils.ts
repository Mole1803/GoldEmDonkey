import {CardDto} from "../models/card-dto";

export class CardUtils {
    static getCardAsStringFromNumber(card:number){
      let erg:string="";
      switch (Math.floor(card/13)){
        case 3:
          erg="kreuz";
          break;
        case 2:
          erg="pik";
          break;
        case 1:
          erg="herz";
          break;
        case 0:
          erg="karo";
          break;
      }
      switch (card%13){
        case 11:
          erg+="B"
          break;
        case 12:
          erg+="D"
          break;
        case 0:
          erg+="K"
          break;
        case 1:
          erg+="A"
          break;
        default:
          let num=card%13
          erg+=num.toString()
          break;
      }
      return erg;
    }
    static getCardAsString(card:CardDto):string{
    let erg:string="";
    switch (card.colour){
      case 3:
        erg="kreuz";
        break;
      case 2:
        erg="pik";
        break;
      case 1:
        erg="herz";
        break;
      case 0:
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
