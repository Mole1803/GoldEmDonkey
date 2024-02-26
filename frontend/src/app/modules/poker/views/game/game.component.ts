
import {Component, ViewChild} from '@angular/core';
@Component({
  selector: 'app-game',
  templateUrl: './game.component.html',
  styleUrls: ['./game.component.css']
})
export class GameComponent {
  // @ts-ignore
  public ctx:  any;
  @ViewChild('gameTable') set content(content:any){
    console.log(content.nativeElement)
    this.ctx = content.nativeElement.getContext("2d")
    this.ctx.canvas.width=3840
    this.ctx.canvas.height=2400


    console.log(this.ctx)
    let img = new Image()
    img.src='/assets/Media/tisch_komplett_plain.svg'
    img.onload= () => {
      this.ctx.drawImage(img,0,0,this.ctx.canvas.width,this.ctx.canvas.height)
    }
    this.drawCard('/assets/Media/Karten/herz2.svg',1)
    this.drawCard('/assets/Media/Karten/pik3.svg',2)
    this.drawCard('/assets/Media/Karten/karo4.svg',3)
    this.drawCard('/assets/Media/Karten/kreuzD.svg',4)
    this.drawCard('/assets/Media/Karten/herzK.svg',5)
  }
  drawCard(path:string,index:number){
    let img1 = new Image()
    img1.src=path
    img1.onload= () => {
      this.ctx.drawImage(img1,(0.098*(index-1)+0.268)*this.ctx.canvas.width,0.4475*this.ctx.canvas.height,this.ctx.canvas.width*0.087,this.ctx.canvas.height*0.215)
    }
  }

}
