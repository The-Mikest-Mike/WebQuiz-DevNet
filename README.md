# Overview

Flask quiz app that allows users to answer multiple-choice questions. Provides questions, answer options, and explanations for correct answers. 
Users can navigate through the questions and get their score at the end.

## Structure of Folders:

    app.py              # main Flask application file
    templates/          # folder for HTML templates
        correct.html
        explanation.html
        incorrect.html
        question.html
        result.html
        start.html
    static/             # folder for static files (CSS styles, images)
        styles.css      # all css styles
    data/               # folder for data files
        questions.json  # containing questions, options and explanations pool


## Usage
1. Clone repository and install requirements.txt file with command: `pip3 install -r requirements.txt`
2. Run `app.py` file with command: `python3 app.py`
4. Open your web browser and navigate to `http://localhost:5000/` to start the quiz.

## Features
- User friendly interface
- Multiple-choice questions with options.
- Keeps track of user answers and calculates the score.
- Instantly know by colors whether correct or incorrect.
- Provides explanations for correct answers.
- Simple navigation between questions.


