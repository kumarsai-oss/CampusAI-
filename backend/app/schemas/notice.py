from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.notice import NoticeType


class NoticeBase(BaseModel):
    """Base notice schema"""
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10)
    notice_type: NoticeType
    department: Optional[str] = None


class NoticeCreate(NoticeBase):
    """Schema for notice creation"""
    expires_at: Optional[datetime] = None


class NoticeUpdate(BaseModel):
    """Schema for notice update"""
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    notice_type: Optional[NoticeType] = None
    is_published: Optional[bool] = None
    expires_at: Optional[datetime] = None


class NoticeResponse(NoticeBase):
    """Schema for notice response"""
    id: int
    summary: Optional[str]
    issued_by: int
    attachment_url: Optional[str]
    is_published: bool
    expires_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoticeSummarizationRequest(BaseModel):
    """Request for notice summarization"""
    content: str = Field(..., min_length=10)
    max_length: Optional[int] = Field(None, ge=50, le=500)
