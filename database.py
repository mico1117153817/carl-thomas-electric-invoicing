"""
Database configuration for Carl Thomas Electric Invoicing Portal
"""
import os
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL - using SQLite for simplicity
DATABASE_URL = "sqlite+aiosqlite:///./invoice_portal.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Set to True for development debugging
    future=True  # Use SQLAlchemy 2.0 style sessions
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


async def get_db():
    """Database session dependency"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            pass  # Session will close automatically when context manager exits


def create_database_tables():
    """Create all database tables"""
    from models import (
        Customer, Invoice, Estimate
    )
    from schemas import Base  # This creates the metadata
    
    Base.metadata.create_all(bind=engine)
