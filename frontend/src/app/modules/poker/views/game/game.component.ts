
import {Component, ViewChild} from '@angular/core';
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
      this.drawPlayer("r",15,0,true,'/assets/Media/Karten/rueckseite.svg',"n")
      this.drawPlayer("r",15,1,true,'/assets/Media/Karten/rueckseite.svg',"n")
      this.drawPlayer("r",15,2,true,'/assets/Media/Karten/rueckseite.svg',"n")
      this.drawPlayer("r",15,3,true,'/assets/Media/Karten/rueckseite.svg',"n")
      this.drawPlayer("r",15,4,true,'/assets/Media/Karten/rueckseite.svg',"n")
      this.drawPlayer("r",15,5,true,'/assets/Media/Karten/rueckseite.svg',"n")
      this.drawPlayer("r",15,6,true,'/assets/Media/Karten/rueckseite.svg',"n")
    }
    this.drawCard('/assets/Media/Karten/rueckseite.svg',1)
    this.drawCard('/assets/Media/Karten/pik3.svg',2)
    this.drawCard('/assets/Media/Karten/karo4.svg',3)
    this.drawCard('/assets/Media/Karten/kreuzD.svg',4)
    this.drawCard('/assets/Media/Karten/herzK.svg',5)

  }
  drawCard(path:string,index:number){
    let img1 = new Image()
    img1.src=path
    img1.onload= () => {
      this.ctx.drawImage(img1,(0.098*(index-1)+0.268)*this.ctx.canvas.width,0.4475*this.ctx.canvas.height,this.board_card_width,this.board_card_height)
    }
  }

  drawPlayer(name:string,chips:number,position:number,active:boolean,card1:string,card2:string){
    let mid = this.ctx.canvas.width/2-300
    let y,x;
    switch(position){
      case 0:
      case 6:
        y=this.ctx.canvas.height*0.65
        x=mid+(3-position)*500
        break
      case 1:
      case 3:
      case 5:
        x=x=mid+(3-position)*600
        y=this.ctx.canvas.height*0.2
        break
      case 2:
      case 4:
        x=mid+(3-position)*700
        y=this.ctx.canvas.height*0.93
        break

    }
    this.ctx.fillRect(x, y, 600, 150)
    /*let img1 = new Image()
    img1.src=card1
    img1.onload= () => {
      this.ctx.drawImage(img1,this.board_card_width*0.8,this.board_card_height*0.8)
    }*/
  }

}
