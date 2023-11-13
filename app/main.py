from fastapi import FastAPI
from .routers import api, ws
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    app = FastAPI(
        title="geo@cacko.net",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        redoc_url="/api/redoc"
    )

    origins = [
        "http://localhost:4200",
        "https://geo.cacko.net"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api.router)
    app.include_router(ws.router)

    return app
