import typing
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.application.use_cases.authenticate_user.authenticate_user import (
    AuthenticateUser,
)
from app.application.use_cases.authenticate_user.request import AuthenticaeUserRequest
from app.application.use_cases.register_user.register_user_case import RegisterUser
from app.application.use_cases.register_user.request import RegisterUserRequest
from app.config.enviroment import Settings
from app.infraestructure.api.config.auth import Auth

from app.infraestructure.api.config.auth_model import Token
from app.infraestructure.api.exceptions.http_exceptions import exception_handlers
from app.infraestructure.database.config.dynamodb import (
    create_table,
    get_dynamodb_client,
)
from app.infraestructure.database.user_repository_db import UserRepositoryDB


app = FastAPI()


client = get_dynamodb_client()
create_table(client)

exception_handlers(app=app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
def health_check() -> typing.Dict:
    return {"name": "AI Feedback", "version": "0.0.1"}


@app.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session=Depends(get_dynamodb_client),
) -> Token:
    user_repository_db = UserRepositoryDB(session=session)
    hashed_password = user_repository_db.hash_password(form_data.password)
    authenticate_user_case = AuthenticateUser(user_repository=user_repository_db)
    authenticate_user_request = AuthenticaeUserRequest(
        email=form_data.username,
        password=form_data.password,
        hashed_password=hashed_password,
    )
    auth = Auth()
    user = authenticate_user_case.execute(
        authenticate_user_request=authenticate_user_request
    )

    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.user.email}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@app.post("/signup")
async def signup(request: RegisterUserRequest, session=Depends(get_dynamodb_client)):
    new_user = RegisterUserRequest(**request.model_dump())
    register_user_use_case = RegisterUser(
        user_repository=UserRepositoryDB(session=session)
    )

    return register_user_use_case.execute(new_user=new_user)
