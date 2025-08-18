from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Matter
from ..schemas import MatterIn, MatterOut
router = APIRouter(prefix="/matters", tags=["matters"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@router.get("", response_model=list[MatterOut])
def list_matters(db: Session = Depends(get_db)): return db.query(Matter).all()
@router.post("", response_model=MatterOut)
def create_matter(payload: MatterIn, db: Session = Depends(get_db)):
    m = Matter(**payload.dict()); db.add(m); db.commit(); db.refresh(m); return m
