from datetime import datetime

from pydantic import BaseModel


class AdCardCreate(BaseModel):
    id: int
    title: str
    text: str
    price: int
    photo: str
    date: datetime
    category_id: int


class AdCardEdit(BaseModel):
    title: str
    text: str
    price: int
    photo: str
    date: datetime
    category_id: int
