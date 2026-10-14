from task_manager import TaskManager
from ai_service import create_simple_task

def print_menu():
    print("\n--- Intelligent Task Manager ---")
    print("1. Add Task")
    print("2. Add complex task")
    print("3. List Tasks")
    print("4. Complete Task")
    print("5. Delete Task")
    print("6. Exit")

def main():

    manager = TaskManager()
    
    while True:

        print_menu()

        try:

            choice = int(input("Enter your choice: "))

            match choice:
                case 1:
                    description = input("Enter task description: ")
                    manager.add_task(description)

                case 2:
                    description = input("Enter complex task description: ")
                    subtasks = create_simple_task(description)
                    for subtask in subtasks:
                        if not subtask.startswith("Error:"):
                            manager.add_task(subtask)
                        else:
                            print(subtask)
                            break

                case 3:
                    manager.list_tasks()

                case 4:
                    id = int(input("Enter the task ID to complete: "))
                    manager.complete_task(id)

                case 5:
                    id = int(input("Enter the task ID to delete: "))
                    manager.delete_task(id)

                case 6:
                    print("Exiting the Task Manager. Goodbye!")
                    break
                case _:
                    print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()