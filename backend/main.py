import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import admin, analytics, auth, pets, recommend, ws


app = FastAPI(
    title="FurFinds",
    description="Find. Adopt. Love.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
configured_origins = os.getenv("CORS_ORIGINS", "")
allow_origins = [origin.strip() for origin in configured_origins.split(",") if origin.strip()] or default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    # Accept local frontend dev ports like 5173/5174 consistently.
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pets.router)
app.include_router(recommend.router)
app.include_router(ws.router)
app.include_router(analytics.router)
app.include_router(auth.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "Welcome to FurFinds API"}
