"""
Utility Helper Functions
Common functions used across the application
"""

import os
import sys

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text, char="*"):
    """Print a formatted header"""
    width = 60
    print("\n" + char * width)
    print(text.center(width))
    print(char * width)

def pause():
    """Pause and wait for user input"""
    input("\nPress Enter to continue...")

def print_table(headers, rows):
    """Print data in a formatted table"""
    if not rows:
        print("\n No data to display")
        return
    
    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Print header
    header_line = " | ".join(str(h).ljust(w) for h, w in zip(headers, col_widths))
    print("\n" + header_line)
    print("-" * len(header_line))
    
    # Print rows
    for row in rows:
        row_line = " | ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
        print(row_line)

def format_currency(amount):
    """Format number as currency"""
    return f"৳{amount:,.2f}"

def validate_email(email):
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]

def validate_phone(phone):
    """Basic phone validation"""
    return phone.isdigit() and len(phone) >= 10

def get_input(prompt, validation_func=None, error_msg="Invalid input"):
    """Get validated input from user"""
    while True:
        value = input(prompt).strip()
        
        if not validation_func or validation_func(value):
            return value
        
        print(f"\n {error_msg}")

def confirm_action(message):
    """Ask user to confirm an action"""
    response = input(f"\n{message} (yes/no): ").strip().lower()
    return response == "yes"

def print_success(message):
    """Print success message"""
    print(f"\n {message}")

def print_error(message):
    """Print error message"""
    print(f"\n {message}")

def print_warning(message):
    """Print warning message"""
    print(f"\n {message}")

def print_info(message):
    """Print info message"""

    print(f"\n {message}")
