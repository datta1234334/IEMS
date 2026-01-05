"""
Data Manager Module
Handles all file-based data operations
"""

import os
import json

class DataManager:
    DATA_DIR = "data"
    
    @staticmethod
    def ensure_file(filename):
        """Ensure file exists"""
        filepath = os.path.join(DataManager.DATA_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                f.write("")
        return filepath
    
    @staticmethod
    def read_data(filename):
        """Read data from file"""
        filepath = DataManager.ensure_file(filename)
        data = []
        
        try:
            with open(filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data.append(json.loads(line))
        except Exception as e:
            print(f"Error reading {filename}: {e}")
        
        return data
    
    @staticmethod
    def write_data(filename, data):
        """Write data to file"""
        filepath = DataManager.ensure_file(filename)
        
        try:
            with open(filepath, 'w') as f:
                for item in data:
                    f.write(json.dumps(item) + "\n")
            return True
        except Exception as e:
            print(f"Error writing {filename}: {e}")
            return False
    
    @staticmethod
    def add_record(filename, record):
        """Add a single record"""
        data = DataManager.read_data(filename)
        data.append(record)
        return DataManager.write_data(filename, data)
    
    @staticmethod
    def update_record(filename, key, value, updated_record):
        """Update a record based on key-value match"""
        data = DataManager.read_data(filename)
        updated = False
        
        for i, record in enumerate(data):
            if record.get(key) == value:
                data[i] = updated_record
                updated = True
                break
        
        if updated:
            return DataManager.write_data(filename, data)
        return False
    
    @staticmethod
    def delete_record(filename, key, value):
        """Delete a record based on key-value match"""
        data = DataManager.read_data(filename)
        data = [record for record in data if record.get(key) != value]
        return DataManager.write_data(filename, data)
    
    @staticmethod
    def find_record(filename, key, value):
        """Find a single record"""
        data = DataManager.read_data(filename)
        for record in data:
            if record.get(key) == value:
                return record
        return None
    
    @staticmethod
    def find_records(filename, key, value):
        """Find multiple records"""
        data = DataManager.read_data(filename)
        return [record for record in data if record.get(key) == value]
    
    @staticmethod
    def generate_id(filename, prefix):
        """Generate unique ID"""
        data = DataManager.read_data(filename)
        if not data:
            return f"{prefix}001"
        
        # Extract numbers from existing IDs
        numbers = []
        for record in data:
            record_id = record.get('id', '')
            if record_id.startswith(prefix):
                try:
                    num = int(record_id[len(prefix):])
                    numbers.append(num)
                except:
                    pass
        
        next_num = max(numbers) + 1 if numbers else 1
        return f"{prefix}{next_num:03d}"
    
    @staticmethod
    def initialize_system():
        """Initialize system with default data"""
        # Create default staff account
        staff_data = DataManager.read_data("staff.txt")
        if not staff_data:
            default_staff = {
                "id": "STF001",
                "name": "Admin Staff",
                "email": "admin@smuct.edu",
                "phone": "01700000000",
                "password": "admin123",
                "role": "Administrator"
            }
            DataManager.add_record("staff.txt", default_staff)
            print("✅ Default staff account created (STF001/admin123)")
        
        # Create sample courses
        courses_data = DataManager.read_data("courses.txt")
        if not courses_data:
            sample_courses = [
                {"id": "CSE101", "name": "Introduction to Programming", "credits": 3, "teacher_id": ""},
                {"id": "CSE102", "name": "Data Structures", "credits": 3, "teacher_id": ""},
                {"id": "CSE201", "name": "Database Management", "credits": 3, "teacher_id": ""},
                {"id": "CSE202", "name": "Web Development", "credits": 3, "teacher_id": ""},
                {"id": "ENG101", "name": "English Composition", "credits": 3, "teacher_id": ""}
            ]
            DataManager.write_data("courses.txt", sample_courses)
            print("✅ Sample courses created")