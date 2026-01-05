import json
import os

class DataManager:
    """Handles all JSON data operations"""
    
    def __init__(self):
        self.data_dir = 'data'
        self._ensure_data_files()
    
    def _ensure_data_files(self):
        """Create all necessary JSON files if they don't exist"""
        files = {
            'students.json': {},
            'teachers.json': {},
            'staff.json': {},
            'courses.json': {
                "CS101": {"name": "Introduction to CS", "credits": 3, "instructor": "TBD"},
                "MATH201": {"name": "Calculus", "credits": 4, "instructor": "TBD"},
                "ENG101": {"name": "English Composition", "credits": 3, "instructor": "TBD"}
            },
            'attendance.json': {}
        }
        
        os.makedirs(self.data_dir, exist_ok=True)
        
        for filename, default_content in files.items():
            filepath = os.path.join(self.data_dir, filename)
            if not os.path.exists(filepath):
                self._save_json(filepath, default_content)
    
    def _load_json(self, filepath: str) -> dict:
        """Load data from JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_json(self, filepath: str, data: dict):
        """Save data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_user_data(self, user_id: str, role: str) -> dict:
        """Get user data based on role"""
        filename = f"{role}s.json"
        filepath = os.path.join(self.data_dir, filename)
        data = self._load_json(filepath)
        return data.get(user_id, {})
    
    def update_user_data(self, user_id: str, role: str, data: dict) -> bool:
        """Update user data"""
        filename = f"{role}s.json"
        filepath = os.path.join(self.data_dir, filename)
        all_data = self._load_json(filepath)
        all_data[user_id] = data
        self._save_json(filepath, all_data)
        return True
    
    def get_all_students(self) -> dict:
        """Get all student records"""
        return self._load_json(os.path.join(self.data_dir, 'students.json'))
    
    def get_all_courses(self) -> dict:
        """Get all courses"""
        return self._load_json(os.path.join(self.data_dir, 'courses.json'))
