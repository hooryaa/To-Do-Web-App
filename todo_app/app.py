import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TodoistStyleApp:
    """Main application class for the Todoist-style to-do list"""
    
    DATA_FILE = "todos.json"
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.todos = []
        self.setup_window()
        self.create_widgets()
        self.apply_styles()
        self.center_window()
        self.load_todos()
        self.refresh_list()
        
    def setup_window(self):
        """Configure the main window settings"""
        self.root.title("Productivity Pro")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.configure(bg="#202826")

    def create_widgets(self):
        """Create all GUI components"""
        # Main container
        self.main_container = tk.Frame(self.root, bg="#202826")
        self.main_container.pack(expand=True, fill=tk.BOTH)
        
        # [Keep all other widget creation code exactly the same...]
        
    def apply_styles(self):
        """Configure widget styles"""
        style = ttk.Style()
        style.theme_use("clam")
        # [Keep all style configurations the same...]

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_todos(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    self.todos = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.todos = []
        else:
            self.todos = []

    def save_todos(self):
        """Save tasks to JSON file"""
        try:
            with open(self.DATA_FILE, "w") as f:
                json.dump(self.todos, f, indent=2)
        except IOError:
            messagebox.showerror("Error", "Could not save tasks to file.")

    def refresh_list(self):
        """Refresh the task list display"""
        self.task_tree.delete(*self.task_tree.get_children())
        
        for todo in self.todos:
            status = "✓" if todo["completed"] else ""
            priority_text = {
                "1": "❗️ Priority 1",
                "2": "❗️ Priority 2",
                "3": "❗️ Priority 3",
                "4": "No Priority"
            }.get(todo.get("priority", "4"), "No Priority")
            
            self.task_tree.insert(
                "",
                "end",
                values=(status, todo["task"], priority_text),
                tags=("completed" if todo["completed"] else "pending")
            )
        
        self.task_tree.tag_configure("completed", foreground="#6c757d")
        self.task_tree.tag_configure("pending", foreground="#EFCADF")

    def add_todo(self):
        """Add a new task to the list"""
        task = self.task_var.get().strip()
        if not task:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        
        priority = self.priority_var.get()
        
        new_todo = {
            "task": task,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        self.todos.append(new_todo)
        self.save_todos()
        self.refresh_list()
        self.task_var.set("")

    def toggle_completion(self, event=None):
        """Toggle completion status of selected task"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        
        try:
            item_index = self.task_tree.index(selected_item[0])
            if 0 <= item_index < len(self.todos):
                self.todos[item_index]["completed"] = not self.todos[item_index]["completed"]
                self.save_todos()
                self.refresh_list()
        except (IndexError, tk.TclError):
            pass  # Silently handle selection errors

    def delete_todo(self):
        """Delete the selected task"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            item_index = self.task_tree.index(selected_item[0])
            del self.todos[item_index]
            self.save_todos()
            self.refresh_list()

    def show_context_menu(self, event):
        """Show right-click context menu"""
        item = self.task_tree.identify_row(event.y)
        if item:
            self.task_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

def main():
    """Main entry point for the application"""
    root = tk.Tk()
    app = TodoistStyleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()