from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.models.complaint import Complaint, ComplaintStatus, ComplaintCategory
from app.models.student import Student
from app.schemas.complaint import (
    ComplaintCreate, ComplaintResponse, ComplaintUpdate, ComplaintListResponse
)
from app.security import get_current_user, get_admin_user

router = APIRouter(prefix="/api/complaints", tags=["Complaints"])


@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def create_complaint(
    complaint_data: ComplaintCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new complaint"""
    
    # Verify student belongs to current user if student role
    if current_user.role == UserRole.STUDENT:
        student = db.query(Student).filter(
            (Student.id == complaint_data.student_id) &
            (Student.user_id == current_user.id)
        ).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create complaint for this student"
            )
    
    new_complaint = Complaint(**complaint_data.dict())
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    
    return new_complaint


@router.get("/", response_model=ComplaintListResponse)
async def list_complaints(
    status: str = Query(None),
    category: str = Query(None),
    priority: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List complaints"""
    
    query = db.query(Complaint)
    
    # Filter by role
    if current_user.role == UserRole.STUDENT:
        # Students can only see their own complaints
        student = db.query(Student).filter(Student.user_id == current_user.id).first()
        if student:
            query = query.filter(Complaint.student_id == student.id)
    
    if status:
        query = query.filter(Complaint.status == status)
    if category:
        query = query.filter(Complaint.category == category)
    if priority:
        query = query.filter(Complaint.priority == priority)
    
    complaints = query.order_by(Complaint.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": len(complaints),
        "complaints": complaints
    }


@router.get("/student/{student_id}", response_model=list[ComplaintResponse])
async def get_student_complaints(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complaints for a student"""
    
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Authorization check
    if current_user.role == UserRole.STUDENT and current_user.id != student.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    complaints = db.query(Complaint).filter(
        Complaint.student_id == student_id
    ).order_by(Complaint.created_at.desc()).all()
    
    return complaints


@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get complaint details"""
    
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Authorization check
    if current_user.role == UserRole.STUDENT:
        student = db.query(Student).filter(
            (Student.id == complaint.student_id) &
            (Student.user_id == current_user.id)
        ).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
    
    return complaint


@router.put("/{complaint_id}", response_model=ComplaintResponse)
async def update_complaint(
    complaint_id: int,
    update_data: ComplaintUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update complaint (admin only)"""
    
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    update_dict = update_data.dict(exclude_unset=True)
    
    # Update resolved_at if status changed to resolved
    if 'status' in update_dict and update_dict['status'] == ComplaintStatus.RESOLVED:
        from datetime import datetime
        update_dict['resolved_at'] = datetime.utcnow()
    
    for key, value in update_dict.items():
        setattr(complaint, key, value)
    
    db.commit()
    db.refresh(complaint)
    
    return complaint
