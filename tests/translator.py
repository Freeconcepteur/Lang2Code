import sqlite3
import streamlit as st
import openai  # Assurez-vous que la bibliothèque OpenAI est installée et configurée
import sys
import os
from io import StringIO
from dotenv import load_dotenv

# Charger la clé API OpenAI à partir du fichier .env situé dans le répertoire config
load_dotenv(dotenv_path='../config/.env')

# Configurer la clé API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


def python_openai_api(prompt_human: str):
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


def create_tables():

    db_path = 'scripts.db'
    db_exists = os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    if not db_exists:
        # si la db n'existe pas

        c = conn.cursor()

        # Création de la table
        c.execute('''
        CREATE TABLE IF NOT EXISTS scripts_titres (
            ID INTEGER PRIMARY KEY,
            titre TEXT NOT NULL
        )
        ''')

        # Création de la table
        c.execute('''
        CREATE TABLE IF NOT EXISTS scripts_contenus (
            ID INTEGER PRIMARY KEY,
            txt_humain TEXT NOT NULL,
            cde_python TEXT NOT NULL,
            scripts_titre_id INTEGER,
            FOREIGN KEY (scripts_titre_id) REFERENCES scripts_titres (ID)
        )
        ''')

    conn.commit()
    conn.close()


def save_title_to_db(title):
    """
    Save the title to the 'scripts_titres' table in the database.
    """
    db_path = 'scripts.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert or update the title in the 'scripts_titres' table
    cursor.execute("""
        INSERT OR REPLACE INTO scripts_titres (ID, titre)
        VALUES ((SELECT ID FROM scripts_titres WHERE titre = ?), ?)
    """, (title, title))

    # Committing the transaction and closing the connection
    conn.commit()
    conn.close()


def save_script(titre, txt_humain, cde_python):

    db_path = 'scripts.db'
    db_exists = os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    if db_exists:
        c = conn.cursor()
        c.execute('INSERT INTO scripts_titres (titre) VALUES (?)', (titre,))
        titre_id = c.lastrowid

        c.execute('INSERT INTO scripts_contenus (txt_humain, cde_python, scripts_titre_id) VALUES (?, ?, ?)',
                  (txt_humain, cde_python, titre_id))

    conn.commit()
    conn.close()


def get_titles_from_db():
    """
    Get all titles from the 'scripts_titres' table in the database.
    """
    db_path = 'scripts.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT titre FROM scripts_titres")
    titles = cursor.fetchall()

    # Committing the transaction and closing the connection
    conn.close()

    # Returning the titles as a list of strings
    return [title[0] for title in titles]


def get_script_from_db(title):
    """Get a script from the database based on the title."""
    db_path = 'scripts.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT txt_humain, cde_python FROM scripts_contenus WHERE scripts_titre_id = (SELECT ID FROM scripts_titres WHERE titre = ?)", (title,))
    script = cursor.fetchone()

    conn.close()

    return script


st.title('Traducteur de texte en code Python')

script_title = st.text_input('Titre de mon script Python')

# Création de deux colonnes
col1, col2 = st.columns(2)

with col1:
    st.header('Texte humain')
    human_text = st.text_area('Entrez votre texte ici :', height=200)
    translate_button = st.button('Traduire en Python')

with col2:
    st.header('Code Python généré')
    if translate_button and human_text:
        # Vous pouvez décommenter et utiliser cette ligne si vous avez les clés API d'OpenAI configurées.
        st.session_state.python_code = python_openai_api(human_text)
        # Ceci est une ligne temporaire.
        # st.session_state.python_code = 'Votre code traduit apparaîtra ici.'

    python_code = st.text_area('Votre code traduit sera affiché ici :',
                               value=st.session_state.get('python_code', ''), height=200)

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


create_tables()


if st.button('Sauvegarder les changements'):
    # save_title_to_db(script_title)
    save_script(script_title, human_text, python_code)


titles = get_titles_from_db()
selected_title = st.sidebar.selectbox(
    'Sélectionnez un script', options=get_titles_from_db(), key='selected_title')

# Si un titre est sélectionné, mettez à jour les états de session avec les valeurs du script sélectionné
if selected_title:
    selected_script = get_script_from_db(selected_title)
    if selected_script:
        st.session_state.script_title = selected_title
        st.session_state.human_text, st.session_state.python_code = selected_script
    else:
        st.session_state.script_title = st.session_state.human_text = st.session_state.python_code = ""
else:
    st.session_state.script_title = st.session_state.human_text = st.session_state.python_code = ""

# Utiliser les états de session comme valeurs par défaut pour les widgets
script_title = st.text_input(
    'Titre de mon script Python', value=st.session_state.script_title)
human_text = st.text_area('Texte humain', value=st.session_state.human_text)
python_code = st.text_area(
    'Code Python généré', value=st.session_state.python_code)


def display_tables():
    """
    Display the content of the 'scripts_titres' and 'scripts_contenus' tables.
    """
    db_path = 'scripts.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query and display the 'scripts_titres' table
    cursor.execute("SELECT * FROM scripts_titres")
    scripts_titres_data = cursor.fetchall()
    scripts_titres_columns = [column[0] for column in cursor.description]
    st.write("### Table 'scripts_titres'")
    st.write(scripts_titres_columns)
    st.write(scripts_titres_data)

    # Query and display the 'scripts_contenus' table
    cursor.execute("SELECT * FROM scripts_contenus")
    scripts_contenus_data = cursor.fetchall()
    scripts_contenus_columns = [column[0] for column in cursor.description]
    st.write("### Table 'scripts_contenus'")
    st.write(scripts_contenus_columns)
    st.write(scripts_contenus_data)

    # Closing the connection
    conn.close()


# Call this function where you want to display the tables in your Streamlit app
display_tables()
