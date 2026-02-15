from fastapi import FastAPI,Path,HTTPException
from fastapi import Header, Cookie
from typing import Union
from pydantic import BaseModel,Field
from fastapi.responses import HTMLResponse


# fastapi启动：uvicorn test:app --reload
app = FastAPI()

@app.get('/')
async def read_root():
    return {"hello":'world'}

# 路径参数
# 类型注解，给参数声明额外的信息和校验
@app.get("/book/{id}")
async def read_book(id: int = Path(..., gt=0,lt=101)):
    return {"id": id, "title": f"这是第{id}标签"}

# 查询参数
# 声明的参数不是路径参数时，路径操作函数会把该函数自动解释为查询参数
@app.get("/search/")
async def search(key:int, value:int):
    return {"键：": key, "值:":value}

# 请求体参数
# 1. 定义类型
# 2. 请求体参数，类型注解 Field函数
class User(BaseModel):
    usename: str = Field(...,min_length=6,max_length=20)
    password: str = Field(...,min_length=6,max_length=20)
# 2. 类型注解
@app.post("/register")
async def register(user:User):
    return user

# 响应类型
# 返回HTML
@app.get("/html", response_class=HTMLResponse)
# @app.get("/html")
async def get_html():
    return "<h1>Hello World<h1>"

# 异常处理
# 对客户端引发的错误（4xx，如资源未找到，认证失败），
# 应使用fastapi.HTTPException 来中断正常的处理流程，并返回错误响应。
@app.get('/new/{id}')
async def get_news(id:int):
    id_lst = [1,2,3,4,5,6]
    if id not in id_lst:
        raise HTTPException(status_code=404, detail = f"当前{id}不存在")
    return {"id":id}

# 中间件
# 函数顶部使用装饰器：@app.middleware("http")
@app.middleware("http")
async def middlesware(request, call_next): # request：请求；call_next：传递请求给路径处理函数
    print("中间件开始处理 —— start")
    response = await call_next(request)
    print("中间件处理完成 —— end")
    return response