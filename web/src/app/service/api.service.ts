import { Injectable, NgZone } from "@angular/core";
import {
  HttpClient,
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse,
} from "@angular/common/http";
import { Observable, Subject } from "rxjs";
import { ApiType } from "../entity/api.entity";
import { tap } from "rxjs/operators";
import { Params } from "@angular/router";
import { omitBy, isEmpty } from "lodash-es";
import * as md5 from "md5";
import * as moment from "moment";
import { LoaderService } from "./loader.service";
import { LookupModel } from "../models/lookup.model";
import { LocationModel } from "../models/location.model";

const b64encode = window.btoa;

interface CacheEntry {
  timestamp: moment.Moment;
  data: any;
}

@Injectable({ providedIn: "root" })
export class ApiService implements HttpInterceptor {
  static readonly API_MENU = "";
  static readonly CACHE_MINUTES = 5;
  static readonly API_BASEURL = "https://geo.cacko.net/api";

  renew = false;

  errorSubject = new Subject<string>();
  error = this.errorSubject.asObservable();

  backgroundSubject = new Subject<string>();
  $background = this.backgroundSubject.asObservable();

  lookupSubject = new Subject<LookupModel>();
  $lookup = this.lookupSubject.asObservable();
  locationSubject = new Subject<LocationModel>();
  $location = this.locationSubject.asObservable();

  constructor(
    private httpClient: HttpClient,
    private loader: LoaderService,
    private zone: NgZone
  ) { }

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {
    this.loader.show();
    return next.handle(req).pipe(
      tap(
        (event: HttpEvent<any>) => {
          if (event instanceof HttpResponse) {
            this.onEnd();
          }
        },
        (err: HttpErrorResponse) => {
          this.onEnd();
          this.errorSubject.next(err.message);
        }
      )
    );
  }
  private onEnd(): void {
    this.loader.hide();
  }


  fetch(type: ApiType, params: Params = {}, cache = true): Promise<any> {
    return new Promise((resolve, reject) => {
      const cacheKey = this.cacheKey(type, params);
      let url = `${ApiService.API_BASEURL}/${type}`;
      const cached = this.inCache(cacheKey);

      if ("path" in params) {
        url += "/" + params["path"];
        params["path"] = "";
      }

      if (cache && cached) {
        return resolve(cached);
      }

      this.httpClient
        .get(url, {
          params: omitBy(params, isEmpty),
        })
        .subscribe({
          next: (data) => {
            if (data && cache) {
              this.toCache(cacheKey, data);
            }
            return resolve(data);
          },
          error: (error) => {
            return reject(error);
          },
        });
    });
  }

  private cacheKey(type: ApiType, params: Params = {}): string {
    return md5(`${type}-${JSON.stringify(params)}`);
  }

  private inCache(key: string): any {
    const cached: string | null = localStorage.getItem(key);

    if (!cached) {
      return null;
    }

    const entry: CacheEntry = JSON.parse(cached);

    const age = moment.duration(moment().diff(entry.timestamp));

    if (age.asMinutes() > ApiService.CACHE_MINUTES) {
      return null;
    }

    return entry.data;
  }

  private toCache(key: string, data: any) {
    localStorage.setItem(
      key,
      JSON.stringify({ data: data, timestamp: moment() })
    );
  }
}
