import math
import tkinter as tk


class Timer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)


        self.master = master
        self.players = []
        self.pairings = []
        self.round = 1
        self.round_results = []
        self.pack()
        # Constants
        self.master = master
        self.PINK = "#e2979c"
        self.RED = "#e7305b"
        self.GREEN = "#9bdeac"
        self.YELLOW = "#f7f5dd"
        self.FONT_NAME = "Courier"
        self.reps = 0
        self.timer = None
        self.create_widgets()
    #     self.master.geometry('800x160')
        self.master.title("BATTLE TIMER")
        self.master.minsize(width=300, height=400)
        self.master.config(padx=100, pady=50, bg=self.YELLOW)




    def create_widgets(self):
        #
        #     self.label_timer = tk.Label(text="Timer", fg=self.GREEN, bg=self.YELLOW, font=(self.FONT_NAME, 40))
        #     self.label_timer.grid(column=1, row=0)
        #
        #     self.canvas = tk.Canvas(width=210, height=224, bg=self.YELLOW, highlightthickness=0)
        #     self.tomato_ing = tk.PhotoImage(file="tomato.png")
        #     self.canvas.create_image(105, 112, image=self.tomato_ing)
        #     self.timer_text = self.canvas.create_text(103, 120, text="00:00", fill="white", font=(self.FONT_NAME, 35, "bold"))
        #     self.canvas.grid(column=1, row=1)
        #
        #     self.start_button = tk.Button(text="Start", fg=self.GREEN, bg=self.YELLOW, command=self.start_timer)
        #     self.start_button.grid(column=0, row=3)
        #
        #     self.reset_button = tk.Button(text="Reset", command=self.reset_timer)
        #     self.reset_button.grid(column=2, row=3)
        #
        #     self.check_marks = tk.Label(fg=self.GREEN)
        #     self.check_marks.grid(column=1, row=4)
        # Quit button
        self.quit_button = tk.Button(self, text="Quit", fg="red", command=self.master.destroy, width=40)
        self.quit_button.pack(side="bottom")
        # # Constants for the timer
        # self.WORK_MIN = work_min
        # self.SHORT_BREAK_MIN = short_break_min
        # self.LONG_BREAK_MIN = long_break_min

    # def reset_timer(self):
    #     self.window.after_cancel(self.timer)
    #     self.label_timer.config(text="Timer", fg=self.GREEN)
    #     self.canvas.itemconfig(self.timer_text, text="00:00")
    #     self.check_marks.config(text="")
    #     self.reps = 0
    #
    # def start_timer(self):
    #     self.reps += 1
    #     work_sec = self.WORK_MIN * 60
    #     short_break_sec = self.SHORT_BREAK_MIN * 60
    #     long_break_sec = self.LONG_BREAK_MIN * 60
    #
    #     if self.reps % 8 == 0:
    #         self.count_down(work_sec)
    #         self.label_timer.config(text="STOP", fg=self.RED)
    #     elif self.reps % 2 == 0:
    #         self.count_down(short_break_sec)
    #         self.label_timer.config(text="Break", fg=self.PINK)
    #     else:
    #         self.count_down(long_break_sec)
    #         self.label_timer.config(text="Work", fg=self.GREEN)
    #
    # def count_down(self, count):
    #     count_min = math.floor(count / 60)
    #     count_sec = count % 60
    #     if count_sec == 0:
    #         count_sec = "00"
    #     elif count_sec < 10:
    #         count_sec = f"0{count_sec}"
    #
    #     self.canvas.itemconfig(self.timer_text, text=f"{count_min}:{count_sec}")
    #     if count > 0:
    #         self.timer = self.window.after(1000, self.count_down, count - 1)
    #     else:
    #         self.start_timer()
    #         marks = ""
    #         work_sessions = math.floor(self.reps / 2)
    #         for _ in range(work_sessions):
    #             marks += "✓"
    #         self.check_marks.config(text=marks)
    #
    # def reset_timer(self):
    #     self.window.after_cancel(self.timer)
    #     self.label_timer.config(text="Timer", fg=self.GREEN)
    #     self.canvas.itemconfig(self.timer_text, text=f"00:00")
    #     self.check_marks.config(text="")
    #     self.reps = 0




root = tk.Tk()
app = Timer(master=root)
app.mainloop()


















# from tkinter import *
# import math
#
#
#
# # ---------------------------- CONSTANTS ------------------------------- #
# PINK = "#e2979c"
# RED = "#e7305b"
# GREEN = "#9bdeac"
# YELLOW = "#f7f5dd"
# FONT_NAME = "Courier"
# WORK_MIN = 1 #25
# SHORT_BREAK_MIN = 1#5
# LONG_BREAK_MIN = 1#20
# reps = 0
# timer = None
#
#
# # ---------------------------- TIMER RESET ------------------------------- #
#
#
# def reset_timer():
#     window.after_cancel(timer)
#     label_timer.config(text="Timer", fg=GREEN)
#     canvas.itemconfig(timer_text, text=f"00:00")
#     check_marks.config(text="")
#     global reps
#     reps = 0
#
#
# # ---------------------------- TIMER MECHANISM ------------------------------- #
#
#
# def start_timer():
#     global reps
#     reps += 1
#     work_sec = WORK_MIN * 60
#     short_break_sec = SHORT_BREAK_MIN * 60
#     long_break_sec = LONG_BREAK_MIN * 60
#     count_down(5 * 60)
#
#     if reps % 8 == 0:
#         count_down(work_sec)
#         label_timer.config(text="STOP", fg=RED)
#     elif reps % 2 == 0:
#         count_down(short_break_sec)
#         label_timer.config(text="Break", fg=PINK)
#     else:
#         count_down(long_break_sec)
#         label_timer.config(text="Work", fg=GREEN)
#
#
# # ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
#
#
# def count_down(count):
#
#
#     count_min = math.floor(count / 60)
#     count_sec = count % 60
#     if count_sec == 0:
#         count_sec = "00"
#     elif count_sec < 10:
#         count_sec = f"0{count_sec}"
#
#     canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
#     if count > 0:
#         global timer
#         timer = window.after(1000, count_down, count - 1)
#     else:
#         start_timer()
#         marks = ""
#         work_sessions = math.floor(reps/2)
#         for _ in range(work_sessions):
#             marks += "✓"
#         check_marks.config(text=marks)
# # ---------------------------- UI SETUP ------------------------------- #
#
# window = Tk()
# window.title("BATTLE")
# window.minsize(width=300, height=400)
# window.config(padx=100, pady=50, bg=YELLOW)
#
#
# label_timer = Label(text="BATTLE", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40))
# label_timer.grid(column=1, row=0)
#
# canvas = Canvas(width=210, height=224, bg=YELLOW, highlightthickness=0)
# BG_ing = PhotoImage(file="BG.png")
# canvas.create_image(105, 112, image=BG_ing)
# timer_text = canvas.create_text(103, 120, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
# canvas.grid(column=1, row=1)
#
# start_button = Button(text="start", fg=GREEN, bg=YELLOW, command=start_timer)
# start_button.grid(column=0, row=3)
#
# reset_button = Button(text="Reset", command=reset_timer)
# reset_button.grid(column=2, row=3)
#
# check_marks = Label(fg=GREEN)
# check_marks.grid(column=1, row=4)
#
#
# window.mainloop()