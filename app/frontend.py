from fastapi import FastAPI, Header, Request, HTTPException
from nicegui import ui, Client
from app.config import app_config
from pathlib import Path
from app.geo.maxmind import MaxMind, GeoInfo
from app.geo.lookup_image import LookupImage
from app.core.ip import get_remote_ip
from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Optional
from dataclasses import dataclass, field, asdict
import logging



@dataclass
class InfoRow:
    label: str
    value: str


class InfoData:

    __geo: GeoInfo

    def __init__(self, geo: GeoInfo):
        self.__geo = geo
    
    def get_data(self) -> list[InfoRow]:
        return [
            InfoRow("IP", self.__geo.ip),
            InfoRow("Country", self.__geo.country),
            InfoRow("City", self.__geo.city),
            InfoRow("GPS", ",".join(map(str, self.__geo.location))),
            InfoRow("Timezone", self.__geo.timezone),
            InfoRow("Owner", self.__geo.ISP.name)
        ]


def init(app: FastAPI) -> None:
    @ui.page("/")
    async def main_page(
        client: Client,
        request: Request,
        ip: str = "",
        x_forwarded_for: str | None = Header(default=None),
    ):
        client.content.classes(remove="q-pa-md gap-4")
        ui.add_head_html(
            f"<style>{(Path(__file__).parent / 'css' / 'main.css').read_text()}</style>"
        )
        ui.add_static_files("/b", app_config.web.backgrounds)
        container = (
            ui.row()
            .classes("w-full h-screen items-center no-wrap root loading")
            .style('background-image: url("/b/loading.png")')
        )
        with container:
            info_container = ui.row().classes("w-full info-container")
            with info_container:
                ip = get_remote_ip(request.client.host, x_forwarded_for)
                geo = MaxMind.lookup(ip)
                info = InfoData(geo=geo)
                for row in info.get_data():
                    with ui.row().classes("info-row"):
                        ui.label(row.label).classes("label")
                        ui.label(row.value)

                def get_bg():
                    image = LookupImage(name=f"{geo.country}, {geo.city}")
                    image_path = image.path
                    name = image_path.name
                    dst = Path(app_config.web.backgrounds) / name
                    dst.write_bytes(image_path.read_bytes())
                    container.style(f'background-image: url("/b/{name}")')
                    container.classes(remove="loading")



                ui.timer(0.1, get_bg, once=True)


    ui.run_with(app, dark=True, title="Geo")
