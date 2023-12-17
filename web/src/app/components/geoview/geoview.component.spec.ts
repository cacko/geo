import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeoviewComponent } from './geoview.component';

describe('GeoviewComponent', () => {
  let component: GeoviewComponent;
  let fixture: ComponentFixture<GeoviewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GeoviewComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(GeoviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
