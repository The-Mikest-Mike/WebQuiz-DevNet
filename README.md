## Usage
1. Clone repository and install requirements.txt file:
   ```bash
   git clone <repo-url>
   ```
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run app.py file:
   ```bash
   python3 app.py
   ```
5. Open your web browser and start the quiz. Navigate to local host:
   ```bash
   http://127.0.0.1:5000/
   ``` 

## Features
- User friendly interface.
- Single and Multiple-choice questions with options.
- Keeps track of user answers and calculates the score.
- Instantly know by colors whether correct or incorrect.
- Provides explanations for answers.
- Simple navigation between questions.

## Structure of Folders:

    app.py              # main Flask application file
    README.md
    requirements.txt
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
        multiple_choice_questions.json  # single choice questions pool
        single_choice_questions.json # multiple choice questions pool

