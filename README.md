# Flask-Web-Quiz-App-DevNet-Demo-Exam

This is a flask quiz app that allows users to answer multiple-choice questions.
The app provides questions, answer options, and explanations for correct answers. 
Users can navigate through the questions and get their score at the end.

## Usage
1. Clone repository (templates and app.py) and make sure you have Flask installed:
pip install flask

2. clone repository and run "app.py"
3. Open your web browser and navigate to http://localhost:5000/ to start the quiz.

## Features
- Multiple-choice questions with options.
- Keeps track of user answers and calculates the score.
- Provides explanations for correct answers.
- Simple navigation between questions.

## Adding Questions
You can add more questions to the quiz by extending the questions list in the code. 
Each question is represented by a Question object, and you can add as many questions as you like by following the existing format:

Question(
    "Your question goes here?",
    ["Option A", "Option B", "Option C", "Option D"],
    "Correct Option (A, B, C, or D)",
    "Explanation for the correct answer."
)

