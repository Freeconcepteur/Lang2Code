from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Title(Base):
    __tablename__ = 'titles_tbl'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    
    # Relationship to the Prompt table
    prompts = relationship("Prompt", back_populates="title")

class Prompt(Base):
    __tablename__ = 'prompts_tbl'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title_id = Column(Integer, ForeignKey('titles_tbl.id'))
    prompt_txt = Column(Text)

    # Relationship to the Code table
    codes = relationship("Code", back_populates="prompt")
    
    # Relationship to the Titre table
    title = relationship("Title", back_populates="prompts")

class Code(Base):
    __tablename__ = 'code_tbl'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code_txt = Column(Text)
    prompt_id = Column(Integer, ForeignKey('prompts_tbl.id'))

    # Relationship to the Prompt table
    prompt = relationship("Prompt", back_populates="codes")