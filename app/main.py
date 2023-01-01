from fastapi import Depends, FastAPI
from .routers import api
from fastapi.middleware.cors import CORSMiddleware
from app.frontend import init as frontend

app = FastAPI()

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

frontend(app=app)