import sqlite3
from datetime import datetime

class SimpleTaskManager:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                description TEXT,
                deadline TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def add_task(self):
        description = input("Enter task description: ")
        
        while True:
            deadline = input("Enter deadline (YYYY-MM-DD) or press Enter to skip: ")
            if deadline == "":
                deadline = None
                break
            try:
                datetime.strptime(deadline, '%Y-%m-%d')
                break
            except ValueError:
                print("Please use YYYY-MM-DD format (example: 2024-02-01)")
        
        self.conn.execute(
            'INSERT INTO tasks (description, deadline, status) VALUES (?, ?, ?)',
            (description, deadline, 'pending')
        )
        self.conn.commit()
        print("Task added successfully!")

    def view_tasks(self, status=None):
        if status:
            cursor = self.conn.execute(
                'SELECT * FROM tasks WHERE status = ?', 
                (status,)
            )
        else:
            cursor = self.conn.execute('SELECT * FROM tasks')
        
        tasks = cursor.fetchall()
        
        if not tasks:
            print("No tasks found!")
            return
        
        print("\nYour Tasks:")
        print("ID  | Description          | Deadline   | Status")
        print("-" * 50)
        for task in tasks:
            deadline = task[2] if task[2] else "No deadline"
            print(f"{task[0]:<4}| {task[1][:20]:<20}| {deadline:<10}| {task[3]}")

    def update_task(self):
        self.view_tasks()
        
        try:
            task_id = int(input("\nEnter the ID of the task to update: "))
        except ValueError:
            print("Please enter a valid number!")
            return
        
        cursor = self.conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        if not cursor.fetchone():
            print("Task not found!")
            return
        
        print("\n1. Mark as completed")
        print("2. Mark as pending")
        choice = input("Enter your choice (1-2): ")
        
        if choice == "1":
            new_status = "completed"
        elif choice == "2":
            new_status = "pending"
        else:
            print("Invalid choice!")
            return
        
        self.conn.execute(
            'UPDATE tasks SET status = ? WHERE id = ?',
            (new_status, task_id)
        )
        self.conn.commit()
        print("Task updated successfully!")

    def delete_task(self):
        self.view_tasks()
        
        try:
            task_id = int(input("\nEnter the ID of the task to delete: "))
        except ValueError:
            print("Please enter a valid number!")
            return
        
        self.conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        print("Task deleted!")

def main():
    task_manager = SimpleTaskManager()
    
    while True:
        print("\n=== Task Manager ===")
        print("1. Add new task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update task")
        print("6. Delete task")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ")
        
        if choice == "1":
            task_manager.add_task()
        elif choice == "2":
            task_manager.view_tasks()
        elif choice == "3":
            task_manager.view_tasks("pending")
        elif choice == "4":
            task_manager.view_tasks("completed")
        elif choice == "5":
            task_manager.update_task()
        elif choice == "6":
            task_manager.delete_task()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()