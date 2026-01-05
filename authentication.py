import json
import hashlib
import os
from getpass import getpass
from utils.helpers import generate_id

class AuthSystem:
    """Handles user authentication and registration"""
    
    def __init__(self):
        self.data_file = 'data/users.json'
        self._initialize_data()
    
    def _initialize_data(self):
        """Create users.json if it doesn't exist"""
        if not os.path.exists(self.data_file):
            # Create default admin user: admin / admin123
            default_data = {
                "users": {
                    "ADMIN001": {
                        "username": "admin",
                        "password_hash": self._hash_password("admin123"),
                        "role": "staff",
                        "email": "admin@school.edu"
                    }
                }
            }
            with open(self.data_file, 'w') as f:
                json.dump(default_data, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self) -> dict:
        """User login functionality"""
        print("\n" + "="*50)
        print("LOGIN")
        print("="*50)
        
        username = input("Username: ").strip()
        password = getpass("Password: ").strip()
        
        users_data = self._load_users()
        password_hash = self._hash_password(password)
        
        for user_id, user_info in users_data['users'].items():
            if user_info['username'] == username and user_info['password_hash'] == password_hash:
                return {
                    'user_id': user_id,
                    'username': username,
                    'role': user_info['role'],
                    'email': user_info.get('email', '')
                }
        
        return None
    
    def register_user(self, current_user: dict) -> bool:
        """Register new user (Staff only)"""
        if current_user.get('role') != 'staff':
            input("\n❌ Only staff can register new users! Press Enter...")
            return False
        
        print("\n" + "="*50)
        print("REGISTER NEW USER")
        print("="*50)
        
        username = input("Enter username: ").strip()
        email = input("Enter email: ").strip()
        role = input("Enter role (student/teacher/staff): ").strip().lower()
        
        if role not in ['student', 'teacher', 'staff']:
            input("\n⚠️  Invalid role! Press Enter to continue...")
            return False
        
        # Auto-generate user ID based on role
        prefix = {'student': 'STU', 'teacher': 'TEC', 'staff': 'STA'}
        user_id = generate_id(prefix[role], self._load_users()['users'].keys())
        
        # Default password is username + 123
        temp_password = username + "123"
        
        users_data = self._load_users()
        users_data['users'][user_id] = {
            'username': username,
            'password_hash': self._hash_password(temp_password),
            'role': role,
            'email': email
        }
        
        self._save_users(users_data)
        
        # Create role-specific record
        if role == 'student':
            self._create_student_record(user_id, username, email)
        elif role == 'teacher':
            self._create_teacher_record(user_id, username, email)
        elif role == 'staff':
            self._create_staff_record(user_id, username, email)
        
        print(f"\n✅ User created successfully!")
        print(f"User ID: {user_id}")
        print(f"Temporary Password: {temp_password}")
        input("\nPress Enter to continue...")
        return True
    
    def _create_student_record(self, user_id, username, email):
        """Initialize student record"""
        from data_manager import DataManager
        dm = DataManager()
        students = dm._load_json('data/students.json')
        students[user_id] = {
            'name': username,
            'email': email,
            'enrollment_date': '2024-01-01',
            'courses': [],
            'grades': {},
            'attendance': {},
            'contact': {'phone': '', 'address': ''}
        }
        dm._save_json('data/students.json', students)
    
    def _create_teacher_record(self, user_id, username, email):
        """Initialize teacher record"""
        from data_manager import DataManager
        dm = DataManager()
        teachers = dm._load_json('data/teachers.json')
        teachers[user_id] = {
            'name': username,
            'email': email,
            'department': 'General',
            'courses': [],
            'contact': {'phone': '', 'office': ''}
        }
        dm._save_json('data/teachers.json', teachers)
    
    def _create_staff_record(self, user_id, username, email):
        """Initialize staff record"""
        from data_manager import DataManager
        dm = DataManager()
        staff = dm._load_json('data/staff.json')
        staff[user_id] = {
            'name': username,
            'email': email,
            'department': 'Administration',
            'position': 'Staff',
            'permissions': ['full_access']
        }
        dm._save_json('data/staff.json', staff)
    
    def _load_users(self) -> dict:
        """Load users from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except:
            return {'users': {}}
    
    def _save_users(self, data: dict):
        """Save users to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def reset_password(self, current_user: dict):
        """Reset password for any user (Staff only)"""
        if current_user.get('role') != 'staff':
            input("\n❌ Only staff can reset passwords! Press Enter...")
            return
        
        target_user_id = input("Enter User ID to reset: ").strip().upper()
        
        users_data = self._load_users()
        if target_user_id not in users_data['users']:
            input("\n⚠️  User not found! Press Enter...")
            return
        
        username = users_data['users'][target_user_id]['username']
        new_password = username + "123"  # Reset to default
        
        users_data['users'][target_user_id]['password_hash'] = self._hash_password(new_password)
        self._save_users(users_data)
        
        print(f"\n✅ Password reset for {username}!")
        print(f"New password: {new_password}")
        input("\nPress Enter to continue...")
