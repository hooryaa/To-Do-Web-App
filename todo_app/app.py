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
        self.setup_window()
        self.todos = []  # Initialize todos list
        self.load_todos()
        self.create_widgets()
        self.apply_styles()
        self.center_window()
        self.refresh_list()  # Initial refresh
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Productivity Pro")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        self.root.configure(bg="#202826")  # Dark background
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_container = tk.Frame(self.root, bg="#202826")
        main_container.pack(expand=True, fill=tk.BOTH)
        
        # Header
        header_frame = tk.Frame(main_container, bg="#202826", height=60)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame,
            text="PRODUCTIVITY PRO",
            font=("Segoe UI", 18, "bold"),
            bg="#202826",
            fg="#F695C5"  # Primary pink accent
        ).pack(side=tk.LEFT, padx=20)
        
        # Sidebar
        sidebar_frame = tk.Frame(main_container, bg="#202826", width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Sidebar items
        sidebar_items = ["Inbox", "Today", "Upcoming", "Projects"]
        for item in sidebar_items:
            btn = tk.Button(
                sidebar_frame,
                text=item,
                font=("Segoe UI", 11),
                bg="#202826",
                fg="#EFCADF",  # Secondary pale pink
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
        content_frame = tk.Frame(main_container, bg="#202826")
        content_frame.pack(expand=True, fill=tk.BOTH)
        
        # Task input
        input_frame = tk.Frame(content_frame, bg="#202826", padx=20, pady=15)
        input_frame.pack(fill=tk.X)
        
        self.task_var = tk.StringVar()
        self.task_entry = ttk.Entry(
            input_frame,
            textvariable=self.task_var,
            font=("Segoe UI", 12)
        )
        self.task_entry.pack(fill=tk.X, padx=(0, 10), side=tk.LEFT, expand=True)
        self.task_entry.bind("<Return>", lambda e: self.add_todo())
        
        # Priority dropdown
        self.priority_var = tk.StringVar(value="4")
        priorities = {"1": "❗️ Priority 1", "2": "❗️ Priority 2", "3": "❗️ Priority 3", "4": "No Priority"}
        priority_menu = ttk.OptionMenu(
            input_frame,
            self.priority_var,
            "4",
            *priorities.values()
        )
        priority_menu.pack(side=tk.LEFT)
        
        # Add button
        add_btn = ttk.Button(
            input_frame,
            text="Add Task",
            command=self.add_todo,
            style="Accent.TButton"
        )
        add_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Task list
        list_frame = tk.Frame(content_frame, bg="#202826")
        list_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 20))
        
        self.task_tree = ttk.Treeview(
            list_frame,
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
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#202826", fg="#EFCADF")
        self.context_menu.add_command(label="Complete Task", command=self.toggle_completion)
        self.context_menu.add_command(label="Delete Task", command=self.delete_todo)
        
        # Bind events
        self.task_tree.bind("<Button-3>", self.show_context_menu)
        self.task_tree.bind("<Double-1>", self.toggle_completion)
    
    def apply_styles(self):
        """Configure custom styles with the pink and black color palette"""
        style = ttk.Style()
        
        # Configure the theme
        style.theme_use('clam')  # 'clam' theme is more customizable
        
        # Base styles
        style.configure(".",
                      background="#202826",
                      foreground="#EFCADF",
                      font=("Segoe UI", 11))
        
        # Treeview styles
        style.configure("Treeview",
                      background="#2a3432",  # Slightly lighter dark background
                      fieldbackground="#2a3432",
                      foreground="#EFCADF",  # Pale pink text
                      rowheight=35,
                      font=("Segoe UI", 11),
                      borderwidth=0)
        
        style.configure("Treeview.Heading",
                      background="#202826",
                      foreground="#F695C5",  # Brighter pink for headings
                      font=("Segoe UI", 10, "bold"),
                      borderwidth=0)
        
        style.map("Treeview",
                background=[("selected", "#3a4442")],  # Even lighter for selection
                foreground=[("selected", "#F695C5")])  # Brighter pink for selected text
        
        # Button styles
        style.configure("Accent.TButton",
                      foreground="#202826",  # Dark text
                      background="#F695C5",  # Bright pink button
                      font=("Segoe UI", 10, "bold"),
                      padding=6,
                      borderwidth=1)
        
        style.map("Accent.TButton",
                background=[("active", "#e485b5")])  # Slightly darker pink when pressed
        
        # Entry and Combobox styles
        style.configure("TEntry",
                      fieldbackground="#2a3432",
                      foreground="#EFCADF",
                      insertcolor="#EFCADF",
                      bordercolor="#3a4442",
                      lightcolor="#3a4442",
                      darkcolor="#3a4442")
        
        style.configure("TCombobox",
                      fieldbackground="#2a3432",
                      foreground="#EFCADF",
                      background="#202826",
                      selectbackground="#3a4442")
        
        style.map("TCombobox",
                fieldbackground=[("readonly", "#2a3432")],
                selectbackground=[("readonly", "#3a4442")])
    
    def load_todos(self):
        """Load tasks from JSON file"""
        try:
            if os.path.exists(self.DATA_FILE):
                with open(self.DATA_FILE, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):  # Check if data is a list
                        self.todos = data
                    else:
                        self.todos = []
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tasks: {str(e)}")
            self.todos = []
    
    def save_todos(self):
        """Save tasks to JSON file"""
        try:
            with open(self.DATA_FILE, "w") as f:
                json.dump(self.todos, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tasks: {str(e)}")
    
    def refresh_list(self):
        """Refresh the task list display"""
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        for todo in self.todos:
            # Ensure each todo has the required keys
            if not isinstance(todo, dict):
                continue
                
            if "task" not in todo:
                continue
                
            status = "✓" if todo.get("completed", False) else "◯"
            priority = todo.get("priority", "4")
            
            priority_emoji = {
                "1": "❗️ P1",
                "2": "❗️ P2",
                "3": "❗️ P3",
                "4": "⏱️ No Priority"
            }.get(priority, "⏱️ No Priority")
            
            tags = ("completed",) if todo.get("completed", False) else ()
            
            self.task_tree.insert("", "end",
                                values=(status, todo["task"], priority_emoji),
                                tags=tags)
        
        self.task_tree.tag_configure("completed", foreground="#7a7a7a")  # Gray for completed items
    
    def add_todo(self):
        """Add a new task to the list"""
        task_text = self.task_var.get().strip()
        if not task_text:
            messagebox.showwarning("Warning", "Task cannot be empty!")
            return
        
        new_todo = {
            "task": task_text,
            "priority": self.priority_var.get(),
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        self.todos.append(new_todo)
        self.task_var.set("")
        self.save_todos()
        self.refresh_list()
    
    def toggle_completion(self, event=None):
        """Toggle task completion status"""
        selected = self.task_tree.focus()
        if not selected:
            return
        
        selected_item = self.task_tree.item(selected)
        task_text = selected_item["values"][1]
        
        for todo in self.todos:
            if todo["task"] == task_text:
                todo["completed"] = not todo.get("completed", False)
                break
        
        self.save_todos()
        self.refresh_list()
    
    def delete_todo(self):
        """Delete the selected task"""
        selected = self.task_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "No task selected!")
            return
        
        if messagebox.askyesno("Confirm", "Delete this task?"):
            selected_item = self.task_tree.item(selected)
            task_text = selected_item["values"][1]
            
            self.todos = [todo for todo in self.todos if todo["task"] != task_text]
            self.save_todos()
            self.refresh_list()
    
    def show_context_menu(self, event):
        """Show the right-click context menu"""
        item = self.task_tree.identify_row(event.y)
        if item:
            self.task_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = TodoistStyleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()