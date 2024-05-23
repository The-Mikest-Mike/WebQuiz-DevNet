# Import necessary libraries and Flask components:
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory
import random
import json

class Question:
    '''Represents a quiz question'''

    def __init__(self, question, options, answer, explanation, multiple_choice=False):
        '''
        Initialize a Question object with attributes:
            question (str): The question text
            options (list): A list of answer options
            answer (list): The correct answer
            explanation (str): An explanation of the correct answer
            multiple_choice (bool): Indicates whether the question is multiple-choice (default is False)
        '''
        self.question = question # Store question text
        self.options = options # Store the list of options to answer
        self.answer = answer # Store the correct answer(s)
        self.explanation = explanation # Store the explanation
        self.user_answer = None  # Initialize user answer as None, to be set later with user's interaction
        self.multiple_choice = multiple_choice # Store whether the question is multiple-choice

    def check_answer(self, user_answer):
        '''
        Check whether the chosen option(s) is/are correct, comparing it with the answer(s)
        and return a string 'Correct' or 'Incorrect'
        '''       
        # Check if the user's answer is a list data type
        if isinstance(user_answer, list):
            print('Check: user_answer is a list') # Debug: log data type check

            # Sort both user's answer and the correct answer for comparison
            user_answer.sort()
            self.answer.sort()
            print(f'Sorted user_answer: {user_answer}') # Debug: log sorted user answer
            print(f'Sorted correct answer: {self.answer}') # Debug: log sorted correct answer

            # Compare user's answer with correct answer
            if user_answer == self.answer:
                print('Answer is correct') # Debug: log correct answer
                return 'Correct'
            else:
                print('Answer is incorrect') # Debug: log incorrect answer
                return 'Incorrect'
        else:
            # Flash a message if the data type of user_answer is not a list
            print('Invalid data type for user_answer, expected a list') # Debug: log invalid data type
            flash('Invalid data type. A list is expected')
            return False

 
# Initialize Flask application
app = Flask(__name__)

# Set secret key for session management (use a secure secret key in production)
app.secret_key = 'your_secret_key_here'

# Initialize variables to store both lists of questions for further merging
single_choice_questions_pool = []
multiple_choice_questions_pool = []

# Read single-choice questions from json file in 'data' folder and load them into single_choice_questions_pool
with open('data/single_choice_questions.json', 'r') as json_file:
    single_choice_questions_pool = json.load(json_file)
    print('Load single choice questions') # Debug: log loading of single-choice questions

# Read multiple-choice questions from json file in 'data' folder and load them into multiple_choice_questions_pool
with open('data/multiple_choice_questions.json', 'r') as json_file:
    multiple_choice_questions_pool = json.load(json_file)
    print('Load multiple choice questions') # Debug: log loading of multiple-choice questions

 # Mergge both lists of question pools into a single list and get the total count of questions
questions_pool = single_choice_questions_pool + multiple_choice_questions_pool
total_questions = len(questions_pool)
print(f'The total number of questions is: {total_questions}') # Debug: log total number of questions

# Shuffle the list of questions for randomization before starting the quiz
random.shuffle(questions_pool)
print('Shuffle questions_pool') # Debug: log shuffling of questions

# Route for the initial page where user starts the quiz
@app.route('/', methods=['GET', 'POST'], endpoint='index')
def index():
    '''
    Display the index page with a 'Start Exam' button
    If a POST request is received, redirect to the start_exam route
    '''
    print('Display: start page') # Debug: log display of start page
    current_question_index = session.get('current_question_index', 0)
    if request.method == 'POST': 
        print('Received POST request, redirecting to start_exam') # Debug: log POST request
        return redirect(url_for('start_exam', current_question_index=current_question_index))
    else:
        return render_template("start.html")

# Route for starting exam and redirecting to the first question
@app.route('/start', methods=['GET', 'POST'], endpoint='start_exam')
def start_exam():
    ''' When exam is in progress, increment the current question index '''
    current_question_index = session.get('current_question_index', 0)
    print(f'Curreng question index: {current_question_index}') # Debug: log current question index
    if current_question_index < total_questions:
        print('Redirect to display_question') # Debug: log redirection to display_question
        return redirect(url_for('display_question'))
    else:
        print('Invalid access to question.html, redirecting to index') # Debug: log invalid access
        flash('Invalid access to question.html')
        return redirect(url_for('index'))
  
