from fastapi import FastAPI, Request
import httpx
from sqlmodel import SQLModel, Session, create_engine, select
from app.models import Cat, VoteLog
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from datetime import datetime, timedelta
import os

app = FastAPI()

# Підключення статики та шаблонів
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# 🔧 Шлях до БД
DATABASE_URL = "sqlite:///app/kotiki.db"
engine = create_engine(DATABASE_URL)

# --- API котів ---
CAT_IMAGE_URL = "https://api.thecatapi.com/v1/images/search"
CAT_FACT_URL = "https://catfact.ninja/fact"

# --- Створення таблиць ---
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
async def vote_for_cat(request: Request):
    data = await request.json()
    image_url = data.get("image_url")
    fact = data.get("fact")

    with Session(engine) as session:
        new_cat = Cat(image_url=image_url, fact=fact, votes=1)
        session.add(new_cat)

        # UTC+3:00 (Київ)
        log = VoteLog(image_url=image_url, fact=fact, timestamp=datetime.utcnow() + timedelta(hours=3))
        session.add(log)

        session.commit()
        return {"message": "Голос зараховано!"}

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

# --- HTML ---
@app.get("/index.html")
def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/top.html")
def serve_top(request: Request):
    return templates.TemplateResponse("top.html", {"request": request})

@app.get("/votes.html")
def serve_votes_page(request: Request):
    return templates.TemplateResponse("votes.html", {"request": request})

@app.get("/favicon.ico")
def favicon():
    return FileResponse("favicon.ico") if os.path.exists("favicon.ico") else {}

# --- JSON API ---
@app.get("/votes")
def get_votes():
    with Session(engine) as session:
        statement = select(VoteLog).order_by(VoteLog.timestamp.desc())
        results = session.exec(statement).all()
        return results

# --- Очистити всі голоси
@app.post("/clear_votes")
def clear_votes():
    with Session(engine) as session:
        session.exec(text("DELETE FROM votelog"))
        session.exec(text("DELETE FROM cat"))
        session.commit()
        return {"message": "Всі голоси видалено"}
