from sqlalchemy import Column, Integer, String, DateTime,select,func
from sqlalchemy.orm import declarative_base
import datetime

# 创建基类
Base = declarative_base()
# 时间类
class TimestampMixin(Base):
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# 新闻类别模型
class Categories(Base,TimestampMixin):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, comment="新闻类型ID")
    name = Column(String(50),nullable=False,comment="新闻类型")
    

