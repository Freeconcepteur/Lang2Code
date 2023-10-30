# Import necessary libraries
import sys
import json
from io import StringIO
import openai
import re
from langchain.callbacks import get_openai_callback
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains import ConversationChain
from PIL import Image
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(__file__) + "/..")

# Configuration de la clé d'API OpenAI
openai.api_key = "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"


def test_openai_api(prompt_human: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Sans explication hors code, sans commentaire, traduire le texte suivant en code Python : {prompt_human}"}
        ],
        temperature=0.4,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']['content']


# Create a list to store the conversation history
conversation_history = []

# Initialisation de la variable generated_code
generated_code = ""


# Interface Streamlit write the title in yellow

st.title("Ecris moi des mots doux :blossom:  :parrot: ")


# ajouter de l'espace
st.write("")
st.write("")
st.write("")


# Create a two-column layout
col1, col2 = st.columns(2)
col3 = st.columns(1)

# Left column for user input and generated code
with col1:
    # Zone de texte pour l'entrée de l'utilisateur
    user_input = st.text_area(
        "Entrez une description pour créer du code Python")

    if st.button("Traduire en python"):
        if user_input:
            # Utilisez la fonction test_openai_api pour générer le code
            generated_code = test_openai_api(user_input)
            # st.code(generated_code, language="python")
# Right column for pasted code and its execution
with col2:
    code_to_execute = st.text_area("Réponse en python:", value=generated_code)

    if st.button("Exécuter le code"):
        try:
            exec_result = exec(code_to_execute)
            # code pour capturer et afficher la sortie...
        except Exception as e:
            exec_result = f"Erreur : {e}"

with col3:
    if 'exec_result' in locals():  # Vérifier si exec_result est défini
        st.text(f"Résultat : {exec_result}")

# SAVE ON JSON
# Create a dictionary to store the conversation history

# Initialize the variable
preview_memory_store = False

# Check the value of preview_memory_store
if preview_memory_store:
    # Code to handle the selected option
    conversation = {
        'user': user_input,
        'generated': code
    }
    # Append the conversation to the conversation history
    conversation_history.append(conversation)
    # Display the conversation history using an expander
    with st.expander("Conversation History", expanded=False):
        st.write(conversation_history)
    # Display the conversation history using an expander, and allow the user to download it
    import uuid
    # Generate a unique key for the download button
    download_button_key = str(uuid.uuid4())
    # Create a button to download the conversation history as a JSON file
    if st.button("Download Conversation History", key=download_button_key):
        # Generate a unique file name
        file_name = str(uuid.uuid4()) + ".json"
        # Save the conversation history to a JSON file
        with open(file_name, "w") as json_file:
            json.dump(conversation_history, json_file, indent=4)

        # Create a link to download the JSON file
        st.markdown(
            f'<a href="{file_name}" download="{download_button_key}.json">Download JSON File</a>',
            unsafe_allow_html=True,
        )


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.postimg.cc/4xgNnkfX/Untitled-design.png");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
