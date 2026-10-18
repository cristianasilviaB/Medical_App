from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import get_db
import model

router = APIRouter(prefix="/auth", tags=["Auth"])

# configuration for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Settings JWT
SECRET_KEY = "cheie_secreta_super_securizata_medical_app"  # În producție se încarcă din mediu/env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# scheme for OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# functions for password hashing and verification
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# dependency for getting the current user from the token
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(model.User).filter(model.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

#  Register with Password Hashing
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = (
        db.query(model.User).filter(model.User.username == username).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )

    hashed_pwd = hash_password(password)
    new_user = model.User(username=username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


# Login with JWT Token Generation
@router.post("/login")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = (
        db.query(model.User)
        .filter(model.User.username == form_data.username)
        .first()
    )
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# 3. current_user Endpoint 
@router.get("/me")
def read_users_me(current_user: model.User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username}