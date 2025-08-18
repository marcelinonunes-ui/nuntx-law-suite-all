from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from .database import SessionLocal
from .models import User, Role
from .schemas import UserCreate, UserOut
from .config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGO = "HS256"

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def to_token(user: User):
    data = {"sub": str(user.id), "name": user.full_name, "role": user.role.name}
    return jwt.encode({**data, "exp": datetime.utcnow() + timedelta(days=7)}, settings.SECRET_KEY, algorithm=ALGO)

@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter_by(email=payload.email).first():
        raise HTTPException(400, "Email already exists")
    role = db.query(Role).filter_by(id=payload.role_id).first()
    if not role: raise HTTPException(400, "Invalid role")
    u = User(email=payload.email, full_name=payload.full_name, role_id=role.id, hashed_password=pwd.hash(payload.password))
    db.add(u); db.commit(); db.refresh(u); return u

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = db.query(User).filter_by(email=form.username).first()
    if not u or not pwd.verify(form.password, u.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": to_token(u), "token_type": "bearer", "user": {"id": u.id, "name": u.full_name, "role": u.role.name}}
