"""
Student Module
All student-related functionalities
"""

from modules.data_manager import DataManager
from modules.authentication import Authentication
from utils.helpers import clear_screen, print_header, pause, print_table

class StudentModule:
    def __init__(self, user):
        self.user = user
        self.auth = Authentication()
    
    def show_menu(self):
        """Display student menu"""
        while True:
            clear_screen()
            print_header(f"STUDENT DASHBOARD - {self.user['name']}")
            print(f"ID: {self.user['id']} | Department: {self.user.get('department', 'N/A')}")
            print("\n" + "="*60)
            
            print("\n📚 COURSE MANAGEMENT")
            print("1. View Available Courses")
            print("2. Enroll in Course")
            print("3. View Registered Courses")
            print("4. Drop Course")
            
            print("\n📊 ACADEMIC RECORDS")
            print("5. View Grades")
            print("6. View Attendance")
            print("7. View Academic Report")
            
            print("\n💰 FINANCIAL")
            print("8. View Fee Status")
            print("9. Pay Fees")
            
            print("\n⚙️ SETTINGS")
            print("10. View Profile")
            print("11. Change Password")
            print("12. Logout")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.view_available_courses()
            elif choice == "2":
                self.enroll_course()
            elif choice == "3":
                self.view_registered_courses()
            elif choice == "4":
                self.drop_course()
            elif choice == "5":
                self.view_grades()
            elif choice == "6":
                self.view_attendance()
            elif choice == "7":
                self.view_academic_report()
            elif choice == "8":
                self.view_fee_status()
            elif choice == "9":
                self.pay_fees()
            elif choice == "10":
                self.view_profile()
            elif choice == "11":
                self.change_password()
            elif choice == "12":
                return True
            else:
                print("\n❌ Invalid choice!")
                pause()
    
    def view_available_courses(self):
        """View all available courses"""
        clear_screen()
        print_header("AVAILABLE COURSES")
        
        courses = DataManager.read_data("courses.txt")
        
        if not courses:
            print("\n⚠️ No courses available")
        else:
            headers = ["Course ID", "Course Name", "Credits", "Teacher"]
            rows = []
            
            teachers = DataManager.read_data("teachers.txt")
            teacher_map = {t['id']: t['name'] for t in teachers}
            
            for course in courses:
                teacher_name = teacher_map.get(course.get('teacher_id', ''), 'Not Assigned')
                rows.append([
                    course['id'],
                    course['name'],
                    course['credits'],
                    teacher_name
                ])
            
            print_table(headers, rows)
        
        pause()
    
    def enroll_course(self):
        """Enroll in a course"""
        clear_screen()
        print_header("COURSE ENROLLMENT")
        
        course_id = input("\nEnter Course ID to enroll: ").strip().upper()
        
        # Check if course exists
        course = DataManager.find_record("courses.txt", "id", course_id)
        if not course:
            print("\n❌ Course not found!")
            pause()
            return
        
        # Check if already enrolled
        enrollments = DataManager.find_records("enrollments.txt", "student_id", self.user['id'])
        enrolled_courses = [e['course_id'] for e in enrollments]
        
        if course_id in enrolled_courses:
            print("\n⚠️ You are already enrolled in this course!")
            pause()
            return
        
        # Create enrollment
        enrollment = {
            "student_id": self.user['id'],
            "course_id": course_id,
            "semester": "Spring 2026",
            "status": "Active"
        }
        
        if DataManager.add_record("enrollments.txt", enrollment):
            print(f"\n✅ Successfully enrolled in {course['name']}!")
        else:
            print("\n❌ Enrollment failed!")
        
        pause()
    
    def view_registered_courses(self):
        """View registered courses with details"""
        clear_screen()
        print_header("REGISTERED COURSES")
        
        enrollments = DataManager.find_records("enrollments.txt", "student_id", self.user['id'])
        
        if not enrollments:
            print("\n⚠️ You are not enrolled in any courses")
        else:
            courses = DataManager.read_data("courses.txt")
            teachers = DataManager.read_data("teachers.txt")
            grades = DataManager.read_data("grades.txt")
            
            course_map = {c['id']: c for c in courses}
            teacher_map = {t['id']: t['name'] for t in teachers}
            
            headers = ["Course ID", "Course Name", "Credits", "Teacher", "Status", "Grade"]
            rows = []
            
            total_credits = 0
            
            for enrollment in enrollments:
                course_id = enrollment['course_id']
                course = course_map.get(course_id, {})
                
                if course:
                    teacher_name = teacher_map.get(course.get('teacher_id', ''), 'Not Assigned')
                    
                    # Get grade
                    grade_record = next((g for g in grades if g['student_id'] == self.user['id'] 
                                       and g['course_id'] == course_id), None)
                    grade = grade_record['grade'] if grade_record else 'N/A'
                    
                    rows.append([
                        course_id,
                        course['name'],
                        course['credits'],
                        teacher_name,
                        enrollment['status'],
                        grade
                    ])
                    
                    total_credits += course['credits']
            
            print_table(headers, rows)
            print(f"\n📊 Total Credits: {total_credits}")
        
        pause()
    
    def drop_course(self):
        """Drop a course"""
        clear_screen()
        print_header("DROP COURSE")
        
        course_id = input("\nEnter Course ID to drop: ").strip().upper()
        
        enrollments = DataManager.read_data("enrollments.txt")
        found = False
        
        for i, enrollment in enumerate(enrollments):
            if (enrollment['student_id'] == self.user['id'] and 
                enrollment['course_id'] == course_id):
                enrollments.pop(i)
                found = True
                break
        
        if found:
            DataManager.write_data("enrollments.txt", enrollments)
            print("\n✅ Course dropped successfully!")
        else:
            print("\n❌ Enrollment not found!")
        
        pause()
    
    def view_grades(self):
        """View all grades"""
        clear_screen()
        print_header("GRADE REPORT")
        
        grades = DataManager.find_records("grades.txt", "student_id", self.user['id'])
        
        if not grades:
            print("\n⚠️ No grades available")
        else:
            courses = DataManager.read_data("courses.txt")
            course_map = {c['id']: c for c in courses}
            
            headers = ["Course ID", "Course Name", "Grade", "Points", "Remarks"]
            rows = []
            
            for grade_record in grades:
                course = course_map.get(grade_record['course_id'], {})
                rows.append([
                    grade_record['course_id'],
                    course.get('name', 'Unknown'),
                    grade_record['grade'],
                    grade_record.get('points', 'N/A'),
                    grade_record.get('remarks', '-')
                ])
            
            print_table(headers, rows)
        
        pause()
    
    def view_attendance(self):
        """View attendance records"""
        clear_screen()
        print_header("ATTENDANCE REPORT")
        
        attendance_records = DataManager.find_records("attendance.txt", "student_id", self.user['id'])
        
        if not attendance_records:
            print("\n⚠️ No attendance records available")
        else:
            # Group by course
            from collections import defaultdict
            course_attendance = defaultdict(lambda: {"present": 0, "absent": 0, "total": 0})
            
            for record in attendance_records:
                course_id = record['course_id']
                course_attendance[course_id]['total'] += 1
                if record['status'] == 'Present':
                    course_attendance[course_id]['present'] += 1
                else:
                    course_attendance[course_id]['absent'] += 1
            
            courses = DataManager.read_data("courses.txt")
            course_map = {c['id']: c['name'] for c in courses}
            
            headers = ["Course", "Present", "Absent", "Total", "Percentage"]
            rows = []
            
            for course_id, stats in course_attendance.items():
                percentage = (stats['present'] / stats['total'] * 100) if stats['total'] > 0 else 0
                rows.append([
                    f"{course_id} - {course_map.get(course_id, 'Unknown')}",
                    stats['present'],
                    stats['absent'],
                    stats['total'],
                    f"{percentage:.1f}%"
                ])
            
            print_table(headers, rows)
        
        pause()
    
    def view_academic_report(self):
        """View complete academic report"""
        clear_screen()
        print_header("ACADEMIC REPORT")
        
        print(f"\nStudent: {self.user['name']}")
        print(f"ID: {self.user['id']}")
        print(f"Department: {self.user.get('department', 'N/A')}")
        print("\n" + "="*60)
        
        # Enrolled courses
        enrollments = DataManager.find_records("enrollments.txt", "student_id", self.user['id'])
        print(f"\n📚 Total Enrolled Courses: {len(enrollments)}")
        
        # Calculate CGPA
        grades = DataManager.find_records("grades.txt", "student_id", self.user['id'])
        if grades:
            grade_points = {
                'A+': 4.0, 'A': 3.75, 'A-': 3.5,
                'B+': 3.25, 'B': 3.0, 'B-': 2.75,
                'C+': 2.5, 'C': 2.25, 'C-': 2.0,
                'D': 1.0, 'F': 0.0
            }
            
            total_points = 0
            count = 0
            for grade_record in grades:
                if grade_record['grade'] in grade_points:
                    total_points += grade_points[grade_record['grade']]
                    count += 1
            
            cgpa = total_points / count if count > 0 else 0
            print(f"📊 CGPA: {cgpa:.2f}")
        
        # Attendance
        attendance_records = DataManager.find_records("attendance.txt", "student_id", self.user['id'])
        if attendance_records:
            present = sum(1 for r in attendance_records if r['status'] == 'Present')
            total = len(attendance_records)
            attendance_pct = (present / total * 100) if total > 0 else 0
            print(f"📅 Overall Attendance: {attendance_pct:.1f}%")
        
        pause()
    
    def view_fee_status(self):
        """View fee payment status"""
        clear_screen()
        print_header("FEE STATUS")
        
        fee_records = DataManager.find_records("fees.txt", "student_id", self.user['id'])
        
        if not fee_records:
            print("\n⚠️ No fee records found")
        else:
            headers = ["Semester", "Amount", "Paid", "Status", "Date"]
            rows = []
            
            total_due = 0
            
            for record in fee_records:
                rows.append([
                    record['semester'],
                    f"৳{record['amount']}",
                    f"৳{record.get('paid', 0)}",
                    record['status'],
                    record.get('date', 'N/A')
                ])
                
                if record['status'] != 'Paid':
                    total_due += record['amount'] - record.get('paid', 0)
            
            print_table(headers, rows)
            print(f"\n💰 Total Due: ৳{total_due}")
        
        pause()
    
    def pay_fees(self):
        """Pay fees"""
        clear_screen()
        print_header("FEE PAYMENT")
        
        fee_records = DataManager.find_records("fees.txt", "student_id", self.user['id'])
        unpaid = [f for f in fee_records if f['status'] != 'Paid']
        
        if not unpaid:
            print("\n✅ All fees are paid!")
            pause()
            return
        
        print("\nUnpaid Fees:")
        for i, record in enumerate(unpaid, 1):
            due = record['amount'] - record.get('paid', 0)
            print(f"{i}. {record['semester']} - ৳{due} due")
        
        choice = input("\nSelect fee to pay (number): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(unpaid):
                record = unpaid[idx]
                due = record['amount'] - record.get('paid', 0)
                
                print(f"\nAmount Due: ৳{due}")
                amount = input("Enter amount to pay: ").strip()
                
                try:
                    amount = float(amount)
                    if amount > due:
                        print("\n❌ Amount exceeds due amount!")
                    else:
                        # Update payment
                        all_fees = DataManager.read_data("fees.txt")
                        for fee in all_fees:
                            if (fee['student_id'] == self.user['id'] and 
                                fee['semester'] == record['semester']):
                                fee['paid'] = fee.get('paid', 0) + amount
                                if fee['paid'] >= fee['amount']:
                                    fee['status'] = 'Paid'
                                    from datetime import datetime
                                    fee['date'] = datetime.now().strftime("%Y-%m-%d")
                                break
                        
                        DataManager.write_data("fees.txt", all_fees)
                        print(f"\n✅ Payment of ৳{amount} received successfully!")
                except ValueError:
                    print("\n❌ Invalid amount!")
        except:
            print("\n❌ Invalid selection!")
        
        pause()
    
    def view_profile(self):
        """View student profile"""
        clear_screen()
        print_header("STUDENT PROFILE")
        
        print(f"\nID: {self.user['id']}")
        print(f"Name: {self.user['name']}")
        print(f"Email: {self.user.get('email', 'N/A')}")
        print(f"Phone: {self.user.get('phone', 'N/A')}")
        print(f"Department: {self.user.get('department', 'N/A')}")
        print(f"Batch: {self.user.get('batch', 'N/A')}")
        
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
                self.user['id'], 'student', old_pass, new_pass
            )
            
            if success:
                print(f"\n✅ {message}")
                self.user['password'] = new_pass
            else:
                print(f"\n❌ {message}")
        
        pause()