"""
Teacher Module
All teacher-related functionalities
"""

from modules.data_manager import DataManager
from modules.authentication import Authentication
from utils.helpers import clear_screen, print_header, pause, print_table
from datetime import datetime

class TeacherModule:
    def __init__(self, user):
        self.user = user
        self.auth = Authentication()
    
    def show_menu(self):
        """Display teacher menu"""
        while True:
            clear_screen()
            print_header(f"TEACHER DASHBOARD - {self.user['name']}")
            print(f"ID: {self.user['id']} | Department: {self.user.get('department', 'N/A')}")
            print("\n" + "="*60)
            
            print("\n📚 COURSE MANAGEMENT")
            print("1. View Assigned Courses")
            print("2. View Course Students")
            
            print("\n📊 ACADEMIC OPERATIONS")
            print("3. Mark Attendance")
            print("4. Enter Grades")
            print("5. View Student Grades")
            print("6. View Attendance Report")
            
            print("\n⚙️ SETTINGS")
            print("7. View Profile")
            print("8. Change Password")
            print("9. Logout")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.view_assigned_courses()
            elif choice == "2":
                self.view_course_students()
            elif choice == "3":
                self.mark_attendance()
            elif choice == "4":
                self.enter_grades()
            elif choice == "5":
                self.view_student_grades()
            elif choice == "6":
                self.view_attendance_report()
            elif choice == "7":
                self.view_profile()
            elif choice == "8":
                self.change_password()
            elif choice == "9":
                return True
            else:
                print("\n❌ Invalid choice!")
                pause()
    
    def view_assigned_courses(self):
        """View courses assigned to teacher"""
        clear_screen()
        print_header("MY ASSIGNED COURSES")
        
        courses = DataManager.find_records("courses.txt", "teacher_id", self.user['id'])
        
        if not courses:
            print("\n⚠️ No courses assigned")
        else:
            # Get enrollment count for each course
            enrollments = DataManager.read_data("enrollments.txt")
            
            headers = ["Course ID", "Course Name", "Credits", "Enrolled Students"]
            rows = []
            
            for course in courses:
                student_count = sum(1 for e in enrollments if e['course_id'] == course['id'])
                rows.append([
                    course['id'],
                    course['name'],
                    course['credits'],
                    student_count
                ])
            
            print_table(headers, rows)
        
        pause()
    
    def view_course_students(self):
        """View students enrolled in a course"""
        clear_screen()
        print_header("COURSE STUDENTS")
        
        # Show assigned courses
        courses = DataManager.find_records("courses.txt", "teacher_id", self.user['id'])
        
        if not courses:
            print("\n⚠️ No courses assigned")
            pause()
            return
        
        print("\nYour Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['id']} - {course['name']}")
        
        choice = input("\nSelect course (number): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(courses):
                selected_course = courses[idx]
                
                clear_screen()
                print_header(f"STUDENTS - {selected_course['name']}")
                
                # Get enrolled students
                enrollments = DataManager.find_records("enrollments.txt", 
                                                      "course_id", selected_course['id'])
                
                if not enrollments:
                    print("\n⚠️ No students enrolled")
                else:
                    students = DataManager.read_data("students.txt")
                    student_map = {s['id']: s for s in students}
                    
                    headers = ["Student ID", "Name", "Department", "Email", "Status"]
                    rows = []
                    
                    for enrollment in enrollments:
                        student = student_map.get(enrollment['student_id'], {})
                        if student:
                            rows.append([
                                student['id'],
                                student['name'],
                                student.get('department', 'N/A'),
                                student.get('email', 'N/A'),
                                enrollment['status']
                            ])
                    
                    print_table(headers, rows)
        except:
            print("\n❌ Invalid selection!")
        
        pause()
    
    def mark_attendance(self):
        """Mark student attendance"""
        clear_screen()
        print_header("MARK ATTENDANCE")
        
        # Show assigned courses
        courses = DataManager.find_records("courses.txt", "teacher_id", self.user['id'])
        
        if not courses:
            print("\n⚠️ No courses assigned")
            pause()
            return
        
        print("\nYour Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['id']} - {course['name']}")
        
        choice = input("\nSelect course (number): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(courses):
                selected_course = courses[idx]
                
                # Get enrolled students
                enrollments = DataManager.find_records("enrollments.txt", 
                                                      "course_id", selected_course['id'])
                
                if not enrollments:
                    print("\n⚠️ No students enrolled")
                    pause()
                    return
                
                students = DataManager.read_data("students.txt")
                student_map = {s['id']: s for s in students}
                
                clear_screen()
                print_header(f"MARK ATTENDANCE - {selected_course['name']}")
                print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
                print("\n" + "="*60)
                
                attendance_records = []
                
                for enrollment in enrollments:
                    student = student_map.get(enrollment['student_id'])
                    if student:
                        print(f"\nStudent: {student['name']} ({student['id']})")
                        status = input("Status (P=Present, A=Absent): ").strip().upper()
                        
                        attendance = {
                            "student_id": student['id'],
                            "course_id": selected_course['id'],
                            "date": datetime.now().strftime('%Y-%m-%d'),
                            "status": "Present" if status == 'P' else "Absent"
                        }
                        attendance_records.append(attendance)
                
                # Save all attendance records
                for record in attendance_records:
                    DataManager.add_record("attendance.txt", record)
                
                print(f"\n✅ Attendance marked for {len(attendance_records)} students!")
        except:
            print("\n❌ Invalid selection!")
        
        pause()
    
    def enter_grades(self):
        """Enter student grades"""
        clear_screen()
        print_header("ENTER GRADES")
        
        # Show assigned courses
        courses = DataManager.find_records("courses.txt", "teacher_id", self.user['id'])
        
        if not courses:
            print("\n⚠️ No courses assigned")
            pause()
            return
        
        print("\nYour Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['id']} - {course['name']}")
        
        choice = input("\nSelect course (number): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(courses):
                selected_course = courses[idx]
                
                # Get enrolled students
                enrollments = DataManager.find_records("enrollments.txt", 
                                                      "course_id", selected_course['id'])
                
                if not enrollments:
                    print("\n⚠️ No students enrolled")
                    pause()
                    return
                
                students = DataManager.read_data("students.txt")
                student_map = {s['id']: s for s in students}
                
                clear_screen()
                print_header(f"ENTER GRADES - {selected_course['name']}")
                print("\nGrade Scale: A+, A, A-, B+, B, B-, C+, C, C-, D, F")
                print("="*60)
                
                for enrollment in enrollments:
                    student = student_map.get(enrollment['student_id'])
                    if student:
                        print(f"\nStudent: {student['name']} ({student['id']})")
                        grade = input("Enter Grade: ").strip().upper()
                        points = input("Enter Points (Optional): ").strip()
                        remarks = input("Remarks (Optional): ").strip()
                        
                        grade_record = {
                            "student_id": student['id'],
                            "course_id": selected_course['id'],
                            "grade": grade,
                            "points": points if points else "N/A",
                            "remarks": remarks if remarks else "-",
                            "date": datetime.now().strftime('%Y-%m-%d')
                        }
                        
                        # Check if grade already exists
                        all_grades = DataManager.read_data("grades.txt")
                        existing = False
                        
                        for i, g in enumerate(all_grades):
                            if (g['student_id'] == student['id'] and 
                                g['course_id'] == selected_course['id']):
                                all_grades[i] = grade_record
                                existing = True
                                break
                        
                        if not existing:
                            all_grades.append(grade_record)
                        
                        DataManager.write_data("grades.txt", all_grades)
                
                print("\n✅ Grades entered successfully!")
        except:
            print("\n❌ Invalid selection!")
        
        pause()
    
    def view_student_grades(self):
        """View grades for a course"""
        clear_screen()
        print_header("VIEW STUDENT GRADES")
        
        # Show assigned courses
        courses = DataManager.find_records("courses.txt", "teacher_id", self.user['id'])
        
        if not courses:
            print("\n⚠️ No courses assigned")
            pause()
            return
        
        print("\nYour Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['id']} - {course['name']}")
        
        choice = input("\nSelect course (number): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(courses):
                selected_course = courses[idx]
                
                clear_screen()
                print_header(f"GRADES - {selected_course['name']}")
                
                # Get grades for this course
                all_grades = DataManager.read_data("grades.txt")
                course_grades = [g for g in all_grades if g['course_id'] == selected_course['id']]
                
                if not course_grades:
                    print("\n⚠️ No grades entered yet")
                else:
                    students = DataManager.read_data("students.txt")
                    student_map = {s['id']: s['name'] for s in students}
                    
                    headers = ["Student ID", "Name", "Grade", "Points", "Remarks"]
                    rows = []
                    
                    for grade in course_grades:
                        rows.append([
                            grade['student_id'],
                            student_map.get(grade['student_id'], 'Unknown'),
                            grade['grade'],
                            grade.get('points', 'N/A'),
                            grade.get('remarks', '-')
                        ])
                    
                    print_table(headers, rows)
        except:
            print("\n❌ Invalid selection!")
        
        pause()
    
    def view_attendance_report(self):
        """View attendance report for a course"""
        clear_screen()
        print_header("ATTENDANCE REPORT")
        
        # Show assigned courses
        courses = DataManager.find_records("courses.txt", "teacher_id", self.user['id'])
        
        if not courses:
            print("\n⚠️ No courses assigned")
            pause()
            return
        
        print("\nYour Courses:")
        for i, course in enumerate(courses, 1):
            print(f"{i}. {course['id']} - {course['name']}")
        
        choice = input("\nSelect course (number): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(courses):
                selected_course = courses[idx]
                
                clear_screen()
                print_header(f"ATTENDANCE - {selected_course['name']}")
                
                # Get attendance for this course
                all_attendance = DataManager.read_data("attendance.txt")
                course_attendance = [a for a in all_attendance 
                                   if a['course_id'] == selected_course['id']]
                
                if not course_attendance:
                    print("\n⚠️ No attendance records")
                else:
                    # Calculate statistics per student
                    from collections import defaultdict
                    student_stats = defaultdict(lambda: {"present": 0, "absent": 0})
                    
                    for record in course_attendance:
                        student_id = record['student_id']
                        if record['status'] == 'Present':
                            student_stats[student_id]['present'] += 1
                        else:
                            student_stats[student_id]['absent'] += 1
                    
                    students = DataManager.read_data("students.txt")
                    student_map = {s['id']: s['name'] for s in students}
                    
                    headers = ["Student ID", "Name", "Present", "Absent", "Total", "Percentage"]
                    rows = []
                    
                    for student_id, stats in student_stats.items():
                        total = stats['present'] + stats['absent']
                        percentage = (stats['present'] / total * 100) if total > 0 else 0
                        
                        rows.append([
                            student_id,
                            student_map.get(student_id, 'Unknown'),
                            stats['present'],
                            stats['absent'],
                            total,
                            f"{percentage:.1f}%"
                        ])
                    
                    print_table(headers, rows)
        except:
            print("\n❌ Invalid selection!")
        
        pause()
    
    def view_profile(self):
        """View teacher profile"""
        clear_screen()
        print_header("TEACHER PROFILE")
        
        print(f"\nID: {self.user['id']}")
        print(f"Name: {self.user['name']}")
        print(f"Email: {self.user.get('email', 'N/A')}")
        print(f"Phone: {self.user.get('phone', 'N/A')}")
        print(f"Department: {self.user.get('department', 'N/A')}")
        print(f"Designation: {self.user.get('designation', 'N/A')}")
        
        pause()
    
    def change_password(self):
        """Change password"""
        clear_screen()
        print_header("CHANGE PASSWORD")
        
        old_pass = input("\nEnter current password: ").strip()
        new_pass = input("Enter new password: ").strip()
        confirm_pass = input("Confirm new password: ").strip()
        
        if new_pass != confirm_pass:
            print("\n❌ Passwords do not match!")
        else:
            success, message = self.auth.change_password(
                self.user['id'], 'teacher', old_pass, new_pass
            )
            
            if success:
                print(f"\n✅ {message}")
                self.user['password'] = new_pass
            else:
                print(f"\n❌ {message}")
        
        pause()