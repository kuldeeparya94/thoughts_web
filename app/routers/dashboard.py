from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models import Thought, Like, Comment, SiteVisit

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.post("/visit", status_code=204)
def record_visit(db: Session = Depends(get_db)):
    db.add(SiteVisit())
    db.commit()


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    total_thoughts = db.query(func.count(Thought.id)).scalar()
    total_writers  = db.query(func.count(func.distinct(Thought.author))).scalar()
    total_visits   = db.query(func.count(SiteVisit.id)).scalar()
    total_likes    = db.query(func.count(Like.id)).scalar()
    total_comments = db.query(func.count(Comment.id)).scalar()

    # Top 5 posts by likes
    top_liked = (
        db.query(Thought, func.count(Like.id).label("likes"))
        .outerjoin(Like, Like.thought_id == Thought.id)
        .group_by(Thought.id)
        .order_by(func.count(Like.id).desc())
        .limit(5).all()
    )

    # Top 5 posts by comments
    top_commented = (
        db.query(Thought, func.count(Comment.id).label("comments"))
        .outerjoin(Comment, Comment.thought_id == Thought.id)
        .group_by(Thought.id)
        .order_by(func.count(Comment.id).desc())
        .limit(5).all()
    )

    # Top writers by thought count
    top_writers = (
        db.query(Thought.author, func.count(Thought.id).label("count"))
        .group_by(Thought.author)
        .order_by(func.count(Thought.id).desc())
        .limit(5).all()
    )

    return {
        "total_thoughts": total_thoughts,
        "total_writers":  total_writers,
        "total_visits":   total_visits,
        "total_likes":    total_likes,
        "total_comments": total_comments,
        "top_liked": [
            {"id": t.id, "author": t.author, "content": t.content[:80], "likes": likes}
            for t, likes in top_liked
        ],
        "top_commented": [
            {"id": t.id, "author": t.author, "content": t.content[:80], "comments": comments}
            for t, comments in top_commented
        ],
        "top_writers": [
            {"author": author, "count": count}
            for author, count in top_writers
        ],
    }
