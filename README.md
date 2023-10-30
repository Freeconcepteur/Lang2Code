
# Lang2Code

## Description
Lang2Code est une application conçue pour transformer du langage humain en code Python. L'application utilise l'API d'OpenAI pour générer du code à partir de prompts en langage naturel et offre une interface utilisateur intuitive pour interagir avec la fonctionnalité de génération de code. L'application est destinée à être utilisée localement.

## Installation

### Création et activation de l'environnement virtuel

- **Sous Windows**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```

- **Sous Linux**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### Installation des dépendances
Avec l'environnement virtuel activé, naviguez vers le répertoire de l'application et installez les dépendances en utilisant le fichier `requirements.txt` :
   ```bash
   pip install -r requirements.txt
   ```

### Configuration de l'API OpenAI
Placez votre clé API d'OpenAI dans le fichier `config/.env`.

### Configuration de la BDD
Utiliser la fonction create_db_tables() dans le programme finale. Celle-ci va créer 'scripts.db' dans le dossier databse. La BDD contient 2 tables,'scripts_titres' et 'scripts_contenus'.

### Fonction relatives à la BDD lang2code_db.sqlite
Dans le dossier database_operations/models se trouve le module qui contient un ensemble de fonction pour créer la base de donnée et ses tables (voir ci-dessus), implémenter les données dans celle-ci (title, prompt et code) et un ensemble de fonction pour récupérer une liste de chacun de ces éléments.

## Utilisation
1. Naviguez vers le répertoire de l'application via la ligne de commande ou un terminal.
2. Exécutez l'application en utilisant la commande `streamlit run app.py`.
3. L'application devrait être accessible via un navigateur web à une adresse locale telle que `localhost:8501`.
