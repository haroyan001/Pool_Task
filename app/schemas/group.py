
from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime

class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    capacity: int
    max_male: int
    max_female: int
    start_time: datetime
    end_time: datetime
    
    @validator('end_time')
    def end_time_must_be_after_start_time(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v
    
    @validator('max_male', 'max_female')
    def gender_limits_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Gender limits must be positive')
        return v
    
    @validator('capacity')
    def capacity_must_be_positive(cls, v, values):
        if v < 1:
            raise ValueError('Capacity must be at least 1')
        
        max_male = values.get('max_male', 0)
        max_female = values.get('max_female', 0)
        if max_male and max_female and v < (max_male + max_female):
            raise ValueError('Capacity must be at least the sum of gender limits')
        return v

class GroupCreate(GroupBase):
    instructor_id: Optional[int] = None

class GroupUpdate(GroupBase):
    instructor_id: Optional[int] = None

class GroupInDBBase(GroupBase):
    id: int
    instructor_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class Group(GroupInDBBase):
    current_participants: int
    current_male_participants: int
    current_female_participants: int
    is_full: bool
    is_male_full: bool
    is_female_full: bool

class GroupList(BaseModel):
    id: int
    name: str
    start_time: datetime
    end_time: datetime
    capacity: int
    current_participants: int
    instructor_id: Optional[int]
    is_full: bool
    
    class Config:
        orm_mode = True
