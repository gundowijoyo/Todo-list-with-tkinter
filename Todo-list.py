import tkinter as tk
from tkinter import messagebox
import json

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.tasks = self.load_data()

        self.task_input = tk.Entry(root, font=('Helvetica', 14))
        self.task_input.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        self.add_button = tk.Button(root, text="Tambah", font=('Helvetica', 14), command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        self.task_frame = tk.Frame(root)
        self.task_frame.grid(row=1, column=0, columnspan=2)

        self.update_task_layout()

    def load_data(self):
        try:
            with open('data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open('data.json', 'w') as file:
            json.dump(self.tasks, file)

    def add_task(self):
        task_name = self.task_input.get().strip()
        if task_name:
            self.tasks.append({'name': task_name, 'completed': False})
            self.save_data()
            self.update_task_layout()
            self.task_input.delete(0, 'end')

    def remove_task(self, task_name):
        for task in self.tasks:
            if task['name'] == task_name:
                self.tasks.remove(task)
                break
        self.save_data()
        self.update_task_layout()

    def toggle_task_completion(self, task_name):
        for task in self.tasks:
            if task['name'] == task_name:
                task['completed'] = not task['completed']
                break
        self.save_data()
        self.update_task_layout()

    def update_task_layout(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()

        for task in self.tasks:
            task_label = tk.Label(self.task_frame, text=task['name'], font=('Helvetica', 14))
            task_label.grid(sticky="w")

            completion_status = "Selesai" if task['completed'] else "Belum Selesai"
            completion_color = "green" if task['completed'] else "red"
            completion_label = tk.Label(self.task_frame, text=completion_status, font=('Helvetica', 14), fg=completion_color)
            completion_label.grid(row=self.tasks.index(task), column=1, padx=10)

            remove_button = tk.Button(self.task_frame, text="Hapus", font=('Helvetica', 14), command=lambda t=task['name']: self.remove_task(t))
            remove_button.grid(row=self.tasks.index(task), column=2, padx=10)

            toggle_button = tk.Button(self.task_frame, text="Toggle", font=('Helvetica', 14), command=lambda t=task['name']: self.toggle_task_completion(t))
            toggle_button.grid(row=self.tasks.index(task), column=3, padx=10)

root = tk.Tk()
app = ToDoListApp(root)
root.mainloop()

