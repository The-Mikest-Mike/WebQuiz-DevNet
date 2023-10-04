# import necessary libraries and Flask components:
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import random
import json

# classes and methods
class Question:
    """Represents a quiz question."""

    def __init__(self, question, options, answer, explanation):
        """
        Initialize a Question object.

        Args:
            question (str): The question text.
            options (list): A list of answer options.
            answer (str): The correct answer.
            explanation (str): An explanation of the correct answer.
        """
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.user_answer = None  # this value will depend on the user's interaction

    def check_answer(self, user_answer):
        """
        Check if the provided answer is correct.

        Args:
            user_answer (str): The user's answer.

        Returns:
            bool: True if the answer is correct, False otherwise.
        """
        return user_answer == self.answer

# initialize Flask application.
app = Flask(__name__)

# Set a secret key for session management (change this to a secret key in the real application).
app.secret_key = 'your_secret_key_here'

# read quiz questions from the 'questions.json' file located in 'data' folder,
# store it in the 'questions' variable, and get the count of questions
with open('data/questions.json', 'r') as json_file:
    questions = json.load(json_file)
total_questions = len(questions)
print(f'THE TOTAL NUMBER OF QUESTIONS IS: {total_questions}')

# Shuffle the list of questions before starting a quiz.
random.shuffle(questions)

# Route for the initial page where the user starts the quiz.
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Display the index page with a 'Start Exam' button.

    If a POST request is received, redirect to the start_exam route.
    """
    current_question_index = session.get('current_question_index', 0)
    if request.method == 'POST':
        return redirect(url_for('start_exam', current_question_index=current_question_index))
    else:
        return render_template("start.html")

# Route for starting the exam, which redirects to the first question.
@app.route('/start', methods=['GET', 'POST'])
def start_exam():
    """
    Start the exam by redirecting to the first question.

    If the exam is already in progress, increment the current question index.
    """
    current_question_index = session.get('current_question_index', 0)
    session['current_question_index'] = current_question_index + 1
    return redirect(url_for('question'))

# Route for displaying quiz questions and explanations.
@app.route('/question', methods=['GET', 'POST'], endpoint='question')
def display_question():
    """
    Display quiz questions and explanations.

    If a POST request is received, check the user's answer and redirect to the next question with explanation.
    """
    current_question_index = session.get('current_question_index', 0)
    if current_question_index < total_questions:
        current_question = questions[current_question_index]

        if request.method == 'POST':
            user_answer = request.form.get('user_answer')  # Get the user's answer from the form
            explanation = current_question['explanation']  # Get the explanation from the JSON data

            # Increment the question index and redirect to the next question with explanation.
            session['current_question_index'] = current_question_index + 1

            return render_template('question.html', question=current_question, current_question_index=current_question_index, explanation=explanation)

        return render_template('question.html', question=current_question, current_question_index=current_question_index)
    else:
        flash('Invalid access to question.html')
        return redirect(url_for('index'))

# Route for displaying the result of the quiz.
@app.route('/result')
def result():
    """
    Display the quiz result, showing the number of correct answers and the total number of questions.
    """
    # Calculate the number of correct answers by iterating through questions.
    correct_answers = sum(1 for question in questions if question.check_answer(question.user_answer))
    return render_template('result.html', correct_answers=correct_answers, total_questions=total_questions)

# Route for serving static files (if any) from the 'static' folder.
@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    Serve static files from the 'static' folder.

    Args:
        filename (str): The filename of the static file to be served.
    """
    return send_from_directory('static', filename)

# Start the Flask application if this script is executed.
if __name__ == "__main__":
    app.run(debug=True)
