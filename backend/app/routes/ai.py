from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserResponse
from app.security import get_current_user
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/api/ai", tags=["AI Features"])


class ChatMessage:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content


@router.post("/chat")
async def chat_with_bot(
    message: dict,
    current_user: User = Depends(get_current_user)
):
    """Chat with AI bot"""
    
    user_message = message.get("message", "")
    
    if not user_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )
    
    response = await gemini_service.chat_with_bot(user_message)
    
    return {
        "user_message": user_message,
        "bot_response": response,
        "timestamp": None
    }


@router.post("/summarize")
async def summarize_content(
    request: dict,
    current_user: User = Depends(get_current_user)
):
    """Summarize content using AI"""
    
    content = request.get("content", "")
    max_length = request.get("max_length", 200)
    
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Content cannot be empty"
        )
    
    summary = await gemini_service.summarize_text(content, max_length=max_length)
    
    return {
        "original_length": len(content),
        "summary_length": len(summary),
        "summary": summary
    }


@router.post("/performance-prediction")
async def predict_performance(
    student_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Predict student performance using ML"""
    
    from app.services.performance_predictor import performance_predictor
    
    result = performance_predictor.predict_performance(student_data)
    
    return result
