import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { MatChipListboxChange } from '@angular/material/chips';
import { isString } from 'lodash-es';
import { StorageService } from 'src/app/service/storage.service';

@Component({
  selector: 'app-styles',
  templateUrl: './styles.component.html',
  styleUrl: './styles.component.scss'
})
export class StylesComponent {


  @Input() current: string = "";

  constructor(
    public storage: StorageService
  ) {

  }
  ngOnInit(): void {
  }
  readonly categories: string[] = Object.values(this.storage.styles).filter(isString);
  @Input() selected : string = "";

  @Output() change = new EventEmitter<string[]>();


  onChange(ev: MatChipListboxChange) {
    this.change.emit(ev.value);
  }

}
