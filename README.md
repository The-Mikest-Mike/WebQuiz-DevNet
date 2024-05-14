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

WebQuiz-DevNet/<br>
│<br>
├── app.py                                             # Main Flask application file<br>
├── README.md                                          # Project documentation<br>
├── requirements.txt                                   # Required Python packages<br>
│<br>
├── templates/                                         # HTML templates folder<br>
│&emsp;&emsp;&emsp;├── correct.html                    # Correct answer feedback<br>
│&emsp;&emsp;&emsp;├── explanation.html                # Question explanation<br>
│&emsp;&emsp;&emsp;├── incorrect.html                  # Incorrect answer feedback<br>
│&emsp;&emsp;&emsp;├── question.html                   # Display questions<br>
│&emsp;&emsp;&emsp;├── result.html                     # Display quiz results<br>
│&emsp;&emsp;&emsp;└── start.html                       # Start the quiz<br>
│<br>
├── static/                                            # Static files folder (CSS, images)<br>
│&emsp;&emsp;&emsp;└── styles.css                      # CSS styles for the application<br>
│<br>
└── data/                                              # Data files folder<br>
&emsp;&emsp;&emsp;├── multiple_choice_questions.json   # Pool of multiple-choice questions<br>
&emsp;&emsp;&emsp;└── single_choice_questions.json     # Pool of single-choice questions<br>




