import sys
import os
import unittest
import json
from unittest.mock import patch, MagicMock
import tkinter as tk
from tkinter import messagebox

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestTodoistStyleApp(unittest.TestCase):
    """Test cases for the TodoistStyleApp"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class"""
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
            cls.real_gui = True
        except tk.TclError:
            cls.root = MagicMock()
            cls.real_gui = False

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        if cls.real_gui:
            cls.root.destroy()
        if os.path.exists("todos.json"):
            os.remove("todos.json")

    def setUp(self):
        """Set up before each test"""
        if os.path.exists("todos.json"):
            os.remove("todos.json")
        
        from todo_app.app import TodoistStyleApp
        self.app = TodoistStyleApp(self.__class__.root)
        
        if not self.__class__.real_gui:
            # Set up mocks for non-GUI tests
            self.app.task_tree = MagicMock()
            self.app.task_tree.selection.return_value = ['item1']
            self.app.task_tree.index.return_value = 0
            self.app.task_tree.get_children.return_value = ['item1']

    def tearDown(self):
        """Clean up after each test"""
        if os.path.exists("todos.json"):
            os.remove("todos.json")

    def test_initial_state(self):
        """Test the app's initial state"""
        self.assertEqual(len(self.app.todos), 0)
        self.assertEqual(self.app.task_var.get(), "")
        self.assertEqual(self.app.priority_var.get(), "4")

    def test_add_todo(self):
        """Test adding a new task"""
        self.app.task_var.set("Test task")
        self.app.priority_var.set("2")
        self.app.add_todo()
        
        self.assertEqual(len(self.app.todos), 1)
        self.assertEqual(self.app.todos[0]["task"], "Test task")
        self.assertEqual(self.app.todos[0]["priority"], "2")
        self.assertFalse(self.app.todos[0]["completed"])
        self.assertEqual(self.app.task_var.get(), "")

    def test_add_empty_todo(self):
        """Test adding an empty task"""
        with patch.object(messagebox, 'showwarning') as mock_warning:
            self.app.task_var.set("")
            self.app.add_todo()
            mock_warning.assert_called_once_with("Warning", "Task cannot be empty!")
            self.assertEqual(len(self.app.todos), 0)

    def test_toggle_completion(self):
        """Test toggling task completion status"""
        test_todo = {"task": "Test", "priority": "1", "completed": False}
        self.app.todos.append(test_todo)
        
        if self.__class__.real_gui:
            self.app.refresh_list()
            item = self.app.task_tree.get_children()[0]
            self.app.task_tree.selection_set(item)
        else:
            # Reset mock for consistent testing
            self.app.task_tree.selection.return_value = ['item1']
            self.app.task_tree.index.return_value = 0

        # First toggle (False → True)
        self.app.toggle_completion()
        self.assertTrue(self.app.todos[0]["completed"])

        # Reset for second toggle
        if not self.__class__.real_gui:
            self.app.task_tree.selection.return_value = ['item1']
            self.app.task_tree.index.return_value = 0

        # Second toggle (True → False)
        self.app.toggle_completion()
        self.assertFalse(self.app.todos[0]["completed"])

    def test_delete_todo(self):
        """Test deleting a task"""
        test_todo = {"task": "Test", "priority": "1", "completed": False}
        self.app.todos.append(test_todo)
        
        if self.__class__.real_gui:
            self.app.refresh_list()
            item = self.app.task_tree.get_children()[0]
            self.app.task_tree.selection_set(item)
        
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.delete_todo()
            self.assertEqual(len(self.app.todos), 0)
            if self.__class__.real_gui:
                self.assertEqual(len(self.app.task_tree.get_children()), 0)

    def test_load_todos(self):
        """Test loading tasks from file"""
        with open("todos.json", "w") as f:
            json.dump([{"task": "Test", "priority": "1", "completed": False}], f)
        
        from todo_app.app import TodoistStyleApp
        new_app = TodoistStyleApp(self.__class__.root)
        self.assertEqual(len(new_app.todos), 1)
        self.assertEqual(new_app.todos[0]["task"], "Test")

    def test_save_todos(self):
        """Test saving tasks to file"""
        self.app.todos.append({"task": "Test", "priority": "1", "completed": False})
        self.app.save_todos()
        
        with open("todos.json", "r") as f:
            data = json.load(f)
            self.assertEqual(data[0]["task"], "Test")

    def test_refresh_list(self):
        """Test refreshing the task list display"""
        if not self.__class__.real_gui:
            self.skipTest("GUI not available for this test")
            
        self.app.todos.append({"task": "Test", "priority": "1", "completed": False})
        self.app.refresh_list()
        items = self.app.task_tree.get_children()
        self.assertEqual(len(items), 1)
        self.assertEqual(self.app.task_tree.item(items[0])['values'][1], "Test")

    def test_save_load_consistency(self):
        """Test that saving and loading maintains data"""
        self.app.todos.append({"task": "Test", "priority": "1", "completed": False})
        self.app.save_todos()
        
        from todo_app.app import TodoistStyleApp
        new_app = TodoistStyleApp(self.__class__.root)
        self.assertEqual(len(new_app.todos), 1)
        self.assertEqual(new_app.todos[0]["task"], "Test")

if __name__ == '__main__':
    unittest.main()