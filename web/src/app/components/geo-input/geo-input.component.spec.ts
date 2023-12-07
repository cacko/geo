import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeoInputComponent } from './geo-input.component';

describe('GeoInputComponent', () => {
  let component: GeoInputComponent;
  let fixture: ComponentFixture<GeoInputComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GeoInputComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GeoInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
