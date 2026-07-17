import face_recognition
import numpy as np
import cv2
import os
import pickle
import logging
from pathlib import Path
from typing import Optional, Tuple, List

from app.config import settings

logger = logging.getLogger(__name__)


class FaceRecognitionService:
    """Service for face recognition and attendance"""
    
    def __init__(self):
        self.known_faces_dir = settings.KNOWN_FACES_DIR
        self.face_encoding_path = os.path.join(self.known_faces_dir, "face_encodings.pkl")
        self.model = settings.FACE_DETECTION_MODEL
        self.tolerance = settings.FACE_DISTANCE_THRESHOLD
        
        Path(self.known_faces_dir).mkdir(parents=True, exist_ok=True)
        
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_face_encodings()
    
    def load_face_encodings(self):
        """Load face encodings from pickle file"""
        try:
            if os.path.exists(self.face_encoding_path):
                with open(self.face_encoding_path, 'rb') as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data.get('encodings', [])
                    self.known_face_names = data.get('names', [])
                logger.info(f"Loaded {len(self.known_face_names)} face encodings")
        except Exception as e:
            logger.error(f"Error loading face encodings: {str(e)}")
    
    def save_face_encodings(self):
        """Save face encodings to pickle file"""
        try:
            data = {
                'encodings': self.known_face_encodings,
                'names': self.known_face_names
            }
            with open(self.face_encoding_path, 'wb') as f:
                pickle.dump(data, f)
            logger.info("Face encodings saved")
        except Exception as e:
            logger.error(f"Error saving face encodings: {str(e)}")
    
    def register_face(self, image_path: str, student_id: str) -> bool:
        """Register a student's face"""
        try:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                logger.warning(f"No face found in image for student {student_id}")
                return False
            
            encoding = face_encodings[0]
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(student_id)
            
            self.save_face_encodings()
            logger.info(f"Face registered for student {student_id}")
            return True
        except Exception as e:
            logger.error(f"Error registering face: {str(e)}")
            return False
    
    def recognize_faces(self, image_path: str) -> List[Tuple[str, float]]:
        """Recognize faces in an image"""
        try:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            face_locations = face_recognition.face_locations(image)
            
            recognized_faces = []
            
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_face_encodings,
                    face_encoding,
                    tolerance=self.tolerance
                )
                name = "Unknown"
                confidence = 0.0
                
                face_distances = face_recognition.face_distance(
                    self.known_face_encodings,
                    face_encoding
                )
                
                if len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                
                recognized_faces.append((name, confidence))
            
            return recognized_faces
        except Exception as e:
            logger.error(f"Error recognizing faces: {str(e)}")
            return []
    
    def get_face_encoding_from_image(self, image_path: str) -> Optional[np.ndarray]:
        """Get face encoding from image"""
        try:
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) > 0:
                return face_encodings[0]
            return None
        except Exception as e:
            logger.error(f"Error getting face encoding: {str(e)}")
            return None


face_recognition_service = FaceRecognitionService()
