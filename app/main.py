from fastapi import FastAPI
import httpx
from sqlmodel import SQLModel, Session, create_engine, select
from app.models import Cat
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# --- Константи для зовнішніх API ---
CAT_IMAGE_URL = "https://api.thecatapi.com/v1/images/search"
CAT_FACT_URL = "https://catfact.ninja/fact"

# --- БД ---
DATABASE_URL = "sqlite:///kotiki.db"
engine = create_engine(DATABASE_URL)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "Привіт, котики!"}

@app.get("/random_cat")
def get_random_cat():
    try:
        image_response = httpx.get(CAT_IMAGE_URL)
        image_url = image_response.json()[0]["url"]

        fact_response = httpx.get(CAT_FACT_URL)
        fact = fact_response.json()["fact"]

        return {
            "image_url": image_url,
            "fact": fact
        }
    except Exception as e:
        return {"error": str(e)}

@app.post("/vote")
def vote_for_cat(image_url: str, fact: str):
    with Session(engine) as session:
        # Завжди створюємо нового кота з 1 голосом
        new_cat = Cat(image_url=image_url, fact=fact, votes=1)
        session.add(new_cat)
        session.commit()
        return {"message": "Голос зараховано!"}

from sqlalchemy import text

@app.get("/top")
def get_top_cats():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT image_url, fact, SUM(votes) AS total_votes
            FROM "cat"
            GROUP BY image_url, fact
            ORDER BY total_votes DESC
            LIMIT 5
        """))
        cats = [
            {
                "image_url": row.image_url,
                "fact": row.fact,
                "votes": row.total_votes
            }
            for row in result
        ]
        return cats


@app.get("/index.html")
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/top.html")
def serve_top(request: Request):
    return templates.TemplateResponse("top.html", {"request": request})

@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico") if os.path.exists("favicon.ico") else {}
