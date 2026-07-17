import google.generativeai as genai
from app.config import settings
import logging
import json

logger = logging.getLogger(__name__)


class GeminiService:
    """Service for Gemini API interactions"""
    
    def __init__(self):
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    async def chat_with_bot(self, user_message: str, conversation_history: list = None) -> str:
        """Chat with Gemini bot"""
        try:
            if self.model is None:
                return "Gemini API not configured. Please set GEMINI_API_KEY in environment."
            
            if conversation_history is None:
                conversation_history = []
            
            system_prompt = """You are CampusAI, a helpful campus assistant bot. 
            You help students with academic queries, campus information, and general guidance.
            Be helpful, friendly, and provide accurate information."""
            
            conversation_history.append({
                "role": "user",
                "content": user_message
            })
            
            response = self.model.generate_content(
                [system_prompt] + [
                    f"{msg['role']}: {msg['content']}" 
                    for msg in conversation_history
                ]
            )
            
            bot_response = response.text
            conversation_history.append({
                "role": "assistant",
                "content": bot_response
            })
            
            return bot_response
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            return f"Error: {str(e)}"
    
    async def summarize_text(self, text: str, max_length: int = 200) -> str:
        """Summarize text using Gemini"""
        try:
            if self.model is None:
                return "Gemini API not configured."
            
            prompt = f"""Summarize the following text in {max_length} characters or less:
            
            {text}
            
            Provide only the summary without any preamble."""
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini summarization error: {str(e)}")
            return f"Error: {str(e)}"
    
    async def analyze_resume_for_ats(self, resume_text: str, job_description: str) -> dict:
        """Analyze resume for ATS compatibility"""
        try:
            if self.model is None:
                return {
                    "ats_score": 0,
                    "match_percentage": 0,
                    "matched_keywords": [],
                    "missing_keywords": [],
                    "recommendations": ["Gemini API not configured"]
                }
            
            prompt = f"""Analyze this resume against the job description and provide:
1. An ATS score (0-100)
2. List of matched keywords
3. List of missing important keywords
4. Top 3 recommendations for improvement

Resume:
{resume_text}

Job Description:
{job_description}

Format your response as JSON with keys: ats_score, match_percentage, matched_keywords, missing_keywords, recommendations"""
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                result = {
                    "ats_score": 70,
                    "match_percentage": 70,
                    "matched_keywords": [],
                    "missing_keywords": [],
                    "recommendations": [response_text]
                }
            
            return result
        except Exception as e:
            logger.error(f"Resume analysis error: {str(e)}")
            return {
                "ats_score": 0,
                "match_percentage": 0,
                "matched_keywords": [],
                "missing_keywords": [],
                "recommendations": [str(e)]
            }


gemini_service = GeminiService()
