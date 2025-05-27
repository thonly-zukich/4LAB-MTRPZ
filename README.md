# Котячий Тіндер

**Котячий Тіндер** — це вебзастосунок, де користувачі можуть переглядати рандомних котів, дізнаватись цікаві факти та голосувати за найкращих. Результати голосування відображаються у вигляді ТОПу.

## Посилання

- [Design Document](https://docs.google.com/document/d/19bvkkzFvPSkT9niKEoIbwLyqXRdutim1voRButQmHsA/edit?usp=sharing) — документ про архітектуру та реалізацію проєкту

## Інструкції зі зборки та запуску

### 1. Клонування репозиторію

```bash
git clone <repo-url>
cd котопедія
```

### 2. Встановлення залежностей

```bash
python -m venv venv
venv\Scripts\activate  # або source venv/bin/activate на Linux/macOS
pip install -r requirements.txt
```

### 3. Запуск сервера

```bash
uvicorn app.main:app --reload
```

### 4. Командний інтерфейс (CLI)

```bash
python cli.py random
python cli.py vote
python cli.py top
python cli.py log
```

### 5. Запуск тестів

```bash
pytest
```

## Стек технологій

- Python
- FastAPI
- SQLModel + SQLite
- HTML/CSS + JS (Vanilla)
- Pytest

## Автори

Антон Літох, Євген Сунак, ІМ-33
