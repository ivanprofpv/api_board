from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.category.models import category
from src.category.schemas import CategoryCreate, CategoryEdit
from src.database import get_async_session

router = APIRouter(
    prefix="/category",
    tags=["Category"]
)


@router.get("/")
async def get_category(session: AsyncSession = Depends(get_async_session),
                       limit: int = 3, offset: int = 0):
    try:
        query = select(category).limit(limit).offset(offset)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all()[offset:][:limit]
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": "Error 500"
        })


@router.post("/")
async def post_category(new_card: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(category).values(**new_card.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": 200
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "category not save",
            "data": None,
            "details": None
        })


@router.put("/edit")
async def edit_category(id_category: int, edit_card: CategoryEdit, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(category).where(category.c.id == id_category).values(**edit_card.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": "category edited"
        }
    except Exception:
        raise HTTPException(status_code=400, detail={
            "status": "category not edit"
        })


@router.delete("/delete")
async def delete_category(id_category: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(category).where(category.c.id == id_category)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "data": None,
            "details": f"Category {id_category} delete"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "category not delete"
        })