import { NgModule, isDevMode, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LoaderComponent } from './components/loader/loader.component';
import { ApiService } from './service/api.service';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { IPInfoComponent } from './components/ipinfo/ipinfo.component';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatProgressBarModule } from '@angular/material/progress-bar'
import { MatCardModule } from '@angular/material/card';
import { MatTooltipModule } from '@angular/material/tooltip';
import { FlagComponent } from './components/flag/flag.component';
import { ErrorComponent } from './components/error/error.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MapComponent } from './components/map/map.component';
import { MatButtonModule } from '@angular/material/button';
import { ConnectionComponent } from './components/connection/connection.component';
import { WebsocketService } from './service/websocket.service';
import { ClipboardModule } from '@angular/cdk/clipboard';
import { QueryInputComponent } from './components/query-input/query-input.component';
import { QueryButtonComponent } from './components/query-button/query-button.component';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { LocationinfoComponent } from './components/locationinfo/locationinfo.component';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatInputModule } from '@angular/material/input';
import {
  MatFormFieldModule,
  MAT_FORM_FIELD_DEFAULT_OPTIONS,
} from '@angular/material/form-field';
import {MatChipsModule} from '@angular/material/chips'; 
import { GeoInputComponent } from './components/geo-input/geo-input.component';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { LoaderService } from './service/loader.service';
import { StorageService } from './service/storage.service';
import { NgxView360Module } from '@egjs/ngx-view360';
import { GeoviewComponent } from './components/geoview/geoview.component';
import { StylesComponent } from './components/styles/styles.component';
import {MatMenuModule} from '@angular/material/menu'; 
import {MatBadgeModule} from '@angular/material/badge'; 
const MaterialModules = [
  MatSnackBarModule,
  MatProgressBarModule,
  MatCardModule,
  MatIconModule,
  MatTooltipModule,
  MatDialogModule,
  MatButtonModule,
  ClipboardModule,
  MatToolbarModule,
  DragDropModule,
  MatSlideToggleModule,
  MatInputModule,
  MatFormFieldModule,
  MatButtonToggleModule,
  MatChipsModule,
  MatMenuModule,
  MatBadgeModule
];
@NgModule({
  declarations: [
    AppComponent,
    LoaderComponent,
    IPInfoComponent,
    LocationinfoComponent,
    LoaderComponent,
    FlagComponent,
    ErrorComponent,
    MapComponent,
    ConnectionComponent,
    QueryInputComponent,
    QueryButtonComponent,
    GeoInputComponent, 
    GeoviewComponent,
    StylesComponent
  ],
  imports: [
    BrowserModule,
    NgxView360Module,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    ServiceWorkerModule.register('ngsw-worker.js', {
      enabled: !isDevMode(),
      // Register the ServiceWorker as soon as the application is stable
      // or after 30 seconds (whichever comes first).
      registrationStrategy: 'registerWhenStable:30000'
    }),
    BrowserAnimationsModule,
    ...MaterialModules
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ApiService,
      multi: true,
    },
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: { subscriptSizing: 'dynamic' },
    },
    WebsocketService,
    LoaderService,
    StorageService
  ],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],

})
export class AppModule {

  constructor(private readonly iconRegistry: MatIconRegistry) {
    const defaultFontSetClasses = iconRegistry.getDefaultFontSetClass();
    const outlinedFontSetClasses = defaultFontSetClasses
      .filter((fontSetClass) => fontSetClass !== 'material-icons')
      .concat(['material-symbols-outlined']);
    iconRegistry.setDefaultFontSetClass(...outlinedFontSetClasses);
  }

}
