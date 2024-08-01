from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

from embrapadataapi.configuration.environment import get_config

auth_config = get_config().auth
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    """Classe que define o token JTW usado para autenticação"""
    # Conteúdo do token (hash)
    access_token: str
    # Tipo do token (Bearer)
    token_type: str = "bearer"


class User(BaseModel):
    """Classe que define o usuário para autenticação"""
    # Nome do usuário (login)
    username: str
    # Senha em formato de hash
    password: str


def get_user(username: str):
    """Função que captura o usuário de autenticação das configurações se ele
    conincidir com o usuário passado como parâmetro. Utilizado para comparação no momento dos requests
    Args:
        username: Nome de acesso do usuário
    Returns:
        User
    """
    # Se o nome do usuário passado for igual ao que está configurado na API retornamos a instância do usuário
    # com a senha em formato de hash
    if username == auth_config.username:
        user_dict = {"username": auth_config.username, "password": auth_config.password}
        return User(**user_dict)


def authenticate_user(username: str, password: str):
    """Função que verifica se o usuário e senha passados estão corretos
    Args:
        username: Nome de acesso do usuário
        password: Senha do usuário
    Returns:
        User
    """
    # Pega o usuário das configurações se ele existir
    user = get_user(username)
    # Verifica se o usuário existe e se a senha coincide
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user


def create_access_token(user: User) -> Token:
    """Função que cria o access token JTW
    Args:
        user: Usuário configurado na API
    """
    # Dados que serão armazenados no token. Apenas o nome do usuário
    to_encode = {"sub": user.username}
    # Intervalo de expiração do token retirado das configurações da aplicação
    expires_delta = timedelta(minutes=auth_config.expires_minutes)
    # Calcula a data de expiração
    expire = datetime.now(timezone.utc) + expires_delta
    # Adiciona a data de expiração no token
    to_encode.update({"exp": expire})
    # Gera o token
    encoded_jwt = jwt.encode(to_encode, auth_config.secret_key, algorithm=auth_config.algorithm)
    return Token(access_token=encoded_jwt)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """Função utilitária para proteger recursos autenticados da API.
    Verifica o token JWT e recuperar os dados do usário.
    Caso não seja possível capturar os dados do usuário um erro HTTP 401 será retornado
    Args:
        token: Token JWT que será decodificado e verificado
    """

    # Cria o erro 401 para ser usado em casos onde a autenticação falhe
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token com a secret_key e o algoritmo
        payload = jwt.decode(token, auth_config.secret_key, algorithms=[auth_config.algorithm])
        # Extrai o username de dentro do token
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    # verifica se existe um usuário com esse username
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user

