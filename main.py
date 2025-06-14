#!/usr/bin/env python3
from todo_app.app import TodoistStyleApp
import tkinter as tk

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = TodoistStyleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()