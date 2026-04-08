import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from . import models  # 导入我们之前定义的数据库模型

def scrape_github_and_store(db: Session):
    url = "https://github.com/trending"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch GitHub: {response.status_code}")
            return None
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 批量存储的容器
        new_repos = []
        
        # 查找 GitHub Trending 的项目列表
        for article in soup.select("article.Box-row")[:10]:
            # 1. 提取数据
            title = article.select_one("h2 a").get_text(strip=True).replace("\n", "").replace(" ", "")
            description = article.select_one("p").get_text(strip=True) if article.select_one("p") else "No description"
            
            # GitHub 的星数通常在特定的 a 标签里，这里用 select 确保精准
            star_tag = article.select_one('a[href$="/stargazers"]')
            stars = star_tag.get_text(strip=True) if star_tag else "0"
            
            # 2. 核心：创建数据库模型实例
            # 注意：这里的字段名要和你 models.py 里定义的对应 (repo_name, stars 等)
            db_repo = models.TrendingRepo(
                title=title,
                description=description,
                stars=stars
            )
            new_repos.append(db_repo)

        # 3. 批量写入数据库 (比一条条写快得多)
        if new_repos:
            db.add_all(new_repos)
            db.commit()
            return [repo.title for repo in new_repos]
            
    except Exception as e:
        db.rollback() # 出错时回滚，保证数据库数据一致性
        print(f"Scraper Error: {e}")
        return None