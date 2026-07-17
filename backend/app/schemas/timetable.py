from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time
from app.models.timetable import DayOfWeek


class TimeSlotBase(BaseModel):
    """Base time slot schema"""
    day: DayOfWeek
    start_time: time
    end_time: time
    subject_code: str = Field(..., max_length=20)
    subject_name: str
    faculty_id: int
    classroom: str = Field(..., max_length=50)
    batch_group: Optional[str] = None
    slot_number: int


class TimeSlotCreate(TimeSlotBase):
    """Schema for time slot creation"""
    pass


class TimeSlotResponse(TimeSlotBase):
    """Schema for time slot response"""
    id: int
    timetable_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TimetableBase(BaseModel):
    """Base timetable schema"""
    semester: int = Field(..., ge=1, le=8)
    department: str
    academic_year: str = Field(..., min_length=4, max_length=10)


class TimetableCreate(TimetableBase):
    """Schema for timetable creation"""
    time_slots: Optional[List[TimeSlotCreate]] = None


class TimetableResponse(TimetableBase):
    """Schema for timetable response"""
    id: int
    created_at: datetime
    updated_at: datetime
    time_slots: Optional[List[TimeSlotResponse]] = None

    class Config:
        from_attributes = True


class TimetableOptimizationRequest(BaseModel):
    """Request for timetable optimization"""
    semester: int
    department: str
    academic_year: str
    constraints: Optional[dict] = None
