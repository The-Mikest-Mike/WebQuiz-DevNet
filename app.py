# import necessary libraries and Flask components:
from flask import Flask, render_template, request, session, redirect, url_for, flash, send_from_directory, session
import random
import json

class Question:
    '''represents a quiz question'''
    def __init__(self, question, options, answer, explanation):
        '''
        initialize a Question object with attributes:
            question (str): the question text
            options (list): a list of answer options
            answer (str): the correct answer
            explanation (str): An explanation of the correct answer
        '''
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.user_answer = None  # this value will depend on the user's interaction

    def check_answer(self, user_answer):
        '''
        Check if the provided answer is correct and return boolean with attribute:
            user_answer (str): the user's answer
        '''
        if user_answer == self.answer:
            return 'Correct'
        else:
            return 'Incorrect'

# initialize Flask application.
app = Flask(__name__)
# set secret key while in production for session management)
app.secret_key = 'your_secret_key_here'

# read quiz questions from 'questions.json' file in 'data' folder (which is a list of dictionaries),
# store it in the 'questions_pool' variable, and get the count of questions
with open('data/questions.json', 'r') as json_file:
    questions_pool = json.load(json_file)
total_questions = len(questions_pool)
print(f'THE TOTAL NUMBER OF QUESTIONS IS: {total_questions}') # debug purpose only

# shuffle the list of questions before starting a quiz
random.shuffle(questions_pool)

# route for the initial page where the user starts the quiz
@app.route('/', methods=['GET', 'POST'], endpoint='index')
def index():
    '''
    display the index page with a 'Start Exam' button
    if a POST request is received, redirect to the start_exam route
    '''
    current_question_index = session.get('current_question_index', 0)
    if request.method == 'POST':
        return redirect(url_for('start_exam', current_question_index=current_question_index))
    else:
        return render_template("start.html")

'''
 route for starting the exam and redirecting to the first question
 when exam is in progress, increment the current question index
'''
@app.route('/start', methods=['GET', 'POST'], endpoint='start_exam')
def start_exam():
    current_question_index = session.get('current_question_index', 0)
    
    if current_question_index < total_questions:
        session['current_question_index'] = current_question_index + 1
        return redirect(url_for('display_question'))
    else:
        flash('Invalid access to question.html')
        return redirect(url_for('index'))
  
# route for displaying quiz questions and explanations
@app.route('/question', methods=['GET', 'POST'], endpoint='display_question')
def display_question():
    '''
    if a POST request is received, check the user's answer calling the 
    check_answer method of the current_question object and display the explanation
    '''
    current_question_index = session.get('current_question_index', 0)
    if current_question_index < total_questions:
        current_question_data = questions_pool[current_question_index]
        current_question = Question(current_question_data['question'], current_question_data['options'], current_question_data['answer'], current_question_data['explanation'])

        if request.method == 'POST':
            user_answer = request.form.get('user_answer')  # Get the user's answer from the form
            explanation = current_question_data['explanation']  # Get the explanation from the JSON data

            # check whether user answer is correct using check_answer method
            result = current_question.check_answer(user_answer)
        
            # Store the user's answer and result in a list in the session
            user_answers = session.get('user_answers', [])
            user_answers.append({'user_answer': user_answer, 'result': result})
            session['user_answers'] = user_answers

            # update the question index to move to the next question
            session['current_question_index'] = current_question_index + 1        

            return render_template('explanation.html', explanation=explanation, result=result)
        else:
            return render_template('question.html', question=current_question, current_question_index=current_question_index)
    else:
        flash('Invalid access to question.html')
        return redirect(url_for('result'))

# route for displaying the result of the quiz
@app.route('/result', endpoint='result')
def result():
    '''
    display the quiz result, showing the number of correct answers and the total number of questions
    calculate the number of correct answers by iterating through user answers
    '''
    # Calculate the number of correct answers by iterating through user answers
    user_answers = session.get('user_answers', [])
    correct_answers = sum(1 for answer in user_answers if answer['result'] == 'Correct')
    
    # retrieve the 'result' from the session
    result = session.get('result', '')
    
    return render_template('result.html', correct_answers=correct_answers, total_questions=total_questions, result=result)

# route for serving static files (if any) from the 'static' folder
@app.route('/static/<path:filename>', endpoint='serve_static')
def serve_static(filename):
    '''
    serve static files from the 'static' folder with arguments:
        filename (str): The filename of the static file to be served
    '''
    return send_from_directory('static', filename)

# start the Flask application if this script is executed
if __name__ == "__main__":
    app.run(debug=True)
