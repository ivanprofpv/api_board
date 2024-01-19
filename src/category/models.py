from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, MetaData

metadata = MetaData()

category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
)