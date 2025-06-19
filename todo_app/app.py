import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class TodoistStyleApp:
    """Todoist-inspired To-Do List Application"""
    
    DATA_FILE = "todos.json"
    
    def __init__(self, root):
        self.root = root
        self.todos = []
        self.setup_window()
        self.create_widgets()
        self.apply_styles()
        self.center_window()
        self.load_todos()
        self.refresh_list()
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Productivity Pro")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.configure(bg="#202826")

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_container = tk.Frame(self.root, bg="#202826")
        self.main_container.pack(expand=True, fill=tk.BOTH)
        
        # Header
        self.header_frame = tk.Frame(self.main_container, bg="#202826", height=60)
        self.header_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.title_label = tk.Label(
            self.header_frame,
            text="PRODUCTIVITY PRO",
            font=("Segoe UI", 18, "bold"),
            bg="#202826",
            fg="#F695C5"
        )
        self.title_label.pack(side=tk.LEFT, padx=20)
        
        # Sidebar
        self.sidebar_frame = tk.Frame(self.main_container, bg="#202826", width=200)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Sidebar items
        sidebar_items = ["Inbox", "Today", "Upcoming", "Projects"]
        for item in sidebar_items:
            btn = tk.Button(
                self.sidebar_frame,
                text=item,
                font=("Segoe UI", 11),
                bg="#202826",
                fg="#EFCADF",
                bd=0,
                padx=20,
                pady=10,
                anchor="w",
                relief=tk.FLAT,
                activebackground="#2a3432",
                activeforeground="#F695C5"
            )
            btn.pack(fill=tk.X)
        
        # Content area
        self.content_frame = tk.Frame(self.main_container, bg="#202826")
        self.content_frame.pack(expand=True, fill=tk.BOTH)
        
        # Task input
        self.input_frame = tk.Frame(self.content_frame, bg="#202826", padx=20, pady=15)
        self.input_frame.pack(fill=tk.X)
        
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(
            self.input_frame,
            textvariable=self.task_var,
            font=("Segoe UI", 12)
        )
        self.task_entry.pack(fill=tk.X, padx=(0, 10), side=tk.LEFT, expand=True)
        self.task_entry.bind("<Return>", lambda e: self.add_todo())
        
        # Priority dropdown
        self.priority_var = tk.StringVar(value="4")
        priorities = {"1": "❗️ Priority 1", "2": "❗️ Priority 2", "3": "❗️ Priority 3", "4": "No Priority"}
        self.priority_menu = ttk.OptionMenu(
            self.input_frame,
            self.priority_var,
            "4",
            *priorities.values()
        )
        self.priority_menu.pack(side=tk.LEFT)
        
        # Add button
        self.add_btn = ttk.Button(
            self.input_frame,
            text="Add Task",
            command=self.add_todo,
            style="Accent.TButton"
        )
        self.add_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Task list
        self.list_frame = tk.Frame(self.content_frame, bg="#202826")
        self.list_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 20))
        
        self.task_tree = ttk.Treeview(
            self.list_frame,
            columns=("status", "task", "priority"),
            show="headings",
            selectmode="browse",
            style="Treeview"
        )
        
        # Configure columns
        self.task_tree.heading("status", text="", anchor=tk.W)
        self.task_tree.heading("task", text="Task", anchor=tk.W)
        self.task_tree.heading("priority", text="Priority", anchor=tk.W)
        
        self.task_tree.column("status", width=40, stretch=False)
        self.task_tree.column("task", width=400, stretch=True)
        self.task_tree.column("priority", width=100, stretch=False)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#202826", fg="#EFCADF")
        self.context_menu.add_command(label="Complete Task", command=self.toggle_completion)
        self.context_menu.add_command(label="Delete Task", command=self.delete_todo)
        
        # Bind events
        self.task_tree.bind("<Button-3>", self.show_context_menu)
        self.task_tree.bind("<Double-1>", self.toggle_completion)

    def apply_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configure colors
        style.configure("TFrame", background="#202826")
        style.configure("TLabel", background="#202826", foreground="#EFCADF", font=("Segoe UI", 10))
        style.configure("TEntry", fieldbackground="#2a3432", foreground="#EFCADF", 
                      insertcolor="#EFCADF", font=("Segoe UI", 12), padding=5)
        style.configure("TButton", background="#3d4a47", foreground="#EFCADF", 
                      font=("Segoe UI", 10), padding=6)
        style.map("TButton", background=[("active", "#4a5a56")], foreground=[("active", "#F695C5")])
        style.configure("Accent.TButton", background="#F695C5", foreground="#202826", 
                       font=("Segoe UI", 10, "bold"), padding=6)
        style.map("Accent.TButton", background=[("active", "#ffa9d9")], foreground=[("active", "#202826")])
        style.configure("Treeview", background="#2a3432", foreground="#EFCADF", 
                       fieldbackground="#2a3432", rowheight=30, font=("Segoe UI", 11))
        style.configure("Treeview.Heading", background="#3d4a47", foreground="#EFCADF", 
                       font=("Segoe UI", 11, "bold"), padding=5, relief="flat")
        style.map("Treeview", background=[("selected", "#F695C5")], foreground=[("selected", "#202826")])
        style.configure("TMenubutton", background="#3d4a47", foreground="#EFCADF", 
                       font=("Segoe UI", 10), padding=6, arrowcolor="#EFCADF")
        style.configure("Vertical.TScrollbar", background="#3d4a47", troughcolor="#202826")

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_todos(self):
        """Load todos from JSON file"""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    self.todos = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.todos = []
        else:
            self.todos = []

    def save_todos(self):
        """Save todos to JSON file"""
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
        """Add a new todo item"""
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
            pass  # Handle cases where selection doesn't match todos list

    def delete_todo(self):
        """Delete selected todo item"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            item_index = self.task_tree.index(selected_item[0])
            del self.todos[item_index]
            self.save_todos()
            self.refresh_list()

    def show_context_menu(self, event):
        """Show context menu for tasks"""
        item = self.task_tree.identify_row(event.y)
        if item:
            self.task_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

def main():
    root = tk.Tk()
    app = TodoistStyleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
