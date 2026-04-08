# GitHub Trending Scraper API

A practical data pipeline that scrapes GitHub Trending repositories and stores them in a MySQL database. Built with FastAPI for high-performance API access and BeautifulSoup4 for robust web scraping.

## Key Components

- **Scraper**: Extracts repo title, description, and star count from GitHub's trending page.
- **API**: FastAPI-based endpoints to trigger manual scrapes and retrieve historical data.
- **Database**: SQLAlchemy ORM for structured data persistence in MySQL.
- **Tests**: Pytest suite using an in-memory SQLite database to verify scraper logic and database integrity.
- **Docker**: Containerized environment for consistent deployment.

## Project Structure

- `app/main.py`: API entry point and database initialization.
- `app/scraper.py`: Core scraping logic and data extraction.
- `app/models.py`: Database schema definitions.
- `app/database.py`: MySQL connection setup and session management.
- `tests/`: Automated test cases for the scraper and API.

## Getting Started

### Prerequisites
- Python 3.11+
- MySQL Server
- Docker 

### Installation
1. Clone the repository:
   ```bash
   git clone <your-repo-link>
   cd fastapi-data-scraper
