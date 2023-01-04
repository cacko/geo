from fastapi import FastAPI, Header, Request, HTTPException
from nicegui import ui, Client
from app.config import app_config
from pathlib import Path
from app.geo.maxmind import MaxMind, GeoInfo
from app.geo.lookup_image import LookupImage
from app.core.ip import get_remote_ip
from pydantic import BaseModel, Field
import flag
from typing import Optional
import logging

ASSETS = Path(__file__).parent / 'assets'


class InfoRow(BaseModel):
    label: str
    value: str

    @property
    def display(self):
        return self.value

    @property
    def isEmpty(self) -> bool:
        return len(self.value.strip()) < 1

class IPRow(InfoRow):
    label = "IP"

class CountryRow(InfoRow):
    label = "Country"
    iso_code: str

    @property
    def display(self):
        return f"{self.value} {flag.flag(self.iso_code)}"

class CityRow(InfoRow):
    label = "City"

class GPSRow(InfoRow):
    label = "GPS"

class TimezoneRow(InfoRow):
    label = "Timezone"

class OwnerRow(InfoRow):
    label = "Owner"
    value: str
    id: Optional[int] = None


class InfoData:

    __geo: GeoInfo

    def __init__(self, geo: GeoInfo):
        self.__geo = geo

    def get_data(self) -> list[InfoRow]:
        return list(filter(lambda x: not x.isEmpty, [
            IPRow(value=self.__geo.ip),
            CountryRow(value=self.__geo.country, iso_code=self.__geo.country_iso),
            CityRow(value=self.__geo.city),
            GPSRow(value=",".join(map(str, self.__geo.location))),
            TimezoneRow(value=self.__geo.timezone),
            OwnerRow(value=self.__geo.ISP.name, id=self.__geo.ISP.id),
        ]))


def init(app: FastAPI) -> None:
    @ui.page("/")
    async def main_page(
        client: Client,
        request: Request,
        ip: str = "",
        x_forwarded_for: str | None = Header(default=None),
    ):
        if app_config.log.level == "DEBUG":
            ui.add_static_files("/bg", app_config.web.backgrounds)
        ui.add_static_files("/assets", (ASSETS / "icons").as_posix())
        client.content.classes(remove="q-pa-md gap-4")
        ui.add_head_html(
            f"<style>{(ASSETS / 'css' / 'main.css').read_text()}</style>"
        )
        ui.add_head_html('<meta name="viewport" content="width=device-width, initial-scale=1">')
        ui.add_head_html('<link rel="manifest" href="/assets/site.webmanifest">')
        ui.add_head_html('<link rel="preconnect" href="https://fonts.gstatic.com">')
        ui.add_head_html(
            '<link href="https://fonts.googleapis.com/css2?family=Bubblegum+Sans&amp;family=Syne+Mono&amp;display=swap" rel="stylesheet" />'
        )

        container = (
            ui.row()
            .classes("w-full h-screen items-center no-wrap root loading")
            .style('background-image: url("/bg/loading.png")')
        )
        with container:
            info_container = ui.row().classes("w-full info-container")
            with info_container:
                if not ip:
                    ip = get_remote_ip(request.client.host, x_forwarded_for)
                geo = MaxMind.lookup(ip)
                info = InfoData(geo=geo)
                with ui.row().classes(add="content-data", remove="gap-4"):
                    for row in info.get_data():
                        with ui.row().classes("info-row items-center"):
                            ui.label(row.label).classes("label")
                            ui.label(row.display)

                    def get_bg():
                        image = LookupImage(geo=geo)
                        image_path = image.path
                        name = image_path.name
                        dst = Path(app_config.web.backgrounds) / name
                        dst.write_bytes(image_path.read_bytes())
                        container.style(f'background-image: url("/bg/{name}")')
                        container.classes(remove="loading")

                    ui.timer(0.1, get_bg, once=True)

    ui.run_with(app, dark=True, title="Geo", favicon=(ASSETS / "icons" / "favicon.ico").as_posix())
