from pydantic import BaseModel


class CategoryCreate(BaseModel):
    id: int
    title: str