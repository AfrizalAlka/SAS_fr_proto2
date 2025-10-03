from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import sys
import os

# Add config to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.database import DATABASE_URL

Base = declarative_base()

class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_name = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(String(10), nullable=False)
    status = Column(String(20), default='Present')
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Attendance(id={self.id}, student_name='{self.student_name}', date='{self.date}', time='{self.time}')>"

# Database connection
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Get database session"""
    return SessionLocal()

def create_tables():
    """Create all tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def init_database():
    """Initialize database and create tables"""
    try:
        create_tables()
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False