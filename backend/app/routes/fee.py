from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.models.fee import Fee, FeeStatus
from app.models.student import Student
from app.schemas.fee import FeeCreate, FeeResponse, FeeUpdate, StudentFeeStatusResponse
from app.security import get_current_user, get_admin_user

router = APIRouter(prefix="/api/fees", tags=["Fees"])


@router.post("/", response_model=FeeResponse, status_code=status.HTTP_201_CREATED)
async def create_fee(
    fee_data: FeeCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a fee record (admin only)"""
    
    student = db.query(Student).filter(Student.id == fee_data.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    existing = db.query(Fee).filter(
        (Fee.student_id == fee_data.student_id) &
        (Fee.semester == fee_data.semester) &
        (Fee.academic_year == fee_data.academic_year)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fee record already exists for this period"
        )
    
    amount_due = fee_data.total_amount - fee_data.amount_paid
    
    new_fee = Fee(
        **fee_data.dict(),
        amount_due=amount_due
    )
    db.add(new_fee)
    db.commit()
    db.refresh(new_fee)
    
    return new_fee


@router.get("/student/{student_id}", response_model=StudentFeeStatusResponse)
async def get_student_fees(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student's fee status"""
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    if current_user.role == UserRole.STUDENT and current_user.id != student.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    fees = db.query(Fee).filter(Fee.student_id == student_id).all()
    
    total_due = sum([f.amount_due for f in fees])
    total_paid = sum([f.amount_paid for f in fees])
    pending_fees = [f for f in fees if f.status in [FeeStatus.PENDING, FeeStatus.PARTIALLY_PAID, FeeStatus.OVERDUE]]
    
    return {
        "student_id": student_id,
        "total_due": total_due,
        "total_paid": total_paid,
        "pending_fees": pending_fees
    }


@router.put("/{fee_id}", response_model=FeeResponse)
async def update_fee(
    fee_id: int,
    update_data: FeeUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update fee record (admin only)"""
    
    fee = db.query(Fee).filter(Fee.id == fee_id).first()
    if not fee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee not found"
        )
    
    update_dict = update_data.dict(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(fee, key, value)
    
    # Recalculate amount due
    fee.amount_due = fee.total_amount - fee.amount_paid
    
    db.commit()
    db.refresh(fee)
    
    return fee


@router.get("/", response_model=list[FeeResponse])
async def list_fees(
    status: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """List all fees (admin only)"""
    
    query = db.query(Fee)
    
    if status:
        query = query.filter(Fee.status == status)
    
    fees = query.offset(skip).limit(limit).all()
    return fees
