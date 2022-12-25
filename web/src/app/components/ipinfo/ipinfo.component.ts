import { Component, Input } from '@angular/core';
import { LookupEntity } from 'src/app/entity/lookup.entity';

@Component({
  selector: 'app-ipinfo',
  templateUrl: './ipinfo.component.html',
  styleUrls: ['./ipinfo.component.scss']
})
export class IPInfoComponent {

  @Input() lookup!: LookupEntity;


}
