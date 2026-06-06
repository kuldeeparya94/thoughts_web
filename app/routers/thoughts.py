from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Thought, Like, Comment
from app.schemas import ThoughtCreate, ThoughtOut

router = APIRouter(prefix="/api", tags=["thoughts"])


def _enrich(thought: Thought, voter_token: str, db: Session) -> dict:
    like_count = db.query(Like).filter_by(thought_id=thought.id).count()
    liked      = db.query(Like).filter_by(thought_id=thought.id, voter_token=voter_token).first() is not None
    comments   = db.query(Comment).filter_by(thought_id=thought.id).order_by(Comment.created_at).all()
    d = {c.name: getattr(thought, c.name) for c in thought.__table__.columns}
    d.update(like_count=like_count, liked=liked, comments=comments)
    return d


@router.post("/thoughts", response_model=ThoughtOut, status_code=201)
def create_thought(body: ThoughtCreate, db: Session = Depends(get_db)):
    if not body.content or len(body.content.strip()) < 1:
        raise HTTPException(400, "Content cannot be empty")
    if len(body.content) > 500:
        raise HTTPException(400, "Content too long (max 500 chars)")
    thought = Thought(
        author      = (body.author or "Anonymous")[:50],
        content     = body.content.strip(),
        owner_token = body.owner_token,
    )
    db.add(thought)
    db.commit()
    db.refresh(thought)
    return thought


@router.get("/thoughts", response_model=list[ThoughtOut])
def list_thoughts(skip: int = 0, limit: int = 50, voter_token: str = "", db: Session = Depends(get_db)):
    thoughts = (
        db.query(Thought)
        .order_by(Thought.created_at.desc())
        .offset(skip).limit(limit).all()
    )
    return [_enrich(t, voter_token, db) for t in thoughts]


@router.delete("/thoughts/{thought_id}", status_code=204)
def delete_thought(thought_id: int, token: str = "", db: Session = Depends(get_db)):
    thought = db.query(Thought).filter(Thought.id == thought_id).first()
    if not thought:
        raise HTTPException(404, "Thought not found")
    if thought.owner_token and thought.owner_token != token:
        raise HTTPException(403, "Not allowed")
    db.delete(thought)
    db.commit()


@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    total   = db.query(func.count(Thought.id)).scalar()
    writers = db.query(func.count(func.distinct(Thought.author))).scalar()
    return {"total_thoughts": total, "unique_writers": writers}
