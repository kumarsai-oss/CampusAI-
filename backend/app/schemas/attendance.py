from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from app.models.attendance import AttendanceStatus


class AttendanceBase(BaseModel):
    """Base attendance schema"""
    student_id: int
    faculty_id: int
    subject_code: str = Field(..., max_length=20)
    status: AttendanceStatus
    recognized_by_face: bool = False


class AttendanceCreate(AttendanceBase):
    """Schema for attendance creation"""
    class_date: datetime
    marked_by: int


class AttendanceUpdate(BaseModel):
    """Schema for attendance update"""
    status: AttendanceStatus
    recognized_by_face: Optional[bool] = None


class AttendanceResponse(AttendanceBase):
    """Schema for attendance response"""
    id: int
    class_date: datetime
    marked_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttendanceReportResponse(BaseModel):
    """Attendance report response"""
    student_id: int
    total_classes: int
    present_count: int
    absent_count: int
    late_count: int
    attendance_percentage: float
    subjects: List[dict] = Field(default_factory=list)
