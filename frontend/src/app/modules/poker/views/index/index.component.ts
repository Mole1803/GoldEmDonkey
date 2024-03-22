import {Component, OnInit} from '@angular/core';
import {io} from "socket.io-client";
import {GameDto} from "../../models/game-dto";
import {GameService} from "../../store/game.service";
import {Routing} from "../../../auth/enum/routing";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-index',
  templateUrl: './index.component.html',
  styleUrls: ['./index.component.css']
})
export class IndexComponent implements OnInit{

  constructor(private router: Router, public activatedRoute: ActivatedRoute ) {//public gameService: GameService,

  }
  ngOnInit(): void {
  this.activatedRoute.url.subscribe(url =>{
    if(url.length === 0) { // If route is index
      this.router.navigate([{ outlets : { pokeroutlet: ['menu']}}]); // navigate to menu
    }
  });
}


}
