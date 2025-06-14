import unittest
import os
import json
import tkinter as tk
from unittest.mock import patch, MagicMock
from datetime import datetime
from tkinter import messagebox
from tkinter import Tk
from app import TodoistStyleApp  # For same-directory import

class TestTodoistStyleApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a root window for testing (only once)
        cls.root = Tk()
        cls.root.withdraw()  # Hide the window during tests
    
    @classmethod
    def tearDownClass(cls):
        # Destroy the root window after all tests
        cls.root.destroy()
    
    def setUp(self):
        """Verify initial conditions before each test"""
        self.app = TodoistStyleApp(self.root)
        self.assertEqual(len(self.app.todos), 0)  # Ensure fresh start
        if os.path.exists(self.app.DATA_FILE):
            os.remove(self.app.DATA_FILE)
    
    def tearDown(self):
        # Clean up after each test
        if os.path.exists(self.app.DATA_FILE):
            os.remove(self.app.DATA_FILE)
    
    def test_initial_state(self):
        """Test the application initializes correctly"""
        self.assertEqual(self.app.todos, [])
        self.assertIsInstance(self.app.task_var, type(tk.StringVar()))
        self.assertIsInstance(self.app.priority_var, type(tk.StringVar()))
    
    def test_add_todo(self):
        """Test adding a new todo"""
        # Simulate adding a task
        self.app.task_var.set("Test task")
        self.app.priority_var.set("2")
        self.app.add_todo()
        
        # Check the todo was added
        self.assertEqual(len(self.app.todos), 1)
        self.assertEqual(self.app.todos[0]["task"], "Test task")
        self.assertEqual(self.app.todos[0]["priority"], "2")
        self.assertFalse(self.app.todos[0]["completed"])
        self.assertTrue("created_at" in self.app.todos[0])
        
        # Check the entry was cleared
        self.assertEqual(self.app.task_var.get(), "")
    
    def test_add_empty_todo(self):
        """Test adding an empty todo shows warning"""
        with patch.object(messagebox, 'showwarning') as mock_warning:
            self.app.task_var.set("")
            self.app.add_todo()
            
            mock_warning.assert_called_once_with("Warning", "Task cannot be empty!")
            self.assertEqual(len(self.app.todos), 0)
    
    def test_toggle_completion(self):
        """Test toggling todo completion status"""
        # Add a test todo
        test_todo = {
            "task": "Test task",
            "priority": "2",
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.app.todos.append(test_todo)
        self.app.refresh_list()
        
        # Get and select the first item
        items = self.app.task_tree.get_children()
        self.assertEqual(len(items), 1)
        self.app.task_tree.selection_set(items[0])
        
        # Toggle completion
        self.app.toggle_completion()
        self.app.refresh_list()
        
        # Check the completion status changed
        self.assertTrue(self.app.todos[0]["completed"])
        
        # Toggle again
        self.app.toggle_completion()
        self.app.refresh_list()
        self.assertFalse(self.app.todos[0]["completed"])
    
    def test_delete_todo(self):
        """Test deleting a todo"""
        # Add a test todo
        test_todo = {
            "task": "Test task",
            "priority": "2",
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.app.todos.append(test_todo)
        self.app.refresh_list()
        
        # Ensure the item exists and is selected
        items = self.app.task_tree.get_children()
        self.assertEqual(len(items), 1)
        self.app.task_tree.selection_set(items[0])
        
        # Mock the confirmation dialog to return True
        with patch.object(messagebox, 'askyesno', return_value=True):
            self.app.delete_todo()
            
            # Check the todo was deleted
            self.assertEqual(len(self.app.todos), 0)
            self.assertEqual(len(self.app.task_tree.get_children()), 0)
    
    def test_load_todos(self):
        """Test loading todos from file"""
        # Create test data
        test_data = [
            {
                "task": "Test task 1",
                "priority": "1",
                "completed": False,
                "created_at": datetime.now().isoformat()
            },
            {
                "task": "Test task 2",
                "priority": "2",
                "completed": True,
                "created_at": datetime.now().isoformat()
            }
        ]
        
        # Write to file
        with open(self.app.DATA_FILE, 'w') as f:
            json.dump(test_data, f)
        
        # Load the todos
        self.app.load_todos()
        
        # Check they were loaded correctly
        self.assertEqual(len(self.app.todos), 2)
        self.assertEqual(self.app.todos[0]["task"], "Test task 1")
        self.assertEqual(self.app.todos[1]["task"], "Test task 2")
    
    def test_save_todos(self):
        """Test saving todos to file"""
        # Add test todos
        test_todo1 = {
            "task": "Test task 1",
            "priority": "1",
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        test_todo2 = {
            "task": "Test task 2",
            "priority": "2",
            "completed": True,
            "created_at": datetime.now().isoformat()
        }
        self.app.todos.extend([test_todo1, test_todo2])
        
        # Save the todos
        self.app.save_todos()
        
        # Check the file was created and contains the data
        self.assertTrue(os.path.exists(self.app.DATA_FILE))
        
        with open(self.app.DATA_FILE, 'r') as f:
            loaded_data = json.load(f)
            self.assertEqual(len(loaded_data), 2)
            self.assertEqual(loaded_data[0]["task"], "Test task 1")
            self.assertEqual(loaded_data[1]["task"], "Test task 2")
    
    def test_refresh_list(self):
        """Test refreshing the task list display"""
        # Add test todos
        test_todo1 = {
            "task": "Test task 1",
            "priority": "1",
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        test_todo2 = {
            "task": "Test task 2",
            "priority": "2",
            "completed": True,
            "created_at": datetime.now().isoformat()
        }
        self.app.todos.extend([test_todo1, test_todo2])
        
        # Refresh the list
        self.app.refresh_list()
        
        # Check the items were added to the treeview
        items = self.app.task_tree.get_children()
        self.assertEqual(len(items), 2)
        
        # Check the values are correct
        item1_values = self.app.task_tree.item(items[0])['values']
        self.assertEqual(item1_values[1], "Test task 1")
        self.assertEqual(item1_values[2], "❗️ P1")
        
        item2_values = self.app.task_tree.item(items[1])['values']
        self.assertEqual(item2_values[1], "Test task 2")
        self.assertEqual(item2_values[2], "❗️ P2")
        
        # Updated comparison to check for list instead of tuple
        self.assertEqual(self.app.task_tree.item(items[1])['tags'], ['completed'])

if __name__ == '__main__':
    unittest.main()