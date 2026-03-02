from fastapi import APIRouter

news_router = APIRouter(prefix="/api/news",tags=["news"])

@news_router.get("/categories")
async def get_categories():
    pass