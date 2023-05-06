from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time, timedelta

def my_task():
    # Define the task to be executed at midnight
    print("Task executed at midnight")

scheduler = BackgroundScheduler()

def run_scheduler():
    # Get the current date and time
    now = datetime.now()

    # Calculate the timestamp of the next 00:00
    next_run_time = datetime.combine(now.date(), time(hour=0, minute=0))

    if next_run_time < now:
        next_run_time += timedelta(days=1)

    # Add the task to the scheduler
    scheduler.add_job(my_task, 'interval', days=1, next_run_time=next_run_time)

    # Start the scheduler
    scheduler.start()

