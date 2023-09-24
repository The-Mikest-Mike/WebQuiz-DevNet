# import necessary Flask components:
# - 'Flask': The main Flask application class.
# - 'render_template': Used for rendering HTML templates in your web application.
# - 'request': Used for handling HTTP requests and accessing request data.
# - 'redirect': Used for redirecting users to different URLs.
# - 'url_for': Used for generating URLs for routes defined in your Flask application.
from flask import Flask, render_template, request, redirect, url_for

# import 'random' module for generating random questions
import random

# classes and methods
class Question:    # define 'Question' class to represent quiz questions
    def __init__(self, question, options, answer, explanation):
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.user_answer = None

    def check_answer(self, user_answer):
        return user_answer == self.answer

# objects / constants
app = Flask(__name__)    # initialize Flask application

# functions
def index():
    global current_question_index

    # shuffle the list of questions randomly before starting the quiz
    random.shuffle(questions)
    
    if request.method == "POST":
        user_answer = request.form.get("user_answer")
        questions[current_question_index].user_answer = user_answer
        current_question_index += 1
        if current_question_index < len(questions):
            # redirect to the "question" route if there are more questions to answer
            return redirect(url_for("question"))
        else:
            correct_answers = sum(1 for q in questions if q.check_answer(q.user_answer))
            total_questions = len(questions)
            return render_template("result.html", correct_answers=correct_answers, total_questions=total_questions)
    else:
        # display the first question if available, or redirect to the "result" page if there are no questions
        if current_question_index < len(questions):
            question = questions[current_question_index]
            return render_template("question.html", question=question, current_question_index=current_question_index)
        else:
            return render_template("result.html", correct_answers=0, total_questions=0)  # no questions to answer, show result

# start the Flask application if this script is executed
if __name__ == "__main__":
    app.run(debug=True)

