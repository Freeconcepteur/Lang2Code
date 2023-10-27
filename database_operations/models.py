from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Prompt(Base):
    __tablename__ = 'prompts_tbl'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    prompt_txt = Column(Text)

    # Relationship to the Code table
    codes = relationship("Code", back_populates="prompt")


class Code(Base):
    __tablename__ = 'code_tbl'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code_txt = Column(Text)
    prompt_id = Column(Integer, ForeignKey('prompts_tbl.id'))

    # Relationship to the Prompt table
    prompt = relationship("Prompt", back_populates="codes")
