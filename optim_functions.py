import json
import numpy as np
from itertools import product, combinations
import random
import matplotlib.pyplot as plt
import os


def global_optim():

    # get test questions
    with open('questions_test.json', 'r') as f:
        questions_test = json.load(f)

    # load all scores
    all_scores = [np.load("scores/question" + str(i) + ".npy") for i in range(18)]

    # Generate all combinations of 5 indices
    elements = list(range(0, 18))
    Q_combinations = list(combinations(elements, 5))
    
    # try all combinations of questions
    D_best = {}
    loss_best = 1e8
    Q_comb_best = ()
    for q in range(0, len(Q_combinations)):

        Q_comb = Q_combinations[q]

        scores = [all_scores[i] for i in Q_comb]

        column_counts = [array.shape[1] for array in scores] 

        # Generate combinations based on the number of columns in each array
        answer_combinations = list(product(*[range(count) for count in column_counts]))

        num_animals = scores[0].shape[0]
        D = {i: 0 for i in range(num_animals)}
        for k in range(0, len(answer_combinations)):
            combo = answer_combinations[k]
            selected_columns = [scores[j][:, col:col+1] for j, col in enumerate(combo)]
            stacked = np.hstack(selected_columns)
            sum_result = np.round(np.sum(stacked, axis=1, keepdims=True), decimals=1)
            D[np.argmax(sum_result)] += 1

        loss = 1/num_animals * sum([(val - sum(D.values())/num_animals)**2 for val in D.values()])
        if loss < loss_best:
            loss_best = loss
            D_best = D
            Q_comb_best = Q_comb

    # return
    return {"questions": Q_comb_best, "loss": loss_best, "distribution": D_best}


def plot_distribution(res, path):

    data = res["distribution"]

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(data.keys(), data.values())

    # Customize the plot
    ax.set_xlabel('Categories')
    ax.set_ylabel('Values')
    ax.set_title('Bar Plot. Loss: ' + str(round(res["loss"])))

    # Add a horizontal line
    line_value = sum(data.values()) / len(data)
    ax.axhline(y=line_value, color='r', linestyle='--', label='Threshold')

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}', ha='center', va='bottom')

    # Add legend
    plt.legend()

    # folder and file name
    folder_path = 'images/plots/' 
    file_name = 'plot_' + str(round(res["loss"])) + '.png'

    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Save the plot as an image file
    file_path = os.path.join(folder_path, file_name)
    plt.savefig(file_path)
    plt.close()

    return None

