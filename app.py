import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import json

# Data: States and Capitals (Expanding the question bank with more categories)
question_bank = {
    'State Capitals': {
        'Andhra Pradesh': 'Amaravati',
        'Arunachal Pradesh': 'Itanagar',
        'Assam': 'Dispur',
        'Bihar': 'Patna',
        'Chhattisgarh': 'Raipur',
        'Goa': 'Panaji',
        'Gujarat': 'Gandhinagar',
        'Haryana': 'Chandigarh',
        'Himachal Pradesh': 'Shimla',
        'Jharkhand': 'Ranchi',
        'Karnataka': 'Bengaluru',
        'Kerala': 'Thiruvananthapuram',
        'Madhya Pradesh': 'Bhopal',
        'Maharashtra': 'Mumbai',
        'Manipur': 'Imphal',
        'Meghalaya': 'Shillong',
        'Mizoram': 'Aizawl',
        'Nagaland': 'Kohima',
        'Odisha': 'Bhubaneswar',
        'Punjab': 'Chandigarh',
        'Rajasthan': 'Jaipur',
        'Sikkim': 'Gangtok',
        'Tamil Nadu': 'Chennai',
        'Telangana': 'Hyderabad',
        'Tripura': 'Agartala',
        'Uttar Pradesh': 'Lucknow',
        'Uttarakhand': 'Dehradun',
        'West Bengal': 'Kolkata'
    },
    'Historical Events': {
        'Independence Day': '1947',
        'Republic Day': '1950',
        'Quit India Movement': '1942',
        'Jallianwala Bagh Massacre': '1919',
        'First War of Independence': '1857'
    },
    'Famous Personalities': {
        'Mahatma Gandhi': 'Father of the Nation',
        'Jawaharlal Nehru': 'First Prime Minister of India',
        'Subhash Chandra Bose': 'Founder of INA',
        'Sardar Vallabhbhai Patel': 'Iron Man of India',
        'B. R. Ambedkar': 'Father of the Indian Constitution'
    }
}

# Function to load the leaderboard from a file
def load_leaderboard():
    try:
        with open('leaderboard.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Function to save the leaderboard to a file
def save_leaderboard(leaderboard):
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f)

# Function to add a new score to the leaderboard
def add_to_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]
    save_leaderboard(leaderboard)

