from pydantic import BaseModel
from typing import List

class HashtagBase(BaseModel):
    name: str

class HashtagCreate(HashtagBase):
    pass

class HashtagOut(HashtagBase):
    id: int
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    content: str

class PostOut(PostBase):
    id: int
    hashtags: List[HashtagOut] = []
    class Config:
        orm_mode = True
