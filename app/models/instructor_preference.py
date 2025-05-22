
from sqlalchemy import Column, Integer, ForeignKey, Time, Enum
from sqlalchemy.orm import relationship
import enum

from app.db.base_class import Base, BaseModel

class DayOfWeek(str, enum.Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

class InstructorPreference(Base, BaseModel):
    __tablename__ = "instructor_preferences"

    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    day_of_week = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    instructor = relationship("User", back_populates="instructor_preferences")
