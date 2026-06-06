import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import Base, engine
from app.routers.thoughts import router as thoughts_router
from app.routers.interactions import router as interactions_router
from app.routers.dashboard import router as dashboard_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Thoughts Board", version="1.0")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Pages ──
@app.get("/", response_class=FileResponse)
def root():
    return "static/home.html"


@app.get("/thoughts", response_class=FileResponse)
def thoughts_page():
    return "static/index.html"


@app.get("/dashboard", response_class=FileResponse)
def dashboard_page():
    return "static/dashboard.html"


# ── API Routers ──
app.include_router(thoughts_router)
app.include_router(interactions_router)
app.include_router(dashboard_router)
