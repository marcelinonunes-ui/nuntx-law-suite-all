from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..database import SessionLocal
from ..models import Client, Matter, Doc
router = APIRouter(prefix="/search", tags=["search"])
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()
@router.get("")
def search(q: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    qlike = f"%{q.lower()}%"
    clients = db.query(Client).filter(Client.name.ilike(qlike)).all()
    matters = db.query(Matter).filter(or_(Matter.title.ilike(qlike), Matter.description.ilike(qlike))).all()
    docs = db.query(Doc).filter(Doc.extracted_text.ilike(qlike)).limit(30).all()
    return {
        "clients": [{"id": c.id, "name": c.name} for c in clients],
        "matters": [{"id": m.id, "title": m.title} for m in matters],
        "docs": [{"id": d.id, "filename": d.filename} for d in docs]
    }
