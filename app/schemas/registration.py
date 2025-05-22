
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class RegistrationBase(BaseModel):
    group_id: int
    attended: Optional[bool] = False

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationUpdate(BaseModel):
    attended: Optional[bool] = None

class RegistrationInDBBase(RegistrationBase):
    id: int
    visitor_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class Registration(RegistrationInDBBase):
    pass
