## How to Use
1. Clone repository and install requirements.txt file:
   ```bash
   git clone https://github.com/The-Mikest-Mike/WebQuiz-DevNet.git
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
- Instantly visualize whether answered correct or incorrect.
- Provides explanations for answers.
- Simple navigation between questions.

## Project Directory Structure:
```
WebQuiz-DevNet/
│
├── app.py                                             # Main Flask application file
├── README.md                                          # Project documentation
├── requirements.txt                                   # Required Python packages
│
├── templates/                                         # Folder for HTML templates
│      ├── correct.html                                # Correct answer feedback
│      ├── explanation.html                            # Question explanation
│      ├── incorrect.html                              # Incorrect answer feedback
│      ├── question.html                               # Display questions
│      ├── result.html                                 # Display quiz results
│      └── start.html                                  # Start the quiz
│
├── static/                                            # Folder for static files (CSS, images)
│      └── styles.css                                  # CSS styles for the application
│
└── data/                                              # Folder for data files (JSON questions)
       ├── multiple_choice_questions.json              # Pool of multiple-choice questions
       └── single_choice_questions.json                # Pool of single-choice questions
```





