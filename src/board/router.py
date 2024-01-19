from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.board.models import announcement_card
from src.board.schemas import AdCardCreate, AdCardEdit
from src.database import get_async_session

router = APIRouter(
    prefix="/board",
    tags=["Board"]
)


@router.get("/")
async def get_board_on_category(board_category: int, session: AsyncSession = Depends(get_async_session),
                                limit: int = 3, offset: int = 0):
    try:
        query = select(announcement_card).where(announcement_card.c.category_id == board_category)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.mappings().all()[offset:][:limit]
        }
    except Exception:
        raise HTTPException(status_code=400, detail={
            "status": "error"
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
            "status": "card not save"
        })


@router.put("/edit")
async def edit_board(id_card: int, edit_card: AdCardEdit, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = update(announcement_card).where(announcement_card.c.id == id_card).values(**edit_card.model_dump())
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