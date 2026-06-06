from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional
import os

# ── Database ──────────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./thoughts.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class Thought(Base):
    __tablename__ = "thoughts"
    id         = Column(Integer, primary_key=True, index=True)
    author     = Column(String, default="Anonymous")
    content    = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Schemas ───────────────────────────────────────────────────────────────────
class ThoughtCreate(BaseModel):
    author:  Optional[str] = "Anonymous"
    content: str           # 1–500 chars validated below

    class Config:
        str_strip_whitespace = True


class ThoughtOut(BaseModel):
    id:         int
    author:     str
    content:    str
    created_at: datetime

    class Config:
        from_attributes = True


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Thoughts Board", version="1.0")

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Serve the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
def root():
    return "static/index.html"


# ── API Routes ─────────────────────────────────────────────────────────────────
@app.post("/api/thoughts", response_model=ThoughtOut, status_code=201)
def create_thought(body: ThoughtCreate, db: Session = Depends(get_db)):
    if not body.content or len(body.content.strip()) < 1:
        raise HTTPException(400, "Content cannot be empty")
    if len(body.content) > 500:
        raise HTTPException(400, "Content too long (max 500 chars)")
    thought = Thought(
        author  = (body.author or "Anonymous")[:50],
        content = body.content.strip(),
    )
    db.add(thought)
    db.commit()
    db.refresh(thought)
    return thought


@app.get("/api/thoughts", response_model=list[ThoughtOut])
def list_thoughts(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return (
        db.query(Thought)
        .order_by(Thought.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@app.delete("/api/thoughts/{thought_id}", status_code=204)
def delete_thought(thought_id: int, db: Session = Depends(get_db)):
    thought = db.query(Thought).filter(Thought.id == thought_id).first()
    if not thought:
        raise HTTPException(404, "Thought not found")
    db.delete(thought)
    db.commit()


@app.get("/api/stats")
def stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Thought.id)).scalar()
    return {"total_thoughts": total}
 