"""
Automatic Project Structure Creator
Run this script to automatically create all necessary folders and empty files
"""

import os

def create_structure():
    """Create complete project structure"""
    
    print("="*70)
    print(" "*15 + "IEMS PROJECT STRUCTURE CREATOR")
    print("="*70)
    
    # Create directories
    directories = [
        "modules",
        "utils",
        "data"
    ]
    
    print("\n Creating directories...")
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✓ Created: {directory}/")
        else:
            print(f"   ✓ Exists: {directory}/")
    
    # Create __init__.py files
    print("\n📄 Creating __init__.py files...")
    init_files = [
        "modules/__init__.py",
        "utils/__init__.py"
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Package initialization\n")
            print(f"   ✓ Created: {init_file}")
        else:
            print(f"   ✓ Exists: {init_file}")
    
    # Create validators.py (optional utility file)
    validators_path = "utils/validators.py"
    if not os.path.exists(validators_path):
        with open(validators_path, 'w') as f:
            f.write('''"""
Input Validation Functions
"""

def validate_email(email):
    """Validate email format"""
    return "@" in email and "." in email.split("@")[1]

def validate_phone(phone):
    """Validate phone number"""
    cleaned = phone.replace("-", "").replace(" ", "")
    return cleaned.isdigit() and len(cleaned) >= 10

def validate_id(user_id, prefix):
    """Validate user ID format"""
    return user_id.startswith(prefix) and user_id[len(prefix):].isdigit()

def validate_grade(grade):
    """Validate grade format"""
    valid_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F']
    return grade.upper() in valid_grades

def validate_password(password, min_length=6):
    """Validate password strength"""
    return len(password) >= min_length
''')
        print(f"   ✓ Created: {validators_path}")
    
    print("\n" + "="*70)
    print(" PROJECT STRUCTURE CREATED SUCCESSFULLY!")
    print("="*70)
    
    print("\n Current Structure:")
    print("""
IEMS_Project/
│
├── modules/
│   ├── __init__.py ✓
│   ├── authentication.py (copy your code here)
│   ├── student.py (copy your code here)
│   ├── teacher.py (copy your code here)
│   ├── staff.py (copy your code here)
│   └── data_manager.py (copy your code here)
│
├── utils/
│   ├── __init__.py ✓
│   ├── helpers.py (copy your code here)
│   └── validators.py ✓
│
├── data/ ✓ (will be populated by setup.py)
│
├── main.py (copy your code here)
├── setup.py (copy your code here)
└── README.md (copy your documentation here)
    """)
    
    print("\n NEXT STEPS:")
    print("   1. Copy all your Python code files to their respective locations")
    print("   2. Run: python setup.py")
    print("   3. Run: python main.py")
    print("\n" + "="*70)

if __name__ == "__main__":

    create_structure()
