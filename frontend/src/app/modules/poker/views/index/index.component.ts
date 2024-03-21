import { Component } from '@angular/core';
import {io} from "socket.io-client";
import {GameDto} from "../../models/game-dto";
import {GameService} from "../../store/game.service";

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css']
})
export class IndexComponent {

  constructor( ) {//public gameService: GameService,
  }


}
