import { NgModule, isDevMode } from '@angular/core';
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
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';
import { FlagComponent } from './components/flag/flag.component';
import { LookupImageComponent } from './components/lookup-image/lookup-image.component';
import { ErrorComponent } from './components/error/error.component';


const MaterialModules = [
  MatSnackBarModule,
  MatProgressBarModule,
  MatCardModule,
  MatIconModule,
  MatTooltipModule,
];
@NgModule({
  declarations: [
    AppComponent,
    LoaderComponent,
    IPInfoComponent,
    IPInfoComponent,
    LoaderComponent,
    FlagComponent,
    LookupImageComponent,
    ErrorComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
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
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
