from sqlmodel import SQLModel
from sqlmodel import create_engine
from sqlmodel import Session
from typing import Annotated

from fastapi import Depends

DATABASE_URL = "postgresql://borealis:borealis@db:5432/borealis"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]