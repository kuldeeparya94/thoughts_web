from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ThoughtCreate(BaseModel):
    author:      Optional[str] = "Anonymous"
    content:     str
    owner_token: Optional[str] = None

    model_config = {"str_strip_whitespace": True}


class CommentOut(BaseModel):
    id:         int
    author:     str
    content:    str
    created_at: datetime

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    author:  Optional[str] = "Anonymous"
    content: str

    model_config = {"str_strip_whitespace": True}


class ThoughtOut(BaseModel):
    id:          int
    author:      str
    content:     str
    created_at:  datetime
    owner_token: Optional[str] = None
    like_count:  int = 0
    liked:       bool = False
    comments:    list[CommentOut] = []

    model_config = {"from_attributes": True}
