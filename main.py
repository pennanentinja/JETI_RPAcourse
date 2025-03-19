import json
import os
import datetime
from google_calendar import get_calendar_events 

# A list to hold tasks
tasks = []

# File path for saving tasks
TASKS_FILE = "data/tasks.json"

# Function to add a task to the list
def add_task(name, due_date, priority):
    task = {"name": name, "due_date": due_date, "priority": priority}
    tasks.append(task)

# Function to display all tasks
def show_tasks():
    if not tasks:
        print("No tasks available.")
    else:
        for task in tasks:
            print(f"Task: {task['name']}, Due Date: {task['due_date']}, Priority: {task['priority']}")

# Function to sort tasks by priority (High, Medium, Low)
def sort_tasks_by_priority():
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    sorted_tasks = sorted(tasks, key=lambda x: priority_order[x["priority"]])
    for task in sorted_tasks:
        print(f"Task: {task['name']}, Due Date: {task['due_date']}, Priority: {task['priority']}")

# Function to save tasks to a JSON file
def save_tasks():
    # Ensure the 'data' folder exists
    if not os.path.exists('data'):
        os.makedirs('data')
        
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)
    print("Tasks have been saved.")

# Function to load tasks from a JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):  # Check if the file exists
        with open(TASKS_FILE, "r") as file:
            try:
                return json.load(file)  # Attempt to load JSON data
            except json.JSONDecodeError:
                print("Error: JSON file is empty or invalid. Returning an empty task list.")
                return []  # Return an empty list if JSON is invalid
    return []  # Return an empty list if the file doesn't exist


# Load tasks when the program starts
tasks = load_tasks()

def check_reminders():
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    for task in tasks:
        task_date = datetime.datetime.strptime(task["due_date"], "%Y-%m-%d").date()
        if task_date == today:
            print(f"\n🔔 Reminder: '{task['name']}' due today!")
        elif task_date == tomorrow:
            print(f"\n⏳ Reminder: '{task['name']}' due tomorrow.")

# Main menu for the user to interact with
def display_menu():
    print("\n1. Add Task")
    print("2. View Tasks")
    print("3. Sort Tasks by Priority")
    print("4. Exit")

# Main program loop
def main():
    while True:
        # Retrieve and display Google Calendar events.
        get_calendar_events()  # This shows the upcoming events from Google Calendar.
        
        # Display the menu to the user.
        check_reminders()  # Check and display the reminders.
        display_menu()

        # User's choice
        choice = input("\nChoose an option: ")
    

        if choice == "1":
            name = input("Enter task name: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            priority = input("Enter priority (High, Medium, Low): ")
            add_task(name, due_date, priority)
        elif choice == "2":
            show_tasks()
        elif choice == "3":
            sort_tasks_by_priority()
        elif choice == "4":
            save_tasks()  # Save tasks before exiting
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
