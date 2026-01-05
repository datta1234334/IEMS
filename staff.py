"""
Staff Module
All staff/admin-related functionalities
"""

from modules.data_manager import DataManager
from modules.authentication import Authentication
from utils.helpers import clear_screen, print_header, pause, print_table
from datetime import datetime

class StaffModule:
    def __init__(self, user):
        self.user = user
        self.auth = Authentication()
    
    def show_menu(self):
        """Display staff menu"""
        while True:
            clear_screen()
            print_header(f"STAFF DASHBOARD - {self.user['name']}")
            print(f"ID: {self.user['id']} | Role: {self.user.get('role', 'Staff')}")
            print("\n" + "="*60)
            
            print("\n👥 USER MANAGEMENT")
            print("1. Add New Student")
            print("2. Add New Teacher")
            print("3. Add New Staff")
            print("4. View All Students")
            print("5. View All Teachers")
            print("6. View All Staff")
            print("7. Delete User")
            
            print("\n📚 COURSE MANAGEMENT")
            print("8. Add New Course")
            print("9. Assign Teacher to Course")
            print("10. View All Courses")
            print("11. Delete Course")
            
            print("\n💰 FEE MANAGEMENT")
            print("12. Add Fee Record")
            print("13. View Fee Records")
            print("14. Update Fee Status")
            
            print("\n📊 REPORTS")
            print("15. Generate Student Report")
            print("16. Generate Course Report")
            print("17. Generate Fee Report")
            
            print("\n⚙️ SETTINGS")
            print("18. View Profile")
            print("19. Change Password")
            print("20. Logout")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_teacher()
            elif choice == "3":
                self.add_staff()
            elif choice == "4":
                self.view_all_students()
            elif choice == "5":
                self.view_all_teachers()
            elif choice == "6":
                self.view_all_staff()
            elif choice == "7":
                self.delete_user()
            elif choice == "8":
                self.add_course()
            elif choice == "9":
                self.assign_teacher()
            elif choice == "10":
                self.view_all_courses()
            elif choice == "11":
                self.delete_course()
            elif choice == "12":
                self.add_fee_record()
            elif choice == "13":
                self.view_fee_records()
            elif choice == "14":
                self.update_fee_status()
            elif choice == "15":
                self.generate_student_report()
            elif choice == "16":
                self.generate_course_report()
            elif choice == "17":
                self.generate_fee_report()
            elif choice == "18":
                self.view_profile()
            elif choice == "19":
                self.change_password()
            elif choice == "20":
                return True
            else:
                print("\n❌ Invalid choice!")
                pause()
    
    def add_student(self):
        """Add new student"""
        clear_screen()
        print_header("ADD NEW STUDENT")
        
        name = input("\nStudent Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        department = input("Department: ").strip()
        batch = input("Batch: ").strip()
        password = input("Password: ").strip()
        
        if not all([name, email, password]):
            print("\n❌ Name, email, and password are required!")
            pause()
            return
        
        student_id = DataManager.generate_id("students.txt", "STU")
        
        student = {
            "id": student_id,
            "name": name,
            "email": email,
            "phone": phone,
            "department": department,
            "batch": batch,
            "password": password
        }
        
        if DataManager.add_record("students.txt", student):
            print(f"\n✅ Student added successfully!")
            print(f"Student ID: {student_id}")
        else:
            print("\n❌ Failed to add student!")
        
        pause()
    
    def add_teacher(self):
        """Add new teacher"""
        clear_screen()
        print_header("ADD NEW TEACHER")
        
        name = input("\nTeacher Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        department = input("Department: ").strip()
        designation = input("Designation: ").strip()
        password = input("Password: ").strip()
        
        if not all([name, email, password]):
            print("\n❌ Name, email, and password are required!")
            pause()
            return
        
        teacher_id = DataManager.generate_id("teachers.txt", "TCH")
        
        teacher = {
            "id": teacher_id,
            "name": name,
            "email": email,
            "phone": phone,
            "department": department,
            "designation": designation,
            "password": password
        }
        
        if DataManager.add_record("teachers.txt", teacher):
            print(f"\n✅ Teacher added successfully!")
            print(f"Teacher ID: {teacher_id}")
        else:
            print("\n❌ Failed to add teacher!")
        
        pause()
    
    def add_staff(self):
        """Add new staff"""
        clear_screen()
        print_header("ADD NEW STAFF")
        
        name = input("\nStaff Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        role = input("Role: ").strip()
        password = input("Password: ").strip()
        
        if not all([name, email, password]):
            print("\n❌ Name, email, and password are required!")
            pause()
            return
        
        staff_id = DataManager.generate_id("staff.txt", "STF")
        
        staff = {
            "id": staff_id,
            "name": name,
            "email": email,
            "phone": phone,
            "role": role,
            "password": password
        }
        
        if DataManager.add_record("staff.txt", staff):
            print(f"\n✅ Staff added successfully!")
            print(f"Staff ID: {staff_id}")
        else:
            print("\n❌ Failed to add staff!")
        
        pause()
    
    def view_all_students(self):
        """View all students"""
        clear_screen()
        print_header("ALL STUDENTS")
        
        students = DataManager.read_data("students.txt")
        
        if not students:
            print("\n⚠️ No students found")
        else:
            headers = ["ID", "Name", "Email", "Department", "Batch"]
            rows = []
            
            for student in students:
                rows.append([
                    student['id'],
                    student['name'],
                    student.get('email', 'N/A'),
                    student.get('department', 'N/A'),
                    student.get('batch', 'N/A')
                ])
            
            print_table(headers, rows)
            print(f"\n📊 Total Students: {len(students)}")
        
        pause()
    
    def view_all_teachers(self):
        """View all teachers"""
        clear_screen()
        print_header("ALL TEACHERS")
        
        teachers = DataManager.read_data("teachers.txt")
        
        if not teachers:
            print("\n⚠️ No teachers found")
        else:
            headers = ["ID", "Name", "Email", "Department", "Designation"]
            rows = []
            
            for teacher in teachers:
                rows.append([
                    teacher['id'],
                    teacher['name'],
                    teacher.get('email', 'N/A'),
                    teacher.get('department', 'N/A'),
                    teacher.get('designation', 'N/A')
                ])
            
            print_table(headers, rows)
            print(f"\n📊 Total Teachers: {len(teachers)}")
        
        pause()
    
    def view_all_staff(self):
        """View all staff"""
        clear_screen()
        print_header("ALL STAFF")
        
        staff = DataManager.read_data("staff.txt")
        
        if not staff:
            print("\n⚠️ No staff found")
        else:
            headers = ["ID", "Name", "Email", "Phone", "Role"]
            rows = []
            
            for s in staff:
                rows.append([
                    s['id'],
                    s['name'],
                    s.get('email', 'N/A'),
                    s.get('phone', 'N/A'),
                    s.get('role', 'N/A')
                ])
            
            print_table(headers, rows)
            print(f"\n📊 Total Staff: {len(staff)}")
        
        pause()
    
    def delete_user(self):
        """Delete a user"""
        clear_screen()
        print_header("DELETE USER")
        
        print("\n1. Delete Student")
        print("2. Delete Teacher")
        print("3. Delete Staff")
        
        choice = input("\nSelect user type: ").strip()
        
        if choice == "1":
            user_type = "students"
        elif choice == "2":
            user_type = "teachers"
        elif choice == "3":
            user_type = "staff"
        else:
            print("\n❌ Invalid choice!")
            pause()
            return
        
        user_id = input(f"\nEnter {user_type[:-1]} ID to delete: ").strip().upper()
        
        confirm = input(f"Are you sure you want to delete {user_id}? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            if DataManager.delete_record(f"{user_type}.txt", "id", user_id):
                print(f"\n✅ {user_type[:-1].capitalize()} deleted successfully!")
            else:
                print("\n❌ User not found or deletion failed!")
        else:
            print("\n❌ Deletion cancelled!")
        
        pause()
    
    def add_course(self):
        """Add new course"""
        clear_screen()
        print_header("ADD NEW COURSE")
        
        course_id = input("\nCourse ID (e.g., CSE301): ").strip().upper()
        course_name = input("Course Name: ").strip()
        credits = input("Credits: ").strip()
        
        if not all([course_id, course_name, credits]):
            print("\n❌ All fields are required!")
            pause()
            return
        
        # Check if course ID already exists
        existing = DataManager.find_record("courses.txt", "id", course_id)
        if existing:
            print(f"\n❌ Course {course_id} already exists!")
            pause()
            return
        
        try:
            credits = int(credits)
        except:
            print("\n❌ Credits must be a number!")
            pause()
            return
        
        course = {
            "id": course_id,
            "name": course_name,
            "credits": credits,
            "teacher_id": ""
        }
        
        if DataManager.add_record("courses.txt", course):
            print(f"\n✅ Course added successfully!")
        else:
            print("\n❌ Failed to add course!")
        
        pause()
    
    def assign_teacher(self):
        """Assign teacher to course"""
        clear_screen()
        print_header("ASSIGN TEACHER TO COURSE")
        
        # Show available courses
        courses = DataManager.read_data("courses.txt")
        if not courses:
            print("\n⚠️ No courses available")
            pause()
            return
        
        print("\nAvailable Courses:")
        for course in courses:
            teacher_status = "Assigned" if course.get('teacher_id') else "Not Assigned"
            print(f"{course['id']} - {course['name']} ({teacher_status})")
        
        course_id = input("\nEnter Course ID: ").strip().upper()
        
        # Show available teachers
        teachers = DataManager.read_data("teachers.txt")
        if not teachers:
            print("\n⚠️ No teachers available")
            pause()
            return
        
        print("\nAvailable Teachers:")
        for teacher in teachers:
            print(f"{teacher['id']} - {teacher['name']} ({teacher.get('department', 'N/A')})")
        
        teacher_id = input("\nEnter Teacher ID: ").strip().upper()
        
        # Update course
        course = DataManager.find_record("courses.txt", "id", course_id)
        if not course:
            print("\n❌ Course not found!")
            pause()
            return
        
        teacher = DataManager.find_record("teachers.txt", "id", teacher_id)
        if not teacher:
            print("\n❌ Teacher not found!")
            pause()
            return
        
        course['teacher_id'] = teacher_id
        
        if DataManager.update_record("courses.txt", "id", course_id, course):
            print(f"\n✅ {teacher['name']} assigned to {course['name']}!")
        else:
            print("\n❌ Assignment failed!")
        
        pause()
    
    def view_all_courses(self):
        """View all courses"""
        clear_screen()
        print_header("ALL COURSES")
        
        courses = DataManager.read_data("courses.txt")
        
        if not courses:
            print("\n⚠️ No courses found")
        else:
            teachers = DataManager.read_data("teachers.txt")
            teacher_map = {t['id']: t['name'] for t in teachers}
            
            enrollments = DataManager.read_data("enrollments.txt")
            
            headers = ["Course ID", "Course Name", "Credits", "Teacher", "Students"]
            rows = []
            
            for course in courses:
                teacher_name = teacher_map.get(course.get('teacher_id', ''), 'Not Assigned')
                student_count = sum(1 for e in enrollments if e['course_id'] == course['id'])
                
                rows.append([
                    course['id'],
                    course['name'],
                    course['credits'],
                    teacher_name,
                    student_count
                ])
            
            print_table(headers, rows)
            print(f"\n📊 Total Courses: {len(courses)}")
        
        pause()
    
    def delete_course(self):
        """Delete a course"""
        clear_screen()
        print_header("DELETE COURSE")
        
        course_id = input("\nEnter Course ID to delete: ").strip().upper()
        
        course = DataManager.find_record("courses.txt", "id", course_id)
        if not course:
            print("\n❌ Course not found!")
            pause()
            return
        
        # Check if students are enrolled
        enrollments = DataManager.find_records("enrollments.txt", "course_id", course_id)
        if enrollments:
            print(f"\n⚠️ Warning: {len(enrollments)} students are enrolled in this course!")
        
        confirm = input(f"Delete {course['name']}? (yes/no): ").strip().lower()
        
        if confirm == "yes":
            if DataManager.delete_record("courses.txt", "id", course_id):
                print("\n✅ Course deleted successfully!")
            else:
                print("\n❌ Deletion failed!")
        else:
            print("\n❌ Deletion cancelled!")
        
        pause()
    
    def add_fee_record(self):
        """Add fee record for student"""
        clear_screen()
        print_header("ADD FEE RECORD")
        
        student_id = input("\nStudent ID: ").strip().upper()
        
        student = DataManager.find_record("students.txt", "id", student_id)
        if not student:
            print("\n❌ Student not found!")
            pause()
            return
        
        print(f"\nStudent: {student['name']}")
        
        semester = input("Semester (e.g., Spring 2026): ").strip()
        amount = input("Fee Amount (৳): ").strip()
        
        try:
            amount = float(amount)
        except:
            print("\n❌ Invalid amount!")
            pause()
            return
        
        fee_record = {
            "student_id": student_id,
            "semester": semester,
            "amount": amount,
            "paid": 0,
            "status": "Unpaid",
            "date": ""
        }
        
        if DataManager.add_record("fees.txt", fee_record):
            print("\n✅ Fee record added successfully!")
        else:
            print("\n❌ Failed to add fee record!")
        
        pause()
    
    def view_fee_records(self):
        """View all fee records"""
        clear_screen()
        print_header("FEE RECORDS")
        
        fees = DataManager.read_data("fees.txt")
        
        if not fees:
            print("\n⚠️ No fee records found")
        else:
            students = DataManager.read_data("students.txt")
            student_map = {s['id']: s['name'] for s in students}
            
            headers = ["Student ID", "Name", "Semester", "Amount", "Paid", "Status"]
            rows = []
            
            total_due = 0
            
            for fee in fees:
                rows.append([
                    fee['student_id'],
                    student_map.get(fee['student_id'], 'Unknown'),
                    fee['semester'],
                    f"৳{fee['amount']}",
                    f"৳{fee.get('paid', 0)}",
                    fee['status']
                ])
                
                if fee['status'] != 'Paid':
                    total_due += fee['amount'] - fee.get('paid', 0)
            
            print_table(headers, rows)
            print(f"\n💰 Total Outstanding: ৳{total_due:.2f}")
        
        pause()
    
    def update_fee_status(self):
        """Update fee payment status"""
        clear_screen()
        print_header("UPDATE FEE STATUS")
        
        student_id = input("\nStudent ID: ").strip().upper()
        
        fees = DataManager.find_records("fees.txt", "student_id", student_id)
        
        if not fees:
            print("\n⚠️ No fee records found for this student")
            pause()
            return
        
        print("\nFee Records:")
        for i, fee in enumerate(fees, 1):
            print(f"{i}. {fee['semester']} - ৳{fee['amount']} ({fee['status']})")
        
        choice = input("\nSelect record to update: ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(fees):
                selected_fee = fees[idx]
                
                print("\n1. Mark as Paid")
                print("2. Update Paid Amount")
                
                action = input("\nSelect action: ").strip()
                
                all_fees = DataManager.read_data("fees.txt")
                
                for i, fee in enumerate(all_fees):
                    if (fee['student_id'] == student_id and 
                        fee['semester'] == selected_fee['semester']):
                        
                        if action == "1":
                            all_fees[i]['paid'] = all_fees[i]['amount']
                            all_fees[i]['status'] = 'Paid'
                            all_fees[i]['date'] = datetime.now().strftime("%Y-%m-%d")
                        elif action == "2":
                            amount = input("Enter paid amount: ").strip()
                            try:
                                amount = float(amount)
                                all_fees[i]['paid'] = amount
                                if amount >= all_fees[i]['amount']:
                                    all_fees[i]['status'] = 'Paid'
                                    all_fees[i]['date'] = datetime.now().strftime("%Y-%m-%d")
                                else:
                                    all_fees[i]['status'] = 'Partial'
                            except:
                                print("\n❌ Invalid amount!")
                                pause()
                                return
                        break
                
                DataManager.write_data("fees.txt", all_fees)
                print("\n✅ Fee status updated!")
        except:
            print("\n❌ Invalid selection!")
        
        pause()
    
    def generate_student_report(self):
        """Generate comprehensive student report"""
        clear_screen()
        print_header("STUDENT REPORT")
        
        students = DataManager.read_data("students.txt")
        enrollments = DataManager.read_data("enrollments.txt")
        grades = DataManager.read_data("grades.txt")
        
        print(f"\n📊 Total Students: {len(students)}")
        
        # Students by department
        from collections import defaultdict
        dept_count = defaultdict(int)
        
        for student in students:
            dept = student.get('department', 'N/A')
            dept_count[dept] += 1
        
        print("\n📚 Students by Department:")
        for dept, count in dept_count.items():
            print(f"  {dept}: {count}")
        
        # Enrollment statistics
        total_enrollments = len(enrollments)
        print(f"\n📖 Total Course Enrollments: {total_enrollments}")
        
        # Grade distribution
        grade_count = defaultdict(int)
        for grade in grades:
            grade_count[grade['grade']] += 1
        
        if grade_count:
            print("\n📈 Grade Distribution:")
            for grade, count in sorted(grade_count.items()):
                print(f"  {grade}: {count}")
        
        pause()
    
    def generate_course_report(self):
        """Generate course report"""
        clear_screen()
        print_header("COURSE REPORT")
        
        courses = DataManager.read_data("courses.txt")
        enrollments = DataManager.read_data("enrollments.txt")
        
        print(f"\n📊 Total Courses: {len(courses)}")
        
        # Courses by enrollment
        headers = ["Course ID", "Course Name", "Enrolled Students"]
        rows = []
        
        for course in courses:
            student_count = sum(1 for e in enrollments if e['course_id'] == course['id'])
            rows.append([
                course['id'],
                course['name'],
                student_count
            ])
        
        # Sort by enrollment
        rows.sort(key=lambda x: x[2], reverse=True)
        
        print("\n📚 Courses by Enrollment:")
        print_table(headers, rows)
        
        pause()
    
    def generate_fee_report(self):
        """Generate fee collection report"""
        clear_screen()
        print_header("FEE COLLECTION REPORT")
        
        fees = DataManager.read_data("fees.txt")
        
        if not fees:
            print("\n⚠️ No fee records available")
        else:
            total_fees = sum(f['amount'] for f in fees)
            total_collected = sum(f.get('paid', 0) for f in fees)
            total_due = total_fees - total_collected
            
            paid_count = sum(1 for f in fees if f['status'] == 'Paid')
            unpaid_count = len(fees) - paid_count
            
            print(f"\n💰 Total Fees: ৳{total_fees:.2f}")
            print(f"💵 Total Collected: ৳{total_collected:.2f}")
            print(f"⚠️ Total Outstanding: ৳{total_due:.2f}")
            print(f"\n✅ Paid Records: {paid_count}")
            print(f"❌ Unpaid Records: {unpaid_count}")
            
            collection_rate = (total_collected / total_fees * 100) if total_fees > 0 else 0
            print(f"\n📊 Collection Rate: {collection_rate:.1f}%")
        
        pause()
    
    def view_profile(self):
        """View staff profile"""
        clear_screen()
        print_header("STAFF PROFILE")
        
        print(f"\nID: {self.user['id']}")
        print(f"Name: {self.user['name']}")
        print(f"Email: {self.user.get('email', 'N/A')}")
        print(f"Phone: {self.user.get('phone', 'N/A')}")
        print(f"Role: {self.user.get('role', 'N/A')}")
        
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
                self.user['id'], 'staff', old_pass, new_pass
            )
            
            if success:
                print(f"\n✅ {message}")
                self.user['password'] = new_pass
            else:
                print(f"\n❌ {message}")
        
        pause()