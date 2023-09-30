# import necessary Flask components:
# - 'Flask': The main Flask application class.
# - 'render_template': Used for rendering HTML templates in your web application.
# - 'request': Used for handling HTTP requests and accessing request data.
# - 'redirect': Used for redirecting users to different URLs.
# - 'url_for': Used for generating URLs for routes defined in your Flask application.

from flask import Flask, render_template, request, redirect, url_for

# import 'random' module for generating random questions
import random
# import Python standard library module 'json' for reading 'questions.json' file that contains the quiz questions
import json
# classes and methods
class Question:    # define 'Question' class to represent quiz questions
    def __init__(self, question, options, answer, explanation):
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.user_answer = None    # this value will depend on the user's interaction

    def check_answer(self, user_answer):
        return user_answer == self.answer

 # initialize Flask application. '__name__' determines the root path of the application and locates resources like templates and static files
app = Flask(__name__)   

# read quiz questtions from the 'questions.json' file located in 'data' folder and get the count of questions
with open('data/questions.json', 'r') as json_file:
    questions = json.load(json_file)    
total_questions = len(questions)
print(f'THE TOTAL NUMBER OF QUESTIONS IS: {total_questions}')

# reads quiz questions from the 'questions.json' file, parses the JSON data, and stores it in the 'questions' variable as a list of dictionaries containing quiz questions. 
with open('data/questions.json', 'r') as json_file:
    questions = json.load(json_file)

# shuffle the list of questions before starting a quiz
random.shuffle(questions)

# define and initialize global variable:
current_question_index = 0

# Flask '@app.route' decorator associate a function with routes handlers for the URL paths
@app.route('/', methods=['GET', 'POST'])
def index():
    global current_question_index
    if request.method == 'POST':
        current_question_index = 0
        return redirect(url_for('question', question_index=current_question_index))
    return render_template("start.html")


# sets up a Flask route to handle requests to URLs like /question/1, /question/2, etc., where the 'question_index' parameter captures the specific question index from the URL

@app.route('/question//<int:question_index>', methods=['GET', 'POST'])
def question(question_index):
    global current_question_index  # access the global variable
    if request.method == 'POST':
        # get the user's answer from the form
        user_answer = request.form.get('user_answer')
        # get the current question based on the current_question_index
        current_question = questions[current_question_index]
        
        if current_question.check_answer(user_answer):
            # if the answer is correct, display 'correct.html' with explanation
            explanation = current_question.explanation
            return render_template('correct.html', explanation=explanation)
        else:
            # if the answer is incorrect, display 'incorrect.html' with explanation
            explanation = current_question.explanation
            return render_template('incorrect.html', explanation=explanation)

    if current_question_index < len(questions):
        # render the 'question.html' template with the current question
        return render_template('question.html', question=questions[current_question_index], question_index=question_index, current_question_index=current_question_index)
    else:
        # if all questions have been answered, redirect to the result page
        return redirect(url_for('result'))

@app.route('/correct.html')
def correct():
    return render_template('correct.html')

@app.route('/incorrect.html')
def incorrect():
    return render_template('incorrect.html')

@app.route('/result.html')
def result():
    return render_template('result.html')

# Start the Flask application if this script is executed
if __name__ == "__main__":
    app.run(debug=True)