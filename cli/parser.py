import sys
from .commands import list_users, list_categories, list_tasks, add_task

def run_once():
    print("Task Manager CLI")
    print("1. List Users")
    print("2. List Categories")
    print("3. List Tasks")
    print("4. Add Task")
    print("0. Exit")
    choice = input("Choose an option: ")
    if choice == "1":
        list_users()
    elif choice == "2":
        list_categories()
    elif choice == "3":
        list_tasks()
    elif choice == "4":
        add_task()
    elif choice == "0":
        sys.exit()
    else:
        print("Invalid choice.")

def run():
    try:
        while True:
            run_once()
    except KeyboardInterrupt:
        print("\nExiting.")

if __name__ == "__main__":
    run()