# Route for displaying quiz questions and handling user's answer submission
@app.route('/question', methods=['GET', 'POST'], endpoint='display_question')
def display_question():
    '''
    If a POST request is received, check the user's answer by calling the 
    check_answer method of the current_question object and display the explanation
    '''
    # Get the current question index from the session, default to 0 if no found
    current_question_index = session.get('current_question_index', 0)
    print(f'Current question index: {current_question_index}') # Debug: log current question index

    # Check if the current question index is within the total number of questions
    if current_question_index < total_questions:
        # Retrieve the current question data from the questions pool
        current_question_data = questions_pool[current_question_index]
        print(f'Current question data: {current_question_data}') # Debug: log current question data

        # Shuffle the list of options before displaying a question for randomization
        random.shuffle(current_question_data['options'])
        print('Shuffle options') # Debug: log 'shuffled options' event

        # Determine if the current question is multiple choice or single choice
        is_multiple_choice = current_question_data.get('multiple_choice', False)
        print(f'Is multiple choice: {is_multiple_choice}') # Debug: log if the question is multiple choice

        # Create a Question object with the current question data
        current_question = Question(
            question=current_question_data['question'],
            options=current_question_data['options'],
            answer=current_question_data['answer'],
            explanation=current_question_data['explanation'],
            multiple_choice=is_multiple_choice
            )
        print(f'Create question object: {current_question}') # Debug: log created Question object

        # Determine the required number of answers based on the question type
        required_answers = len(current_question_data['answer']) if is_multiple_choice else 1
        print(f'Required answers: {required_answers}') # Debug: log required number of answers

        # Check if the request method is POST, indicating form submission
        if request.method == 'POST':
            print('Button press: submit_answer') # Debug: log submit botton press

            # Get the list of options selected by the user from the form
            user_selected_options = request.form.getlist('user_answer')
            print(f'User selects options: {user_selected_options}') # Debug: log user-selected options
            
            # Check if the number of selected options matches the required number
            if len(user_selected_options) != required_answers:
                # If the number of selected options is incorrect (does not match the required number), flash an error message
                if is_multiple_choice:
                    flash(f'Please select exactly {required_answers} options', 'error') # Display red message following CSS style
                else:
                    flash('Please select exactly one option', 'error') # Display red message following CSS style
                print('Validation fails: Incorrect number of options selected') # Debug: log required ammount of options validation failure
                
                # Re-render the question page with an error message
                return render_template('question.html', question=current_question, current_question_index=current_question_index, error=True)

            # Check whether user's answer is correct using check_answer method
            result = current_question.check_answer(user_selected_options) # Returns either "Correct" or "Incorrect"
            print(f'Answer check result: {result}') # Debug: log result of answer check
        
            # Retrieve the list of user's answer from the session, default to empty list if not found
            user_answers = session.get('user_answers', [])
            print(f'User answers: {user_answers}') # Debug: log user answers

            # Append the user's selected options and result to the list of answers
            user_answers.append({'user_answer': user_selected_options, 'result': result})

            # Store the updated list of user's answers in the session
            session['user_answers'] = user_answers
            print(f'Update user answers in session: {session["user_answers"]}') # Debug: log updated session data

            # Increment the current question index and store it in the session
            session['current_question_index'] = current_question_index + 1   
            print(f'Increment question index: {session ["current_question_index"]}') # Debug: log incremented question index

            print('Display: explanation page') # Debug: log displaying explanation page

            # Render the explanation page with the explanation and result of the current question
            return render_template('explanation.html', explanation=current_question.explanation, result=result)
        else:
            # Render the question page if the request method is GET
            return render_template('question.html', question=current_question, current_question_index=current_question_index, error=None)
    else:
        # Fash error message if current question index is invalid
        flash('Invalid access to question.html')
        print('Invalid access attempt: current question index is out of range') # Debug: log invalid access attempt

        print('Display: result_page') # Debug: log displaying result page

        # Redirect to the result page
        return redirect(url_for('result'))

# Route for displaying the result of the quiz
@app.route('/result', endpoint='result')
def result():
    '''
    Display the quiz result, showing the number of correct answers and the total number of questions
    Calculate the number of correct answers by iterating through user answers
    '''
    # Retrieve the list of user answers from the session. If 'user_answers' does not exist, return an empty list 
    user_answers = session.get('user_answers', [])
    print(f'User answers: {user_answers}') # Debug: log user answers

    # Iterate through the list of user answers and count how many have the result 'Correct'
    correct_answers = sum(1 for answer in user_answers if answer['result'] == 'Correct')
    print(f'Number of correct answers: {correct_answers}') # Debug: log number of correct answers
    
    # Retrieve the 'result' from the session. If 'result' does not exist in the session, return default empty string
    result = session.get('result', '')
    print(f'Quiz result: {result}') # Debug: log quiz result
    
    # Render the result template with the ammount of correct answers, total questions, and result
    return render_template('result.html', correct_answers=correct_answers, total_questions=total_questions, result=result)

# Route for serving static files from the 'static' folder
@app.route('/static/<path:filename>', endpoint='serve_static')
def serve_static(filename):
    '''
    Serve static files from the 'static' folder with arguments:
        filename (str): The filename of the static file to be served
    '''
    print(f'Serve static file: {filename}') # Debug: log the filename of static file being served
    return send_from_directory('static', filename)

# Start the Flask application if this script is executed
if __name__ == "__main__":
    print('Start Flask application') # Debug: log application start
    app.run(debug=True)
