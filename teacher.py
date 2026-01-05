from models.user import BaseUser
from utils.helpers import clear_screen, print_header, print_menu
from data_manager import DataManager

class TeacherDashboard(BaseUser):
    """Teacher-specific features and dashboard"""
    
    def __init__(self, user_data: dict):
        super().__init__(user_data)
        self.dm = DataManager()
        self.profile = self.dm.get_user_data(self.user_id, 'teacher')
    
    def show(self) -> bool:
        """Display teacher dashboard"""
        while self.is_logged_in:
            clear_screen()
            print_header(f"TEACHER DASHBOARD - {self.username}")
            print(f"User ID: {self.user_id} | Department: {self.profile.get('department', 'N/A')}")
            print("="*60)
            
            print_menu([
                "View My Profile",
                "View My Courses",
                "Manage Student Grades",
                "Take Attendance",
                "View Student Details",
                "Logout"
            ])
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                self.view_profile()
            elif choice == '2':
                self.view_teacher_courses()
            elif choice == '3':
                self.manage_grades()
            elif choice == '4':
                self.take_attendance()
            elif choice == '5':
                self.view_student_details()
            elif choice == '6':
                return self.logout()
            else:
                input("\n  Invalid option! Press Enter to continue...")
        
        return False
    
    def view_profile(self):
        """Display teacher profile"""
        clear_screen()
        print_header("MY PROFILE")
        
        print(f"\n Name: {self.profile.get('name', 'N/A')}")
        print(f" Email: {self.profile.get('email', 'N/A')}")
        print(f" Department: {self.profile.get('department', 'N/A')}")
        print(f" Phone: {self.profile.get('contact', {}).get('phone', 'N/A')}")
        print(f" Office: {self.profile.get('contact', {}).get('office', 'N/A')}")
        
        input("\nPress Enter to continue...")
    
    def view_teacher_courses(self):
        """Display courses taught by this teacher"""
        clear_screen()
        print_header("MY COURSES")
        
        teacher_courses = self.profile.get('courses', [])
        all_courses = self.dm.get_all_courses()
        
        if not teacher_courses:
            print("\n No courses assigned yet.")
        else:
            print(f"\n{'Course Code':<12} {'Course Name':<30}")
            print("-"*45)
            for course_code in teacher_courses:
                course = all_courses.get(course_code, {})
                print(f"{course_code:<12} {course.get('name', 'Unknown'):<30}")
        
        input("\nPress Enter to continue...")
    
    def manage_grades(self):
        """Manage student grades"""
        clear_screen()
        print_header("MANAGE STUDENT GRADES")
        
        course_code = input("Enter course code: ").strip().upper()
        student_id = input("Enter student ID: ").strip().upper()
        grade = input("Enter grade (A/B/C/D/F): ").strip().upper()
        
        if grade not in ['A', 'B', 'C', 'D', 'F']:
            input("\n  Invalid grade! Press Enter...")
            return
        
        students = self.dm.get_all_students()
        if student_id not in students:
            input("\n Student not found! Press Enter...")
            return
        
        student = students[student_id]
        student.setdefault('grades', {})[course_code] = grade
        self.dm.update_user_data(student_id, 'student', student)
        
        print(f"\n Grade {grade} assigned to {student['name']} for {course_code}")
        input("\nPress Enter to continue...")
    
    def take_attendance(self):
        """Record attendance"""
        clear_screen()
        print_header("TAKE ATTENDANCE")
        
        course_code = input("Enter course code: ").strip().upper()
        student_id = input("Enter student ID: ").strip().upper()
        
        try:
            attendance_percent = float(input("Enter attendance percentage: "))
        except:
            input("\n  Invalid percentage! Press Enter...")
            return
        
        students = self.dm.get_all_students()
        if student_id not in students:
            input("\n❌ Student not found! Press Enter...")
            return
        
        student = students[student_id]
        student.setdefault('attendance', {})[course_code] = attendance_percent
        self.dm.update_user_data(student_id, 'student', student)
        
        print(f"\n Attendance recorded for {student['name']}")
        input("\nPress Enter to continue...")
    
    def view_student_details(self):
        """View any student's details"""
        clear_screen()
        print_header("VIEW STUDENT DETAILS")
        
        student_id = input("Enter student ID: ").strip().upper()
        students = self.dm.get_all_students()
        
        if student_id not in students:
            input("\n Student not found! Press Enter...")
            return
        
        student = students[student_id]
        print(f"\n Student ID: {student_id}")
        print(f" Name: {student.get('name', 'N/A')}")
        print(f" Email: {student.get('email', 'N/A')}")
        print(f" Enrollment: {student.get('enrollment_date', 'N/A')}")
        print(f"\n Enrolled Courses: {', '.join(student.get('courses', ['None']))}")
        print(f" Grades: {student.get('grades', {})}")
        print(f" Attendance: {student.get('attendance', {})}")
        
        input("\nPress Enter to continue...")
