from abc import ABC, abstractmethod
from utils.helpers import clear_screen, print_header

class BaseUser(ABC):
    """Abstract base class for all user types"""
    
    def __init__(self, user_data: dict):
        self.user_id = user_data.get('user_id')
        self.username = user_data.get('username')
        self.role = user_data.get('role')
        self.email = user_data.get('email')
        self.is_logged_in = True
    
    @abstractmethod
    def show_dashboard(self) -> bool:
        """Show user-specific dashboard, returns False if logout"""
        pass
    
    def logout(self) -> bool:
        """Handle logout"""
        confirm = input("\nAre you sure you want to logout? (y/n): ").lower()
        if confirm == 'y':
            print("\n Logging out...")
            self.is_logged_in = False
            return False
        return True
