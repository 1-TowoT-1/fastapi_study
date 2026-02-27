from sqlalchemy.ext.asyncio import create_async_engine,async_session,AsyncSession,async_sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey,select
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from fastapi import FastAPI,Depends,HTTPException
from contextlib import asynccontextmanager
from pydantic import BaseModel

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



# ============================================= 创建异步会话注入路由 ==================================================

# 路由中使用ORM
## 需求：查询数据库功能的接口，查询图书 ➡ 依赖注入：创建依赖项获取数据库会话 + Depends 注入路由函数
AsyncSession_Local = async_sessionmaker(
    bind = async_engine, # 绑定数据库引擎
    class_ = AsyncSession, # 指定会话类
    expire_on_commit = False  # 提交后会话不会过期，不会重新查询数据库
)

# 只负责提供 AsyncSession，不自动提交事务，适合查询接口或手动控制事务。
async def get_session():
    """只读或手动控制的会话依赖"""
    async with AsyncSession_Local() as session:
        yield session

# 在 yield 后自动 commit，异常时 rollback，适合写操作接口。
async def get_tx_session():
    """具有自动提交/回滚功能的事务会话依赖。"""
    async with AsyncSession_Local() as session:
        try:
            yield session # yield相当于分界点，yield前：准备阶段；yield中：提交阶段；yield后：收尾阶段。
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# 将会话注入路由
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_tx_session)):
    # 查询
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books 


# ============================================= 添加数据库行操作 ==================================================
class BookBase(BaseModel):
	id: int
	username: str
	bookname: str
	author: str

@app.post("/book/add_book")
async def add_book(book: BookBase, db: AsyncSession=Depends(get_session)):
	#获取book参数，创建读书对象（__dict__ 返回book对象的属性字典）
	book_obj = Book(**book.__dict__) # __dict__将book对象转成字典类型，**将字典展开
	db.add(book_obj)
	await db.commit()
	return book



# ============================================= 更新数据库行操作 ==================================================
class BookUpdate(BaseModel):
	username: str
	bookname: str
	author: str

@app.post("/book/update_book/{book_id}")
async def update_book(book_id: int, data: BookUpdate, db: AsyncSession=Depends(get_session)):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(
            status_code = 404,
            detail = "查无此书"
        )
    db_book.username = data.username
    db_book.bookname = data.bookname
    db_book.author = data.author
    await db.commit()
    return db_book



# ============================================= 删除数据库数据操作 ==================================================
@app.post("/book/delete_book/{book_id}")
async def update_book(book_id: int, db: AsyncSession=Depends(get_session)):
    db_book = await db.get(Book, book_id)
    if db_book is None:
        raise HTTPException(
            status_code = 404,
            detail = "查无此书"
        )
    await db.delete(db_book)
    await db.commit()
    return db_book
