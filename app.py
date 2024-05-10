# Import necessary libraries and Flask components:
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory, session
import random
import json

class Question:
    '''Represents a quiz question'''
    def __init__(self, question, options, answer, explanation, multiple_choice=False):
        '''
        Initialize a Question object with attributes:
            question (str): the question text
            options (list): a list of answer options
            answer (str): the correct answer
            explanation (str): An explanation of the correct answer
            multiple_choice (bool): Indicates whether the question is multiple-choice (default is False)
        '''
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.user_answer = None  # This value will depend on the user's interaction
        self.multiple_choice = multiple_choice

    def check_answer(self, user_answer):
        '''
        Check whether the choosen option is correct, comparing it with the answer and return boolean:
        '''       
        # Check whether 'user_answer' is a 'list' data type. if so, both the user's selected option(s) and correct answer are sorted
        if isinstance(user_answer, list):
            user_answer.sort()
            self.answer.sort()
            # If no options is selected (the user_answer list is empty) flash message
            if not user_answer:
                print("No option was selected") # Debug Line Only
                flash('No option was selected')
                return False
            # Compare user's answer with correct answer
            if user_answer and user_answer == self.answer:
                print("Correct_answer") # Debug Line Only
                return 'Correct'
            else:
                print("Incorrect_answer") # Debug Line Only
                return 'Incorrect'
        else:
            flash('Invalid data type. A list is expected')                
 
# Initialize Flask application.
app = Flask(__name__)

# Set secret key while in production for session management (Develop line purpose only)
app.secret_key = 'your_secret_key_here'

# Variables to store both lists of questions for further merge
single_choice_questions_pool = []
multiple_choice_questions_pool = []

# Read quiz questions from json files in 'data' folder and load them into question pools
with open('data/single_choice_questions.json', 'r') as json_file:
    single_choice_questions_pool = json.load(json_file)

with open('data/multiple_choice_questions.json', 'r') as json_file:
    multiple_choice_questions_pool = json.load(json_file)

 # Variable to store the merge of both lists of question pools and get the count of questions
questions_pool = single_choice_questions_pool + multiple_choice_questions_pool
total_questions = len(questions_pool)
print(f'The total number of questions is: {total_questions}') # Debug purpose only

# Shuffle the list of questions before starting a quiz for randomization
random.shuffle(questions_pool)
print('Shuffled questions_pool') # Debug Line Only

# Route for the initial page where user starts the quiz
@app.route('/', methods=['GET', 'POST'], endpoint='index')
def index():
    print('Display: start page') # Debug Line Only
    '''
    Display the index page with a 'Start Exam' button
    If a POST request is received, redirect to the start_exam route
    '''
    current_question_index = session.get('current_question_index', 0)
    if request.method == 'POST': 
        return redirect(url_for('start_exam', current_question_index=current_question_index))
    else:
        return render_template("start.html")


# Route for starting exam and redirecting to the first question
@app.route('/start', methods=['GET', 'POST'], endpoint='start_exam')
def start_exam():
    ''' When exam is in progress, increment the current question index '''
    current_question_index = session.get('current_question_index', 0)
    if current_question_index < total_questions:
        return redirect(url_for('display_question'))
    else:
        flash('Invalid access to question.html')
        return redirect(url_for('index'))
  
# Route for displaying quiz questions and after user submits answer displays 'explanation' page
@app.route('/question', methods=['GET', 'POST'], endpoint='display_question')
def display_question():
    '''
    If a POST request is received, check the user's answer calling the 
    check_answer method of the current_question object and display the explanation
    '''
    current_question_index = session.get('current_question_index', 0)
    if current_question_index < total_questions:
        current_question_data = questions_pool[current_question_index]
        # If the question is absent of "multiple_choice" key) in "current_question data dictionary, 
        # return the default value 'False', indicating a single choice question
        if current_question_data.get('multiple_choice', False):
            # Data considered when Question is multiple choice
            current_question = Question(current_question_data['question'], current_question_data['options'], current_question_data['answer'], current_question_data['explanation'], multiple_choice=True)
        else:
            # Data considered when Question is single choice
            current_question = Question(current_question_data['question'], current_question_data['options'], current_question_data['answer'], current_question_data['explanation'])

        if request.method == 'POST':
            print('Button press: submit_answer') # Debug Line Only
            user_selected_options = request.form.getlist('user_answer') # Get user's selection from the form
            explanation = current_question_data['explanation']  # Get the explanation from the JSON data

            # Check if at least one option is selected
            if current_question_data.get('multiple_choice', False) and not user_selected_options:
                flash('Please select at least one option')
                return redirect(url_for('display_question'))
           
            if not user_selected_options:
                print("No option was selected")
                flash('No option was selected', 'error') # Display a red message following CSS styles
                return render_template('question.html', question=current_question, current_question_index=current_question_index, error=True)
            
            explanation = current_question_data['explanation']  # Get the explanation from the JSON data

            # Check whether user's answer is correct using check_answer method and handle accordingly
            result = current_question.check_answer(user_selected_options) # Return either "Correct" or "Incorrect" based on the user's answer
        
            # Store the user's selected options and result in a list in the session
            user_answers = session.get('user_answers', [])
            user_answers.append({'user_answer': user_selected_options, 'result': result})
            session['user_answers'] = user_answers

            # Update the question index
            session['current_question_index'] = current_question_index + 1   
            print('Display: explanation page') # Debug Line Only 
            return render_template('explanation.html', explanation=explanation, result=result)
                
        else:
            return render_template('question.html', question=current_question, current_question_index=current_question_index, error=None)
    else:
        flash('Invalid access to question.html')
        print('Display: result_page')
        return redirect(url_for('result'))
        

# Route for displaying the result of the quiz
@app.route('/result', endpoint='result')
def result():
    '''
    Display the quiz result, showing the number of correct answers and the total number of questions
    Calculate the number of correct answers by iterating through user answers
    '''
    # Calculate the number of correct answers by iterating through user answers
    user_answers = session.get('user_answers', [])
    correct_answers = sum(1 for answer in user_answers if answer['result'] == 'Correct')
    
    # Retrieve the 'result' from the session
    result = session.get('result', '')
    
    return render_template('result.html', correct_answers=correct_answers, total_questions=total_questions, result=result)

# Route for serving static files from the 'static' folder
@app.route('/static/<path:filename>', endpoint='serve_static')
def serve_static(filename):
    '''
    Serve static files from the 'static' folder with arguments:
        filename (str): The filename of the static file to be served
    '''
    return send_from_directory('static', filename)

# Start the Flask application if this script is executed
if __name__ == "__main__":
    app.run(debug=True)
