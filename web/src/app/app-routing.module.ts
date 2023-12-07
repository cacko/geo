import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ErrorComponent } from './components/error/error.component';
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
//   {
//     path: 'login',
//     component: LoginComponent,
//     pathMatch: 'full',
//   },
//   {
//     path: 'privacy',
//     component: PrivacyComponent,
//     pathMatch: 'full',
//   },
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes),
  ],
  exports: [RouterModule],
})
export class AppRoutingModule {}
