from sqlmodel import Field, SQLModel
from typing import Optional

class Cat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_url: str
    fact: str
    votes: int = 0
