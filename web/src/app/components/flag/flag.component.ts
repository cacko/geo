import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-flag',
  templateUrl: './flag.component.html',
  styleUrls: ['./flag.component.scss']
})
export class FlagComponent implements OnInit {

  @Input() isoCode!: string;

  flag?: string;

  ngOnInit(): void {
    this.flag = this.getEmoji();
  }

  private getEmoji(): string {
    return this.isoCode.replace(/./g, (ch) => String.fromCodePoint(0x1f1a5 + ch.toUpperCase().charCodeAt(0)))
  }


}
