import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IPInfoComponent } from './ipinfo.component';

describe('IPInfoComponent', () => {
  let component: IPInfoComponent;
  let fixture: ComponentFixture<IPInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ IPInfoComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(IPInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
