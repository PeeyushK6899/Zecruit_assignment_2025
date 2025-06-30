from sqlalchemy import Column, Integer, String, JSON, Float
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    extracted_data = Column(JSON)  
    score = Column(Float)