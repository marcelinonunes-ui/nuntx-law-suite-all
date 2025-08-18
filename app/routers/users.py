from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User, Role
from ..schemas import UserOut
from ..deps import current_user
router = APIRouter(prefix="/users", tags=["users"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@router.get("/me", response_model=UserOut)
def me(cur=Depends(current_user), db: Session = Depends(get_db)):
    u = db.query(User).filter_by(id=cur["id"]).first(); return u
@router.get("/roles")
def roles(db: Session = Depends(get_db)): return db.query(Role).all()
