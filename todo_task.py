import json
import datetime
import os


def add_task(task_id):
   task = {
      "id": str(task_id),
      "name": input("Enter task name: "),
      "status": "todo",
      "description": input("Enter task description: "),
      "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "updated_at": ""
   }
   return task


def load_json(filename):
   if not os.path.exists(filename) or os.path.getsize(filename) == 0:
      with open("task_tracker/tasks.json", "x") as f:
         return json.load(f)
   try:
      with open(filename, "r") as f:
         return json.load(f)
   except json.JSONDecodeError:
      return []


def save_update(filename, data):
   with open(filename, "w") as f:
      json.dump(data, f, indent=4)
   print(f"Updated data saved to '{filename}'.")


def update_task(filename):
   tasks = load_json(filename)
   if not tasks:
      print("No tasks to update.")
      return

   task_id = input("Enter task id: ")
   found = False

   for task in tasks:
      if task["id"] == task_id:
         print(f"\nFound task: {task['name']}")
         new_status = input("Enter new status (todo, in-progress, done): ").lower()
         task["status"] = new_status
         task["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         found = True
         print("Task updated successfully.")
         break

   if found:
      save_update(filename, tasks)
   else:
      print("Task not found.")


def delete_task(filename):
   tasks = load_json(filename)
   task_id = input("Enter task id to delete: ")
   new_list = [task for task in tasks if task["id"] != task_id]

   if len(new_list) < len(tasks):
      save_update(filename, new_list)
      print("Task deleted successfully.")
   else:
      print("Task not found.")


def main():
   filename = "task_tracker/tasks.json"

   while True:
      action = input("\nChoose an option: [Add], [Update], [Delete], [Exit]: ").lower()

      if action == "add":
         task_list = load_json(filename)
         next_id = len(task_list) + 1

         while True:
            task = add_task(next_id)
            task_list.append(task)
            next_id += 1

            more = input("Do you want to add another task? (yes/no): ").lower()
            if more != "yes":
               break

         save_update(filename, task_list)

      elif action == "update":
         update_task(filename)

      elif action == "delete":
         delete_task(filename)

      elif action == "exit":
         print("Exited program.")
         break

      else:
         print("Invalid option. Please enter a valid action.")


if __name__ == "__main__":
    main()
