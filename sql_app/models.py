from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class logChannel(Base):
    __tablename__ = "test"

    guild_id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, index=True)
