import tkinter as tk
from tkinter import messagebox, simpledialog, LabelFrame
import json

# Validation Functions
# --------------------

# Validate the name input
def validate_name(name):
    if not name.isalpha():
        messagebox.showerror("Invalid Name", "Name must contain only alphabetic characters.")
        return False
    if not name:
        messagebox.showerror("Invalid Name", "Name cannot be empty.")
        return False
    return True

# Validate the category input
def validate_category(category):
    if category.lower() not in ["metals", "gases", "liquids"]:
        messagebox.showerror("Invalid Category", "Please choose a valid category: metals, gases, or liquids.")
        return False
    return True

# Validate the answer input
def validate_answer(answer):
    if answer.lower() not in ["yes", "no"]:
        messagebox.showerror("Invalid Answer", "Please answer with 'yes' or 'no'.")
        return False
    return True

# Quiz Functions
# --------------

# Ask chemistry questions based on the chosen category
def ask_chemistry_questions(category, frame):
    questions = {
        "metals": [
            "Is gold a metal? (yes/no)",
            "Is iron a metal? (yes/no)",
            "Is mercury a metal? (yes/no)"
        ],
        "gases": [
            "Is oxygen a gas? (yes/no)",
            "Is nitrogen a gas? (yes/no)",
            "Is carbon dioxide a gas? (yes/no)"
        ],
        "liquids": [
            "Is water a liquid? (yes/no)",
            "Is ethanol a liquid? (yes/no)",
            "Is mercury a liquid? (yes/no)"
        ]
    }
    correct_answers = ['yes', 'yes', 'yes']
    score = 0

    for i, question in enumerate(questions[category]):
        while True:
            answer = simpledialog.askstring("Question", f"Question {i+1}: {question}", parent=frame)
            if validate_answer(answer):
                break
        if answer.lower() == correct_answers[i]:
            messagebox.showinfo("Correct!", "That's the right answer!", parent=frame)
            score += 1
        else:
            messagebox.showerror("Wrong!", f"The correct answer is '{correct_answers[i]}'.", parent=frame)
    return score

# Results Display Functions
# -------------------------

# Function to draw the bar chart
def draw_chart(canvas, scores, names):
    # Draw the bar chart with proper labels
    bar_width = 50
    spacing = 20  # Increased spacing for gap before the first bar
    max_score = max(scores) if scores else 0  # Ensure there's a score to avoid division by zero
    y_scale_interval = max(max_score // 10, 1)  # Avoid zero as interval

    # Starting x position for the first bar
    start_x = 70

    for i, score in enumerate(scores):
        canvas.create_rectangle(start_x + i * (bar_width + spacing), 400, start_x + (i + 1) * (bar_width + spacing) - spacing,
                                400 - (score * (400 / (max_score + 1))), fill="skyblue")
        canvas.create_text(start_x + i * (bar_width + spacing) + (bar_width / 2), 410, text=names[i], anchor=tk.N)

    # Add scale markings to the y-axis
    for i in range(0, max_score + 1, y_scale_interval):
        canvas.create_line(start_x - 20, 400 - (i * (400 / (max_score + 1))), start_x - 10, 400 - (i * (400 / (max_score + 1))), fill="black")
        canvas.create_text(start_x - 40, 400 - (i * (400 / (max_score + 1))), text=str(i), anchor=tk.E)
