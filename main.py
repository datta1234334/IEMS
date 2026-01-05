"""
Shanto Mariam University of Creative Technology
Integrated Educational Management System (IEMS)
Main Application Entry Point
"""

import os
import sys
from modules.authentication import Authentication
from modules.student import StudentModule
from modules.teacher import TeacherModule
from modules.staff import StaffModule
from utils.helpers import clear_screen, print_header, pause

class IEMS:
    def __init__(self):
        self.auth = Authentication()
        self.current_user = None
        self.user_type = None
        
    def run(self):
        """Main application loop"""
        while True:
            clear_screen()
            print_header("SHANTO MARIAM UNIVERSITY OF CREATIVE TECHNOLOGY")
            print_header("INTEGRATED EDUCATIONAL MANAGEMENT SYSTEM", "=")
            
            if not self.current_user:
                self.show_login_menu()
            else:
                self.show_dashboard()
    
    def show_login_menu(self):
        """Display login menu"""
        print("\n1. Student Login")
        print("2. Teacher Login")
        print("3. Staff Login")
        print("4. Exit System")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            self.login("student")
        elif choice == "2":
            self.login("teacher")
        elif choice == "3":
            self.login("staff")
        elif choice == "4":
            print("\nThank you for using IEMS!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice!")
            pause()
    
    def login(self, user_type):
        """Handle user login"""
        clear_screen()
        print_header(f"{user_type.upper()} LOGIN")
        
        user_id = input("\nEnter User ID: ").strip()
        password = input("Enter Password: ").strip()
        
        user = self.auth.authenticate(user_id, password, user_type)
        
        if user:
            self.current_user = user
            self.user_type = user_type
            print(f"\n✅ Login successful! Welcome, {user['name']}")
            pause()
        else:
            print("\n❌ Invalid credentials!")
            pause()
    
    def show_dashboard(self):
        """Show user-specific dashboard"""
        if self.user_type == "student":
            module = StudentModule(self.current_user)
        elif self.user_type == "teacher":
            module = TeacherModule(self.current_user)
        else:
            module = StaffModule(self.current_user)
        
        logout = module.show_menu()
        
        if logout:
            self.current_user = None
            self.user_type = None

if __name__ == "__main__":
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Run the application
    app = IEMS()
    app.run()