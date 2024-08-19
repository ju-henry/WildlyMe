import os
from dotenv import load_dotenv
import streamlit as st
import cohere

# load env variables
load_dotenv()

# Define the questions and answers
questions = [
    {
        "question": "How do you handle social situations?",
        "answers": [
            "I love being around people and enjoy large gatherings.",
            "I prefer smaller groups and can get overwhelmed by too many people.",
            "I'm comfortable in both large and small groups, depending on the situation.",
            "I generally avoid social gatherings and prefer to be alone."
        ]
    },
    {
        "question": "How would you describe your energy levels?",
        "answers": [
            "I have high energy and am always ready to go.",
            "I have moderate energy and can pace myself.",
            "I have low energy and prefer to conserve it.",
            "I have variable energy levels depending on the situation."
        ]
    },
    {
        "question": "How do you approach problem-solving?",
        "answers": [
            "I dive right in and try to solve it quickly.",
            "I take my time and think it through carefully.",
            "I seek input from others before making a decision.",
            "I avoid problems whenever possible."
        ]
    },
    {
        "question": "How do you feel about change?",
        "answers": [
            "I love change and find it exciting.",
            "I am neutral about change; it depends on the situation.",
            "I prefer routine and can be hesitant about change.",
            "I dislike change and prefer things to stay the same."
        ]
    },
    {
        "question": "How would you describe your communication style?",
        "answers": [
            "I am direct and to the point.",
            "I am diplomatic and considerate of others' feelings.",
            "I am a good listener and prefer to observe before speaking.",
            "I am a bit reserved and may need time to open up."
        ]
    }
]

# Initialize session state to keep track of the current question and answers
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = []

# Loop through each question
for i in range(len(questions)):
    if i == st.session_state.current_question:
        question = questions[i]
        st.write(question["question"])
        
        # Create checkboxes for each answer
        selected_answers = []
        for j, answer in enumerate(question["answers"]):
            selected = st.checkbox(answer, key=f"answer_{i}_{j}")
            if selected:
                selected_answers.append(answer)
        
        # Submit button to move to the next question
        if st.button("Submit", key=f"submit_{i}"):
            st.session_state.answers.extend(selected_answers)
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