from pydantic import BaseModel

class ShortenURLRequest(BaseModel):
    url: str

class ShortenedURLResponse(BaseModel):
    short_id: str
    full_url: str

class URLStatsResponse(BaseModel):
    short_id: str
    full_url: str
