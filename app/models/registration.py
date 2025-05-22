
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base, BaseModel

class Registration(Base, BaseModel):
    __tablename__ = "registrations"

    visitor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    
    visitor = relationship("User", back_populates="registrations")
    group = relationship("Group", back_populates="registrations")
    
    attended = Column(Boolean, default=False)
