import { Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-geo-input',
  templateUrl: './geo-input.component.html',
  styleUrl: './geo-input.component.scss'
})
export class GeoInputComponent {
  form: FormGroup;
  geoInput = new FormControl('');
  constructor(
    private builder: FormBuilder,
    public dialogRef: MatDialogRef<string>,
  ) {
    this.form = this.builder.group({
      geoInput: this.geoInput,
    });
  }

  submitForm() {
    const input = this.geoInput.value || '';
    this.geoInput.reset();
    this.dialogRef.close(input.trim());
  }

  triggerSubmit($event: any) {

  }

}
