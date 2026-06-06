from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Thought(Base):
    __tablename__ = "thoughts"
    id          = Column(Integer, primary_key=True, index=True)
    author      = Column(String, default="Anonymous")
    content     = Column(String, nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    owner_token = Column(String, nullable=True)
    likes       = relationship("Like",    back_populates="thought", cascade="all, delete-orphan")
    comments    = relationship("Comment", back_populates="thought", cascade="all, delete-orphan")


class Like(Base):
    __tablename__ = "likes"
    id          = Column(Integer, primary_key=True, index=True)
    thought_id  = Column(Integer, ForeignKey("thoughts.id"), nullable=False)
    voter_token = Column(String, nullable=False)
    thought     = relationship("Thought", back_populates="likes")


class Comment(Base):
    __tablename__ = "comments"
    id          = Column(Integer, primary_key=True, index=True)
    thought_id  = Column(Integer, ForeignKey("thoughts.id"), nullable=False)
    author      = Column(String, default="Anonymous")
    content     = Column(String, nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    thought     = relationship("Thought", back_populates="comments")


class SiteVisit(Base):
    __tablename__ = "site_visits"
    id         = Column(Integer, primary_key=True, index=True)
    visited_at = Column(DateTime, default=datetime.utcnow)
