from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uuid
from models import ShortenedURL
from schemas import ShortenURLRequest, ShortenedURLResponse, URLStatsResponse

DATABASE_URL = "sqlite:///./data/shorturl.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/shorten", response_model=ShortenedURLResponse)
def shorten_url(request: ShortenURLRequest):
    db: Session = SessionLocal()
    short_id = str(uuid.uuid4())[:8]
    db_item = ShortenedURL(short_id=short_id, full_url=request.url)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"short_id": db_item.short_id, "full_url": db_item.full_url}

@app.get("/{short_id}")
def redirect(short_id: str):
    db: Session = SessionLocal()
    item = db.query(ShortenedURL).filter(ShortenedURL.short_id == short_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"url": item.full_url}

@app.get("/stats/{short_id}", response_model=URLStatsResponse)
def url_stats(short_id: str):
    db: Session = SessionLocal()
    item = db.query(ShortenedURL).filter(ShortenedURL.short_id == short_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return {"short_id": item.short_id, "full_url": item.full_url}
