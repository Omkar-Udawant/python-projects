import tkinter as tk
from tkinter import ttk

class QuizUI:
    def __init__(self, quiz):
        self.quiz = quiz
        self.root = tk.Tk()
        self.root.title("Quizzler")
        self.root.geometry("420x520")
        self.root.configure(bg="#1e1e2f")
        self.root.resizable(False, False)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 12), padding=10)
        style.configure("Score.TLabel", font=("Segoe UI", 12), background="#1e1e2f", foreground="white")
        style.configure("Q.TLabel", font=("Segoe UI", 16), wraplength=360, background="white")

        self.score = ttk.Label(self.root, text="Score: 0", style="Score.TLabel")
        self.score.pack(pady=15)

        self.card = tk.Frame(self.root, bg="white", bd=0)
        self.card.pack(padx=20, pady=20, fill="both", expand=True)

        self.question = ttk.Label(self.card, text="", style="Q.TLabel", anchor="center", justify="center")
        self.question.pack(expand=True, padx=20, pady=20)

        self.buttons = tk.Frame(self.root, bg="#1e1e2f")
        self.buttons.pack(pady=20)

        ttk.Button(self.buttons, text="True", width=12, command=lambda: self.answer("True")).grid(row=0, column=0, padx=10)
        ttk.Button(self.buttons, text="False", width=12, command=lambda: self.answer("False")).grid(row=0, column=1, padx=10)

        self.load_question()
        self.root.mainloop()

    def load_question(self):
        self.card.configure(bg="white")
        self.score.config(text=f"Score: {self.quiz.score}")
        if self.quiz.has_next():
            self.question.config(text=self.quiz.next_question())
        else:
            self.question.config(text="Quiz Completed 🎉")

    def answer(self, choice):
        correct = self.quiz.check(choice)
        self.card.configure(bg="#2ecc71" if correct else "#e74c3c")
        self.root.after(900, self.load_question)
