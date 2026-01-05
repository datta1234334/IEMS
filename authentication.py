"""
Authentication Module
Handles user login and authentication
"""

from modules.data_manager import DataManager

class Authentication:
    def authenticate(self, user_id, password, user_type):
        """Authenticate user credentials"""
        filename = f"{user_type}s.txt"
        user = DataManager.find_record(filename, "id", user_id)
        
        if user and user.get("password") == password:
            return user
        return None
    
    def change_password(self, user_id, user_type, old_password, new_password):
        """Change user password"""
        filename = f"{user_type}s.txt"
        user = DataManager.find_record(filename, "id", user_id)
        
        if not user:
            return False, "User not found"
        
        if user.get("password") != old_password:
            return False, "Incorrect old password"
        
        user["password"] = new_password
        if DataManager.update_record(filename, "id", user_id, user):
            return True, "Password changed successfully"
        
        return False, "Failed to update password"