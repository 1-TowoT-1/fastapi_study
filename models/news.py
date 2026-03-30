from sqlalchemy import Column, Integer, String, DateTime, Text, select, func, Index, ForeignKey
from sqlalchemy.orm import declarative_base

# 基类
Base = declarative_base()
# 时间类
class TimestampMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

# 新闻类别模型
class Categories(TimestampMixin, Base):
    __tablename__ = "news_category"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True, comment="新闻类别ID")
    name = Column(String(50),nullable=False,comment="类别名称")
    sort_order = Column(Integer, default=0, nullable=False, comment="排序")

    # __repr__: 面向开发者的字符串表示，用于调试和开发，应该明确无歧义
    def __repr__(self):
        return f'<Category(id={self.id}), name={self.name}, sort_order={self.sort_order}>'


# 新闻内容表格模型
class News_List(TimestampMixin, Base):
    __tablename__ = "news"

    # 创建索引，提升查询速度
    __table_args__ = (
        Index('news_category_idx', 'category_id'),
        Index('publish_time_idx', 'publish_time')
    )

    id = Column(Integer, primary_key=True, nullable=False, comment="新闻条数ID")
    title = Column(String(255), comment="新闻标题")
    description = Column(String(500), comment="新闻简介")
    content = Column(Text, comment="新闻内容")
    image = Column(String(255), comment="新闻图片url")
    author = Column(String(50), comment="作者")
    category_id = Column(Integer, ForeignKey('new_category.id'),comment="分类ID",nullable=False)
    views = Column(Integer, comment="浏览量")
    publish_time = Column(DateTime, default=func.now(), comment="发布时间")