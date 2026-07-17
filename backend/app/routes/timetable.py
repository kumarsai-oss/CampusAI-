from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.timetable import Timetable, TimeSlot, DayOfWeek
from app.schemas.timetable import (
    TimetableCreate, TimetableResponse, TimeSlotCreate, TimeSlotResponse,
    TimetableOptimizationRequest
)
from app.security import get_current_user, get_admin_user
from app.services.timetable_optimizer import timetable_optimizer

router = APIRouter(prefix="/api/timetable", tags=["Timetable"])


@router.post("/", response_model=TimetableResponse, status_code=status.HTTP_201_CREATED)
async def create_timetable(
    timetable_data: TimetableCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new timetable (admin only)"""
    
    existing = db.query(Timetable).filter(
        (Timetable.semester == timetable_data.semester) &
        (Timetable.department == timetable_data.department) &
        (Timetable.academic_year == timetable_data.academic_year)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Timetable already exists for this period"
        )
    
    new_timetable = Timetable(
        semester=timetable_data.semester,
        department=timetable_data.department,
        academic_year=timetable_data.academic_year
    )
    db.add(new_timetable)
    db.commit()
    db.refresh(new_timetable)
    
    # Add time slots if provided
    if timetable_data.time_slots:
        for slot_data in timetable_data.time_slots:
            new_slot = TimeSlot(
                timetable_id=new_timetable.id,
                **slot_data.dict()
            )
            db.add(new_slot)
        db.commit()
    
    db.refresh(new_timetable)
    return new_timetable


@router.get("/", response_model=list[TimetableResponse])
async def list_timetables(
    semester: int = Query(None),
    department: str = Query(None),
    academic_year: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List timetables"""
    
    query = db.query(Timetable)
    
    if semester:
        query = query.filter(Timetable.semester == semester)
    if department:
        query = query.filter(Timetable.department == department)
    if academic_year:
        query = query.filter(Timetable.academic_year == academic_year)
    
    timetables = query.offset(skip).limit(limit).all()
    return timetables


@router.get("/{timetable_id}", response_model=TimetableResponse)
async def get_timetable(
    timetable_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get timetable details"""
    
    timetable = db.query(Timetable).filter(Timetable.id == timetable_id).first()
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found"
        )
    
    time_slots = db.query(TimeSlot).filter(TimeSlot.timetable_id == timetable_id).all()
    
    return {
        **timetable.__dict__,
        "time_slots": time_slots
    }


@router.post("/slots", response_model=TimeSlotResponse, status_code=status.HTTP_201_CREATED)
async def add_time_slot(
    slot_data: TimeSlotCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Add time slot to timetable (admin only)"""
    
    timetable = db.query(Timetable).filter(Timetable.id == slot_data.timetable_id).first()
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found"
        )
    
    new_slot = TimeSlot(**slot_data.dict())
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)
    
    return new_slot


@router.post("/optimize", status_code=status.HTTP_200_OK)
async def optimize_timetable(
    request: TimetableOptimizationRequest,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Optimize timetable using OR-Tools (admin only)"""
    
    # Get timetable
    timetable = db.query(Timetable).filter(
        (Timetable.semester == request.semester) &
        (Timetable.department == request.department) &
        (Timetable.academic_year == request.academic_year)
    ).first()
    
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found"
        )
    
    time_slots = db.query(TimeSlot).filter(TimeSlot.timetable_id == timetable.id).all()
    
    result = timetable_optimizer.optimize_timetable(
        classes=[{"id": i} for i in range(len(time_slots))],
        faculty=[{"id": i} for i in range(5)],
        rooms=[{"id": i} for i in range(10)],
        constraints=request.constraints
    )
    
    return result
