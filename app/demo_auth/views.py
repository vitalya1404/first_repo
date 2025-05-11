import secrets

from fastapi import APIRouter, status
from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.exceptions import HTTPException
from typing import Annotated

demo_auth_router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()

@demo_auth_router.get("/basic-auth/")
def demo_basic_auth_credentials(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }

usernames_to_passwords = {
    "admin": "admin",
    "john": "password"
}

def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unauthed_exc = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate":"Basic"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    #secrets
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username

@demo_auth_router.get("/basic-auth-username")
def demo_basic_auth_username(
        auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }