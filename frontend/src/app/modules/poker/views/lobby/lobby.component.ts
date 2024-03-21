import {Component} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {Observable} from "rxjs";
import * as io from "socket.io-client";
import {GameService} from "../../store/game.service";

@Component({
  selector: 'app-lobby',
  templateUrl: './lobby.component.html',
  styleUrls: ['./lobby.component.css']
})
export class LobbyComponent {
  gameId: string = "";


//public gameService: GameService,
  constructor(private route: ActivatedRoute,public gameService: GameService) {
    this.gameId = this.route.snapshot.queryParams["gameId"];
    this.gameService.joinGame(this.gameId);
  }



  startGame(){
    this.gameService.startGame()
  }
}
