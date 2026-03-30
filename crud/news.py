from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from models.news import Categories,News_List
from fastapi import Query

async def get_categories(db: AsyncSession, skip: int=0, limit: int=100):
    stmt = select(Categories).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_newslist(db: AsyncSession, category_id: int, skip: int=0, page_size: int = Query(default=10, le=100)):
    stmt = select(News_List).where(News_List.category_id == category_id).offset(skip).limit(page_size)
    newslist = await db.execute(stmt)

    stmt2 = select(func.count(News_List.id)).where(News_List.category_id == category_id)
    search_result = await db.execute(stmt2)
    
    return newslist.scalars().all(),search_result.scalar_one()