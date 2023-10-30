import sys, os
sys.path.append(os.path.dirname(__file__) + "/..")
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database #importer package nécessaire
from database_operations.models import Base, Prompt, Code, Title
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_operations.db_utilities import table_feed


# Définir l'URL de la base de données
db_url = "sqlite:///database_operations/lang2code_db.sqlite"

if database_exists(db_url) :         
    print('database already exists') #Si elle existe, elle sera effacée
    
else :
    create_database(db_url)
    print('A new database has been created') #Sinon le programme nous prévient et en crée une nouvelle
    engine = create_engine(db_url)
    Base.metadata.create_all(engine) #On crée toute les tables depuis le 'package' 'model', tous les objet ayant hérité de 'Base'
    print('Tables have been created')


#db_url = "sqlite:///database_operations/lang2code_db.sqlite"
#engine = create_engine(db_url)

title = 'Titre'
prompt = 'améliore la fonction fichtre'
title_id = 2
code = 'la fonction est améliorer fichtre'
prompt_id = 2


table_feed(title, prompt, title_id, code, prompt_id) #Ici la fonction à testes

db_url = "sqlite:///database_operations/lang2code_db.sqlite"
engine = create_engine(db_url)


Session = sessionmaker(bind=engine)
session = Session()

#Read table

session = Session() #on ouvre une nouvelle session

ti = session.get(Title, 1)
pr = session.get(Prompt, 1)  #Ici on lit le nom du premier produit : retourne olive
co = session.get(Code, 1)


#print("TITLE", ti.title)
#print("PROMPT", pr.prompt_txt)
#print("TITLE_ID",pr.title_id)
#print("CODE", co.code_txt)
#print("PROMT_ID", co.prompt_id)

titles = session.query(Title).all() #Ici on récupère le nom de chaque prompt et title dans la table 'Prompts'

#for title in titles:
    #print(f"ID: {title.id}, title: {title.title}")


#prompts = session.query(Prompt).all() #Ici on récupère le nom de chaque prompt et title dans la table 'Prompts'

#for prompt in prompts:
    #print(f"ID: {prompt.id}, Nom: {prompt.prompt_txt}")

codes = session.query(Code).all() #Ici on récupère le nom de chaque prompt et title dans la table 'Prompts'

#for code in codes:
    #print(f"ID: {code.id}, Code: {code.code_txt}")


# Effectuez une jointure pour obtenir la sortie combinée des trois tables
result = session.query(Title, Prompt, Code).\
    join(Prompt, Title.id == Prompt.title_id).\
    join(Code, Prompt.id == Code.prompt_id).\
    all()

# Parcourez les résultats et affichez-les
for title, prompt, code in result:
    print("Title:", title.title)
    print("Prompt Text:", prompt.prompt_txt)
    print("Code Text:", code.code_txt)
    print("\n")



session.close()