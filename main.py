from task_manager import TaskManager

def print_menu():
    print("\n--- Intelligent Task Manager ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")

def main():

    manager = TaskManager()
    
    while True:

        print_menu()

        choice = input("Enter your choice: ")

        match choice:
            case "1":
                description = input("Enter task description: ")
                manager.add_task(description)

            case "2":
                manager.list_tasks()

            case "3":
                id = int(input("Enter the task ID to complete: "))
                manager.complete_task(id)

            case "4":
                id = int(input("Enter the task ID to delete: "))
                manager.delete_task(id)

            case "5":
                print("Exiting the Task Manager. Goodbye!")
                break
            case _:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()