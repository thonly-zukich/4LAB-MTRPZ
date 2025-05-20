from fastapi import FastAPI
import httpx
from sqlmodel import SQLModel, Session, create_engine, select
from models import Cat

app = FastAPI()

# --- Константи для зовнішніх API ---
CAT_IMAGE_URL = "https://api.thecatapi.com/v1/images/search"
CAT_FACT_URL = "https://catfact.ninja/fact"

# --- Налаштування бази даних ---
DATABASE_URL = "sqlite:///kotiki.db"
engine = create_engine(DATABASE_URL)

@app.on_event("startup")
def on_startup():
    """
    Створює таблиці у базі даних при запуску серверу
    """
    SQLModel.metadata.create_all(engine)

# --- Головна сторінка ---
@app.get("/")
def read_root():
    return {"message": "Привіт, котики!"}

# --- Отримати випадкового кота з фото та фактом ---
@app.get("/random_cat")
def get_random_cat():
    try:
        # Отримати зображення кота
        image_response = httpx.get(CAT_IMAGE_URL)
        image_url = image_response.json()[0]["url"]

        # Отримати факт про котів
        fact_response = httpx.get(CAT_FACT_URL)
        fact = fact_response.json()["fact"]

        return {
            "image_url": image_url,
            "fact": fact
        }

    except Exception as e:
        return {"error": str(e)}

# --- Голосування за кота ---
@app.post("/vote")
def vote_for_cat(image_url: str, fact: str):
    with Session(engine) as session:
        # Перевіряємо, чи такий кіт уже існує
        statement = select(Cat).where(Cat.image_url == image_url)
        result = session.exec(statement).first()

        if result:
            result.votes += 1  # Збільшуємо кількість голосів
        else:
            # Створюємо нового кота з 1 голосом
            result = Cat(image_url=image_url, fact=fact, votes=1)
            session.add(result)

        session.commit()
        return {"message": "Голос зараховано!"}

# --- Показати топ 5 котів за голосами ---
@app.get("/top")
def get_top_cats():
    with Session(engine) as session:
        statement = select(Cat).order_by(Cat.votes.desc()).limit(5)
        results = session.exec(statement).all()
        return results
