import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QueryButtonComponent } from './query-button.component';

describe('QueryButtonComponent', () => {
  let component: QueryButtonComponent;
  let fixture: ComponentFixture<QueryButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QueryButtonComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(QueryButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
