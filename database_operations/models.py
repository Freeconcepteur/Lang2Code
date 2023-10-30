import sqlite3
import streamlit as st
import os


def create_connection(db_path='database/scripts.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def close_connection(conn):
    conn.close()


def create_tables():
    db_path = 'database/scripts.db'

    # Vérifier si le fichier de la base de données existe, sinon le créer
    if not os.path.exists(db_path):
        open(db_path, 'w').close()

    conn, cursor = create_connection()

    # Création de la table scripts_titres si elle n'existe pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scripts_titres (
        ID INTEGER PRIMARY KEY,
        titre TEXT NOT NULL
    )
    ''')

    # Création de la table scripts_contenus si elle n'existe pas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scripts_contenus (
        ID INTEGER PRIMARY KEY,
        txt_humain TEXT NOT NULL,
        cde_python TEXT NOT NULL,
        scripts_titre_id INTEGER,
        FOREIGN KEY (scripts_titre_id) REFERENCES scripts_titres (ID)
    )
    ''')

    conn.commit()  # Committing before closing the connection
    close_connection(conn)  # Closing the connection here


def save_script(titre, txt_humain, cde_python):
    conn, cursor = create_connection()

    db_exists = os.path.exists('database/scripts.db')

    if db_exists:
        cursor.execute(
            'INSERT INTO scripts_titres (titre) VALUES (?)', (titre,))
        titre_id = cursor.lastrowid

        cursor.execute('INSERT INTO scripts_contenus (txt_humain, cde_python, scripts_titre_id) VALUES (?, ?, ?)',
                       (txt_humain, cde_python, titre_id))

    conn.commit()
    close_connection(conn)


def get_titles_from_db():
    """
    Get all titles from the 'scripts_titres' table in the database.
    """
    conn, cursor = create_connection()

    cursor.execute("SELECT titre FROM scripts_titres")
    titles = cursor.fetchall()

    close_connection(conn)

    # Returning the titles as a list of strings
    return [title[0] for title in titles]


def get_script_from_db(title):
    """Get a script from the database based on the title."""
    conn, cursor = create_connection()

    cursor.execute(
        "SELECT txt_humain, cde_python FROM scripts_contenus WHERE scripts_titre_id = (SELECT ID FROM scripts_titres WHERE titre = ?)", (title,))
    script = cursor.fetchone()

    close_connection(conn)

    return script


def get_data_from_selection(title):
    """
    Get script details based on the title.
    """
    conn, cursor = create_connection()

    if title:
        # Getting the script ID based on the title
        cursor.execute(
            "SELECT ID FROM scripts_titres WHERE titre = ?", (title,))
        script_id = cursor.fetchone()

        if script_id:
            # Getting the script content based on the script ID
            cursor.execute(
                "SELECT txt_humain, cde_python FROM scripts_contenus WHERE scripts_titre_id = ?", (script_id[0],))
            script_content = cursor.fetchone()

            if script_content:
                txt_humain, cde_python = script_content
                close_connection(conn)
                return {
                    'script_title': title,
                    'human_text': txt_humain,
                    'python_code': cde_python
                }

    # Closing the connection if no data is found
    close_connection(conn)

    # If the title is not selected or if the script details are not found
    return {
        'script_title': '',
        'human_text': '',
        'python_code': ''
    }


def display_tables():

    conn, cursor = create_connection()

    cursor.execute("SELECT * FROM scripts_titres")
    scripts_titres_data = cursor.fetchall()
    scripts_titres_columns = [column[0] for column in cursor.description]
    st.write("### Table 'scripts_titres'")
    st.write(scripts_titres_columns)
    st.write(scripts_titres_data)

    cursor.execute("SELECT * FROM scripts_contenus")
    scripts_contenus_data = cursor.fetchall()
    scripts_contenus_columns = [column[0] for column in cursor.description]
    st.write("### Table 'scripts_contenus'")
    st.write(scripts_contenus_columns)
    st.write(scripts_contenus_data)

    close_connection(conn)
