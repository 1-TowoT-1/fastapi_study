from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

# 数据库URL
ASYNC_DATABASE_URL = 'postgresql+asyncpg://postgres:hbxt9688@localhost:5432/news_app'

# 创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True, # 可选，输出SQL日志
    pool_size = 10, # 设置连接池中保持的持久连接数目
    max_overflow = 20 # 设置连接池允许创建的额外连接数目
)

# 创建异步会话工厂
AsyncSession_Local = async_sessionmaker(
    bind = async_engine, # 绑定数据库引擎
    class_ = AsyncSession, # 指定会话类
    expire_on_commit = False # 提交后会话不会过期，不会重新查询数据库
)

# 依赖项注入，用于获取数据库数据
async def get_db():
    async with AsyncSession_Local() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise