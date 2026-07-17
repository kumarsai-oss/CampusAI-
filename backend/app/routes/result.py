from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.models.result import Result, Subject, Grade
from app.models.student import Student
from app.schemas.result import (
    ResultCreate, ResultResponse, ResultUpdate, SubjectCreate, SubjectResponse, StudentResultsResponse
)
from app.security import get_current_user, get_admin_user, get_faculty_user

router = APIRouter(prefix="/api/results", tags=["Results"])


@router.post("/subjects", response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(
    subject_data: SubjectCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new subject (admin only)"""
    
    existing = db.query(Subject).filter(Subject.subject_code == subject_data.subject_code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject code already exists"
        )
    
    new_subject = Subject(**subject_data.dict())
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    
    return new_subject


@router.get("/subjects", response_model=list[SubjectResponse])
async def list_subjects(
    semester: int = Query(None),
    department: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List subjects"""
    
    query = db.query(Subject)
    
    if semester:
        query = query.filter(Subject.semester == semester)
    if department:
        query = query.filter(Subject.department == department)
    
    subjects = query.offset(skip).limit(limit).all()
    return subjects


def calculate_grade(total_marks: float) -> tuple[Grade, float]:
    """Calculate grade and grade points"""
    if total_marks >= 90:
        return Grade.A_PLUS, 4.0
    elif total_marks >= 80:
        return Grade.A, 3.9
    elif total_marks >= 70:
        return Grade.B_PLUS, 3.7
    elif total_marks >= 60:
        return Grade.B, 3.3
    elif total_marks >= 50:
        return Grade.C, 2.5
    elif total_marks >= 40:
        return Grade.D, 2.0
    else:
        return Grade.F, 0.0


@router.post("/", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
async def create_result(
    result_data: ResultCreate,
    current_user: User = Depends(get_faculty_user),
    db: Session = Depends(get_db)
):
    """Create a result record"""
    
    student = db.query(Student).filter(Student.id == result_data.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    subject = db.query(Subject).filter(Subject.id == result_data.subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    existing = db.query(Result).filter(
        (Result.student_id == result_data.student_id) &
        (Result.subject_id == result_data.subject_id) &
        (Result.academic_year == result_data.academic_year)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Result already exists for this student-subject combination"
        )
    
    grade, grade_points = calculate_grade(result_data.total_marks)
    credit_earned = subject.credits * (grade_points / 4.0) if grade != Grade.F else 0
    
    new_result = Result(
        **result_data.dict(),
        grade=grade,
        grade_points=grade_points,
        credit_earned=credit_earned
    )
    
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    
    return new_result


@router.get("/student/{student_id}", response_model=StudentResultsResponse)
async def get_student_results(
    student_id: int,
    semester: int = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student's results"""
    
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
    
    query = db.query(Result).filter(Result.student_id == student_id)
    
    if semester:
        query = query.filter(Result.semester == semester)
    
    results = query.all()
    
    total_credits = sum([r.credit_earned for r in results])
    earned_credits = sum([r.credit_earned for r in results if r.grade != Grade.F])
    
    return {
        "student_id": student_id,
        "semester": semester or student.semester,
        "academic_year": results[0].academic_year if results else "2024-2025",
        "cgpa": student.cgpa,
        "total_credits": int(total_credits),
        "earned_credits": int(earned_credits),
        "results": results
    }


@router.put("/{result_id}", response_model=ResultResponse)
async def update_result(
    result_id: int,
    update_data: ResultUpdate,
    current_user: User = Depends(get_faculty_user),
    db: Session = Depends(get_db)
):
    """Update result"""
    
    result = db.query(Result).filter(Result.id == result_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    update_dict = update_data.dict(exclude_unset=True)
    
    for key, value in update_dict.items():
        setattr(result, key, value)
    
    # Recalculate total marks and grade
    if 'internal_marks' in update_dict or 'external_marks' in update_dict:
        result.total_marks = result.internal_marks + result.external_marks
        grade, grade_points = calculate_grade(result.total_marks)
        result.grade = grade
        result.grade_points = grade_points
        
        subject = db.query(Subject).filter(Subject.id == result.subject_id).first()
        result.credit_earned = subject.credits * (grade_points / 4.0) if grade != Grade.F else 0
    
    db.commit()
    db.refresh(result)
    
    return result
