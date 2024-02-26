import {Component} from '@angular/core';
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-lobby',
  templateUrl: './lobby.component.html',
  styleUrls: ['./lobby.component.css']
})
export class LobbyComponent {
  gameId: string = "";
  constructor(private route: ActivatedRoute) {
    this.route.queryParams.subscribe(
      (params) => {
        this.gameId = params["gameId"];
      });
  }
}
