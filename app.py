from flask import Flask, render_template, request, session, redirect, url_for
import random
import json
import numpy as np
from dotenv import load_dotenv
import os

# load env variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Define questions and animals
with open('questions.json', 'r') as f:
    questions = json.load(f)

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'question_num' not in session:
        session['question_num'] = 0
        session['answers'] = []
        session['questions_asked'] = []

    if request.method == 'POST':
        session['answers'].append(int(request.form['answer']))
        session['questions_asked'].append(session['question_num'])
        session['question_num'] += 1

    if session['question_num'] >= 5:
        return redirect(url_for('result'))

    return render_template('question.html', 
                           question=questions[session['question_num']], 
                           question_number=session['question_num'])

@app.route('/result')
def result():
    # predict the animal

    # get scores
    score_answers = np.zeros((10, 1))
    for i, j in zip(session['questions_asked'], session['answers']):
        score_answers += np.load("scores/question" + str(i) + ".npy")[:, j:(j+1)]
    
    # get animal names
    with open('animals.json', 'r') as f:
        animals = json.load(f)

    # get the predicted animal
    pred_animal = list(animals.keys())[np.argmax(score_answers)]

    return render_template('result.html', animal=pred_animal, info=animals[pred_animal])

if __name__ == '__main__':
    app.run(debug=True)
