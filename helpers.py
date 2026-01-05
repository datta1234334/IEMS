import os

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str):
    """Print formatted header"""
    print("="*60)
    print(f" {title:^58} ")
    print("="*60)

def print_menu(options: list):
    """Print numbered menu"""
    print("\n MENU:")
    for i, option in enumerate(options, 1):
        print(f" {i}. {option}")

def generate_id(prefix: str, existing_ids: list) -> str:
    """Generate unique ID"""
    if not existing_ids:
        return f"{prefix}001"
    
    existing_nums = []
    for id_str in existing_ids:
        if id_str.startswith(prefix):
            try:
                num = int(id_str[len(prefix):])
                existing_nums.append(num)
            except:
                continue
    
    next_num = max(existing_nums) + 1 if existing_nums else 1
    return f"{prefix}{next_num:03d}"

