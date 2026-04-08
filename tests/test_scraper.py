# tests/test_scraper.py
import pytest
from app.scraper import scrape_and_store_github
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

# 使用内存数据库进行快速测试，不污染正式数据库
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)

def test_scrape_logic():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # 运行你的爬虫
    results = scrape_and_store_github(db)
    
    # 断言（判断结果是否符合预期）
    assert results is not None
    assert len(results) > 0
    assert isinstance(results[0], str)
    
    db.close()
    Base.metadata.drop_all(bind=engine)