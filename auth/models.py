from datetime import datetime
from sqlalchemy import Column, String, TIMESTAMP, Boolean, Integer
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


Base: DeclarativeMeta = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(length=1024), nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True, nullable=True)
    is_superuser = Column(Boolean, default=False, nullable=True)
    is_verified = Column(Boolean, default=False, nullable=True)
