import logging
from typing import List, Dict, Any
from datetime import time

logger = logging.getLogger(__name__)


class TimetableOptimizer:
    """Service for optimizing timetable"""
    
    def __init__(self):
        pass
    
    def optimize_timetable(
        self,
        classes: List[Dict[str, Any]],
        faculty: List[Dict[str, Any]],
        rooms: List[Dict[str, Any]],
        constraints: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Optimize timetable"""
        try:
            if constraints is None:
                constraints = {}
            
            max_classes_per_day = constraints.get('max_classes_per_day', 6)
            max_classes_per_week = constraints.get('max_classes_per_week', 30)
            days = constraints.get('days', ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'])
            slots_per_day = constraints.get('slots_per_day', 6)
            
            # Simple scheduling algorithm without OR-Tools
            schedule = []
            scheduled_classes = set()
            
            for class_item in classes:
                for d_idx, day in enumerate(days):
                    for slot in range(slots_per_day):
                        for fac in faculty:
                            for room in rooms:
                                # Check if this combination works
                                conflict = False
                                for scheduled in schedule:
                                    if (scheduled['day'] == day and 
                                        scheduled['slot'] == slot and 
                                        (scheduled['faculty_id'] == fac.get('id') or 
                                         scheduled['room_id'] == room.get('id'))):
                                        conflict = True
                                        break
                                
                                if not conflict:
                                    schedule.append({
                                        'class_id': class_item.get('id'),
                                        'day': day,
                                        'slot': slot,
                                        'faculty_id': fac.get('id'),
                                        'room_id': room.get('id')
                                    })
                                    scheduled_classes.add(class_item.get('id'))
                                    break
                            if class_item.get('id') in scheduled_classes:
                                break
                        if class_item.get('id') in scheduled_classes:
                            break
                    if class_item.get('id') in scheduled_classes:
                        break
            
            unscheduled = len(classes) - len(scheduled_classes)
            
            return {
                'status': 'success',
                'schedule': schedule,
                'unscheduled_count': unscheduled,
                'solver_status': 'success'
            }
        
        except Exception as e:
            logger.error(f"Error optimizing timetable: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def validate_timetable(self, schedule: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate a timetable schedule"""
        try:
            errors = []
            warnings = []
            
            scheduled_slots = {}
            for item in schedule:
                key = (item['day'], item['slot'], item['room_id'])
                if key in scheduled_slots:
                    errors.append(f"Room {item['room_id']} has conflict on {item['day']} slot {item['slot']}")
                scheduled_slots[key] = item
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings
            }
        except Exception as e:
            logger.error(f"Error validating timetable: {str(e)}")
            return {
                'valid': False,
                'errors': [str(e)]
            }


timetable_optimizer = TimetableOptimizer()
