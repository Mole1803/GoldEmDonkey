
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
        this.drawCard('/assets/Media/Karten/'+cards[i]+'.svg',i+1)
      }
      for (let i = 0; i < playersRounds.length; i++) {
        this.drawPlayer(playersRounds[i])
      }
    })
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
    let mid = this.ctx.canvas.width/2-300
    let y,x;
    switch(playerRound.player.position){
      case 0:
      case 6:
        y=this.ctx.canvas.height*0.65
        x=mid+(3-playerRound.player.position)*500
        break
      case 1:
      case 3:
      case 5:
        x=x=mid+(3-playerRound.player.position)*600
        y=this.ctx.canvas.height*0.2
        break
      case 2:
      case 4:
        x=mid+(3-playerRound.player.position)*700
        y=this.ctx.canvas.height*0.93
        break

    }
    this.ctx.fillRect(x, y, 600, 150)
    let img1 = new Image()
    let img2 = new Image()
    img1.src='/assets/Media/Karten/'+playerRound.card1+'.svg'
    img2.src='/assets/Media/Karten/'+playerRound.card2+'.svg'
    img1.onload= () => {
      this.ctx.drawImage(img1,this.board_card_width*0.8,this.board_card_height*0.8)
    }
    img2.onload= () => {
     this.ctx.drawImage(img2,this.board_card_width*0.8,this.board_card_height*0.8)
    }
  }

}
