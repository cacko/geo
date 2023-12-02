import { NgModule, isDevMode, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

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
import { LocationBgDirective } from './directives/location-bg.directive';
import { MatDialogModule } from '@angular/material/dialog';
import { MapComponent } from './components/map/map.component';
import { MatButtonModule } from '@angular/material/button';
import { ConnectionComponent } from './components/connection/connection.component';
import { WebsocketService } from './service/websocket.service';
import { NgxLongPress2Module } from 'ngx-long-press2';
import { ClipboardModule } from '@angular/cdk/clipboard';
import { QueryInputComponent } from './components/query-input/query-input.component';
import { QueryButtonComponent } from './components/query-button/query-button.component';
import { MatIconModule, MatIconRegistry } from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar'; 
const MaterialModules = [
  MatSnackBarModule,
  MatProgressBarModule,
  MatCardModule,
  MatIconModule,
  MatTooltipModule,
  MatDialogModule,
  MatButtonModule,
  ClipboardModule,
  MatToolbarModule
];
@NgModule({
  declarations: [
    AppComponent,
    LoaderComponent,
    IPInfoComponent,
    IPInfoComponent,
    LoaderComponent,
    FlagComponent,
    ErrorComponent,
    LocationBgDirective,
    MapComponent,
    ConnectionComponent,
    QueryInputComponent,
    QueryButtonComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    NgxLongPress2Module,
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
    WebsocketService
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
