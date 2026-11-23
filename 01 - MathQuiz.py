import tkinter as tk
from tkinter import ttk, messagebox
import random

class MathQuiz:

    def __init__(self, root):
        self.root = root
        self.root.title("Quick Maffs")
        self.root.geometry("500x500")
        self.root.configure(bg="#121F16")
        self.root.resizable(False, False)

        self.score_tracker = 0
        self.current = 0
        self.active = False
        self.lifelines = 1
        self.duration = 10
        self.timer = None

        self.difficulty = {
            "Easy": (1, 9),
            "Medium": (10, 99),
            "Hard": (1000, 9999)
        }

        self.createDesign()
        self.displayMenu()
        

    def createDesign(self):
        tk.Label(
            self.root,
            text="placeholder",
            font= ("Helvetica", 10, "bold"),
            bg="#121F16",
            fg= "white"
        ).place(x=10, y=10)

        self.main = tk.Frame(self.root, bg="#121F16")
        self.game = tk.Frame(self.root, bg="#121F16")
        self.end = tk.Frame(self.root, bg="#121F16")

        self.counter = tk.Label(
            self.game,
            font=("Helvetica", 14, "bold"),
            bg="#121F16"
        )
        self.counter.pack(pady=10)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Green.Horizontal.TProgressbar",
            background="#27AE60",
            thickness=20
        )

        style.configure(
            "Orange.Horizontal.TProgressbar",
            background="#27AE60",
            thickness=20
        )

        style.configure(
            "Red.Horizontal.TProgressbar",
            background="#27AE60",
            thickness=20
        )

        self.bar = ttk.Progressbar(
            self.game,
            length= 400,
            maximum= 100,
            style="Green.Horizontal.TProgressbar"
        )
        self.bar.pack(pady=15)

        self.question = tk.Label(
            self.game,
            font=("Helvetica", 24, "bold"),
        )
        self.question.pack(pady=25)

        self.entry = tk.Entry(
            self.game,
            font=("Helvetica", 24),
            justify="center",
            width= 15
        )
        self.entry.pack(pady=20)
        self.entry.bind("<Return>", lambda event: self.isCorrect())

        self.feedback = tk.Label(
            self.game,
            font=("Arial", 12),
            bg="#EAF2F8"
        )
        self.feedback.pack(pady=15)

        tk.Button(
            self.game,
            text="Submit Answer",
            font=("Arial", 12, "bold"),
            width=18,
            bg="#3498DB",
            fg="white",
            command=self.isCorrect
        ).pack(pady=10)

        self.result = tk.Label(
            self.end,
            font=("Arial", 20, "bold"),
            bg="#EAF2F8",
            fg="#154360"
        )
        self.result.pack(pady=40)

        tk.Button(
            self.end,
            text="Play Again",
            width=18,
            command=self.displayMenu
        ).pack(pady=10)

        tk.Button(
            self.end,
            text="Exit",
            width=18,
            command=self.root.destroy
        ).pack(pady=10)

    def displayMain(self):
        self.stopTimer()
        self.active = False

        self.game.pack_forget()
        self.end.pack_forget()
        self.main.pack(fill="both", expand=True)

        for widget in self.main.winfo_children():
            widget.destroy()

        tk.Label(
            self.main,
            text="SELECT DIFFICULTY LEVEL",
            font=("Arial", 16, "bold"),
            bg="#EAF2F8"
        ).pack(pady=20)

        number = 1

        for level in self.difficulty:
            tk.Button(
                self.main,
                text=f"{number}. {level}",
                width=20,
                font=("Arial", 12),
                command=lambda l=level: self.startQuiz(l)
            ).pack(pady=8)

            number += 1  

    def randomInt(self):
        return random.randint(self.minimum, self.maximum) 

    def decideOperation(self):
        return random.choice(["+", "-"])                 

root = tk.Tk()
app = MathQuiz(root)
root.mainloop()
