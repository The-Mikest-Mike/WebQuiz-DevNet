from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__)

class Question:
    def __init__(self, question, options, answer, explanation):
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.user_answer = None

    def check_answer(self, user_answer):
        return user_answer == self.answer

questions = [
    Question("Which of the following is a characteristic of XML format?",
             ["Pre-defined tags", "Concerned with carrying data", "Used for displaying data", "Key:value pairs"],
             "B", "XML format is primarily concerned with carrying data."
    ),
    Question("Which of the following is NOT a characteristic of JSON format?",
             ["Comments are not allowed", "Whitespace has no impact on data", "No ability to use arrays", "Uses a bracketing system to identify objects"],
             "C", "JSON format does have the ability to use arrays."
    ),
    # Add more questions here
]

current_question_index = 0

@app.route("/", methods=["GET", "POST"])
def index():
    global current_question_index
    if request.method == "POST":
        user_answer = request.form.get("user_answer")
        questions[current_question_index].user_answer = user_answer
        current_question_index += 1
        if current_question_index < len(questions):
            return redirect(url_for("question"))
        else:
            correct_answers = sum(1 for q in questions if q.check_answer(q.user_answer))
            total_questions = len(questions)
            return render_template("result.html", correct_answers=correct_answers, total_questions=total_questions)
    else:
        current_question_index = 0  # Move this line outside of the 'else' block
        return render_template("start.html", current_question_index=current_question_index)

@app.route("/question", methods=["GET"])
def question():
    global current_question_index
    if current_question_index < len(questions):
        question = questions[current_question_index]
        return render_template("question.html", question=question, current_question_index=current_question_index)  # Pass current_question_index to the template
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
