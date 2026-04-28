import uuid
from typing import Literal
from datetime import datetime , timedelta
from validator import(valid_habit ,
                      valid_category)
class HabitTracker:

    def __init__(self):
        self.habits = {}
    def add_new_habit(self , habit , category : Literal['Health' , 'Productivity' , 'Personal' , 'Social' , 'Other'] ):

        habit_id = str(uuid.uuid4())
        habit = valid_habit(habit)
        category = valid_category(category)
        created_at = datetime.now().isoformat(timespec='seconds')
        updated_at = None
        completed_days = []
        

        self.habits[habit_id]  = {
            "id" : habit_id,
            "habit" : habit,
            "category" : category,
            "created_at" : created_at,
            "completed_days" : completed_days,
            "updated_at" : updated_at
        }
        
        return self.habits[habit_id]
    
    def mark_habit_done(self ,habit_id):
        if habit_id not in self.habits:
            raise ValueError("Habit ID not found")
        
        today = datetime.now().date().isoformat()
        habit = self.habits[habit_id]

        if today not in habit['completed_days'] :
            habit['completed_days'].append(today)
        else:
            raise ValueError("Habit already marked completed for today.")
        
        return habit['completed_days']

            
    def get_current_streak(self , habit_id):
        if habit_id not in self.habits:
            raise ValueError("Habit ID not found")
        
        habit = self.habits[habit_id]
        completed = set(habit['completed_days'])

        today = datetime.now().date()
        yesterday = today - timedelta(days = 1)


        if today.isoformat() in completed:
            current = today
        elif yesterday.isoformat() in completed:
            current = yesterday
        else:
            return 0

        streak = 0 

        while current.isoformat() in completed:
            streak += 1
            current = current - timedelta(days=1)
        
        return streak

    def get_max_streak(self , habit_id):
        if habit_id not in self.habits:
            raise ValueError("Habit ID not found")
        
        habit = self.habits[habit_id]
        days = habit['completed_days']

        if not days:
            return 0
        
        dates = sorted(datetime.fromisoformat(d).date() for d in days)

        max_streak = 1
        current_streak = 1

        for i in range(1 , len(dates)):
            if dates[i] == dates[i-1] + timedelta(days =1):
                current_streak += 1
            else:
                current_streak = 1
            
            max_streak = max(max_streak , current_streak)
        
        return max_streak


    
    def edit_habit(self , habit_id , new_habit = None , new_category = None):
        if habit_id not in self.habits:
            raise ValueError("Habit ID not found")
        
        habit = self.habits[habit_id]
        updated = False

        if new_habit is None and new_category is None:
            raise ValueError("At least one field must be provided")

        if new_habit is not None:
            validate = valid_habit(new_habit)
            if validate != habit['habit']:
                habit['habit'] = validate
                updated = True

        if new_category is not None:
            validate = valid_category(new_category)
            if validate != habit['category']:
                habit['category'] = validate
                updated = True

        if updated:
            habit['updated_at'] = datetime.now().isoformat(timespec='seconds')

        return habit
    
    def delete_habit(self , habit_id):
        if habit_id not in self.habits:
            raise ValueError("Habit ID not found")
        
        
        deleted =  self.habits.pop(habit_id)

        return deleted

        


        

