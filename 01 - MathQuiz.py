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
        self.displayMain()
        

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
            command=self.displayMain
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
                     
    def displayQuestion(self):
        num1 = self.randomInt()
        num2 = self.randomInt()
        operation = self.decideOperation()

        if operation == "+":
            self.correct = num1 + num2
        else:
            self.correct = num1 - num2

        self.question.config(
            text=f"{num1} {operation} {num2} = ?"
        )

        self.entry.delete(0, tk.END)
        self.entry.focus()

        self.lifelines = 1
        self.active = True
        self.startTimer()

    def isCorrect(self):
        if not self.active:
            return

        try:
            entry = int(self.entry.get())

        except ValueError:
            messagebox.showerror(
                " Nope!",
                "Thats Not A Valid Number!"
            )
            self.entry.delete(0, tk.END)
            self.entry.focus()
            return

        if entry == self.correct:
            self.active = False
            self.stopTimer()

            if self.lifelines == 1:
                self.score_tracker += 10
                points = 10
            else:
                self.score_tracker += 5
                points = 5

            self.feedback.config(
                text=f"+{points} points !",
                fg="green"
            )
            self.root.after(300, self.nextQuestion)

        else:
            if self.lifelines == 1:
                self.lifelines = 2

                messagebox.showwarning(
                    "Incorrect !",
                    "try againnn"
                )

                self.entry.delete(0, tk.END)
                self.entry.focus()

            else:
                self.active = False
                self.stopTimer()

                messagebox.showerror(
                    "Incorrect !",
                    f"le answer was{self.correct}."
                )

                self.root.after(300, self.nextQuestion)

    def displayResults(self):
        self.stopTimer()
        self.active = False
        self.game.pack_forget()

        if self.score_tracker > 90:
            grade = "A+"
        elif self.score_tracker >= 80:
            grade = "A"
        elif self.score_tracker >= 70:
            grade = "B"
        elif self.score_tracker >= 60:
            grade = "C"
        elif self.score_tracker >= 50:
            grade = "D"
        else:
            grade = "F"

        self.result.config(
            text=f"YOU'RE DONE!\n\n"
                 f"Final Score: {self.score_tracker}/100\n\n"
                 f"Grade: {grade}"
        )

        self.end.pack(fill="both", expand=True)

    def startQuiz(self, level):
        self.minimum, self.maximum = self.difficulty[level]

        self.score_tracker = 0
        self.current = 0

        self.main.pack_forget()
        self.game.pack(fill="both", expand=True)

        self.nextQuestion()

    def nextQuestion(self):
        self.stopTimer()

        if self.current == 10:
            self.displayResults()
        else:
            self.current += 1

            self.counter.config(
                text=f"Question {self.current} of 10"
            )

            self.displayQuestion()

    def startTimer(self):
        self.time = 10
        self.updateTimer()

    def updateTimer(self):
        if not self.active:
            return

        self.bar["value"] = self.time * 10

        if self.time <= 3:
            colour = "Red"
        elif self.time <= 6:
            colour = "Orange"
        else:
            colour = "Green"

        self.bar.configure(
            style=f"{colour}.Horizontal.TProgressbar"
        )

        if self.time == 0:
            self.active = False
            self.duration = None

            messagebox.showwarning(
                "Time's Up",
                f"You're out of time !\n"
                f"The answer was {self.correct}."
            )

            self.nextQuestion()

        else:
            self.time -= 1
            self.duration = self.root.after(
                1000, self.updateTimer
            )

root = tk.Tk()
app = MathQuiz(root)
root.mainloop()
