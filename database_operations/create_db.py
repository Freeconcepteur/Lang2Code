

def create_db_tables():
    from sqlalchemy_utils import database_exists, create_database #importer package nécessaire
    from database_operations.models import Base, Prompt, Code
    from sqlalchemy import create_engine
# Définir l'URL de la base de données
    db_url = "sqlite:///database_operations/tmpdb.sqlite"

    if database_exists(db_url) : 
            
            print('database already exists') #Si elle existe, elle sera effacée
    else :
            create_database(db_url)
            print('A new database has been created') #Sinon le programme nous prévient et en crée une nouvelle
            engine = create_engine(db_url)
            Base.metadata.create_all(engine) #On crée toute les tables depuis le 'package' 'model', tous les objet ayant hérité de 'Base'
            print('Tables have been created')

