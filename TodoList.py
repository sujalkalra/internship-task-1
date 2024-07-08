import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TASKS_FILE = 'tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('To-Do List')
        self.root.configure(bg='#8698da')
        self.tasks = load_tasks()
        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg='#8698da')
        self.frame.pack(pady=10)

        self.listbox = tk.Listbox(self.frame, width=100, height=10, bg='#FFFFFF', fg='#000000', selectbackground='#D3D3D3', selectforeground='#000000')
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.entry_frame = tk.Frame(self.root, bg='#8698da')
        self.entry_frame.pack(pady=10)

        self.entry = tk.Entry(self.entry_frame, width=40, bg='#FFFFFF', fg='#000000', font=('Helvetica', 16), bd=5)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5, ipadx=5, ipady=5)

        self.add_button = tk.Button(self.entry_frame, text='Add Task', command=self.add_task, bg='#4CAF50', fg='#FFFFFF', activebackground='#45A049', padx=15, pady=10, font=('Helvetica', 10, 'bold'))
        self.add_button.pack(side=tk.LEFT)

        self.button_frame = tk.Frame(self.root, bg='#8698da')
        self.button_frame.pack(pady=5)

        self.update_button = tk.Button(self.button_frame, text='Update Task', command=self.update_task, bg='#2196F3', fg='#FFFFFF', activebackground='#0B84E7', padx=15, pady=10, font=('Helvetica', 10, 'bold'))
        self.update_button.pack(side=tk.LEFT, padx=5)

        self.done_button = tk.Button(self.button_frame, text='Mark as Done', command=self.mark_done, bg='#FF9800', fg='#FFFFFF', activebackground='#E68A00', padx=15, pady=10, font=('Helvetica', 10, 'bold'))
        self.done_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.button_frame, text='Delete Task', command=self.delete_task, bg='#F44336', fg='#FFFFFF', activebackground='#D32F2F', padx=15, pady=10, font=('Helvetica', 10, 'bold'))
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for idx, task in enumerate(self.tasks, 1):  # Start enumeration from 1
            status = 'Done' if task['done'] else 'Pending'
            self.listbox.insert(tk.END, f'{idx}. {task["title"]} [{status}]')

    def add_task(self):
        title = self.entry.get()
        if title:
            self.tasks.append({'title': title, 'done': False})
            save_tasks(self.tasks)
            self.update_listbox()
            self.entry.delete(0, tk.END)

    def update_task(self):
        selected = self.listbox.curselection()
        if selected:
            task_id = selected[0]
            new_title = simpledialog.askstring("Update Task", "Enter new title:", initialvalue=self.tasks[task_id]['title'])
            if new_title:
                self.tasks[task_id]['title'] = new_title
                save_tasks(self.tasks)
                self.update_listbox()

    def mark_done(self):
        selected = self.listbox.curselection()
        if selected:
            task_id = selected[0]
            self.tasks[task_id]['done'] = True
            save_tasks(self.tasks)
            self.update_listbox()

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            task_id = selected[0]
            self.tasks.pop(task_id)
            save_tasks(self.tasks)
            self.update_listbox()

if __name__ == '__main__':
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
