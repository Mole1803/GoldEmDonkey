import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import {GameService} from "../../store/game.service";

@Component({
  selector: 'app-action-modal',
  templateUrl: './action-modal.component.html',
  styleUrls: ['./action-modal.component.css']
})
export class ActionModalComponent {

  isVisible: boolean = true;
  options = [
    { name: 'Fold' },
    { name: 'Raise' },
    { name: 'Call' },
    { name: 'All in' }
  ];
  selectedOption = this.options[0].name;

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
    if (this.form.valid) {
      this.isVisible = false;
      console.log(this.form.value);
      // todo send action to server
    }
  }
}
