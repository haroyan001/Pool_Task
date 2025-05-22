
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base, BaseModel

class InstructorSchedule(Base, BaseModel):
    __tablename__ = "instructor_schedules"


    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    instructor = relationship("User", back_populates="instructor_schedules")
