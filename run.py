from todo_app.app import TodoistStyleApp
import tkinter as tk

def main():
    root = tk.Tk()
    app = TodoistStyleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()