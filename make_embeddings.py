from sentence_transformers import SentenceTransformer
import numpy as np
import json
import os

# directory work
dir_path = "embeddings"

# delete everything
if os.path.exists(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
    os.rmdir(dir_path)

# create a fresh directory
os.mkdir(dir_path)


# Load a pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# load questions
with open('questions.json', 'r') as f:
    questions = json.load(f)
questions = [{**q, "answer_encode": [q["answer_head"] + ": " + ans for ans in q["answers"]]} for q in questions]

# encode and save answers
i = 0
for element in questions:
    res = model.encode(element["answer_encode"])
    np.save(dir_path + "/question" + str(i) + ".npy", res)
    i += 1

# load animals
with open('animals.json', 'r') as f:
    animals = json.load(f)

# encode and save animals
res = model.encode(list(animals.keys()))
np.save(dir_path + "/animals.npy", res)