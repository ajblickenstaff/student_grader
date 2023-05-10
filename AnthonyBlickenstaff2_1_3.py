import csv
import tkinter as tk
from tkinter import messagebox
from typing import List, Union

class StudentGrades:
    def __init__(self, total_students: int, scores: List[int]):
        self.total_students = total_students
        self.scores = scores
        self.student_grades = self.get_grades()

    def get_grades(self) -> List[str]:
        grades = []
        best_score = max(self.scores)
        for score in self.scores:
            if score >= best_score - 10:
                grades.append("A")
            elif score >= best_score - 20:
                grades.append("B")
            elif score >= best_score - 30:
                grades.append("C")
            elif score >= best_score - 40:
                grades.append("D")
            else:
                grades.append("F")
        return grades

class StudentGradesGUI:
    def __init__(self, master):
        self.master = master
        master.title("Student Grades")

        self.total_students_label = tk.Label(master, text="Total number of students:")
        self.total_students_label.grid(row=0, column=0)
        self.total_students_entry = tk.Entry(master)
        self.total_students_entry.grid(row=0, column=1)
        self.total_students_entry.bind('<Return>', self.create_score_entries)

        self.calculate_button = tk.Button(master, text="Calculate Grades", command=self.calculate_grades)
        self.result_label = tk.Label(master, text="")

        # Initialize score entries and labels lists
        self.score_entries = []
        self.score_labels = []

    def create_score_entries(self, event):
        try:
            self.total_students = int(self.total_students_entry.get())

            # Add this condition to check if the total students entered is greater than 4
            if self.total_students > 4:
                messagebox.showerror("Error", "You can only select up to 4 students.")
                return

            # Remove existing score entries and labels
            for entry in self.score_entries:
                entry.destroy()
            for label in self.score_labels:
                label.destroy()

            self.score_entries = [tk.Entry(self.master) for _ in range(self.total_students)]
            self.score_labels = [tk.Label(self.master, text=f"Student #{i+1}") for i in range(self.total_students)]

            for i, (label, entry) in enumerate(zip(self.score_labels, self.score_entries)):
                label.grid(row=i+1, column=0)
                entry.grid(row=i+1, column=1)

            self.calculate_button.grid(row=self.total_students + 1, column=0, columnspan=2)
            self.result_label.grid(row=self.total_students + 2, column=0, columnspan=2)

            self.master.geometry("")
            self.master.update()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_grades(self):
        try:
            self.scores = [int(entry.get()) for entry in self.score_entries]
            student_grades = StudentGrades(self.total_students, self.scores)
            self.display_grades(student_grades.student_grades)
            self.write_grades_to_csv(student_grades.student_grades)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_grades(self, grades: List[str]):
        result = ""
        for i, grade in enumerate(grades):
            result += f"Student {i+1} score is {self.scores[i]} and grade is {grade}\n"
        self.result_label.config(text=result)

    def write_grades_to_csv(self, grades: List[str]):
        with open('student_grades.csv', 'w', newline='') as csvfile:
            fieldnames = ['Student', 'Score', 'Grade']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for i, grade in enumerate(grades):
                writer.writerow({'Student': f"Student {i+1}", 'Score': self.scores[i], 'Grade': grade})

if __name__ == "__main__":
    root = tk.Tk()
    gui = StudentGradesGUI(root)
    root.mainloop()
