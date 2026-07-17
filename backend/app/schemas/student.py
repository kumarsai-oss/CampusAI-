from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.student import StudentStatus


class StudentBase(BaseModel):
    """Base student schema"""
    roll_number: str = Field(..., min_length=3, max_length=20)
    department: str
    semester: int = Field(..., ge=1, le=8)
    batch_year: int
    cgpa: float = Field(default=0.0, ge=0.0, le=10.0)


class StudentCreate(StudentBase):
    """Schema for student creation"""
    user_id: int


class StudentUpdate(BaseModel):
    """Schema for student update"""
    semester: Optional[int] = Field(None, ge=1, le=8)
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0)
    status: Optional[StudentStatus] = None


class StudentResponse(StudentBase):
    """Schema for student response"""
    id: int
    user_id: int
    status: StudentStatus
    date_of_admission: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentAcademicResponse(BaseModel):
    """Schema for student academic info"""
    id: int
    student_id: int
    semester: int
    gpa: float
    total_credits: int
    earned_credits: int
    attendance_percentage: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentDetailedResponse(StudentResponse):
    """Detailed student response with academic info"""
    academic_history: Optional[List[StudentAcademicResponse]] = None
