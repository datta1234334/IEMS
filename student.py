from models.user import BaseUser
from utils.helpers import clear_screen, print_header, print_menu
from data_manager import DataManager

class StudentDashboard(BaseUser):
    """Student-specific features and dashboard"""
    
    def __init__(self, user_data: dict):
        super().__init__(user_data)
        self.dm = DataManager()
        self.profile = self.dm.get_user_data(self.user_id, 'student')
    
    def show(self) -> bool:
        """Display student dashboard"""
        while self.is_logged_in:
            clear_screen()
            print_header(f"STUDENT DASHBOARD - {self.username}")
            print(f"User ID: {self.user_id} | Email: {self.email}")
            print("="*60)
            
            print_menu([
                "View My Profile",
                "View My Courses",
                "View Grades & Attendance",
                "Update Contact Info",
                "Change Password",
                "Logout"
            ])
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                self.view_profile()
            elif choice == '2':
                self.view_courses()
            elif choice == '3':
                self.view_grades_attendance()
            elif choice == '4':
                self.update_contact()
            elif choice == '5':
                self.change_password()
            elif choice == '6':
                return self.logout()
            else:
                input("\n  Invalid option! Press Enter to continue...")
        
        return False
    
    def view_profile(self):
        """Display student profile"""
        clear_screen()
        print_header("MY PROFILE")
        
        if not self.profile:
            print("\n Profile not found!")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n Name: {self.profile.get('name', 'N/A')}")
        print(f" Email: {self.profile.get('email', 'N/A')}")
        print(f" Enrollment: {self.profile.get('enrollment_date', 'N/A')}")
        print(f" Phone: {self.profile.get('contact', {}).get('phone', 'N/A')}")
        print(f" Address: {self.profile.get('contact', {}).get('address', 'N/A')}")
        
        input("\nPress Enter to continue...")
    
    def view_courses(self):
        """Display enrolled courses"""
        clear_screen()
        print_header("MY COURSES")
        
        courses = self.profile.get('courses', [])
        if not courses:
            print("\n No courses enrolled yet.")
        else:
            all_courses = self.dm.get_all_courses()
            print(f"\n{'Course Code':<12} {'Course Name':<30} {'Credits':<8}")
            print("-"*50)
            for course_code in courses:
                course = all_courses.get(course_code, {})
                print(f"{course_code:<12} {course.get('name', 'Unknown'):<30} {course.get('credits', 0):<8}")
        
        input("\nPress Enter to continue...")
    
    def view_grades_attendance(self):
        """Display grades and attendance"""
        clear_screen()
        print_header("GRADES & ATTENDANCE")
        
        grades = self.profile.get('grades', {})
        attendance = self.profile.get('attendance', {})
        
        print("\n GRADES:")
        if not grades:
            print("   No grades recorded yet.")
        else:
            for course, grade in grades.items():
                print(f"   {course}: {grade}")
        
        print("\n ATTENDANCE:")
        if not attendance:
            print("   No attendance records yet.")
        else:
            for course, status in attendance.items():
                print(f"   {course}: {status}%")
        
        input("\nPress Enter to continue...")
    
    def update_contact(self):
        """Update contact information"""
        clear_screen()
        print_header("UPDATE CONTACT INFO")
        
        phone = input(f"Enter new phone (current: {self.profile.get('contact', {}).get('phone', 'N/A')}): ").strip()
        address = input(f"Enter new address (current: {self.profile.get('contact', {}).get('address', 'N/A')}): ").strip()
        
        if phone:
            self.profile.setdefault('contact', {})['phone'] = phone
        if address:
            self.profile.setdefault('contact', {})['address'] = address
        
        self.dm.update_user_data(self.user_id, 'student', self.profile)
        print("\n Contact information updated!")
        input("\nPress Enter to continue...")
    
    def change_password(self):
        """Change password (would need auth system integration)"""
        input("\n  Password change feature coming soon! Press Enter...")
