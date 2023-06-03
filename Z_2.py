import tkinter as tk
from tkinter import ttk

class PomodoroApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pomodoro App")
        self.geometry("400x400")

        # create the "To Do" and "Done" lists
        self.todo_list = []
        self.done_list = []

        # create the "To Do" and "Done" frames
        self.todo_frame = ttk.Frame(self, padding=(10, 10, 10, 0))
        self.todo_frame.grid(row=0, column=0, sticky="nsew")
        self.done_frame = ttk.Frame(self, padding=(10, 0, 10, 10))
        self.done_frame.grid(row=1, column=0, sticky="nsew")

        # create the "To Do" and "Done" labels
        self.todo_label = ttk.Label(self.todo_frame, text="To Do")
        self.todo_label.pack(side="top", anchor="w")
        self.done_label = ttk.Label(self.done_frame, text="Done")
        self.done_label.pack(side="top", anchor="w")

        # create the "To Do" and "Done" listboxes
        self.todo_listbox = tk.Listbox(self.todo_frame, height=10)
        self.todo_listbox.pack(side="left", fill="both", expand=True)
        self.done_listbox = tk.Listbox(self.done_frame, height=10)
        self.done_listbox.pack(side="left", fill="both", expand=True)

        # add some items to the "To Do" list
        self.add_todo_item("Task 1")
        self.add_todo_item("Task 2")
        self.add_todo_item("Task 3")

        # bind the drag and drop events for the listboxes
        self.todo_listbox.bind("<Button-1>", self.start_drag)
        self.todo_listbox.bind("<B1-Motion>", self.drag)
        self.done_listbox.bind("<Button-1>", self.start_drag)
        self.done_listbox.bind("<B1-Motion>", self.drag)
        self.todo_listbox.bind("<ButtonRelease-1>", self.drop)
        self.done_listbox.bind("<ButtonRelease-1>", self.drop)

        # create the Pomodoro timer label
        self.timer_label = ttk.Label(self, text="25:00", font=("Helvetica", 36))
        self.timer_label.grid(row=0, column=1, rowspan=2, padx=10)

        # create the Pomodoro timer buttons
        self.start_button = ttk.Button(self, text="Start", command=self.start_timer)
        self.start_button.grid(row=2, column=1, sticky="nsew", pady=10)
        self.pause_button = ttk.Button(self, text="Pause", command=self.pause_timer)
        self.pause_button.grid(row=3, column=1, sticky="nsew", pady=10)
        self.reset_button = ttk.Button(self, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=4, column=1, sticky="nsew", pady=10)

        # set the initial timer state
        self.timer_running = False
        self.time_remaining = 0
        self.timer_direction = 1

    def add_todo_item(self, item):
        self.todo_list.append(item)
        self.todo_listbox.insert("end", item)

    def add_done_item(self, item):
        self.done_list.append(item)
        self.done_listbox.insert
    self.done_listbox.insert("end", item)

def start_drag(self, event):
    widget = event.widget
    index = widget.nearest(event.y)
    if widget == self.todo_listbox:
        self.dragging_item = self.todo_listbox.get(index)
        self.source_list = self.todo_list
        self.dest_list = self.done_list
        self.source_widget = self.todo_listbox
        self.dest_widget = self.done_listbox
    elif widget == self.done_listbox:
        self.dragging_item = self.done_listbox.get(index)
        self.source_list = self.done_list
        self.dest_list = self.todo_list
        self.source_widget = self.done_listbox
        self.dest_widget = self.todo_listbox

def drag(self, event):
    try:
        widget = event.widget
        index = widget.nearest(event.y)
        item = widget.get(index)
        if widget == self.source_widget and item == self.dragging_item:
            self.source_widget.selection_clear(0, "end")
            self.source_widget.activate(index)
            self.source_widget.selection_set(index)
            self.source_widget.dragging = True
    except Exception as e:
        pass

def drop(self, event):
    try:
        widget = event.widget
        index = widget.nearest(event.y)
        if widget == self.dest_widget:
            self.dest_widget.selection_clear(0, "end")
            self.dest_widget.activate(index)
            self.dest_widget.selection_set(index)
            self.dest_list.insert(index, self.dragging_item)
            self.source_list.remove(self.dragging_item)
            self.source_widget.delete(self.source_widget.nearest(event.y))
            self.dest_widget.insert(index, self.dragging_item)
    except Exception as e:
        pass

def start_timer(self):
    if not self.timer_running:
        self.time_remaining = 25 * 60
        self.timer_running = True
        self.update_timer()

def pause_timer(self):
    self.timer_running = False

def reset_timer(self):
    self.timer_running = False
    self.timer_direction = 1
    self.time_remaining = 0
    self.update_timer()

def update_timer(self):
    if self.timer_running and self.time_remaining > 0:
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        self.timer_label.configure(text="{:02d}:{:02d}".format(minutes, seconds))
        self.time_remaining -= self.timer_direction
        self.after(1000, self.update_timer)
    elif self.timer_running and self.time_remaining == 0:
        self.timer_running = False
        self.timer_direction = -1
        self.time_remaining = 5 * 60
        self.update_timer()
    else:
        self.timer_label.configure(text="25:00")

if name == "main":
    app = PomodoroApp()
    app.mainloop()