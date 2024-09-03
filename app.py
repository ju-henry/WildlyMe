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
questions = [{**q, "answer_encode": [q["answer_head"] + ": " + ans for ans in q["answers"]]} for q in questions]
questions = [{**q, "answer_display": [shortans + ": " + ans for shortans, ans in zip(q["answer_short"], q["answers"])]} for q in questions]

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

    return render_template('question.html', question=questions[session['question_num']])

@app.route('/result')
def result():
    # predict the animal

    # get answers embeddings
    embedding_answers = np.zeros((1, 384))
    for i, j in zip(session['questions_asked'], session['answers']):
        embedding_answers += np.load("embeddings/question" + str(i) + ".npy")[j,:]
    
    # get animal embeddings and names
    embeddings_animal = np.load("embeddings/animals.npy")
    with open('animals.json', 'r') as f:
        animals = json.load(f)

    # get the predicted animal
    cosine_distances = np.dot(embeddings_animal, np.transpose(embedding_answers))
    pred_animal = list(animals.keys())[np.argmax(cosine_distances)]

    return render_template('result.html', animal=pred_animal, info=animals[pred_animal])

if __name__ == '__main__':
    app.run(debug=True)
