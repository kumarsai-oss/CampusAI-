import numpy as np
import pickle
import os
import logging
from typing import Dict, List, Any, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from pathlib import Path

logger = logging.getLogger(__name__)


class PerformancePredictor:
    """Service for predicting student performance using ML"""
    
    def __init__(self, model_dir: str = "models"):
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, "performance_model.pkl")
        self.scaler_path = os.path.join(model_dir, "scaler.pkl")
        
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        
        self.model = None
        self.scaler = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info("Performance model loaded")
            
            if os.path.exists(self.scaler_path):
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                logger.info("Scaler loaded")
        except Exception as e:
            logger.warning(f"Could not load model: {str(e)}")
            self.model = None
            self.scaler = None
    
    def train_model(self, X: np.ndarray, y: np.ndarray) -> bool:
        """Train performance prediction model"""
        try:
            if self.scaler is None:
                self.scaler = StandardScaler()
            
            X_scaled = self.scaler.fit_transform(X)
            
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
            self.model.fit(X_scaled, y)
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            
            with open(self.scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            
            logger.info("Model trained and saved")
            return True
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            return False
    
    def predict_performance(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict student performance"""
        try:
            if self.model is None or self.scaler is None:
                return {
                    'status': 'error',
                    'message': 'Model not trained',
                    'prediction': None
                }
            
            features = np.array([
                student_data.get('attendance_percentage', 0),
                student_data.get('cgpa', 0),
                student_data.get('previous_semester_gpa', 0),
                student_data.get('study_hours_per_week', 0),
                student_data.get('assignment_submission_rate', 0),
                student_data.get('lab_performance', 0),
                student_data.get('test_average', 0)
            ]).reshape(1, -1)
            
            features_scaled = self.scaler.transform(features)
            
            prediction = self.model.predict(features_scaled)[0]
            
            feature_names = [
                'attendance_percentage',
                'cgpa',
                'previous_semester_gpa',
                'study_hours_per_week',
                'assignment_submission_rate',
                'lab_performance',
                'test_average'
            ]
            feature_importance = dict(zip(
                feature_names,
                self.model.feature_importances_.tolist()
            ))
            
            recommendations = self._generate_recommendations(student_data, prediction)
            
            return {
                'status': 'success',
                'prediction': float(prediction),
                'prediction_range': self._get_prediction_range(prediction),
                'feature_importance': feature_importance,
                'recommendations': recommendations
            }
        except Exception as e:
            logger.error(f"Error predicting performance: {str(e)}")
            return {
                'status': 'error',
                'message': str(e),
                'prediction': None
            }
    
    def _generate_recommendations(self, student_data: Dict[str, Any], prediction: float) -> List[str]:
        """Generate recommendations based on student data"""
        recommendations = []
        
        if student_data.get('attendance_percentage', 100) < 75:
            recommendations.append("Improve attendance. It's crucial for better grades.")
        
        if student_data.get('study_hours_per_week', 0) < 10:
            recommendations.append("Increase study hours. Aim for at least 10 hours per week.")
        
        if student_data.get('assignment_submission_rate', 100) < 90:
            recommendations.append("Submit assignments on time. This significantly impacts grades.")
        
        if student_data.get('lab_performance', 0) < 3:
            recommendations.append("Focus on lab work and practical skills.")
        
        if prediction < 5.0:
            recommendations.append("Consider seeking tutor support or attending extra classes.")
        
        if not recommendations:
            recommendations.append("Keep up the good work! Continue your current study habits.")
        
        return recommendations
    
    def _get_prediction_range(self, prediction: float) -> str:
        """Get prediction range category"""
        if prediction >= 8.0:
            return "Excellent (8.0 - 10.0)"
        elif prediction >= 7.0:
            return "Very Good (7.0 - 7.9)"
        elif prediction >= 6.0:
            return "Good (6.0 - 6.9)"
        elif prediction >= 5.0:
            return "Average (5.0 - 5.9)"
        else:
            return "Below Average (<5.0)"


performance_predictor = PerformancePredictor()
