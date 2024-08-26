import os
from dotenv import load_dotenv
import streamlit as st
import cohere
import json

# load env variables
load_dotenv()

st.markdown("""
    <style>
    :root {
        --primary-color: #4CAF50;
        --background-color: #F5F5F5;
        --text-color: #333333;
        --accent-color: #FFA500;
    }
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
    }
    .stButton > button:hover {
        background-color: var(--primary-color);
        color: white;
    }
    
    /* Style for the entire radio group */
    div.row-widget.stRadio > div[role="radiogroup"] {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
            
    /* Hide the label above the radio buttons */
    div.row-widget.stRadio > label {
        display: none !important;
    }

    /* Style for each radio option */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] {
        display: flex;
        align-items: center;
        cursor: pointer;
        margin: 12px 0;
    }

    /* Hide the default radio button */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
        display: none;
    }

    /* Create a custom radio button */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]::before {
        content: "";
        display: inline-block;
        width: 40px;
        height: 40px;
        border: 4px solid #ccc;
        border-radius: 50%;
        margin-right: 12px;
        transition: all 0.3s ease;
        flex-shrink: 0;
    }

    /* Style for the selected radio button */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"][aria-checked="true"]::before {
        border-color: #00acee;
        background-color: #00acee;
        box-shadow: inset 0 0 0 4px #fff;
    }

    /* Hover effect */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:hover::before {
        border-color: #00acee;
    }

    /* Style for the text */
    div.row-widget.stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] > div:last-child {
        display: flex;
        align-items: center;
        line-height: 1.3;
        font-size: 22px;
    }
    </style>
    """, unsafe_allow_html=True)

# Define the questions and answers
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Initialize session state to keep track of the current question and answers
if "current_question" not in st.session_state:
    st.session_state.current_question = -1
if "answers" not in st.session_state:
    st.session_state.answers = []

if st.session_state.current_question == -1:

    st.markdown("""
    <style>
    h2 {
        font-size: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.header("Let an AI robot determine your animal personality!")
    st.text("Answer 10 questions adjusted to you and you'll know!")
    st.markdown("<br>", unsafe_allow_html=True)

    st.write("Click the button below to start.")
    if st.button("Start the test"):
        st.session_state.current_question += 1
        st.rerun()

# Loop through each question
for i in range(len(questions)):
    if i == st.session_state.current_question:

        question = questions[i]
        st.subheader(question["question"])
        answer = st.radio("Choose one:", question["answers"], index=None, key=f"question_{i}")
        if answer:
            st.session_state.answers.append(answer)
            st.session_state.current_question += 1
            st.rerun()

# Display the final message after all questions have been answered
if st.session_state.current_question == len(questions):

    st.write("You are a horse\n\n")

    instructions = "Please give me the reasons that might make me comparable to a horse given the information provided in Input Text."
    prompt = "\n" + "## Instructions\n" + instructions + " \n\n" + "## Input Text\n" + "\n".join(st.session_state.answers) + "\n"

    co = cohere.Client(api_key=os.getenv('API_KEY_COHERE'))

    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=400,
        seed=1  # Optional: Set seed for reproducibility
    )
    
    st.write(response.generations[0].text.strip())