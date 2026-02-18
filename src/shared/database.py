"""
Database service module.
Handles connection to Azure/Postgres using SQLAlchemy.
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from src.shared.config import settings

Base = declarative_base()

# Table schema
class FinancialReport(Base):
    __tablename__ = "reports_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(15), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class DatabaseService:
    def __init__(self):
        # Grab URL from settings
        db_url = settings.database_url

        if not db_url:
            raise ValueError("Database URL is missing in configuration")

        # Fix legacy URL format if needed
        if db_url.startswith("postgres://"):
            db_url = db_url.replace("postgres://", "postgresql://", 1)

        print("DATABASE_URL BEING USED:", db_url)

        # Create engine & session
        self.engine = create_engine(db_url, echo=False, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

        # Create tables if they don't exist
        Base.metadata.create_all(bind=self.engine)

    def save_reports(self, ticker: str, content: str):
        """
        Save a new analysis report to the database.
        """
        session = self.SessionLocal()
        try:
            report = FinancialReport(ticker=ticker, content=content)
            session.add(report)
            session.commit()
            print(f"Saved {ticker} report to Database (ID: {report.id})")
        except Exception as e:
            print(f"Database Error: {e}")
            session.rollback()
        finally:
            session.close()
