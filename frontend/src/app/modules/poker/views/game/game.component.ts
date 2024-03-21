
import {Component, ViewChild} from '@angular/core';
import {GameService} from "../../store/game.service";
import {PlayerDto} from "../../models/player-dto";
import {RoundPlayerDto} from "../../models/round-player-dto";
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

  constructor(public gameService: GameService) {
  }

  initializeSubscriber(){
    this.gameService.gameUpdated.subscribe((data) =>{
      let player1=new PlayerDto("id1",1,1000,"game1","user1")
      let player2=new PlayerDto("id2",2,578,"game1","user2")
      let player3=new PlayerDto("id3",3,100,"game1","user3")
      let playerRound1=new RoundPlayerDto(40,false,true,player1,[],"herz2","herz3")
      let playerRound2=new RoundPlayerDto(50,false,true,player2,[],"kreuz2","herz7")
      let playerRound3=new RoundPlayerDto(40,false,true,player3,[],"herzA","herz10")
      let playersRounds: RoundPlayerDto[]=[playerRound1,playerRound2,playerRound3]
      let cards:String[]=["pik3","karo4","kreuzD"]
      for (let i = 0; i < cards.length; i++) {
        this.drawCard('/assets/Media/Karten/pik3.svg',i+1)
      }
      for (let i = 0; i < playersRounds.length; i++) {
        this.drawPlayer(playersRounds[i])
      }
    })
  }

  testDrawCard(){
    let player1=new PlayerDto("id1",1,1000,"game1","user1")
    let player2=new PlayerDto("id2",2,578,"game1","user2")
    let player3=new PlayerDto("id3",3,100,"game1","user3")
    let player4=new PlayerDto("id3",4,100,"game1","user4")
    let player5=new PlayerDto("id3",5,100,"game1","user5")
    let player6=new PlayerDto("id3",6,100,"game1","user6")
    let player7=new PlayerDto("id3",7,100,"game1","user7")
    let playerRound1=new RoundPlayerDto(40,false,true,player1,[],"herz2","herz3")
    let playerRound2=new RoundPlayerDto(50,false,true,player2,[],"kreuz2","herz7")
    let playerRound3=new RoundPlayerDto(40,false,true,player3,[],"herzA","herz10")
    let playerRound4=new RoundPlayerDto(40,false,true,player4,[],"herzA","herz10")
    let playerRound5=new RoundPlayerDto(40,false,true,player5,[],"herzA","herz10")
    let playerRound6=new RoundPlayerDto(40,false,true,player6,[],"herzA","herz10")
    let playerRound7=new RoundPlayerDto(40,false,true,player7,[],"herzA","herz10")
    let playersRounds: RoundPlayerDto[]=[playerRound1,playerRound2,playerRound3,playerRound4,playerRound5,playerRound6,playerRound7]
    let cards:String[]=["pik3","karo4","kreuzD","kreuzD","kreuzD"]
    for (let i = 0; i < cards.length; i++) {
      this.drawCard('/assets/Media/Karten/'+cards[i]+'.svg',i+1)
    }
    for (let i = 0; i < playersRounds.length; i++) {
      this.drawPlayer(playersRounds[i])
    }
  }


  @ViewChild('gameTable') set content(content:any){
    console.log(content.nativeElement)
    this.ctx = content.nativeElement.getContext("2d")
    this.ctx.canvas.width=3840
    this.ctx.canvas.height=2400
    this.board_card_width=this.ctx.canvas.width*0.087
    this.board_card_height=this.ctx.canvas.height*0.215


    console.log(this.ctx)
    let img = new Image()
    img.src='/assets/Media/tisch_komplett_plain.svg'
    img.onload= () => {
      this.ctx.drawImage(img,0,0,this.ctx.canvas.width,this.ctx.canvas.height)
    }


  }
  drawCard(path:string,index:number){
    let img1 = new Image()
    img1.src=path
    img1.onload= () => {
      this.ctx.drawImage(img1,(0.098*(index-1)+0.268)*this.ctx.canvas.width,0.4475*this.ctx.canvas.height,this.board_card_width,this.board_card_height)
    }
  }

  drawPlayer(playerRound:RoundPlayerDto){
    let mid = this.ctx.canvas.width/2
    let x = 0
    let y = 0
    let yPositions:number[] = [this.ctx.canvas.height*0.28,
                               this.ctx.canvas.height*0.60,
                               this.ctx.canvas.height*0.92]
    switch(playerRound.player.position){
      case 1:
        x=mid+600
        y=yPositions[2]
        break
      case 2:
        x=mid+1200
        y=yPositions[1]
        break
      case 3:
        x=mid+800
        y=yPositions[0]
        break
      case 4:
        x=mid-300
        y=yPositions[0]
        break
      case 5:
        x=mid-1400
        y=yPositions[0]
        break
      case 6:
        x=mid-1800
        y=yPositions[1]
        break
      case 7:
        x=mid-1200
        y=yPositions[2]
        break
    }
    this.drawPlayerInfo(playerRound, x, y)
    this.drawPlayerCards(playerRound, x, y)
  }

  drawPlayerInfo(playerRound:RoundPlayerDto, x:number, y:number){
    this.ctx.font = `${100}px Arial`;
    this.ctx.fillStyle = "black"
    this.ctx.fillRect(x, y, 600, 150)
    this.ctx.fillStyle = "white"

    let name = playerRound.player.userId
    this.ctx.fillText(name, x+50, y+110, 400)

    let chipsValue: any = playerRound.player.chips
    this.ctx.fillText(chipsValue as string, x+400, y+110, 180)
  }

  drawPlayerCards(playerRound:RoundPlayerDto, x:number, y:number){
    let img1 = new Image()
    let img2 = new Image()
    img1.src='/assets/Media/Karten/'+playerRound.card1+'.svg'
    img2.src='/assets/Media/Karten/'+playerRound.card2+'.svg'

    let x1 = x+15
    let y1 = y-500
    img1.onload= () => {
      this.ctx.drawImage(img1, x1, y1,this.board_card_width*0.8,this.board_card_height*0.8)
    }

    let x2 = x+315
    let y2 = y-500
    img2.onload= () => {
     this.ctx.drawImage(img2, x2, y2, this.board_card_width*0.8,this.board_card_height*0.8)
    }
  }
}
