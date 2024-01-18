from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.board.models import category, announcement_card
from src.board.schemas import AdCardCreate
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
            "data": result.mappings().all()[offset:][:limit],
            "details": None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.post("/")
async def post_board(new_card: AdCardCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(announcement_card).values(**new_card.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": 200}