from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.fee import FeeStatus


class FeeBase(BaseModel):
    """Base fee schema"""
    student_id: int
    semester: int = Field(..., ge=1, le=8)
    academic_year: str
    tuition_fee: float = Field(..., ge=0)
    other_charges: float = Field(default=0.0, ge=0)
    total_amount: float = Field(..., ge=0)
    due_date: datetime


class FeeCreate(FeeBase):
    """Schema for fee creation"""
    pass


class FeeUpdate(BaseModel):
    """Schema for fee update"""
    amount_paid: Optional[float] = Field(None, ge=0)
    status: Optional[FeeStatus] = None
    transaction_id: Optional[str] = None
    payment_mode: Optional[str] = None
    payment_date: Optional[datetime] = None
    notes: Optional[str] = None


class FeeResponse(FeeBase):
    """Schema for fee response"""
    id: int
    amount_paid: float
    amount_due: float
    status: FeeStatus
    transaction_id: Optional[str]
    payment_mode: Optional[str]
    payment_date: Optional[datetime]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentFeeStatusResponse(BaseModel):
    """Student fee status summary"""
    student_id: int
    total_due: float
    total_paid: float
    pending_fees: list[FeeResponse] = Field(default_factory=list)
