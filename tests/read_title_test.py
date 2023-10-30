import sys, os
sys.path.append(os.path.dirname(__file__) + "/..")
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database #importer package nécessaire
from database_operations.models import Base, Prompt, Code, Title
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_operations.db_utilities import table_feed




db_url = "sqlite:///database_operations/lang2code_db.sqlite"
engine = create_engine(db_url)


Session = sessionmaker(bind=engine)
session = Session()

#Read table

session = Session() #on ouvre une nouvelle session

titles = session.query(Title).all() #Ici on récupère le nom de chaque prompt et title dans la table 'Prompts'
liste_titres = []

for title in titles:
    print(f"ID: {title.id}, title: {title.title}")
    liste_titres.append(title.title)
    
print(len(liste_titres))
print(liste_titres)
