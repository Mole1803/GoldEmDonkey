import { Component } from '@angular/core';
import {GameHttpService} from "../../services/game-http.service";
import {GameDto} from "../../models/game-dto";

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {
  activeGames: GameDto[] = [];

  constructor(private gameHttpService: GameHttpService) {
    this.listActiveGames();
  }

  public listActiveGames(): void {
    this.gameHttpService.listActiveGames().subscribe(
      (games: GameDto[]) => {
        this.activeGames = games;
        console.log(games);
      }
    );
  }
}
