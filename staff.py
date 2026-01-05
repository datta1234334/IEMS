from models.user import BaseUser
from utils.helpers import clear_screen, print_header, print_menu
from data_manager import DataManager
from auth import AuthSystem

class StaffDashboard(BaseUser):
    """Staff/Admin features and dashboard"""
    
    def __init__(self, user_data: dict):
        super().__init__(user_data)
        self.dm = DataManager()
        self.auth = AuthSystem()
        self.profile = self.dm.get_user_data(self.user_id, 'staff')
    
    def show(self) -> bool:
        """Display staff dashboard"""
        while self.is_logged_in:
            clear_screen()
            print_header(f"STAFF ADMIN PANEL - {self.username}")
            print(f"User ID: {self.user_id} | Role: Administrator")
            print("="*60)
            
            print_menu([
                "View System Statistics",
                "Manage Users",
                "View All Students",
                "View All Teachers",
                "View All Staff",
                "Register New User",
                "Reset User Password",
                "Logout"
            ])
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == '1':
                self.view_statistics()
            elif choice == '2':
                self.manage_users()
            elif choice == '3':
                self.view_all_students()
            elif choice == '4':
                self.view_all_teachers()
            elif choice == '5':
                self.view_all_staff()
            elif choice == '6':
                self.auth.register_user({'user_id': self.user_id, 'role': 'staff'})
            elif choice == '7':
                self.auth.reset_password({'user_id': self.user_id, 'role': 'staff'})
            elif choice == '8':
                return self.logout()
            else:
                input("\n  Invalid option! Press Enter to continue...")
        
        return False
    
    def view_statistics(self):
        """Display system statistics"""
        clear_screen()
        print_header("SYSTEM STATISTICS")
        
        users = self.auth._load_users()['users']
        students = self.dm.get_all_students()
        teachers = self.dm._load_json('data/teachers.json')
        staff = self.dm._load_json('data/staff.json')
        courses = self.dm.get_all_courses()
        
        print(f"\n Total Users: {len(users)}")
        print(f" Students: {len(students)}")
        print(f" Teachers: {len(teachers)}")
        print(f" Staff: {len(staff)}")
        print(f" Courses: {len(courses)}")
        
        input("\nPress Enter to continue...")
    
    def manage_users(self):
        """User management interface"""
        clear_screen()
        print_header("USER MANAGEMENT")
        
        users = self.auth._load_users()['users']
        print(f"\n{'User ID':<10} {'Username':<20} {'Role':<10} {'Email':<25}")
        print("-"*70)
        
        for user_id, info in users.items():
            print(f"{user_id:<10} {info['username']:<20} {info['role']:<10} {info.get('email', 'N/A'):<25}")
        
        input("\nPress Enter to continue...")
    
    def view_all_students(self):
        """Display all students"""
        clear_screen()
        print_header("ALL STUDENTS")
        
        students = self.dm.get_all_students()
        if not students:
            print("\n No students found!")
        else:
            print(f"\n{'Student ID':<12} {'Name':<20} {'Email':<25} {'Courses':<15}")
            print("-"*75)
            for stu_id, info in students.items():
                courses = len(info.get('courses', []))
                print(f"{stu_id:<12} {info.get('name', 'N/A'):<20} {info.get('email', 'N/A'):<25} {courses:<15}")
        
        input("\nPress Enter to continue...")
    
    def view_all_teachers(self):
        """Display all teachers"""
        clear_screen()
        print_header("ALL TEACHERS")
        
        teachers = self.dm._load_json('data/teachers.json')
        if not teachers:
            print("\n No teachers found!")
        else:
            print(f"\n{'Teacher ID':<12} {'Name':<20} {'Department':<20} {'Courses':<10}")
            print("-"*65)
            for tec_id, info in teachers.items():
                courses = len(info.get('courses', []))
                print(f"{tec_id:<12} {info.get('name', 'N/A'):<20} {info.get('department', 'N/A'):<20} {courses:<10}")
        
        input("\nPress Enter to continue...")
    
    def view_all_staff(self):
        """Display all staff"""
        clear_screen()
        print_header("ALL STAFF")
        
        staff = self.dm._load_json('data/staff.json')
        if not staff:
            print("\n No staff found!")
        else:
            print(f"\n{'Staff ID':<10} {'Name':<20} {'Department':<20} {'Position':<15}")
            print("-"*65)
            for stf_id, info in staff.items():
                print(f"{stf_id:<10} {info.get('name', 'N/A'):<20} {info.get('department', 'N/A'):<20} {info.get('position', 'N/A'):<15}")
        
        input("\nPress Enter to continue...")
