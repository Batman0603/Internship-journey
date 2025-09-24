from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Many-to-many relationship between posts and hashtags
post_hashtag = Table(
    "post_hashtag",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("hashtag_id", ForeignKey("hashtags.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)

    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(500), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    hashtags = relationship("Hashtag", secondary=post_hashtag, back_populates="posts")

class Hashtag(Base):
    __tablename__ = "hashtags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    posts = relationship("Post", secondary=post_hashtag, back_populates="hashtags")
