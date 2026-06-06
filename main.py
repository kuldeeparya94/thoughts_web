import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import Base, engine
from app.routers.thoughts import router as thoughts_router
from app.routers.interactions import router as interactions_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Thoughts Board", version="1.0")

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS","https://kuldeeparya94.github.io").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
def root():
    return "static/index.html"


# Routers
app.include_router(thoughts_router)
