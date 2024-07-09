import tkinter as tk
from tkinter import messagebox, simpledialog, LabelFrame
import json
import os

def validate_name(name):
    if not name.isalpha():
        messagebox.showerror("Invalid Name", "Name must contain only alphabetic characters.")
        return False
    if not name:
        messagebox.showerror("Invalid Name", "Name cannot be empty.")
        return False
    return True

def validate_category(category):
    if category.lower() not in ["metals", "gases", "liquids"]:
        messagebox.showerror("Invalid Category", "Please choose a valid category: metals, gases, or liquids.")
        return False
    return True

def validate_answer(answer):
    if answer.lower() not in ["yes", "no"]:
        messagebox.showerror("Invalid Answer", "Please answer with 'yes' or 'no'.")
        return False
    return True
def ask_chemistry_questions(category, frame):
    questions = {
        "metals": [
            "Is gold a metal and states as 'Au' in IUPAC naming? (yes/no)",
            "Is Argon a metal? (yes/no)",
            "Is mercury a metal? (yes/no)"
        ],
        "gases": [
            "Is oxygen a gas? (yes/no)",
            "Strontium gives an Orange color in the flame test. Is it a gas? (yes/no)",
            "Carbon monoxide is toxic and binds with blood irreversibly. Is carbon monoxide a gas? (yes/no)"
        ],
        "liquids": [
            "Water is known as Oxidane in IUPAC naming. Is water a liquid at RT? (yes/no)",
            "Is Sodium a liquid? (yes/no)",
            "Mercury shines at RT. Is mercury a liquid? (yes/no)"
        ]
    }
    correct_answers = ['yes', 'no', 'yes']
    score = 0
    answers = []

    for i, question in enumerate(questions[category]):
        while True:
            answer = simpledialog.askstring("Question", f"Question {i+1}: {question}", parent=frame)
            if validate_answer(answer):
                break
        answers.append(answer.lower())
        if answer.lower() == correct_answers[i]:
            messagebox.showinfo("Correct!", "That's the right answer!", parent=frame)
            score += 1
        else:
            messagebox.showerror("Wrong!", f"The correct answer is '{correct_answers[i]}'.", parent=frame)
    return score, answers
def draw_chart(scores, names):
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.bar(names, scores, color='green')
        plt.xlabel("Participant Names")
        plt.ylabel("Scores")
        plt.title("Chemistry Quiz Results")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
    except ImportError:
        messagebox.showerror("Error", "matplotlib is not installed. Please install it to view the chart.")

def create_frame(scores, names):
    draw_chart(scores, names)

if __name__ == "__main__":
    app_window = tk.Tk()
    app_window.title("Chemistry Quiz")

    if os.path.exists('quiz_results.json'):
        with open('quiz_results.json', 'r') as json_file:
            participants = json.load(json_file)
            # Ensure participants is a list
            if not isinstance(participants, list):
                participants = []
    else:
        participants = []

    # Main quiz loop
    while True:
        # Ask for user's name and validate it
        while True:
            user_name = simpledialog.askstring("Name", "Please enter your name:", parent=app_window)
            if validate_name(user_name):
                break

        # Ask for category and validate it
        while True:
            category = simpledialog.askstring("Category", "Choose a category: metals, gases, or liquids", parent=app_window)
            if validate_category(category):
                break
        score, user_answers = ask_chemistry_questions(category, app_window)

        participants.append({
            "name": user_name,
            "category": category,
            "score": score,
            "answers": user_answers
        })

        # Ask if another participant wants to take the quiz
        another_participant = messagebox.askyesno("Another Participant", "Do you want another participant to take the quiz?")
        if not another_participant:
            break

    participant_names = [participant["name"] for participant in participants]
    participant_scores = [participant["score"] for participant in participants]
    create_frame(participant_scores, participant_names)
    with open('quiz_results.json', 'w') as json_file:
        json.dump(participants, json_file, indent=4)

    app_window.mainloop()
