from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.result import Grade


class SubjectBase(BaseModel):
    """Base subject schema"""
    subject_code: str = Field(..., min_length=3, max_length=20)
    subject_name: str
    credits: int = Field(..., ge=1, le=8)
    semester: int = Field(..., ge=1, le=8)
    department: str


class SubjectCreate(SubjectBase):
    """Schema for subject creation"""
    pass


class SubjectResponse(SubjectBase):
    """Schema for subject response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResultBase(BaseModel):
    """Base result schema"""
    student_id: int
    subject_id: int
    semester: int = Field(..., ge=1, le=8)
    internal_marks: float = Field(..., ge=0, le=30)
    external_marks: float = Field(..., ge=0, le=70)
    total_marks: float = Field(..., ge=0, le=100)
    academic_year: str


class ResultCreate(ResultBase):
    """Schema for result creation"""
    pass


class ResultUpdate(BaseModel):
    """Schema for result update"""
    internal_marks: Optional[float] = Field(None, ge=0, le=30)
    external_marks: Optional[float] = Field(None, ge=0, le=70)


class ResultResponse(ResultBase):
    """Schema for result response"""
    id: int
    grade: Grade
    grade_points: float
    credit_earned: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentResultsResponse(BaseModel):
    """Student results summary"""
    student_id: int
    semester: int
    academic_year: str
    cgpa: float
    total_credits: int
    earned_credits: int
    results: List[ResultResponse] = Field(default_factory=list)
