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
        this.activeGames = this.sortByGamesHasStarted(games);
        console.log(games);
      }
    );
  }


  sortByGamesHasStarted(games: GameDto[]): GameDto[] {
    return games.sort((a: GameDto, b: GameDto) => {
      if (a.hasStarted && !b.hasStarted) {
        return 1;
      } else if (!a.hasStarted && b.hasStarted) {
        return -1;
      } else {
        return 0;
      }
    });
  }

}
