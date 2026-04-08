from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base

class TrendingRepo(Base):
    __tablename__ = "trending_repos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text, nullable=True)
    stars = Column(String(50))
    captured_at = Column(DateTime, default=datetime.utcnow) # 记录抓取时间