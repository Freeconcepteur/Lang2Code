from sqlalchemy.orm import Session
from . import models

# Ajouter un nouveau prompt et le code généré


def create_entry(db: Session, title: str, prompt_txt: str, code_txt: str):
    db_prompt = models.Prompt(title=title, prompt_txt=prompt_txt)
    db.add(db_prompt)
    db.flush()
    db_code = models.Code(code_txt=code_txt, prompt_id=db_prompt.id)
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code

# Obtenir un prompt et le code généré le plus récent par ID de prompt


def get_entry(db: Session, prompt_id: int):
    return db.query(models.Prompt, models.Code).filter(models.Prompt.id == prompt_id).join(models.Code).order_by(models.Code.id.desc()).first()

# Mettre à jour le code généré d'un prompt spécifique par ID de prompt (en créant une nouvelle entrée)


def update_code(db: Session, prompt_id: int, code_txt: str):
    new_code = models.Code(code_txt=code_txt, prompt_id=prompt_id)
    db.add(new_code)
    db.commit()
    db.refresh(new_code)
    return new_code

# Obtenir le code généré précédent (id précédent de code généré) d'un prompt spécifique par ID de prompt


def get_previous_code(db: Session, prompt_id: int, current_code_id: int):
    return db.query(models.Code).filter(models.Code.prompt_id == prompt_id, models.Code.id < current_code_id).order_by(models.Code.id.desc()).first()
