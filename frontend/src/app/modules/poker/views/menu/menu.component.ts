import {Component, OnDestroy} from '@angular/core';
import {GameHttpService} from "../../services/game-http.service";
import {GameDto} from "../../models/game-dto";
import {root} from "postcss";
import {ActivatedRoute, Router} from "@angular/router";
import {GameService} from "../../store/game.service";
import {Subscriber, Subscription} from "rxjs";

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnDestroy{
  activeGames: GameDto[] = [];
  subscribers: Subscription = new Subscriber();

  constructor(private gameHttpService: GameHttpService,public route: ActivatedRoute, public gameService: GameService, private router: Router) {
    this.listActiveGames();
    this.subscribeToGameCreated();
  }

  public subscribeToGameCreated(): void {
    this.subscribers.add(this.gameService.gameCreated.subscribe((data) => {
      this.navigateToGame(data);
    }));

  }

  ngOnDestroy(): void {
    this.subscribers.unsubscribe();
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

  navigateToGame(gameId: string): void {
    this.router.navigate([{outlets: {pokeroutlet: ['lobby']}}], {queryParams: {gameId: gameId}});

  }

  createGame(): void {
    this.gameService.createGame();
    // redirect to lobby (lobby is sub router outlet


  }

  protected readonly root = root;
}
