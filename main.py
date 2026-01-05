#!/usr/bin/env python3
"""
Student IEMS - Main Application
Integrated Education Management System
"""

import os
from auth import AuthSystem
from models.student import StudentDashboard
from models.teacher import TeacherDashboard
from models.staff import StaffDashboard
from utils.helpers import clear_screen, print_header

def main():
    """Main application loop"""
    auth = AuthSystem()
    current_user = None
    
    while True:
        clear_screen()
        print_header("STUDENT IEMS - MAIN MENU")
        
        if not current_user:
            print("1. Login")
            print("2. Exit")
            choice = input("\nSelect option (1-2): ").strip()
            
            if choice == '1':
                current_user = auth.login()
                if current_user:
                    input("\n✅ Login successful! Press Enter to continue...")
                else:
                    input("\n❌ Invalid credentials! Press Enter to continue...")
            elif choice == '2':
                print("\n👋 Thank you for using Student IEMS!")
                break
            else:
                input("\n⚠️  Invalid option! Press Enter to continue...")
        else:
            # Route to appropriate dashboard based on role
            role = current_user.get('role', '').lower()
            
            if role == 'student':
                dashboard = StudentDashboard(current_user)
            elif role == 'teacher':
                dashboard = TeacherDashboard(current_user)
            elif role == 'staff':
                dashboard = StaffDashboard(current_user)
            else:
                input(f"\n⚠️  Unknown role: {role}! Press Enter to continue...")
                current_user = None
                continue
            
            # Show dashboard and handle logout
            if not dashboard.show():
                current_user = None  # Logout

if __name__ == "__main__":
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    main()
