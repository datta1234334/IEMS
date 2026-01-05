"""
Setup Script for IEMS
Run this once to initialize the system with sample data
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_manager import DataManager

def setup_system():
    """Initialize the system with sample data"""
    print("="*60)
    print("IEMS SYSTEM SETUP")
    print("="*60)
    
    # Ensure data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
        print("\n Created data directory")
    
    # Initialize system data
    print("\n Initializing system...")
    DataManager.initialize_system()
    
    # Create sample students
    print("\n Creating sample students...")
    students = DataManager.read_data("students.txt")
    if len(students) < 3:
        sample_students = [
            {
                "id": "STU001",
                "name": "Ahmed Rahman",
                "email": "ahmed@student.smuct.edu",
                "phone": "01711111111",
                "department": "Computer Science",
                "batch": "2023",
                "password": "student123"
            },
            {
                "id": "STU002",
                "name": "Fatima Khan",
                "email": "fatima@student.smuct.edu",
                "phone": "01722222222",
                "department": "Computer Science",
                "batch": "2023",
                "password": "student123"
            },
            {
                "id": "STU003",
                "name": "Rahim Ahmed",
                "email": "rahim@student.smuct.edu",
                "phone": "01733333333",
                "department": "Business",
                "batch": "2024",
                "password": "student123"
            }
        ]
        
        for student in sample_students:
            DataManager.add_record("students.txt", student)
        
        print(" Sample students created")
        print("   Login with: STU001, STU002, STU003 (password: student123)")
    
    # Create sample teachers
    print("\n Creating sample teachers...")
    teachers = DataManager.read_data("teachers.txt")
    if len(teachers) < 2:
        sample_teachers = [
            {
                "id": "TCH001",
                "name": "Dr. Kamal Hossain",
                "email": "kamal@smuct.edu",
                "phone": "01711222333",
                "department": "Computer Science",
                "designation": "Professor",
                "password": "teacher123"
            },
            {
                "id": "TCH002",
                "name": "Ms. Nadia Rahman",
                "email": "nadia@smuct.edu",
                "phone": "01722333444",
                "department": "Computer Science",
                "designation": "Lecturer",
                "password": "teacher123"
            }
        ]
        
        for teacher in sample_teachers:
            DataManager.add_record("teachers.txt", teacher)
        
        print(" Sample teachers created")
        print("   Login with: TCH001, TCH002 (password: teacher123)")
    
    # Assign teachers to courses
    print("\n Assigning teachers to courses...")
    courses = DataManager.read_data("courses.txt")
    if courses and any(not c.get('teacher_id') for c in courses):
        teachers = DataManager.read_data("teachers.txt")
        for i, course in enumerate(courses):
            if not course.get('teacher_id') and teachers:
                course['teacher_id'] = teachers[i % len(teachers)]['id']
        
        DataManager.write_data("courses.txt", courses)
        print(" Teachers assigned to courses")
    
    # Create sample enrollments
    print("\n Creating sample enrollments...")
    enrollments = DataManager.read_data("enrollments.txt")
    if not enrollments:
        sample_enrollments = [
            {"student_id": "STU001", "course_id": "CSE101", "semester": "Spring 2026", "status": "Active"},
            {"student_id": "STU001", "course_id": "CSE102", "semester": "Spring 2026", "status": "Active"},
            {"student_id": "STU002", "course_id": "CSE101", "semester": "Spring 2026", "status": "Active"},
            {"student_id": "STU002", "course_id": "ENG101", "semester": "Spring 2026", "status": "Active"},
            {"student_id": "STU003", "course_id": "CSE101", "semester": "Spring 2026", "status": "Active"},
        ]
        
        for enrollment in sample_enrollments:
            DataManager.add_record("enrollments.txt", enrollment)
        
        print(" Sample enrollments created")
    
    # Create sample grades
    print("\n Creating sample grades...")
    grades = DataManager.read_data("grades.txt")
    if not grades:
        sample_grades = [
            {"student_id": "STU001", "course_id": "CSE101", "grade": "A", "points": "95", "remarks": "Excellent", "date": "2025-12-15"},
            {"student_id": "STU002", "course_id": "CSE101", "grade": "B+", "points": "87", "remarks": "Good", "date": "2025-12-15"},
        ]
        
        for grade in sample_grades:
            DataManager.add_record("grades.txt", grade)
        
        print(" Sample grades created")
    
    # Create sample fee records
    print("\n Creating sample fee records...")
    fees = DataManager.read_data("fees.txt")
    if not fees:
        sample_fees = [
            {"student_id": "STU001", "semester": "Spring 2026", "amount": 50000, "paid": 50000, "status": "Paid", "date": "2026-01-01"},
            {"student_id": "STU002", "semester": "Spring 2026", "amount": 50000, "paid": 25000, "status": "Partial", "date": ""},
            {"student_id": "STU003", "semester": "Spring 2026", "amount": 50000, "paid": 0, "status": "Unpaid", "date": ""},
        ]
        
        for fee in sample_fees:
            DataManager.add_record("fees.txt", fee)
        
        print(" Sample fee records created")
    
    # Create sample attendance
    print("\n Creating sample attendance records...")
    attendance = DataManager.read_data("attendance.txt")
    if not attendance:
        from datetime import datetime, timedelta
        
        sample_attendance = []
        students_ids = ["STU001", "STU002", "STU003"]
        courses_ids = ["CSE101", "CSE102"]
        
        # Create 5 days of attendance
        for day in range(5):
            date = (datetime.now() - timedelta(days=day)).strftime('%Y-%m-%d')
            for student_id in students_ids:
                for course_id in courses_ids:
                    status = "Present" if (day + ord(student_id[-1])) % 3 != 0 else "Absent"
                    sample_attendance.append({
                        "student_id": student_id,
                        "course_id": course_id,
                        "date": date,
                        "status": status
                    })
        
        for att in sample_attendance:
            DataManager.add_record("attendance.txt", att)
        
        print(" Sample attendance records created")
    
    print("\n" + "="*60)
    print(" SYSTEM SETUP COMPLETE!")
    print("="*60)
    
    print("\n DEFAULT LOGIN CREDENTIALS:")
    print("\n Staff/Admin:")
    print("   ID: STF001")
    print("   Password: admin123")
    
    print("\n Teachers:")
    print("   ID: TCH001, TCH002")
    print("   Password: teacher123")
    
    print("\n Students:")
    print("   ID: STU001, STU002, STU003")
    print("   Password: student123")
    
    print("\n" + "="*60)
    print(" Run 'python main.py' to start the application")
    print("="*60 + "\n")

if __name__ == "__main__":

    setup_system()
