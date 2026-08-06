
from app.database import Base
from sqlalchemy import Column, Integer, String,Date

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer,primary_key=True )
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default='pending')
    
