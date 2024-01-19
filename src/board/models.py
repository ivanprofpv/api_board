from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, MetaData

from src.category.models import category

metadata = MetaData()

announcement_card = Table(
    "announcement_card",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("text", String, nullable=False),
    Column("price", Integer, nullable=True),
    Column("photo", String, nullable=True),
    Column("date", TIMESTAMP),
    Column("category_id", Integer, ForeignKey(category.c.id)),
)