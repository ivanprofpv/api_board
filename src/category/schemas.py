from pydantic import BaseModel


class CategoryCreate(BaseModel):
    id: int
    title: str


class CategoryEdit(BaseModel):
    title: str