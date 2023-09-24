# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class URLInfo(Base):
    __tablename__ = "url_info"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(100), index=True)
    
class save_url(Base):
    __tablename__ = "saved_url"

    ai_output = Column(String(20),index=True)
    url_type = Column(String(20),index=True)
    url = Column(String(100),index=True,primary_key=True)