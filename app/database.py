import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_USER = "root"
DB_PASSWORD = "123456"  
DB_NAME = "scraper_db"   


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

# 3. create engine
# check_same_thread=False 仅用于 SQLite，MySQL 不需要
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 4. 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. 声明基类，供 models.py 继承
Base = declarative_base()

# 6. 数据库连接依赖项 (Dependency Injection)
# 这在 FastAPI 中非常重要，确保每个请求都有独立的数据库连接，并在完成后自动关闭
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()