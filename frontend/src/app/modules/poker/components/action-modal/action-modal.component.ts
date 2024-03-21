import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import {GameService} from "../../store/game.service";
import {PlayerDto} from "../../models/player-dto";

@Component({
  selector: 'app-action-modal',
  templateUrl: './action-modal.component.html',
  styleUrls: ['./action-modal.component.css']
})
export class ActionModalComponent {

  isVisible: boolean = true;
  options = [
    { id: 0, name: 'Fold' },
    { id: 1, name: 'Check' },
    { id: 2, name: 'Call' },
    { id: 3, name: 'Raise' }
  ];
  selectedOption = this.options[0].id;

  form: FormGroup;

  constructor(private gameService: GameService) {
    this.form = new FormGroup({
      bet: new FormControl('', [Validators.required, Validators.min(0)]), // Set validators in form initialization
      selectedOption: new FormControl(this.selectedOption) // added selectedOption FormControl
    });

    this.form.valueChanges.subscribe((value) => {
      if (value.bet < 0) {
        // If the value is < 0, reset the control's value to 0.
        this.form.controls['bet'].setValue(0, {emitEvent: false});  // added second argument to prevent infinite loop
      }
    });

    gameService.clientAtMove.subscribe((value) => {
      this.isVisible = true;
    })
  }

  submit() {
    this.isVisible = false;
    this.gameMove(this.options[this.form.value.selectedOption].id, this.form.value.bet??0);
    console.log(this.form.value);
      // todo send action to server

  }

    gameMove(action: number, value: number) {
    /*if(!this.isPlayerMoveClient(player)){
      return;
    }*/

    switch (action) {
      case 0:
        this.gameService.sendPerformFold();
        break;
      case 1:
        this.gameService.sendPerformCheck();
        break;
      case 2:
        this.gameService.sendPerformCall();
        break;
      case 3:
        this.gameService.sendPerformRaise(value);
        break;
      default:
        console.log("Invalid action");
    }
  }
}
