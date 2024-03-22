
import {Component, ViewChild} from '@angular/core';
import {GameService} from "../../store/game.service";
import {PlayerDto} from "../../models/player-dto";
import {RoundPlayerDto} from "../../models/round-player-dto";
import {CardDto} from "../../models/card-dto";
import {CardUtils} from "../../utils/card-utils";
import {Router} from "@angular/router";



@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent {
  // @ts-ignore
  public ctx:  any;
  // @ts-ignore
  public board_card_width:number;
  // @ts-ignore
  public board_card_height:number;

  constructor(public gameService: GameService, private router: Router) {
    if(!gameService.socket.connected || gameService.game == undefined){
      this.router.navigate([{outlets: {pokeroutlet: ['menu']}}])
    }
    this.initializeSubscriber()
  }

  onGameUpdate(){
    console.log("onGameUpdate")
    // @ts-ignore
    let cards:CardDto[]=this.gameService.gameData["kwargs"]["cards"]
    // @ts-ignore
    let roundPlayers:RoundPlayerDto[]=this.gameService.gameData["kwargs"]["roundPlayers"]
    // @ts-ignore
    let nextPlayer:PlayerDto=this.gameService.gameData["kwargs"]["nextPlayer"]
    // @ts-ignore
    let gamePlayers:PlayerDto[]=this.gameService.gameData["kwargs"]["gamePlayers"]
    if(cards.length==0){
      this.drawTable()

    }
    for (let i = 0; i < cards.length; i++) {
      this.drawCard('/assets/Media/Karten/'+CardUtils.getCardAsString(cards[i])+'.svg',i+1)
    }
    for (let i = 0; i < roundPlayers.length; i++) {
      for(let j = 0; j < gamePlayers.length; j++){
        if(roundPlayers[i].idPlayer==gamePlayers[j].id){
          this.drawPlayer(roundPlayers[i],gamePlayers[j])
        }
      }
    }
  }

  initializeSubscriber(){
    this.gameService.gameUpdated.subscribe(() =>{
      this.onGameUpdate()
    })
  }

  testDrawCard(){
    let player1=new PlayerDto("id1",1,1000,"game1","user1")
    let player2=new PlayerDto("id2",2,578,"game1","user2")
    let player3=new PlayerDto("id3",3,100,"game1","user3")
    let player4=new PlayerDto("id4",4,100,"game1","user4")
    let player5=new PlayerDto("id5",5,100,"game1","user5")
    let player6=new PlayerDto("id6",6,100,"game1","user6")
    let player7=new PlayerDto("id7",7,100,"game1","user7")
    let players=[player1,player2,player3,player4,player5,player6,player7]
    let playerRound1=new RoundPlayerDto("40","id1",true,false,0,true,1,1,2)
    let playerRound2=new RoundPlayerDto("50","id2",true,false,0,true,2,3,4)
    let playerRound3=new RoundPlayerDto("40","id3",true,false,0,true,3,5,6)
    let playerRound4=new RoundPlayerDto("40","id4",true,false,0,true,4,7,8)
    let playerRound5=new RoundPlayerDto("40","id5",true,false,0,true,5,9,10)
    let playerRound6=new RoundPlayerDto("40","id6",true,false,0,true,6,11,12)
    let playerRound7=new RoundPlayerDto("40","id7",true,false,0,true,7,13,14)
    let playersRounds: RoundPlayerDto[]=[playerRound1,playerRound2,playerRound3,playerRound4,playerRound5,playerRound6,playerRound7]
    let cards:String[]=["pik3","karo4","kreuzD","kreuzD","kreuzD"]
    for (let i = 0; i < cards.length; i++) {
      this.drawCard('/assets/Media/Karten/'+cards[i]+'.svg',i+1)
    }
    for (let i = 0; i < playersRounds.length; i++) {
      this.drawPlayer(playersRounds[i],players[i])
    }
  }

  @ViewChild('gameTable') set content(content:any){
    this.ctx = content.nativeElement.getContext("2d")
    this.ctx.canvas.width=3840
    this.ctx.canvas.height=2400
    this.board_card_width=this.ctx.canvas.width*0.087
    this.board_card_height=this.ctx.canvas.height*0.215
    this.drawTable()
  }

  async drawTable() {

    //let img = await loadImage('./assets/Media/tisch_komplett_plain.svg');
    //this.ctx.drawImage(img, 0, 0,this.ctx.canvas.width, this.ctx.canvas.height);
    let img = new Image()
    img.src = './assets/Media/tisch_komplett_plain.svg'
      img.onload = () => {
        this.ctx.drawImage(img, 0, 0, this.ctx.canvas.width, this.ctx.canvas.height)
      }
  }

  drawCard(path:string,index:number){
    let img1 = new Image()
    img1.src=path
    img1.onload= () => {
      this.ctx.drawImage(img1,(0.098*(index-1)+0.268)*this.ctx.canvas.width,0.4475*this.ctx.canvas.height,this.board_card_width,this.board_card_height)
    }
  }

  drawPlayer(roundPlayer:RoundPlayerDto,gamePlayer:PlayerDto){
    console.log("Draw Players")
    let mid = this.ctx.canvas.width/2
    let x = 0
    let y = 0
    let yPositions:number[] = [this.ctx.canvas.height*0.28,
                               this.ctx.canvas.height*0.60,
                               this.ctx.canvas.height*0.92]
    switch(gamePlayer["position"]){
      case 0:
        x=mid+600
        y=yPositions[2]
        break
      case 1:
        x=mid+1200
        y=yPositions[1]
        break
      case 2:
        x=mid+800
        y=yPositions[0]
        break
      case 3:
        x=mid-300
        y=yPositions[0]
        break
      case 4:
        x=mid-1400
        y=yPositions[0]
        break
      case 5:
        x=mid-1800
        y=yPositions[1]
        break
      case 6:
        x=mid-1200
        y=yPositions[2]
        break
    }
    this.drawPlayerInfo(roundPlayer,gamePlayer, x, y)
    this.drawPlayerCards(roundPlayer,gamePlayer, x, y)
  }

  drawPlayerInfo(roundPlayer:RoundPlayerDto,gamePlayer:PlayerDto, x:number, y:number){
    setTimeout(()=> {
      console.log("draw player info")
      this.ctx.font = `${100}px Arial`;
      this.ctx.fillStyle = "black"
      this.ctx.fillRect(x, y, 600, 150)
      this.ctx.fillStyle = "white"

      let name = gamePlayer.userId
      this.ctx.fillText(name, x + 30, y + 110, 330)

      let chipsValue: any = gamePlayer.chips
      this.ctx.fillText(chipsValue as string, x + 400, y + 110, 180)
    },20)
  }

  drawPlayerCards(playerRound:RoundPlayerDto,nextPlayer:PlayerDto, x:number, y:number){
    setTimeout(()=>{
    console.log("draw player cards")
    let img1 = new Image()
    let img2 = new Image()
    if(this.gameService.isPlayerMoveClient(nextPlayer)) {
      img1.src = '/assets/Media/Karten/' + CardUtils.getCardAsStringFromNumber(playerRound.card1) + '.svg'
      img2.src = '/assets/Media/Karten/' + CardUtils.getCardAsStringFromNumber(playerRound.card2) + '.svg'
    }else {
      img1.src = '/assets/Media/Karten/rueckseite.svg'
      img2.src = '/assets/Media/Karten/rueckseite.svg'
    }
    let x1 = x+15
    let y1 = y-500
    img1.onload= () => {
      this.ctx.drawImage(img1, x1, y1,this.board_card_width*0.8,this.board_card_height*0.8)
    }

    let x2 = x+315
    let y2 = y-500
    img2.onload= () => {
     this.ctx.drawImage(img2, x2, y2, this.board_card_width*0.8,this.board_card_height*0.8)
    }},10)
  }
}
