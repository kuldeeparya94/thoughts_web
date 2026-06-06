from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Thought, Like, Comment
from app.schemas import CommentCreate, CommentOut

router = APIRouter(prefix="/api", tags=["interactions"])


@router.post("/thoughts/{thought_id}/like", status_code=200)
def toggle_like(thought_id: int, voter_token: str, db: Session = Depends(get_db)):
    thought = db.query(Thought).filter(Thought.id == thought_id).first()
    if not thought:
        raise HTTPException(404, "Thought not found")
    existing = db.query(Like).filter_by(thought_id=thought_id, voter_token=voter_token).first()
    if existing:
        db.delete(existing)
        db.commit()
        liked = False
    else:
        db.add(Like(thought_id=thought_id, voter_token=voter_token))
        db.commit()
        liked = True
    count = db.query(Like).filter_by(thought_id=thought_id).count()
    return {"liked": liked, "like_count": count}


@router.get("/thoughts/{thought_id}/comments", response_model=list[CommentOut])
def list_comments(thought_id: int, db: Session = Depends(get_db)):
    if not db.query(Thought).filter(Thought.id == thought_id).first():
        raise HTTPException(404, "Thought not found")
    return db.query(Comment).filter_by(thought_id=thought_id).order_by(Comment.created_at).all()


@router.post("/thoughts/{thought_id}/comments", response_model=CommentOut, status_code=201)
def add_comment(thought_id: int, body: CommentCreate, db: Session = Depends(get_db)):
    if not db.query(Thought).filter(Thought.id == thought_id).first():
        raise HTTPException(404, "Thought not found")
    if not body.content or len(body.content.strip()) < 1:
        raise HTTPException(400, "Comment cannot be empty")
    if len(body.content) > 300:
        raise HTTPException(400, "Comment too long (max 300 chars)")
    comment = Comment(
        thought_id = thought_id,
        author     = (body.author or "Anonymous")[:50],
        content    = body.content.strip(),
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(404, "Comment not found")
    db.delete(comment)
    db.commit()
