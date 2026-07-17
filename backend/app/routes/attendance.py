from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User, UserRole
from app.models.attendance import Attendance, AttendanceStatus
from app.models.student import Student
from app.schemas.attendance import AttendanceCreate, AttendanceResponse, AttendanceUpdate, AttendanceReportResponse
from app.security import get_current_user, get_faculty_user
from app.services.face_recognition_service import face_recognition_service

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
async def mark_attendance(
    attendance_data: AttendanceCreate,
    current_user: User = Depends(get_faculty_user),
    db: Session = Depends(get_db)
):
    """Mark attendance for a student (faculty only)"""
    
    student = db.query(Student).filter(Student.id == attendance_data.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    new_attendance = Attendance(**attendance_data.dict())
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    
    return new_attendance


@router.get("/student/{student_id}", response_model=list[AttendanceResponse])
async def get_student_attendance(
    student_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student's attendance records"""
    
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
    
    records = db.query(Attendance).filter(
        Attendance.student_id == student_id
    ).offset(skip).limit(limit).all()
    
    return records


@router.get("/report/{student_id}", response_model=AttendanceReportResponse)
async def get_attendance_report(
    student_id: int,
    semester: int = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get attendance report for a student"""
    
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
    
    query = db.query(Attendance).filter(Attendance.student_id == student_id)
    
    records = query.all()
    
    total_classes = len(records)
    present_count = len([r for r in records if r.status == AttendanceStatus.PRESENT])
    absent_count = len([r for r in records if r.status == AttendanceStatus.ABSENT])
    late_count = len([r for r in records if r.status == AttendanceStatus.LATE])
    
    attendance_percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
    
    return {
        "student_id": student_id,
        "total_classes": total_classes,
        "present_count": present_count,
        "absent_count": absent_count,
        "late_count": late_count,
        "attendance_percentage": attendance_percentage,
        "subjects": []
    }


@router.put("/{attendance_id}", response_model=AttendanceResponse)
async def update_attendance(
    attendance_id: int,
    update_data: AttendanceUpdate,
    current_user: User = Depends(get_faculty_user),
    db: Session = Depends(get_db)
):
    """Update attendance record"""
    
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found"
        )
    
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(attendance, key, value)
    
    db.commit()
    db.refresh(attendance)
    
    return attendance
