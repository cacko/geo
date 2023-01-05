import { Component, Input, OnInit } from '@angular/core';
import { LookupEntity } from 'src/app/entity/lookup.entity';

@Component({
  selector: 'app-error',
  templateUrl: './error.component.html',
  styleUrls: ['./error.component.scss']
})
export class ErrorComponent {


  @Input() lookup!: LookupEntity;

}
