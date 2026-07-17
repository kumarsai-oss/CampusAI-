from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, UserRole
from app.models.faculty import Faculty
from app.schemas.faculty import FacultyCreate, FacultyResponse, FacultyUpdate
from app.security import get_admin_user, get_current_user

router = APIRouter(prefix="/api/faculty", tags=["Faculty"])


@router.post("/", response_model=FacultyResponse, status_code=status.HTTP_201_CREATED)
async def create_faculty(
    faculty_data: FacultyCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new faculty (admin only)"""
    
    user = db.query(User).filter(User.id == faculty_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    existing_faculty = db.query(Faculty).filter(Faculty.user_id == faculty_data.user_id).first()
    if existing_faculty:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Faculty already exists for this user"
        )
    
    existing_emp_id = db.query(Faculty).filter(Faculty.employee_id == faculty_data.employee_id).first()
    if existing_emp_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    new_faculty = Faculty(**faculty_data.dict())
    db.add(new_faculty)
    db.commit()
    db.refresh(new_faculty)
    
    return new_faculty


@router.get("/", response_model=list[FacultyResponse])
async def list_faculty(
    department: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List faculty members"""
    
    query = db.query(Faculty)
    
    if department:
        query = query.filter(Faculty.department == department)
    
    faculty = query.offset(skip).limit(limit).all()
    return faculty


@router.get("/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(
    faculty_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get faculty details"""
    
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )
    
    return faculty


@router.put("/{faculty_id}", response_model=FacultyResponse)
async def update_faculty(
    faculty_id: int,
    update_data: FacultyUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update faculty (admin only)"""
    
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )
    
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(faculty, key, value)
    
    db.commit()
    db.refresh(faculty)
    
    return faculty


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    faculty_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete faculty (admin only)"""
    
    faculty = db.query(Faculty).filter(Faculty.id == faculty_id).first()
    if not faculty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Faculty not found"
        )
    
    db.delete(faculty)
    db.commit()
    
    return None
