from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.board.models import announcement_card
from src.board.schemas import AdCardCreate, AdCardEdit
from src.category.models import category
from src.database import get_async_session

router = APIRouter(
    prefix="/board",
    tags=["Board"]
)


@router.get("/")
async def get_board_on_id(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(announcement_card).where(announcement_card.c.id == id)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().first()
        }
    except Exception:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.get("/board_in_category")
@cache(expire=10)
async def get_board_on_category(title_category: str, session: AsyncSession = Depends(get_async_session),
                                limit: int = 3, offset: int = 0):
    try:
        query_select_category = select(category).filter(category.c.title == title_category)
        result_category = await session.execute(query_select_category)
        category_obj = result_category.fetchone()
        query = select(announcement_card).where(announcement_card.c.category_id == category_obj.id)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all()[offset:][:limit]
        }
    except Exception:
        raise HTTPException(status_code=400, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/add")
async def post_board(new_card: AdCardCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(announcement_card).values(**new_card.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "details": "card created"
        }
    except Exception:
        raise HTTPException(status_code=400, detail={
            "status": "card not save",
            "data": None,
            "details": None
        })


@router.put("/edit")
async def edit_board(id: int, edit_card: AdCardEdit, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(announcement_card).where(announcement_card.c.id == id).values(**edit_card.model_dump())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "details": "card edited"
        }
    except Exception:
        raise HTTPException(status_code=400, detail={
            "status": "card not edit"
        })


@router.delete("/delete")
async def delete_card(id_card: int, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = delete(announcement_card).where(announcement_card.c.id == id_card)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "success",
            "details": f"Post {id_card} delete"
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "card not delete"
        })