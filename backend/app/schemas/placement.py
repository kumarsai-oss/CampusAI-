from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from app.models.placement import PlacementStatus


class PlacementDriveBase(BaseModel):
    """Base placement drive schema"""
    company_name: str
    company_website: Optional[HttpUrl] = None
    job_profile: str
    package: float = Field(..., gt=0)
    location: str
    eligibility_cgpa: float = Field(..., ge=0, le=10)
    max_backlogs: int = Field(default=0, ge=0)
    description: Optional[str] = None


class PlacementDriveCreate(PlacementDriveBase):
    """Schema for placement drive creation"""
    registration_deadline: datetime
    drive_date: datetime


class PlacementDriveResponse(PlacementDriveBase):
    """Schema for placement drive response"""
    id: int
    registration_deadline: datetime
    drive_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlacementBase(BaseModel):
    """Base placement schema"""
    student_id: int
    drive_id: int
    company_name: str
    job_profile: str
    package: float = Field(..., gt=0)
    location: str
    status: PlacementStatus = PlacementStatus.NOT_PLACED


class PlacementCreate(PlacementBase):
    """Schema for placement creation"""
    pass


class PlacementUpdate(BaseModel):
    """Schema for placement update"""
    status: Optional[PlacementStatus] = None
    placement_date: Optional[datetime] = None
    joining_date: Optional[datetime] = None
    resume_ats_score: Optional[float] = Field(None, ge=0, le=100)


class PlacementResponse(PlacementBase):
    """Schema for placement response"""
    id: int
    placement_date: Optional[datetime]
    joining_date: Optional[datetime]
    resume_ats_score: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeATSAnalysisRequest(BaseModel):
    """Request for resume ATS analysis"""
    job_description: str
    resume_text: str


class ResumeATSAnalysisResponse(BaseModel):
    """Response for resume ATS analysis"""
    ats_score: float
    match_percentage: float
    matched_keywords: List[str] = Field(default_factory=list)
    missing_keywords: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
