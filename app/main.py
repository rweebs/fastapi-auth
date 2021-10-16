from app.database import *
from app.user.models import Token, TokenData
from app.user.controllers import authenticate_user, timedelta, create_access_token
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from typing import Optional
from . import menu
from .menu import main
from . import user
from .user import main

SECRET_KEY = "7049df34ffff4ea67ada6caa17b5d37941ec527c25588062afbb605d74cd2f8e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

description = """
Nama    : Rahmat Wibowo\n
NIM     : 18219040\n
"""
tags_metadata = [
    {
        "name": "authentication",
        "description": "Authentication endpoint",
    },
    {
        "name": "user",
        "description": "User endpoint",
    },
    {
        "name": "menu",
        "description": "Menu endpoint",
    },
]

app = FastAPI(title="UTS II3160 Teknologi Sistem Terintegrasi",
              description=description, openapi_tags=tags_metadata)


@app.get('/')
async def root():
    return RedirectResponse("/docs")

app.include_router(menu.main.router)
app.include_router(user.main.router)


@app.post("/token", response_model=Token, tags=["authentication"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    user = authenticate_user(users_db, form_data.username, form_data.password)

    if not user:

        raise HTTPException(

            status_code=status.HTTP_401_UNAUTHORIZED,

            detail="Incorrect username or password",

            headers={"WWW-Authenticate": "Bearer"},

        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(

        data={"sub": user.username}, expires_delta=access_token_expires

    )

    return {"access_token": access_token, "token_type": "bearer"}
