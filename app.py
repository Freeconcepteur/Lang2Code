import sqlite3
import streamlit as st
import openai
import sys
import os
from io import StringIO
from dotenv import load_dotenv
from src.openai_api import *
from database_operations.models import *

create_tables()

# Charger la clé API OpenAI à partir du fichier .env situé dans le répertoire config
load_dotenv(dotenv_path='config/.env')

# Configurer la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


st.title('Traducteur de texte en code Python')

# script_title = st.text_input('Titre de mon script Python', key='input1')

# Créer une boîte de sélection dans la sidebar
titles = get_titles_from_db()
selection = st.sidebar.selectbox(
    'Sélectionnez un script', options=get_titles_from_db(), key='selected_title')

# Obtenir les données basées sur la sélection
data = get_data_from_selection(selection)

# Utiliser les données pour pré-remplir les champs de texte et les textareas
script_title = st.text_input(
    'Titre de mon script Python', value=data['script_title'])

# Création de deux colonnes
col1, col2 = st.columns(2)

with col1:
    st.header('Texte humain')
    human_text = st.text_area(
        'Entrez votre texte ici :', value=data['human_text'], height=200)
    translate_button = st.button('Traduire en Python')

with col2:
    st.header('Code Python généré')
    python_code = data['python_code']
    python_code_final = ''
    if translate_button:
        python_code = python_openai_api(human_text)
        python_code_final = python_code

    python_code = st.text_area(
        'Votre code traduit sera affiché ici :', value=python_code, height=200)

    execute_button = st.button('Exécuter le code')


if execute_button and python_code:
    try:
        # Rediriger la sortie standard vers un tampon
        old_stdout = sys.stdout
        new_stdout = StringIO()
        sys.stdout = new_stdout

        exec(python_code)
        # Récupérer la sortie standard capturée
        output = new_stdout.getvalue()

        # Restaurer la sortie standard d'origine
        sys.stdout = old_stdout

        # Créer une zone pour afficher le résultat
        st.subheader("Résultat de l'exécution 😊")
        st.text(output)

        st.subheader("Code saisi 😊")
        st.code(python_code, language="python")
        st.success('Le code a été exécuté avec succès.')
    except Exception as e:
        st.error(f'Une erreur est survenue : {e}')
    finally:
        st.info("Merci d'avoir utilisé cette application !")


if st.button('Sauvegarder les changements'):
    # save_title_to_db(script_title)
    save_script(script_title, human_text, python_code)


# Affichage des tables
display_tables()
