from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database, scraper

# 初始化数据库表（如果表不存在会自动创建）
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="GitHub Trending Scraper API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Data Scraper API"}

@app.post("/scrape")
def trigger_scrape(db: Session = Depends(database.get_db)):
    """
    Manually trigger the crawler: scrape GitHub Trending and store the data in MySQL.
    """
    try:
        results = scraper.scrape_github_and_store(db)
        return {"status": "success", "scraped_repos": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trending")
def get_stored_trending(db: Session = Depends(database.get_db)):
    """
    read
    """
    repos = db.query(models.TrendingRepo).all()
    return repos