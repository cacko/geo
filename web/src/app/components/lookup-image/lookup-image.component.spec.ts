import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LookupImageComponent } from './lookup-image.component';

describe('LookupImageComponent', () => {
  let component: LookupImageComponent;
  let fixture: ComponentFixture<LookupImageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LookupImageComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LookupImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
