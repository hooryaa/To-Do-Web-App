import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import json
import tkinter as tk
from unittest.mock import patch
from tkinter import messagebox
from tkinter import Tk
from todo_app.app import TodoistStyleApp

class TestTodoistStyleApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Tk()
        cls.root.withdraw()
    
    @classmethod
    def tearDownClass(cls):
        if os.path.exists("todos.json"):
            os.remove("todos.json")
        cls.root.destroy()
    
    def setUp(self):
        if os.path.exists("todos.json"):
            os.remove("todos.json")
        self.app = TodoistStyleApp(self.root)
    
    def tearDown(self):
        if os.path.exists("todos.json"):
            os.remove("todos.json")

    def test_initial_state(self):
        self.assertEqual(len(self.app.todos), 0)
        self.assertIsInstance(self.app.task_var, tk.StringVar)
        self.assertIsInstance(self.app.priority_var, tk.StringVar)

    def test_add_todo(self):
        self.app.task_var.set("Test task")
        self.app.priority_var.set("2")
        self.app.add_todo()
        
        self.assertEqual(len(self.app.todos), 1)
        self.assertEqual(self.app.todos[0]["task"], "Test task")
        self.assertEqual(self.app.todos[0]["priority"], "2")
        self.assertFalse(self.app.todos[0]["completed"])
        self.assertEqual(self.app.task_var.get(), "")

    def test_add_empty_todo(self):
        with patch.object(messagebox, 'showwarning') as mock_warning:
            self.app.task_var.set("")
            self.app.add_todo()
            mock_warning.assert_called_once_with("Warning", "Task cannot be empty!")
            self.assertEqual(len(self.app.todos), 0)

    def test_toggle_completion(self):
        test_todo = {"task": "Test", "priority": "1", "completed": False}
        self.app.todos.append(test_todo)
        self.app.refresh_list()
        
        item = self.app.task_tree.get_children()[0]
        self.app.task_tree.selection_set(item)
        self.app.toggle_completion()
        
        self.assertTrue(self.app.todos[0]["completed"])
        self.app.toggle_completion()
        self.assertFalse(self.app.todos[0]["completed"])

    def test_delete_todo(self):
        test_todo = {"task": "Test", "priority": "1", "completed": False}
        self.app.todos.append(test_todo)
        self.app.refresh_list()
        
        item = self.app.task_tree.get_children()[0]
        self.app.task_tree.selection_set(item)
        
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.delete_todo()
            self.assertEqual(len(self.app.todos), 0)
            self.assertEqual(len(self.app.task_tree.get_children()), 0)

    def test_load_todos(self):
        with open("todos.json", "w") as f:
            json.dump([{"task": "Test", "priority": "1", "completed": False}], f)
        
        new_app = TodoistStyleApp(self.root)
        self.assertEqual(len(new_app.todos), 1)
        self.assertEqual(new_app.todos[0]["task"], "Test")

    def test_save_todos(self):
        self.app.todos.append({"task": "Test", "priority": "1", "completed": False})
        self.app.save_todos()
        
        with open("todos.json", "r") as f:
            data = json.load(f)
            self.assertEqual(data[0]["task"], "Test")

    def test_refresh_list(self):
        self.app.todos.append({"task": "Test", "priority": "1", "completed": False})
        self.app.refresh_list()
        items = self.app.task_tree.get_children()
        self.assertEqual(len(items), 1)
        self.assertEqual(self.app.task_tree.item(items[0])['values'][1], "Test")

    def test_save_load_consistency(self):
        self.app.todos.append({"task": "Test", "priority": "1", "completed": False})
        self.app.save_todos()
        
        new_app = TodoistStyleApp(self.root)
        self.assertEqual(len(new_app.todos), 1)
        self.assertEqual(new_app.todos[0]["task"], "Test")

if __name__ == '__main__':
    unittest.main()