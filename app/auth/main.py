from pydantic import BaseModel
from sqlmodel import select

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from auth.auth import get_key
from setup.cache import lifespan
from setup.db import SessionDep

from setup.model import User

Borealis = FastAPI(lifespan=lifespan)

@Borealis.post('/keygen')
async def generate_api_key(
    db: SessionDep
):
    api_key = await get_key()
    user = User(api_key=api_key)

    db.add(user)
    db.commit()
    db.refresh(user)

    return JSONResponse(content={"api_key": api_key})


class APIKey(BaseModel):
    api_key: str

@Borealis.post('/validate')
async def validate_api_key(
    api_key: APIKey,
    db: SessionDep,
):

    statement = select(User).where(User.api_key == api_key.api_key)
    user = db.exec(statement).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return JSONResponse(content={"message": "API key is valid"})