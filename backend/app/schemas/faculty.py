from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.faculty import FacultyDepartment


class FacultyBase(BaseModel):
    """Base faculty schema"""
    employee_id: str = Field(..., min_length=3, max_length=20)
    department: FacultyDepartment
    designation: str
    qualification: str
    specialization: Optional[str] = None
    office_room: Optional[str] = None
    office_phone: Optional[str] = None
    experience_years: int = Field(default=0, ge=0)


class FacultyCreate(FacultyBase):
    """Schema for faculty creation"""
    user_id: int


class FacultyUpdate(BaseModel):
    """Schema for faculty update"""
    designation: Optional[str] = None
    specialization: Optional[str] = None
    office_room: Optional[str] = None
    office_phone: Optional[str] = None
    experience_years: Optional[int] = None


class FacultyResponse(FacultyBase):
    """Schema for faculty response"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
