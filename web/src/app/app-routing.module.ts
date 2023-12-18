import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { IPInfoComponent } from './components/ipinfo/ipinfo.component';
import { LocationinfoComponent } from './components/locationinfo/locationinfo.component';


const routes: Routes = [
  {
    path: 'ip/:ip',
    component: IPInfoComponent,
    pathMatch: 'full',
    title: "ip"
  },
  {
    path: 'location/:location',
    component: LocationinfoComponent,
    pathMatch: 'full',
    title: "location"
  },
];
@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      enableTracing: false,
      anchorScrolling: "enabled",
      scrollPositionRestoration: "enabled",
      useHash: true
    })
  ],
  exports: [RouterModule],
})
export class AppRoutingModule { }
