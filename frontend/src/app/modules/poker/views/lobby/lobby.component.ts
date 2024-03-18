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



  constructor(private route: ActivatedRoute, public gameService: GameService) {
    this.route.queryParams.subscribe(
      (params) => {
        this.gameId = params["gameId"];
      });
  }
}
