from datetime import datetime
import hashlib
from flask import flash, session

# hash the password
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# Validate password
def validate_password(password, confirm_password):
    if len(password) < 8:
        flash('Password must be at least 8 characters long!')
        return False
    if not any(char.isdigit() for char in password):
        flash('Password must contain at least one digit!')
        return False
    if not any(char.isupper() for char in password):
        flash('Password must contain at least one uppercase letter!')
        return False
    if not any(char.islower() for char in password):
        flash('Password must contain at least one lowercase letter!')
        return False
    if not any(char in ['$', '#', '@'] for char in password):
        flash('Password must contain at least one special character')
        return False
    if password != confirm_password:
        flash('Passwords do not match!')
        return False

def calculate_age(dob_str: str) -> int:
    dob = datetime.strptime(dob_str, "%Y-%m-%d")
    today = datetime.today()
    
    age = today.year - dob.year
    
    # Check if the birthday has occurred this year or not
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    
    return age