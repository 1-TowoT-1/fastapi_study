from fastapi import APIRouter,Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news
from config.db_conf import get_db

news_router = APIRouter(prefix="/api/news",tags=["news"])

@news_router.get("/categories")
async def get_categories(skip: int=0, limit: int=100, db: AsyncSession = Depends(get_db)):
    # 创建新路由➡
    categories = await news.get_categories(db,skip,limit)
    return{
        "code": 200,
        "message": "新闻类别展示成功",
        "data": categories
    }


@news_router.get("/list")
async def get_list(
    category_id: int = Query(alias="categoryId"),
    page: int = Query(default=1),
    page_size: int = Query(alias="pageSize",default=10, le=100),
    db: AsyncSession = Depends(get_db)
):
    # 思路：处理分页规则 ➡ 查询新闻列表 ➡ 计算总量 ➡ 是否还有更多新闻
    offset = (page - 1) * page_size
    news_list,search_result = await news.get_newslist(db=db, skip=offset, page_size=page_size, category_id=category_id)
    return{
        "code": 200,
        "message": "新闻列表返回成功",
        "data": {
            "list": news_list, # 返回的新闻列表内容
            "total": search_result, # 总量
            "hasMore": True # 是否更多
        }
    }