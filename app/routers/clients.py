from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import Client
from ..schemas import ClientIn, ClientOut
router = APIRouter(prefix="/clients", tags=["clients"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@router.get("", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db)): return db.query(Client).all()
@router.post("", response_model=ClientOut)
def create_client(payload: ClientIn, db: Session = Depends(get_db)):
    c = Client(**payload.dict()); db.add(c); db.commit(); db.refresh(c); return c
