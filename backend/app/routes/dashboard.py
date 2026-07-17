from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.result import Result
from app.models.fee import Fee
from app.security import get_current_user, get_admin_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/student-stats")
async def get_student_stats(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get student statistics (admin only)"""
    
    total_students = db.query(Student).count()
    active_students = db.query(Student).filter(Student.is_active == True).count()
    
    return {
        "total_students": total_students,
        "active_students": active_students,
        "inactive_students": total_students - active_students
    }


@router.get("/faculty-stats")
async def get_faculty_stats(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get faculty statistics (admin only)"""
    
    from app.models.faculty import Faculty
    total_faculty = db.query(Faculty).count()
    
    return {
        "total_faculty": total_faculty
    }


@router.get("/attendance-stats")
async def get_attendance_stats(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get attendance statistics (admin only)"""
    
    today = datetime.utcnow().date()
    
    today_attendance = db.query(Attendance).filter(
        Attendance.class_date >= datetime.combine(today, datetime.min.time())
    ).count()
    
    return {
        "today_attendance": today_attendance
    }


@router.get("/fee-stats")
async def get_fee_stats(
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Get fee statistics (admin only)"""
    
    from app.models.fee import FeeStatus
    
    total_fees = db.query(Fee).count()
    paid_fees = db.query(Fee).filter(Fee.status == FeeStatus.PAID).count()
    pending_fees = db.query(Fee).filter(Fee.status == FeeStatus.PENDING).count()
    
    return {
        "total_fees": total_fees,
        "paid_fees": paid_fees,
        "pending_fees": pending_fees
    }


@router.get("/student-dashboard")
async def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student dashboard info"""
    
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can access this endpoint"
        )
    
    student = db.query(Student).filter(Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student record not found"
        )
    
    # Get attendance
    total_attendance = db.query(Attendance).filter(
        Attendance.student_id == student.id
    ).count()
    
    present_attendance = db.query(Attendance).filter(
        Attendance.student_id == student.id,
        Attendance.status == "present"
    ).count()
    
    attendance_percentage = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    
    # Get results
    results = db.query(Result).filter(Result.student_id == student.id).all()
    
    # Get fees
    fees = db.query(Fee).filter(Fee.student_id == student.id).all()
    pending_fee_amount = sum([f.amount_due for f in fees if f.status == "pending"])
    
    return {
        "student_name": current_user.full_name,
        "roll_number": student.roll_number,
        "department": student.department,
        "semester": student.semester,
        "cgpa": student.cgpa,
        "attendance_percentage": attendance_percentage,
        "results_count": len(results),
        "pending_fees": pending_fee_amount
    }
