from fastapi import FastAPI
from .database import engine, Base
from .routes import hashtags

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Media Analytics - Hashtag Engine")

# Routers
app.include_router(hashtags.router)

@app.get("/")
def root():
    return {"message": "Hashtag Engine is running!"}
