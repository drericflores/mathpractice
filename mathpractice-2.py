"""
Math Practice Application
Version: 2.1
Developed by Dr. Eric O. Flores
Date of Creation: December 14, 2024
Revision Date:  July 20, 2025
Developed for learning purposes – converted from C++ to Python.
GPL3v
"""

import tkinter as tk
import random
from tkinter import messagebox
import time


class MathPracticeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Practice")
        self.root.geometry("750x400")
        self.score = 0
        self.total_questions = 0
        self.start_time = None
        self.time_limit = 10  # seconds for timed mode
        self.current_mode = "Mixed"  # Default mode
        self.timer_active = False  # Tracks if timer is active

        # Game Mode
        self.timed_mode = tk.BooleanVar(value=False)

        # Components
        self.create_widgets()
        self.generate_problem()

    def create_widgets(self):
        # Problem display
        self.problem_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.problem_label.pack(pady=20)

        # Answer input
        self.answer_entry = tk.Entry(self.root, font=("Arial", 14))
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind("<Return>", self.check_answer)  # Handle Enter key
        self.answer_entry.bind("<KP_Enter>", self.check_answer)  # Handle keypad Enter key

        # Feedback display
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 14), fg="green")
        self.feedback_label.pack(pady=10)

        # Score display
        self.score_label = tk.Label(self.root, text="Score: 0%", font=("Arial", 12))
        self.score_label.pack(pady=10)

        # Timed Mode Checkbox
        self.timed_checkbox = tk.Checkbutton(
            self.root, text="Timed Mode", variable=self.timed_mode, command=self.toggle_timed_mode
        )
        self.timed_checkbox.pack(pady=5)

        # Time Limit Slider
        self.time_limit_slider = tk.Scale(
            self.root, from_=5, to=30, orient=tk.HORIZONTAL, label="Time Limit (seconds)"
        )
        self.time_limit_slider.set(self.time_limit)
        self.time_limit_slider.pack(pady=5)

        # Mode Selection Buttons
        self.create_mode_buttons()

        # Quit Button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit, bg="red", fg="white")
        self.quit_button.pack(pady=5)

    def create_mode_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        addition_button = tk.Button(frame, text="Addition Only", command=lambda: self.set_mode("Addition"))
        addition_button.grid(row=0, column=0, padx=5)

        subtraction_button = tk.Button(frame, text="Subtraction Only", command=lambda: self.set_mode("Subtraction"))
        subtraction_button.grid(row=0, column=1, padx=5)

        multiplication_button = tk.Button(frame, text="Multiplication Only", command=lambda: self.set_mode("Multiplication"))
        multiplication_button.grid(row=0, column=2, padx=5)

        division_button = tk.Button(frame, text="Division Only", command=lambda: self.set_mode("Division"))
        division_button.grid(row=0, column=3, padx=5)

        mixed_button = tk.Button(frame, text="Mixed Mode", command=lambda: self.set_mode("Mixed"))
        mixed_button.grid(row=0, column=4, padx=5)

    def set_mode(self, mode):
        self.current_mode = mode
        messagebox.showinfo("Mode Changed", f"Mode set to {mode}!")
        self.generate_problem()

    def generate_problem(self):
        if self.current_mode == "Mixed":
            operators = ["x", "+", "-", "/"]
        elif self.current_mode == "Addition":
            operators = ["+"]
        elif self.current_mode == "Subtraction":
            operators = ["-"]
        elif self.current_mode == "Multiplication":
            operators = ["x"]
        elif self.current_mode == "Division":
            operators = ["/"]

        self.num1 = random.randint(1, 12)
        self.num2 = random.randint(1, 12)
        self.operator = random.choice(operators)

        # Calculate the correct answer
        if self.operator == "x":
            self.correct_answer = self.num1 * self.num2
        elif self.operator == "+":
            self.correct_answer = self.num1 + self.num2
        elif self.operator == "-":
            self.correct_answer = self.num1 - self.num2
        elif self.operator == "/":
            # Avoid division by zero and ensure integer division
            self.num1 = self.num1 * self.num2
            self.correct_answer = self.num1 // self.num2

        # Show the problem
        self.problem_label.config(text=f"{self.num1} {self.operator} {self.num2}")
        self.answer_entry.delete(0, tk.END)
        self.feedback_label.config(text="")
        self.timer_active = False

        # Start timer if in timed mode
        if self.timed_mode.get():
            self.start_time = time.time()
            self.timer_active = True
            self.check_timer()

    def check_timer(self):
        """Check if the user exceeded the time limit in timed mode."""
        if not self.timer_active:
            return  # Exit if timer is not active

        if self.timed_mode.get() and self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > self.time_limit:
                self.timer_active = False  # Stop the timer
                self.feedback_label.config(
                    text=f"You failed to answer on a timely manner! - The Result is {self.correct_answer}",
                    fg="red",
                )
                self.total_questions += 1
                self.update_score()
                self.root.after(3000, self.generate_problem)  # Wait 3 seconds before next problem
                return

        # Check the timer again after 100ms
        self.root.after(100, self.check_timer)

    def check_answer(self, event=None):
        # Stop timer if active
        self.timer_active = False

        # Check elapsed time for timed mode
        if self.timed_mode.get() and self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            if elapsed_time > self.time_limit:
                return  # If time already exceeded, skip processing

        try:
            user_answer = int(self.answer_entry.get())
        except ValueError:
            self.feedback_label.config(text="Invalid input!", fg="red")
            return

        # Check if the answer is correct
        if user_answer == self.correct_answer:
            self.feedback_label.config(text="Correct! Great job!", fg="green")
            self.score += 1
        else:
            self.feedback_label.config(text=f"Incorrect! The answer was {self.correct_answer}", fg="red")

        self.total_questions += 1
        self.update_score()

        # Wait 3 seconds before generating the next problem
        self.root.after(3000, self.generate_problem)

    def update_score(self):
        if self.total_questions > 0:
            percentage = (self.score / self.total_questions) * 100
            self.score_label.config(text=f"Score: {percentage:.1f}%")

    def toggle_timed_mode(self):
        self.time_limit = self.time_limit_slider.get()
        if self.timed_mode.get():
            messagebox.showinfo("Timed Mode", f"Timed mode is ON. Answer within {self.time_limit} seconds!")
        else:
            messagebox.showinfo("Timed Mode", "Timed mode is OFF.")
        self.start_time = None


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MathPracticeApp(root)
    root.mainloop()

