import re

def valid_habit(habit):
    if not isinstance(habit , str):
        raise ValueError("Habit must be a string")
    
    habit = habit.strip()

    if not habit:
        raise ValueError("Habit cannot be empty")
    
    if len(habit) > 50:
        raise ValueError("Habit can't contain more than 50 characters")
    
    if not re.fullmatch('[a-zA-Z0-9 ]+' ,habit):
        raise ValueError('Only letters, numbers, and spaces are allowed')
    
    if not re.search(r"[a-zA-Z]", habit):
        raise ValueError("Habit must contain at least one letter")
    
    return habit

allowed = ['health' , 'productivity' , 'personal' , 'social' , 'other']
def valid_category(category):
    if not isinstance(category , str):
        raise ValueError("Category must be a string")
    
    category = category.strip().lower()

    if not category:
        raise ValueError("Category cannot be empty")
    
    if category not in allowed :
        raise ValueError(f"Category must be one of: {', '.join(allowed)}")
    
    return category


def valid_other(other):
    if not isinstance(other , str):
        raise ValueError("Custom Category must be a string")
    
    other = other.strip()

    if not other:
        raise ValueError("Custom Category cannot be empty")
    
    if len(other)>30:
        raise ValueError("Custom Category cannot exceed 30 characters")
    
    if not re.fullmatch(r"[a-z ]+" ,other):
        raise ValueError("Only letters and spaced are allowed")
    if not re.search(r"[a-z]" , other):
        raise ValueError("Custom category must contain at least one letter")
    
    return other.capitalize()



    