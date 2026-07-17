from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.notice import Notice, NoticeType
from app.schemas.notice import (
    NoticeCreate, NoticeResponse, NoticeUpdate, NoticeSummarizationRequest
)
from app.security import get_current_user, get_admin_user
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/api/notices", tags=["Notices"])


@router.post("/", response_model=NoticeResponse, status_code=status.HTTP_201_CREATED)
async def create_notice(
    notice_data: NoticeCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new notice (admin only)"""
    
    # Generate summary using Gemini
    summary = await gemini_service.summarize_text(notice_data.content, max_length=200)
    
    new_notice = Notice(
        **notice_data.dict(),
        issued_by=current_user.id,
        summary=summary
    )
    db.add(new_notice)
    db.commit()
    db.refresh(new_notice)
    
    return new_notice


@router.get("/", response_model=list[NoticeResponse])
async def list_notices(
    notice_type: str = Query(None),
    department: str = Query(None),
    is_published: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List notices"""
    
    query = db.query(Notice).filter(Notice.is_published == is_published)
    
    if notice_type:
        query = query.filter(Notice.notice_type == notice_type)
    if department:
        query = query.filter(Notice.department == department)
    
    notices = query.order_by(Notice.created_at.desc()).offset(skip).limit(limit).all()
    return notices


@router.get("/{notice_id}", response_model=NoticeResponse)
async def get_notice(
    notice_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notice details"""
    
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )
    
    return notice


@router.put("/{notice_id}", response_model=NoticeResponse)
async def update_notice(
    notice_id: int,
    update_data: NoticeUpdate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Update notice (admin only)"""
    
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )
    
    update_dict = update_data.dict(exclude_unset=True)
    
    # Regenerate summary if content changed
    if 'content' in update_dict:
        summary = await gemini_service.summarize_text(update_dict['content'], max_length=200)
        update_dict['summary'] = summary
    
    for key, value in update_dict.items():
        setattr(notice, key, value)
    
    db.commit()
    db.refresh(notice)
    
    return notice


@router.delete("/{notice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notice(
    notice_id: int,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """Delete notice (admin only)"""
    
    notice = db.query(Notice).filter(Notice.id == notice_id).first()
    if not notice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notice not found"
        )
    
    db.delete(notice)
    db.commit()
    
    return None


@router.post("/summarize")
async def summarize_notice(
    request: NoticeSummarizationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Summarize notice content using AI"""
    
    max_length = request.max_length or 200
    summary = await gemini_service.summarize_text(request.content, max_length=max_length)
    
    return {"summary": summary}
