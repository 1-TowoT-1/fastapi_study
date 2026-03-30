from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(news.news_router)

# 添加中间件，允许前端访问
origins = [
    "http://localhost",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,  # 允许访问的源，一般会使用变量代替，["*"]是所有源都可以访问，这里我作限制，只能本机访问。
    allow_credentials = True, # 允许鞋带 Cookies
    allow_methods = ["*"],    # 允许所有请求方式
    allow_headers = ["*"],    # 允许所有请求头
)

@app.get('/')
async def read_root():
    return {"hello":'world'}