from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.models.user import User
from app.models.placement import Placement, PlacementDrive, PlacementStatus
from app.models.student import Student
from app.schemas.placement import (
    PlacementCreate, PlacementResponse, PlacementUpdate,
    PlacementDriveCreate, PlacementDriveResponse,
    ResumeATSAnalysisRequest, ResumeATSAnalysisResponse
)
from app.security import get_current_user, get_admin_user, get_faculty_user
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/api/placements", tags=["Placements"])


@router.post("/drives", response_model=PlacementDriveResponse, status_code=status.HTTP_201_CREATED)
async def create_placement_drive(
    drive_data: PlacementDriveCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new placement drive (admin only)"""
    
    new_drive = PlacementDrive(**drive_data.dict())
    db.add(new_drive)
    db.commit()
    db.refresh(new_drive)
    
    return new_drive


@router.get("/drives", response_model=list[PlacementDriveResponse])
async def list_placement_drives(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List placement drives"""
    
    drives = db.query(PlacementDrive).offset(skip).limit(limit).all()
    return drives


@router.post("/", response_model=PlacementResponse, status_code=status.HTTP_201_CREATED)
async def create_placement(
    placement_data: PlacementCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a placement record (admin only)"""
    
    student = db.query(Student).filter(Student.id == placement_data.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    existing = db.query(Placement).filter(Placement.student_id == placement_data.student_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Placement already exists for this student"
        )
    
    new_placement = Placement(**placement_data.dict())
    db.add(new_placement)
    db.commit()
    db.refresh(new_placement)
    
    return new_placement


@router.get("/student/{student_id}", response_model=PlacementResponse)
async def get_student_placement(
    student_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get student's placement record"""
    
    placement = db.query(Placement).filter(Placement.student_id == student_id).first()
    if not placement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Placement record not found"
        )
    
    return placement


@router.put("/{placement_id}", response_model=PlacementResponse)
async def update_placement(
    placement_id: int,
    update_data: PlacementUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update placement record (admin only)"""
    
    placement = db.query(Placement).filter(Placement.id == placement_id).first()
    if not placement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Placement not found"
        )
    
    update_dict = update_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(placement, key, value)
    
    db.commit()
    db.refresh(placement)
    
    return placement


@router.post("/resume/analyze", response_model=ResumeATSAnalysisResponse)
async def analyze_resume(
    request: ResumeATSAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze resume for ATS compatibility"""
    
    result = await gemini_service.analyze_resume_for_ats(
        request.resume_text,
        request.job_description
    )
    
    return result