# Function to display the leaderboard
def show_leaderboard():
    leaderboard = load_leaderboard()
    leaderboard_text = "\n".join([f"{idx + 1}. {entry['name']}: {entry['score']}" for idx, entry in enumerate(leaderboard)])
    messagebox.showinfo("Leaderboard", leaderboard_text if leaderboard_text else "No scores yet!")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("State Capitals Quiz")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")
        self.score = 0
        self.question_index = 0
        self.selected_questions = []
        self.correct_answers = 0
        self.wrong_answers = 0
        self.time_limit = 30  # Time limit for each question (in seconds)
        self.timer_active = False
        self.hints_used = 0
        self.difficulty = "Easy"
        self.category = "State Capitals"

        # User details
        self.user_name = tk.StringVar()
        self.user_class = tk.StringVar()

        # Initialize UI elements
        self.initialize_ui()

    def initialize_ui(self):
        self.label_name = tk.Label(self.root, text="Enter your name:", font=("Helvetica", 14), bg="#f0f0f0")
        self.label_name.pack(pady=10)
        self.entry_name = tk.Entry(self.root, textvariable=self.user_name, font=("Helvetica", 14), bd=3, relief="sunken")
        self.entry_name.pack(pady=10)

        self.label_class = tk.Label(self.root, text="Enter your class:", font=("Helvetica", 14), bg="#f0f0f0")
        self.label_class.pack(pady=10)
        self.entry_class = tk.Entry(self.root, textvariable=self.user_class, font=("Helvetica", 14), bd=3, relief="sunken")
        self.entry_class.pack(pady=10)

        # Number of questions
        self.num_questions = tk.IntVar()
        self.label_num_questions = tk.Label(self.root, text="Enter the number of questions for the quiz:", font=("Helvetica", 14), bg="#f0f0f0")
        self.label_num_questions.pack(pady=10)
        self.entry_num_questions = tk.Entry(self.root, textvariable=self.num_questions, font=("Helvetica", 14), bd=3, relief="sunken")
        self.entry_num_questions.pack(pady=10)

        # Category selection
        self.label_category = tk.Label(self.root, text="Select Quiz Category:", font=("Helvetica", 14), bg="#f0f0f0")
        self.label_category.pack(pady=10)
        self.category_var = tk.StringVar(value="State Capitals")
        self.category_menu = tk.OptionMenu(self.root, self.category_var, *question_bank.keys())
        self.category_menu.config(font=("Helvetica", 12))
        self.category_menu.pack(pady=10)

        # Difficulty selection
        self.label_difficulty = tk.Label(self.root, text="Select Difficulty Level:", font=("Helvetica", 14), bg="#f0f0f0")
        self.label_difficulty.pack(pady=10)
        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_menu = tk.OptionMenu(self.root, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.config(font=("Helvetica", 12))
        self.difficulty_menu.pack(pady=10)

        # Start Quiz button
        self.start_button = tk.Button(self.root, text="Start Quiz", command=self.start_quiz, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", cursor="hand2")
        self.start_button.pack(pady=10)

        # Leaderboard button
        self.leaderboard_button = tk.Button(self.root, text="Leaderboard", command=show_leaderboard, font=("Helvetica", 12), bg="#FF5722", fg="white", cursor="hand2")
        self.leaderboard_button.pack(pady=10)

    def start_quiz(self):
        num_questions = self.num_questions.get()
        user_name = self.user_name.get().strip()
        user_class = self.user_class.get().strip()

        if not user_name or not user_class:
            messagebox.showerror("Error", "Please enter your name and class.")
            return

        if num_questions <= 0 or num_questions > len(question_bank[self.category_var.get()]):
            messagebox.showerror("Error", "Please enter a valid number of questions.")
            return

        self.category = self.category_var.get()
        self.difficulty = self.difficulty_var.get()
        self.selected_questions = random.sample(list(question_bank[self.category].items()), num_questions)
        self.question_index = 0
        self.score = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.hints_used = 0
        self.timer_active = True

        # Remove the initial input widgets
        self.clear_initial_widgets()

        # Add the quiz interface
        self.add_quiz_widgets()

        self.next_question()

    def clear_initial_widgets(self):
        self.label_name.pack_forget()
        self.entry_name.pack_forget()
        self.label_class.pack_forget()
        self.entry_class.pack_forget()
        self.label_num_questions.pack_forget()
        self.entry_num_questions.pack_forget()
        self.label_category.pack_forget()
        self.category_menu.pack_forget()
        self.label_difficulty.pack_forget()
        self.difficulty_menu.pack_forget()
        self.start_button.pack_forget()
        self.leaderboard_button.pack_forget()

    def add_quiz_widgets(self):
        self.label = tk.Label(self.root, text="", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333333")
        self.label.pack(pady=20)

        self.hint_button = tk.Button(self.root, text="Hint", command=self.use_hint, font=("Helvetica", 12, "bold"), bg="#FFC107", fg="white", cursor="hand2")
        self.hint_button.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="Time: 30", font=("Helvetica", 14), bg="#f0f0f0", fg="#333333")
        self.timer_label.pack(pady=10)

        self.radio_var = tk.StringVar()
        self.radio_buttons = []
        for i in range(4):  # Maximum 4 options for Hard mode
            rb = tk.Radiobutton(self.root, text="", variable=self.radio_var, value="", font=("Helvetica", 14), bg="#f0f0f0", fg="#333333", anchor="w")
            self.radio_buttons.append(rb)

        for rb in self.radio_buttons:
            rb.pack(fill="x", padx=20, pady=5)

        self.next_button = tk.Button(self.root, text="Next", command=self.check_answer, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", cursor="hand2")
        self.next_button.pack(pady=20)

    def next_question(self):
        if self.question_index < len(self.selected_questions):
            self.radio_var.set("")
            question, answer = self.selected_questions[self.question_index]
            self.label.config(text=f"Question {self.question_index + 1}: What is the capital of {question}?")
            options = self.generate_options(answer)
            for i, option in enumerate(options):
                self.radio_buttons[i].config(text=option, value=option, state="normal")
            for i in range(len(options), 6):
                self.radio_buttons[i].config(text="", value="", state="disabled")
            self.start_timer()
        else:
            self.end_quiz()

    def generate_options(self, correct_answer):
        options = [correct_answer]
        all_answers = list(question_bank[self.category].values())
        while len(options) < {"Easy": 2, "Medium": 4, "Hard": 6}[self.difficulty]:
            option = random.choice(all_answers)
            if option not in options:
                options.append(option)
        random.shuffle(options)
        return options

    def start_timer(self):
        self.time_left = self.time_limit
        self.update_timer()

    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Time: {self.time_left}")
            self.time_left -= 1
            self.timer_active = True
            self.root.after(1000, self.update_timer)
        else:
            self.timer_active = False
            self.check_answer(auto_next=True)

    def check_answer(self, auto_next=False):
        selected_answer = self.radio_var.get()
        if selected_answer:
            correct_answer = self.selected_questions[self.question_index][1]
            if selected_answer == correct_answer:
                self.correct_answers += 1
                self.score += 10  # Each correct answer awards 10 points
            else:
                self.wrong_answers += 1
            if self.timer_active:
                self.timer_active = False  # Stop timer if answer is checked
        self.question_index += 1
        if not auto_next:
            self.next_question()

    def use_hint(self):
        correct_answer = self.selected_questions[self.question_index][1]
        self.hints_used += 1
        hint = correct_answer[0] + '*' * (len(correct_answer) - 1)
        messagebox.showinfo("Hint", f"The first letter of the capital is: {hint}")

    def end_quiz(self):
        self.label.config(text="Quiz Completed!")
        self.timer_label.pack_forget()
        self.hint_button.pack_forget()
        for rb in self.radio_buttons:
            rb.pack_forget()
        self.next_button.pack_forget()

        feedback = f"Correct Answers: {self.correct_answers}\nWrong Answers: {self.wrong_answers}\nHints Used: {self.hints_used}\nFinal Score: {self.score}\n"
        feedback += "Great job!" if self.correct_answers > self.wrong_answers else "Keep practicing!"
        messagebox.showinfo("Quiz Results", feedback)

        # Add score to leaderboard
        add_to_leaderboard(self.user_name.get(), self.score)

        # Show leaderboard
        show_leaderboard()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
