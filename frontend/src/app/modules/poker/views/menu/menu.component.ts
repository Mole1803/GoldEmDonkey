import { Component } from '@angular/core';
import {GameHttpService} from "../../services/game-http.service";
import {GameDto} from "../../models/game-dto";
import {root} from "postcss";
import {ActivatedRoute, Router} from "@angular/router";
import {GameService} from "../../store/game.service";

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {
  activeGames: GameDto[] = [];

  constructor(private gameHttpService: GameHttpService,public route: ActivatedRoute, public gameService: GameService, private router: Router) {
    this.listActiveGames();
  }

  public listActiveGames(): void {
    this.gameHttpService.listActiveGames().subscribe(
      (games: GameDto[]) => {
        this.activeGames = this.sortByGamesHasStarted(games);
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

  createGame(): void {
    this.gameService.createGame();
    // redirect to lobby (lobby is sub router outlet
    this.router.navigate([{outlets: {pokeroutlet: ['lobby']}}]);

  }

  protected readonly root = root;
}
