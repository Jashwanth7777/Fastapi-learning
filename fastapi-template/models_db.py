from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ImageLog(Base):
    __tablename__ = "image_logs"

    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(String, nullable=False)
    cropped_image_path = Column(String, nullable=False)
    date_cropped = Column(DateTime, default=datetime.utcnow)