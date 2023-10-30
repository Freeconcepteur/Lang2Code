
def create_db_tables():
    from sqlalchemy_utils import database_exists, create_database #importer package nécessaire
    from database_operations.models import Base, Prompt, Code, Title
    from sqlalchemy import create_engine
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

def table_feed(a, b, c, d, e): 
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from database_operations.models import Prompt, Code, Title
    # function to integrate values in Lang2code tables
    # arguments : (title, prompt, code)
    db_url = "sqlite:///database_operations/lang2code_db.sqlite"
    engine = create_engine(db_url)
   
    Session = sessionmaker(bind=engine) #create session
    session = Session()

    title = Title(title = a)
    prompt = Prompt(prompt_txt = b, title_id = c) #assigning values to the tables
    code = Code(code_txt = d, prompt_id = e)

    session.add(title)
    session.add(prompt) #integrate values to the tables
    session.add(code)

    session.commit() #conclue l'ajout des produits dans la table produits
    
    session.close() # Fermer la session