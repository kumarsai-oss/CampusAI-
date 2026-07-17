from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.complaint import ComplaintCategory, ComplaintStatus


class ComplaintBase(BaseModel):
    """Base complaint schema"""
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=10)
    category: ComplaintCategory
    priority: str = Field(default="medium", regex="^(low|medium|high|urgent)$")


class ComplaintCreate(ComplaintBase):
    """Schema for complaint creation"""
    student_id: int


class ComplaintUpdate(BaseModel):
    """Schema for complaint update"""
    status: Optional[ComplaintStatus] = None
    resolution: Optional[str] = None
    assigned_to: Optional[int] = None
    priority: Optional[str] = Field(None, regex="^(low|medium|high|urgent)$")


class ComplaintResponse(ComplaintBase):
    """Schema for complaint response"""
    id: int
    student_id: int
    status: ComplaintStatus
    assigned_to: Optional[int]
    resolution: Optional[str]
    attachment_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]

    class Config:
        from_attributes = True


class ComplaintListResponse(BaseModel):
    """Complaint list response"""
    total: int
    complaints: list[ComplaintResponse] = Field(default_factory=list)
