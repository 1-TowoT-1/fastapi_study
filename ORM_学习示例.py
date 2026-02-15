from sqlalchemy.ext.asyncio import create_async_engine,async_session,AsyncSession
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager

ASYNC_DATABASE_URL = "postgresql+asyncpg://postgres:hbxt9688@172.31.136.83:5432/fastapi"

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,  # 输出SQL日志
    pool_size = 10,  # 设置连接池中保持的连接数
    max_overflow = 20  # 设置连接池允许创建的额外连接数
)


# 基类创建
Base = declarative_base()
class TimestampMixin():
    create_time = Column(DateTime, default = datetime.utcnow, comment = "创建时间")
    update_time = Column(DateTime, default = datetime.utcnow, onupdate = datetime.utcnow , comment='更新时间')

# 具体表
class Book(Base,TimestampMixin):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = Column(String(50), unique=True, nullable=False, index=True, comment='用户名')
    bookname = Column(String(100), unique=False, nullable=False, comment='书名')
    author = Column(String(30), unique=False, nullable=False, comment='作者')


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("Database tables created!")
    try:
        yield
    finally:
        await async_engine.dispose()
        print("Database connections closed!")

app = FastAPI(lifespan=lifespan)

# 后端启动控制数据库建表
@app.get('/')
async def read_root():
    return {"hello":'world'}



# ==========================================================================================================

# 路由中使用ORM
 = async_session()
